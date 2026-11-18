from __future__ import annotations

from collections import defaultdict, deque
from acns.models import Signal


class SignalBus:
    """قناة محلية منظمة: تمنع التكرار وتحتفظ بسجل الإشارات."""

    def __init__(self) -> None:
        self._queues: dict[str, deque[Signal]] = defaultdict(deque)
        self._seen: set[str] = set()
        self.history: list[Signal] = []

    def send(self, signal: Signal) -> bool:
        if signal.message_id in self._seen:
            return False
        self._seen.add(signal.message_id)
        self._queues[signal.destination].append(signal)
        self.history.append(signal)
        return True

    def receive(self, destination: str, task_id: str | None = None) -> list[Signal]:
        queue = self._queues[destination]
        if task_id is None:
            items = list(queue)
            queue.clear()
            return items
        selected = [s for s in queue if s.task_id == task_id]
        self._queues[destination] = deque(s for s in queue if s.task_id != task_id)
        return selected
