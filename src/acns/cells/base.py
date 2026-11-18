from __future__ import annotations

from abc import ABC, abstractmethod
from acns.models import CellResult, TaskState


class CognitiveCell(ABC):
    name: str = "unnamed"

    @abstractmethod
    def process(self, state: TaskState) -> CellResult:
        """نفّذ مسؤولية الخلية على حالة المهمة الحالية."""
        raise NotImplementedError
