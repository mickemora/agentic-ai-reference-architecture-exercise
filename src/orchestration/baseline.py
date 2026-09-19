from __future__ import annotations

import re

from src.orchestration.response_formatter import format_decision
from src.orchestration.tool_registry import WarrantyToolRegistry
from src.orchestration.trace import OrchestrationResult, TraceRecorder

CLAIM_ID_PATTERN = re.compile(r"\bCLM-\d{4}\b", re.IGNORECASE)


class BaselineWarrantyOrchestrator:
    """Deterministic test double for the orchestration contract; it is not an AI agent."""

    def __init__(self, recorder: TraceRecorder | None = None) -> None:
        self.recorder = recorder or TraceRecorder()
        self.registry = WarrantyToolRegistry(self.recorder)

    def review(self, prompt: str) -> OrchestrationResult:
        self.recorder.reset()
        match = CLAIM_ID_PATTERN.search(prompt)
        if not match:
            return OrchestrationResult(
                outcome="CLARIFICATION",
                response="Please provide a synthetic claim ID in the form CLM-####.",
                trace=tuple(self.recorder.events),
            )

        claim_id = match.group(0).upper()
        try:
            claim = self.registry.get_claim_details(claim_id)
            vehicle = self.registry.get_vehicle_details(str(claim["vin"]))
            self.registry.calculate_coverage(claim, vehicle)
        except (LookupError, ValueError) as error:
            return OrchestrationResult(
                outcome="ERROR",
                response=str(error),
                trace=tuple(self.recorder.events),
            )

        decision = self.registry.decision_from_trace()
        if decision is None:
            raise RuntimeError("Coverage tool completed without a validated decision.")
        return OrchestrationResult(
            outcome="DECISION",
            response=format_decision(decision),
            trace=tuple(self.recorder.events),
            decision=decision,
        )
