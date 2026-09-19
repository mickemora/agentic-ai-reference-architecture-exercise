from dataclasses import dataclass


@dataclass(frozen=True)
class OrchestrationMetrics:
    total: int
    passed: int
    tool_selection_passed: int
    tool_order_passed: int
    argument_accuracy_passed: int
    decision_fidelity_passed: int

    @staticmethod
    def _rate(passed: int, total: int) -> float:
        return passed / total if total else 0.0

    @property
    def accuracy(self) -> float:
        return self._rate(self.passed, self.total)

    @property
    def tool_selection_accuracy(self) -> float:
        return self._rate(self.tool_selection_passed, self.total)

    @property
    def tool_order_accuracy(self) -> float:
        return self._rate(self.tool_order_passed, self.total)

    @property
    def argument_accuracy(self) -> float:
        return self._rate(self.argument_accuracy_passed, self.total)

    @property
    def decision_fidelity(self) -> float:
        return self._rate(self.decision_fidelity_passed, self.total)
