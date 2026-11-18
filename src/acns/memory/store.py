from __future__ import annotations

import json
import sqlite3
from abc import ABC, abstractmethod
from typing import Any


class MemoryStore(ABC):
    @abstractmethod
    def put(self, key: str, value: dict[str, Any], *, memory_type: str = "working", source: str = "unknown", confidence: float = 1.0) -> None: ...

    @abstractmethod
    def search(self, query: str, *, memory_type: str | None = None, limit: int = 10) -> list[dict[str, Any]]: ...

    @abstractmethod
    def forget(self, key: str) -> None: ...


class SQLiteMemoryStore(MemoryStore):
    def __init__(self, path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("""CREATE TABLE IF NOT EXISTS memories (
            key TEXT PRIMARY KEY, memory_type TEXT NOT NULL, value TEXT NOT NULL,
            source TEXT NOT NULL, confidence REAL NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        self.connection.commit()

    def put(self, key: str, value: dict[str, Any], *, memory_type: str = "working", source: str = "unknown", confidence: float = 1.0) -> None:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        self.connection.execute("""INSERT INTO memories(key, memory_type, value, source, confidence)
            VALUES (?, ?, ?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value,
            memory_type=excluded.memory_type, source=excluded.source, confidence=excluded.confidence,
            updated_at=CURRENT_TIMESTAMP""", (key, memory_type, json.dumps(value, ensure_ascii=False), source, confidence))
        self.connection.commit()

    def search(self, query: str, *, memory_type: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        pattern = f"%{query}%"
        if memory_type:
            rows = self.connection.execute("SELECT * FROM memories WHERE memory_type=? AND (key LIKE ? OR value LIKE ?) ORDER BY updated_at DESC LIMIT ?", (memory_type, pattern, pattern, limit)).fetchall()
        else:
            rows = self.connection.execute("SELECT * FROM memories WHERE key LIKE ? OR value LIKE ? ORDER BY updated_at DESC LIMIT ?", (pattern, pattern, limit)).fetchall()
        return [{**dict(row), "value": json.loads(row["value"])} for row in rows]

    def forget(self, key: str) -> None:
        self.connection.execute("DELETE FROM memories WHERE key=?", (key,))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
