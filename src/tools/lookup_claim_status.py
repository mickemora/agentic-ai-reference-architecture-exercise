from typing import TypedDict

from src.repositories.json_repository import RecordNotFoundError
from src.tools.get_claim_details import get_claim_details


class ClaimStatusResult(TypedDict):
    """Fields approved for disclosure through the status lookup tool."""

    status: str
    reason: str


def lookup_claim_status(claim_id: str) -> ClaimStatusResult:
    """Return a minimal, read-only status projection for one warranty claim."""
    try:
        claim = get_claim_details(claim_id)
    except RecordNotFoundError:
        return {
            "status": "unavailable",
            "reason": "claim_not_found",
        }

    if not claim.documentation_complete:
        return {
            "status": "pending_review",
            "reason": "documentation_incomplete",
        }

    return {
        "status": "ready_for_evaluation",
        "reason": "documentation_complete",
    }