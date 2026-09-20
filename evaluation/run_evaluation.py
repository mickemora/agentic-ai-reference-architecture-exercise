from __future__ import annotations

import json
from pathlib import Path

from evaluation.metrics import EvaluationMetrics
from src.agent.app import analyze_claim


def run() -> EvaluationMetrics:
    dataset = json.loads((Path(__file__).parent / "golden_dataset.json").read_text())
    passed = 0
    for case in dataset:
        try:
            result = analyze_claim(case["claim_id"])
            actual_reasons = {reason.value for reason in result.reason_codes}
            ok = (
                case["expected_outcome"] == "DECISION"
                and result.decision.value == case["expected_decision"]
                and actual_reasons == set(case["expected_reason_codes"])
            )
        except LookupError as error:
            ok = case["expected_outcome"] == "ERROR" and case["expected_error"] in str(error)
        passed += int(ok)
        print(f"{case['test_id']}: {'PASS' if ok else 'FAIL'}")
    return EvaluationMetrics(total=len(dataset), passed=passed)


if __name__ == "__main__":
    metrics = run()
    print(f"Accuracy: {metrics.accuracy:.0%} ({metrics.passed}/{metrics.total})")
