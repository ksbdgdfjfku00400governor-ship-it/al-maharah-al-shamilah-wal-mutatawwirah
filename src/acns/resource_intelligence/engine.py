from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Iterable

from acns.resource_intelligence.models import Resource, ResourceCandidate, ResourceRegistry


class ResourceDiscovery(ABC):
    @abstractmethod
    def discover(self) -> Iterable[Resource]: ...


class LocalToolDiscovery(ResourceDiscovery):
    def __init__(self, paths: Iterable[str] = ()) -> None:
        self.paths = tuple(paths)

    def discover(self) -> Iterable[Resource]:
        for raw in self.paths:
            path = Path(raw)
            if path.exists():
                yield Resource(path.as_posix(), "local", path.name, frozenset({"local-file"}), reliability=0.9, accuracy=0.9, freshness=0.8, cost=0.1, latency=0.1)


class CapabilityResolver:
    def resolve(self, resources: Iterable[Resource], required: set[str]) -> list[ResourceCandidate]:
        candidates = [ResourceCandidate(r, r.score(required), f"coverage={len(required & r.capabilities)}") for r in resources if r.compatible and required <= r.capabilities]
        return sorted(candidates, key=lambda c: c.score, reverse=True)


class PermissionManager:
    def __init__(self, allowed_kinds: set[str] | None = None) -> None:
        self.allowed_kinds = allowed_kinds or {"local"}

    def can_use(self, resource: Resource) -> bool:
        return resource.kind in self.allowed_kinds and resource.compatible


class ResourceAdapter(ABC):
    @abstractmethod
    def use(self, resource: Resource, payload: dict) -> dict: ...


class MetadataAdapter(ResourceAdapter):
    def use(self, resource: Resource, payload: dict) -> dict:
        return {"resource_id": resource.resource_id, "kind": resource.kind, "payload": payload}


class FallbackManager:
    def choose(self, candidates: list[ResourceCandidate], *, excluded: set[str] | None = None) -> ResourceCandidate | None:
        excluded = excluded or set()
        return next((candidate for candidate in candidates if candidate.resource.resource_id not in excluded), None)


class ResourceIntelligenceEngine:
    """يكتشف الموارد ويقيّمها ويعيد بدائلها دون فرض تحميل أو اتصال خارجي."""

    def __init__(self, registry: ResourceRegistry | None = None, *, permission: PermissionManager | None = None) -> None:
        self.registry = registry or ResourceRegistry()
        self.permission = permission or PermissionManager()
        self.resolvers = CapabilityResolver()
        self.fallbacks = FallbackManager()

    def discover(self, discovery: ResourceDiscovery) -> int:
        count = 0
        for resource in discovery.discover():
            self.registry.register(resource)
            count += 1
        return count

    def select(self, required: set[str]) -> list[ResourceCandidate]:
        permitted = [r for r in self.registry.all() if self.permission.can_use(r)]
        return self.resolvers.resolve(permitted, required)

    def best(self, required: set[str], *, excluded: set[str] | None = None) -> ResourceCandidate | None:
        return self.fallbacks.choose(self.select(required), excluded=excluded)
