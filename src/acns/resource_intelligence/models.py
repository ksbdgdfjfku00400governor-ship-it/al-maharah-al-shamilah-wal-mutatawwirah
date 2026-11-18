from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Resource:
    resource_id: str
    kind: str
    name: str
    capabilities: frozenset[str]
    reliability: float = 0.5
    accuracy: float = 0.5
    freshness: float = 0.5
    cost: float = 0.5
    latency: float = 0.5
    compatible: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def score(self, required: set[str]) -> float:
        coverage = len(required & self.capabilities) / max(1, len(required))
        quality = (self.reliability + self.accuracy + self.freshness + (1 - self.cost) + (1 - self.latency)) / 5
        return round(coverage * 0.6 + quality * 0.4, 4)


@dataclass(frozen=True)
class ResourceCandidate:
    resource: Resource
    score: float
    reason: str


class ResourceRegistry:
    def __init__(self) -> None:
        self._resources: dict[str, Resource] = {}

    def register(self, resource: Resource) -> None:
        if not resource.resource_id:
            raise ValueError("resource_id is required")
        self._resources[resource.resource_id] = resource

    def get(self, resource_id: str) -> Resource | None:
        return self._resources.get(resource_id)

    def all(self) -> list[Resource]:
        return list(self._resources.values())
