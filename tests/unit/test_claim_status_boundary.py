from src.tools.lookup_claim_status import lookup_claim_status


def test_lookup_returns_only_approved_status_fields() -> None:
    result = lookup_claim_status("CLM-1002")

    assert result == {
        "status": "pending_review",
        "reason": "documentation_incomplete",
    }
    assert set(result) == {"status", "reason"}


def test_unknown_claim_returns_controlled_response() -> None:
    result = lookup_claim_status("CLM-9999")

    assert result == {
        "status": "unavailable",
        "reason": "claim_not_found",
    }
    assert set(result) == {"status", "reason"}
