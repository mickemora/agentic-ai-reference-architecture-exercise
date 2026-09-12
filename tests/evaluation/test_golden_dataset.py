from evaluation.run_evaluation import run


def test_all_v1_golden_cases() -> None:
    metrics = run()
    assert metrics.total == 10
    assert metrics.passed == 10
