from src.models import CoverageDecision, VehicleDetails, WarrantyClaim
from src.rules import evaluate_coverage


def calculate_coverage(*, vehicle: VehicleDetails, claim: WarrantyClaim) -> CoverageDecision:
    """Apply deterministic rules; no LLM participates in the decision."""
    return evaluate_coverage(claim, vehicle)
