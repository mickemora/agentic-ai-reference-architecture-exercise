from src.agent.app import analyze_claim
from src.models import Decision


def test_eligible_claim_is_approved() -> None:
    result = analyze_claim("CLM-1001")
    assert result.decision == Decision.APPROVE
    assert result.requires_human_review is False


def test_incomplete_claim_requires_review() -> None:
    result = analyze_claim("CLM-1002")
    assert result.decision == Decision.HUMAN_REVIEW
    assert result.requires_human_review is True
