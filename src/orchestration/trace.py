from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from src.models import CoverageDecision

TraceStatus = Literal["SUCCESS", "ERROR"]
OrchestrationOutcome = Literal["DECISION", "CLARIFICATION", "ERROR"]


@dataclass(frozen=True)
class TraceEvent:
    sequence: int
    tool_name: str
    arguments: dict[str, Any]
    status: TraceStatus
    result: dict[str, Any] | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }


@dataclass
class TraceRecorder:
    events: list[TraceEvent] = field(default_factory=list)

    def reset(self) -> None:
        self.events.clear()

    def success(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        result: dict[str, Any],
    ) -> None:
        self.events.append(
            TraceEvent(len(self.events) + 1, tool_name, arguments, "SUCCESS", result=result)
        )

    def failure(self, tool_name: str, arguments: dict[str, Any], error: Exception) -> None:
        self.events.append(
            TraceEvent(len(self.events) + 1, tool_name, arguments, "ERROR", error=str(error))
        )

    @property
    def tool_names(self) -> list[str]:
        return [event.tool_name for event in self.events]

    def last_successful_result(self, tool_name: str) -> dict[str, Any] | None:
        for event in reversed(self.events):
            if event.tool_name == tool_name and event.status == "SUCCESS":
                return event.result
        return None


@dataclass(frozen=True)
class OrchestrationResult:
    outcome: OrchestrationOutcome
    response: str
    trace: tuple[TraceEvent, ...]
    decision: CoverageDecision | None = None
    model_response: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "response": self.response,
            "decision": self.decision.model_dump(mode="json") if self.decision else None,
            "trace": [event.to_dict() for event in self.trace],
            "model_response": self.model_response,
        }
