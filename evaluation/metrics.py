from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMetrics:
    total: int
    passed: int

    @property
    def accuracy(self) -> float:
        return self.passed / self.total if self.total else 0.0
