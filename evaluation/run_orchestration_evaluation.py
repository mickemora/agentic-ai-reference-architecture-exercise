from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Protocol

from evaluation.orchestration_metrics import OrchestrationMetrics
from src.orchestration.agent import WarrantyReviewAgent
from src.orchestration.baseline import BaselineWarrantyOrchestrator
from src.orchestration.trace import OrchestrationResult


class Orchestrator(Protocol):
    def review(self, prompt: str) -> OrchestrationResult: ...


def _arguments_match(case: dict[str, Any], result: OrchestrationResult) -> bool:
    if not result.trace:
        return "expected_claim_id" not in case and "expected_vin" not in case

    by_name = {event.tool_name: event for event in result.trace}
    claim_event = by_name.get("get_claim_details")
    vehicle_event = by_name.get("get_vehicle_details")
    coverage_event = by_name.get("calculate_coverage")

    if expected_claim_id := case.get("expected_claim_id"):
        if not claim_event or claim_event.arguments.get("claim_id") != expected_claim_id:
            return False
    if expected_vin := case.get("expected_vin"):
        if not vehicle_event or vehicle_event.arguments.get("vin") != expected_vin:
            return False
    if coverage_event:
        claim = coverage_event.arguments.get("claim", {})
        vehicle = coverage_event.arguments.get("vehicle", {})
        if claim.get("claim_id") != case.get("expected_claim_id"):
            return False
        if vehicle.get("vin") != case.get("expected_vin"):
            return False
    return True


def _decision_matches(case: dict[str, Any], result: OrchestrationResult) -> bool:
    if case["expected_outcome"] == "DECISION":
        return bool(result.decision and result.decision.decision.value == case["expected_decision"])
    if case["expected_outcome"] == "ERROR":
        return case["expected_error"] in result.response
    return result.decision is None


def run(orchestrator: Orchestrator | None = None) -> OrchestrationMetrics:
    active = orchestrator or BaselineWarrantyOrchestrator()
    dataset = json.loads(
        (Path(__file__).parent / "orchestration_dataset.json").read_text(encoding="utf-8")
    )
    passed = selection_passed = order_passed = argument_passed = fidelity_passed = 0

    for case in dataset:
        result = active.review(case["prompt"])
        actual_tools = [event.tool_name for event in result.trace]
        expected_tools = case["expected_tools"]
        selection_ok = sorted(actual_tools) == sorted(expected_tools)
        order_ok = actual_tools == expected_tools
        arguments_ok = _arguments_match(case, result)
        fidelity_ok = _decision_matches(case, result)
        outcome_ok = result.outcome == case["expected_outcome"]
        ok = selection_ok and order_ok and arguments_ok and fidelity_ok and outcome_ok

        selection_passed += int(selection_ok)
        order_passed += int(order_ok)
        argument_passed += int(arguments_ok)
        fidelity_passed += int(fidelity_ok)
        passed += int(ok)
        print(f'{case["test_id"]}: {"PASS" if ok else "FAIL"}')

    return OrchestrationMetrics(
        total=len(dataset),
        passed=passed,
        tool_selection_passed=selection_passed,
        tool_order_passed=order_passed,
        argument_accuracy_passed=argument_passed,
        decision_fidelity_passed=fidelity_passed,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the V1.1 orchestration contract.")
    parser.add_argument("--mode", choices=("baseline", "live"), default="baseline")
    parser.add_argument("--model-id", default=os.getenv("BEDROCK_MODEL_ID"))
    parser.add_argument("--region", default=os.getenv("AWS_REGION"))
    args = parser.parse_args()

    orchestrator: Orchestrator
    if args.mode == "live":
        if not args.model_id:
            parser.error("Live mode requires --model-id or BEDROCK_MODEL_ID.")
        orchestrator = WarrantyReviewAgent(model_id=args.model_id, region_name=args.region)
    else:
        orchestrator = BaselineWarrantyOrchestrator()

    metrics = run(orchestrator)
    print(f"Overall accuracy: {metrics.accuracy:.0%} ({metrics.passed}/{metrics.total})")
    print(f"Tool selection: {metrics.tool_selection_accuracy:.0%}")
    print(f"Tool order: {metrics.tool_order_accuracy:.0%}")
    print(f"Argument accuracy: {metrics.argument_accuracy:.0%}")
    print(f"Decision fidelity: {metrics.decision_fidelity:.0%}")


if __name__ == "__main__":
    main()
