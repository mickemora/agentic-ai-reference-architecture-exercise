from evaluation.run_orchestration_evaluation import run


def test_all_baseline_orchestration_cases() -> None:
    metrics = run()
    assert metrics.total == 10
    assert metrics.passed == 10
    assert metrics.tool_selection_accuracy == 1.0
    assert metrics.tool_order_accuracy == 1.0
    assert metrics.argument_accuracy == 1.0
    assert metrics.decision_fidelity == 1.0
