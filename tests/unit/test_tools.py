import pytest

from src.models import Decision, ReasonCode
from src.repositories.json_repository import RecordNotFoundError
from src.tools.warranty import calculate_coverage, get_claim_details, get_vehicle_details


def test_tool_contracts_and_eligible_decision() -> None:
    claim = get_claim_details("CLM-1001")
    vehicle = get_vehicle_details(claim.vin)
    result = calculate_coverage(vehicle=vehicle, claim=claim)
    assert result.decision == Decision.APPROVE
    assert result.reason_codes == [ReasonCode.ELIGIBLE]


def test_missing_claim_is_controlled_error() -> None:
    with pytest.raises(RecordNotFoundError, match="Synthetic claim not found"):
        get_claim_details("CLM-9999")
