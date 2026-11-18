from __future__ import annotations

from uuid import uuid4
from acns.cells.analysis import PerceptionCell, ReasoningCell, PlanningCell
from acns.cells.operations import MemoryCell, ExecutionCell, MonitoringCell, CriticCell, LearningCell, CreativityCell
from acns.communication.bus import SignalBus
from acns.models import CellResult, TaskState
from acns.security.policy import SecurityCell
from acns.memory.store import MemoryStore


class CognitiveCore:
    """منسق ACNS: يوزع العمل ولا يحتكر مسؤوليات الخلايا."""

    def __init__(self, memory: MemoryStore, *, max_attempts: int = 2) -> None:
        self.memory = memory
        self.max_attempts = max_attempts
        self.bus = SignalBus()
        self.cells = {
            "security": SecurityCell(), "perception": PerceptionCell(), "memory": MemoryCell(memory),
            "reasoning": ReasoningCell(), "planning": PlanningCell(), "creativity": CreativityCell(),
            "execution": ExecutionCell(), "monitoring": MonitoringCell(), "critic": CriticCell(),
            "learning": LearningCell(memory),
        }

    def run(self, request: str, *, context: dict | None = None) -> TaskState:
        state = TaskState(str(uuid4()), request, context or {}, status="running")
        security = self.cells["security"].process(state)
        state.record(security)
        if not security.success:
            state.status = "blocked"
            return state
        for name in ("perception", "memory", "reasoning", "planning", "creativity"):
            state.record(self.cells[name].process(state))
        while state.attempts < self.max_attempts:
            state.attempts += 1
            execution = self.cells["execution"].process(state)
            state.record(execution)
            if execution.success:
                break
            state.events.append({"event": "replan", "attempt": state.attempts})
        state.record(self.cells["monitoring"].process(state))
        state.record(self.cells["critic"].process(state))
        state.status = "completed" if state.results["execution"].success and state.results["critic"].success else "failed"
        state.record(self.cells["learning"].process(state))
        return state
