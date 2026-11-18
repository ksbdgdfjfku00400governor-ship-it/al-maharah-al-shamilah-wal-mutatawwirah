from __future__ import annotations

from acns.models import CellResult, Evidence, TaskState
from acns.cells.base import CognitiveCell


class SecurityCell(CognitiveCell):
    name = "security"
    SUSPICIOUS_MARKERS = ("ignore previous instructions", "reveal api key", "disable security", "rm -rf")

    def process(self, state: TaskState) -> CellResult:
        text = f"{state.request} {state.context}".lower()
        found = [marker for marker in self.SUSPICIOUS_MARKERS if marker in text]
        if found:
            return CellResult(self.name, False, {"blocked": True, "markers": found}, [Evidence("request contains unsafe instruction", "security-policy", 1.0)], ["blocked by independent security policy"])
        return CellResult(self.name, True, {"blocked": False}, [Evidence("request passed baseline policy", "security-policy", 1.0)])
