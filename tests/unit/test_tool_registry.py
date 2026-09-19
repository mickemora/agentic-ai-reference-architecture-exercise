from src.orchestration.tool_registry import WarrantyToolRegistry
from src.orchestration.trace import TraceRecorder


def test_registry_records_authoritative_three_tool_sequence() -> None:
    recorder = TraceRecorder()
    registry = WarrantyToolRegistry(recorder)
    claim = registry.get_claim_details("CLM-1001")
    vehicle = registry.get_vehicle_details(claim["vin"])
    decision = registry.calculate_coverage(claim, vehicle)

    assert recorder.tool_names == [
        "get_claim_details",
        "get_vehicle_details",
        "calculate_coverage",
    ]
    assert decision["decision"] == "APPROVE"
    assert registry.decision_from_trace() is not None
