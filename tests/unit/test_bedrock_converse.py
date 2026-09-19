from copy import deepcopy
from typing import Any

import pytest

from src.adapters.bedrock_claim_status import UnsupportedToolError
from src.adapters.bedrock_converse import (
    ToolUseRequiredError,
    run_claim_status_assistant,
)


class FakeBedrockRuntime:
    """Return predetermined Converse responses without calling AWS."""

    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self.responses = responses
        self.calls: list[dict[str, Any]] = []

    def converse(self, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(deepcopy(kwargs))
        return self.responses.pop(0)


def test_successful_tool_round_trip_returns_filtered_result() -> None:
    client = FakeBedrockRuntime(
        [
            {
                "stopReason": "tool_use",
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "toolUse": {
                                    "toolUseId": "tool-123",
                                    "name": "lookup_claim_status",
                                    "input": {"claim_id": "CLM-1002"},
                                }
                            }
                        ],
                    }
                },
            },
            {
                "stopReason": "end_turn",
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "text": (
                                    "Claim CLM-1002 is pending review because "
                                    "its documentation is incomplete."
                                )
                            }
                        ],
                    }
                },
            },
        ]
    )

    result = run_claim_status_assistant(
        client,
        "test-model",
        "What is the status of claim CLM-1002?",
    )

    assert "pending review" in result
    assert len(client.calls) == 2

    tool_result = client.calls[1]["messages"][-1]["content"][0]["toolResult"]

    assert tool_result["toolUseId"] == "tool-123"
    assert tool_result["content"][0]["json"] == {
        "status": "pending_review",
        "reason": "documentation_incomplete",
    }
    assert set(tool_result["content"][0]["json"]) == {"status", "reason"}


def test_model_cannot_bypass_required_tool() -> None:
    client = FakeBedrockRuntime(
        [
            {
                "stopReason": "end_turn",
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [{"text": "The claim is approved."}],
                    }
                },
            }
        ]
    )

    with pytest.raises(ToolUseRequiredError):
        run_claim_status_assistant(
            client,
            "test-model",
            "What is the status of claim CLM-1002?",
        )

    assert len(client.calls) == 1


def test_model_cannot_invoke_unapproved_tool() -> None:
    client = FakeBedrockRuntime(
        [
            {
                "stopReason": "tool_use",
                "output": {
                    "message": {
                        "role": "assistant",
                        "content": [
                            {
                                "toolUse": {
                                    "toolUseId": "tool-456",
                                    "name": "approve_claim",
                                    "input": {"claim_id": "CLM-1002"},
                                }
                            }
                        ],
                    }
                },
            }
        ]
    )

    with pytest.raises(UnsupportedToolError, match="Unsupported tool"):
        run_claim_status_assistant(
            client,
            "test-model",
            "Approve claim CLM-1002.",
        )

    assert len(client.calls) == 1