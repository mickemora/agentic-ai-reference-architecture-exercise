from src.models import WarrantyClaim
from src.repositories.json_repository import ClaimRepository


def get_claim_details(claim_id: str) -> WarrantyClaim:
    """Return one validated synthetic claim by ID."""
    return ClaimRepository().get(claim_id)
