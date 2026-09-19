from __future__ import annotations

import argparse
import json
import os

from src.orchestration.instructions import SYSTEM_PROMPT
from src.orchestration.response_formatter import format_decision
from src.orchestration.tool_registry import WarrantyToolRegistry
from src.orchestration.trace import OrchestrationResult, TraceRecorder


class WarrantyReviewAgent:
    """Live Strands orchestrator backed by Amazon Bedrock."""

    def __init__(self, *, model_id: str, region_name: str | None = None) -> None:
        try:
            from strands import Agent
            from strands.models import BedrockModel
        except ImportError as error:
            raise RuntimeError(
                'Strands is not installed. Run: pip install -e ".[agent]"'
            ) from error

        self.recorder = TraceRecorder()
        self.registry = WarrantyToolRegistry(self.recorder)
        model_args: dict[str, object] = {
            "model_id": model_id,
            "temperature": 0,
        }
        if region_name:
            model_args["region_name"] = region_name
        model = BedrockModel(**model_args)
        self._agent = Agent(
            model=model,
            tools=self.registry.strands_tools(),
            system_prompt=SYSTEM_PROMPT,
        )

    def review(self, prompt: str) -> OrchestrationResult:
        self.recorder.reset()
        model_response = str(self._agent(prompt))
        decision = self.registry.decision_from_trace()

        if decision:
            return OrchestrationResult(
                outcome="DECISION",
                response=format_decision(decision),
                trace=tuple(self.recorder.events),
                decision=decision,
                model_response=model_response,
            )

        failed = next(
            (event for event in reversed(self.recorder.events) if event.status == "ERROR"),
            None,
        )
        if failed:
            return OrchestrationResult(
                outcome="ERROR",
                response=failed.error or "A tool call failed.",
                trace=tuple(self.recorder.events),
                model_response=model_response,
            )

        return OrchestrationResult(
            outcome="CLARIFICATION",
            response=model_response,
            trace=tuple(self.recorder.events),
            model_response=model_response,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the live Strands warranty orchestrator.")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model-id", default=os.getenv("BEDROCK_MODEL_ID"))
    parser.add_argument("--region", default=os.getenv("AWS_REGION"))
    args = parser.parse_args()
    if not args.model_id:
        parser.error("Provide --model-id or set BEDROCK_MODEL_ID.")
    result = WarrantyReviewAgent(
        model_id=args.model_id,
        region_name=args.region,
    ).review(args.prompt)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
