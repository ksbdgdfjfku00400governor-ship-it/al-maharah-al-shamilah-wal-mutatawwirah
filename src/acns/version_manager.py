from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    version: str
    name: str
    capabilities: frozenset[str]
    available: bool = True


class VersionManager:
    """يدير اختيار الإصدار دون تحميل إصدارات أخرى تلقائيًا."""

    def __init__(self) -> None:
        self._versions: dict[str, VersionInfo] = {}
        self._selected: str | None = None

    def register(self, info: VersionInfo) -> None:
        self._versions[info.version] = info

    def available(self) -> list[VersionInfo]:
        return [v for v in self._versions.values() if v.available]

    def select(self, version: str) -> VersionInfo:
        info = self._versions.get(version)
        if info is None or not info.available:
            raise ValueError(f"version is unavailable: {version}")
        self._selected = version
        return info

    def current(self) -> VersionInfo | None:
        return self._versions.get(self._selected) if self._selected else None

    def compatibility(self, version: str, required: set[str]) -> bool:
        info = self._versions.get(version)
        return bool(info and info.available and required <= info.capabilities)
