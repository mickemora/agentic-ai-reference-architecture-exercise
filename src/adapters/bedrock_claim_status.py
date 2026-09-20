from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from src.tools.warranty import lookup_claim_status

TOOL_NAME = "lookup_claim_status"

CLAIM_STATUS_TOOL_CONFIG: dict[str, Any] = {
    "tools": [
        {
            "toolSpec": {
                "name": TOOL_NAME,
                "description": (
                    "Retrieve the read-only workflow status of one synthetic "
                    "warranty claim. This tool does not approve or modify claims."
                ),
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "claim_id": {
                                "type": "string",
                                "description": ("Synthetic claim identifier in CLM-#### format."),
                                "pattern": r"^CLM-\d{4}$",
                            }
                        },
                        "required": ["claim_id"],
                        "additionalProperties": False,
                    }
                },
            }
        }
    ]
}


class ClaimStatusInput(BaseModel):
    """Runtime validation for model-supplied tool arguments."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(pattern=r"^CLM-\d{4}$")


class UnsupportedToolError(ValueError):
    """Raised when a model requests a tool outside the allowlist."""


def execute_requested_tool(
    tool_name: str,
    tool_input: dict[str, Any],
) -> dict[str, str]:
    """Validate and execute one explicitly allowlisted tool request."""
    if tool_name != TOOL_NAME:
        raise UnsupportedToolError(f"Unsupported tool: {tool_name}")

    validated_input = ClaimStatusInput.model_validate(tool_input)
    return lookup_claim_status(validated_input.claim_id)
