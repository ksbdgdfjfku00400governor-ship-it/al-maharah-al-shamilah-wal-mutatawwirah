from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Signal:
    source: str
    destination: str
    signal_type: str
    task_id: str
    content: dict[str, Any]
    source_ref: str | None = None
    confidence: float = 1.0
    status: str = "new"
    timestamp: str = field(default_factory=now_iso)
    message_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.source or not self.destination or not self.task_id:
            raise ValueError("source, destination and task_id are required")


@dataclass
class Evidence:
    claim: str
    source: str
    confidence: float
    kind: str = "observed"


@dataclass
class CellResult:
    cell: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    evidence: list[Evidence] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class TaskState:
    task_id: str
    request: str
    context: dict[str, Any] = field(default_factory=dict)
    results: dict[str, CellResult] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    attempts: int = 0
    status: str = "created"

    def record(self, result: CellResult) -> None:
        self.results[result.cell] = result
        self.events.append({"event": "cell_result", "cell": result.cell, "success": result.success, "timestamp": now_iso()})
