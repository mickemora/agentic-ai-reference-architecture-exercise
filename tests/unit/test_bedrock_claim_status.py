import pytest
from pydantic import ValidationError

from src.adapters.bedrock_claim_status import (
    UnsupportedToolError,
    execute_requested_tool,
)


def test_dispatches_allowlisted_claim_status_tool() -> None:
    result = execute_requested_tool(
        "lookup_claim_status",
        {"claim_id": "CLM-1002"},
    )

    assert result == {
        "status": "pending_review",
        "reason": "documentation_incomplete",
    }


def test_rejects_unapproved_tool() -> None:
    with pytest.raises(UnsupportedToolError, match="Unsupported tool"):
        execute_requested_tool(
            "approve_claim",
            {"claim_id": "CLM-1002"},
        )


def test_rejects_unapproved_input_fields() -> None:
    with pytest.raises(ValidationError):
        execute_requested_tool(
            "lookup_claim_status",
            {
                "claim_id": "CLM-1002",
                "include_repair_cost": True,
            },
        )


def test_rejects_invalid_claim_identifier() -> None:
    with pytest.raises(ValidationError):
        execute_requested_tool(
            "lookup_claim_status",
            {"claim_id": "DROP TABLE CLAIMS"},
        )