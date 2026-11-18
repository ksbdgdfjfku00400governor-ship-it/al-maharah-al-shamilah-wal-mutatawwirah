from __future__ import annotations

from acns.cells.base import CognitiveCell
from acns.models import CellResult, Evidence, TaskState
from acns.memory.store import MemoryStore


class MemoryCell(CognitiveCell):
    name = "memory"
    def __init__(self, store: MemoryStore) -> None: self.store = store
    def process(self, state: TaskState) -> CellResult:
        matches = self.store.search(state.request, limit=5)
        return CellResult(self.name, True, {"matches": matches}, [Evidence("memory lookup completed", "memory-store", 1.0)])


class ExecutionCell(CognitiveCell):
    name = "execution"
    def process(self, state: TaskState) -> CellResult:
        if state.context.get("force_execution_failure") and state.attempts == 1:
            return CellResult(self.name, False, errors=["simulated tool failure"])
        return CellResult(self.name, True, {"result": f"processed: {state.request}"}, [Evidence("local execution completed", "execution-cell", 0.9)])


class MonitoringCell(CognitiveCell):
    name = "monitoring"
    def process(self, state: TaskState) -> CellResult:
        failures = [name for name, result in state.results.items() if not result.success]
        return CellResult(self.name, not failures, {"failures": failures, "events": len(state.events)}, [Evidence("task state monitored", "task-events", 1.0)])


class CriticCell(CognitiveCell):
    name = "critic"
    def process(self, state: TaskState) -> CellResult:
        unsupported = [name for name, result in state.results.items() if not result.evidence and result.success]
        return CellResult(self.name, not unsupported, {"unsupported": unsupported, "reviewed": list(state.results)}, [Evidence("independent output review completed", "critic-cell", 0.95)])


class LearningCell(CognitiveCell):
    name = "learning"
    def __init__(self, store: MemoryStore) -> None: self.store = store
    def process(self, state: TaskState) -> CellResult:
        lesson = {"request": state.request, "status": state.status, "successful_cells": [n for n, r in state.results.items() if r.success]}
        if state.context.get("allow_learning"):
            self.store.put(f"lesson:{state.task_id}", lesson, memory_type="procedural", source="learning-cell", confidence=0.8)
        return CellResult(self.name, True, {"lesson": lesson, "persisted": bool(state.context.get("allow_learning"))}, [Evidence("lesson extracted and permission respected", "learning-cell", 0.85)])


class CreativityCell(CognitiveCell):
    name = "creativity"
    def process(self, state: TaskState) -> CellResult:
        alternatives = ["minimal local path", "modular extensible path"]
        return CellResult(self.name, True, {"alternatives": alternatives}, [Evidence("alternatives generated for evaluation", "creativity-cell", 0.7)])
