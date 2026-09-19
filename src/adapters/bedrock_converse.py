from typing import Any, Protocol

from src.adapters.bedrock_claim_status import (
    CLAIM_STATUS_TOOL_CONFIG,
    execute_requested_tool,
)

SYSTEM_PROMPT = (
    "You are a read-only warranty claim status assistant. "
    "For every claim-status question, you must call lookup_claim_status. "
    "Never infer a status from prior knowledge. Report only the status and "
    "reason returned by the tool. Never approve, deny, or modify a claim."
)


class BedrockRuntimeClient(Protocol):
    """Minimal Bedrock Runtime interface required by this orchestrator."""

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        """Invoke the Bedrock Converse API."""


class ToolUseRequiredError(RuntimeError):
    """Raised when the model answers without requesting the required tool."""


class UnexpectedModelResponseError(RuntimeError):
    """Raised when the model response violates the bounded workflow."""


def _converse(
    client: BedrockRuntimeClient,
    model_id: str,
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    return client.converse(
        modelId=model_id,
        messages=messages,
        system=[{"text": SYSTEM_PROMPT}],
        toolConfig=CLAIM_STATUS_TOOL_CONFIG,
        inferenceConfig={
            "maxTokens": 200,
            "temperature": 0,
        },
    )


def _assistant_message(response: dict[str, Any]) -> dict[str, Any]:
    try:
        return response["output"]["message"]
    except KeyError as error:
        raise UnexpectedModelResponseError(
            "Bedrock response did not contain an assistant message."
        ) from error


def run_claim_status_assistant(
    client: BedrockRuntimeClient,
    model_id: str,
    question: str,
) -> str:
    """Run one strictly bounded request-tool-result-response sequence."""
    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": [{"text": question}],
        }
    ]

    first_response = _converse(client, model_id, messages)

    if first_response.get("stopReason") != "tool_use":
        raise ToolUseRequiredError(
            "The model answered without requesting the required tool."
        )

    tool_request_message = _assistant_message(first_response)
    messages.append(tool_request_message)

    tool_requests = [
        block["toolUse"]
        for block in tool_request_message.get("content", [])
        if "toolUse" in block
    ]

    if len(tool_requests) != 1:
        raise UnexpectedModelResponseError(
            "Exactly one tool request is permitted per interaction."
        )

    tool_request = tool_requests[0]
    tool_name = tool_request.get("name")
    tool_input = tool_request.get("input")
    tool_use_id = tool_request.get("toolUseId")

    if not isinstance(tool_name, str):
        raise UnexpectedModelResponseError("Tool name is missing or invalid.")

    if not isinstance(tool_input, dict):
        raise UnexpectedModelResponseError("Tool input is missing or invalid.")

    if not isinstance(tool_use_id, str):
        raise UnexpectedModelResponseError("Tool-use ID is missing or invalid.")

    tool_result = execute_requested_tool(tool_name, tool_input)

    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "toolResult": {
                        "toolUseId": tool_use_id,
                        "content": [{"json": tool_result}],
                        "status": "success",
                    }
                }
            ],
        }
    )

    final_response = _converse(client, model_id, messages)

    if final_response.get("stopReason") != "end_turn":
        raise UnexpectedModelResponseError(
            "The model did not end after receiving the tool result."
        )

    final_message = _assistant_message(final_response)
    text_blocks = [
        block["text"]
        for block in final_message.get("content", [])
        if isinstance(block.get("text"), str)
    ]

    if not text_blocks:
        raise UnexpectedModelResponseError(
            "The final model response contained no text."
        )

    return "\n".join(text_blocks)