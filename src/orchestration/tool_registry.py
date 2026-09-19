from __future__ import annotations

from typing import Any

from src.models import CoverageDecision, VehicleDetails, WarrantyClaim
from src.orchestration.trace import TraceRecorder
from src.tools.calculate_coverage import calculate_coverage as coverage_service
from src.tools.get_claim_details import get_claim_details as claim_service
from src.tools.get_vehicle_details import get_vehicle_details as vehicle_service


class WarrantyToolRegistry:
    """Controlled adapter between an orchestrator and deterministic business services."""

    def __init__(self, recorder: TraceRecorder | None = None) -> None:
        self.recorder = recorder or TraceRecorder()

    def get_claim_details(self, claim_id: str) -> dict[str, Any]:
        """Retrieve one validated synthetic warranty claim by its CLM-#### identifier."""
        arguments = {"claim_id": claim_id}
        try:
            claim = claim_service(claim_id)
            result = claim.model_dump(mode="json")
            self.recorder.success("get_claim_details", arguments, result)
            return result
        except Exception as error:
            self.recorder.failure("get_claim_details", arguments, error)
            raise

    def get_vehicle_details(self, vin: str) -> dict[str, Any]:
        """Retrieve one validated synthetic vehicle by the VIN returned by the claim tool."""
        arguments = {"vin": vin}
        try:
            vehicle = vehicle_service(vin)
            result = vehicle.model_dump(mode="json")
            self.recorder.success("get_vehicle_details", arguments, result)
            return result
        except Exception as error:
            self.recorder.failure("get_vehicle_details", arguments, error)
            raise

    def calculate_coverage(
        self,
        claim: dict[str, Any],
        vehicle: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply deterministic synthetic rules; the language model never decides coverage."""
        arguments = {
            "claim": claim,
            "vehicle": vehicle,
        }
        try:
            validated_claim = WarrantyClaim.model_validate(claim)
            validated_vehicle = VehicleDetails.model_validate(vehicle)
            decision = coverage_service(claim=validated_claim, vehicle=validated_vehicle)
            result = decision.model_dump(mode="json")
            self.recorder.success("calculate_coverage", arguments, result)
            return result
        except Exception as error:
            self.recorder.failure("calculate_coverage", arguments, error)
            raise

    def decision_from_trace(self) -> CoverageDecision | None:
        result = self.recorder.last_successful_result("calculate_coverage")
        return CoverageDecision.model_validate(result) if result else None

    def strands_tools(self) -> list[Any]:
        """Create Strands tools lazily so deterministic tests do not require the SDK."""
        try:
            from strands import tool
        except ImportError as error:
            raise RuntimeError(
                'Strands is not installed. Run: pip install -e ".[agent]"'
            ) from error

        registry = self

        @tool
        def get_claim_details(claim_id: str) -> dict[str, Any]:
            """Retrieve one validated synthetic warranty claim by its CLM-#### identifier."""
            return registry.get_claim_details(claim_id)

        @tool
        def get_vehicle_details(vin: str) -> dict[str, Any]:
            """Retrieve a synthetic vehicle using only the VIN returned by the claim tool."""
            return registry.get_vehicle_details(vin)

        @tool
        def calculate_coverage(
            claim: dict[str, Any],
            vehicle: dict[str, Any],
        ) -> dict[str, Any]:
            """Apply deterministic coverage rules to complete claim and vehicle objects."""
            return registry.calculate_coverage(claim, vehicle)

        return [get_claim_details, get_vehicle_details, calculate_coverage]
