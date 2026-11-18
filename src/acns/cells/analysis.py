from __future__ import annotations

from acns.cells.base import CognitiveCell
from acns.models import CellResult, Evidence, TaskState


class PerceptionCell(CognitiveCell):
    name = "perception"
    def process(self, state: TaskState) -> CellResult:
        words = state.request.split()
        missing = [] if words else ["request"]
        return CellResult(self.name, not missing, {"intent": state.request, "tokens": words, "missing": missing}, [Evidence("intent extracted from user request", "user-input", 0.9)])


class ReasoningCell(CognitiveCell):
    name = "reasoning"
    def process(self, state: TaskState) -> CellResult:
        perception = state.results.get("perception")
        if not perception or not perception.success:
            return CellResult(self.name, False, errors=["perception result is required"])
        return CellResult(self.name, True, {"known": [state.request], "assumptions": [], "unknown": []}, [Evidence("reasoning used explicit request", "perception", 0.8)])


class PlanningCell(CognitiveCell):
    name = "planning"
    def process(self, state: TaskState) -> CellResult:
        steps = ["retrieve relevant memory", "execute specialized work", "monitor result", "criticize and deliver"]
        return CellResult(self.name, True, {"steps": steps, "dependencies": [(steps[i], steps[i + 1]) for i in range(len(steps) - 1)]}, [Evidence("plan derived from cognitive cycle", "planning-policy", 0.85)])
