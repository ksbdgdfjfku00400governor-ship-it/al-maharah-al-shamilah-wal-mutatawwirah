import time
from acns import CognitiveCore, SQLiteMemoryStore


def test_local_offline_acceptance_scenario():
    started = time.perf_counter()
    state = CognitiveCore(SQLiteMemoryStore()).run("create an offline cognitive cycle")
    elapsed = time.perf_counter() - started
    assert state.status == "completed"
    assert elapsed < 2.0
    assert all(result.evidence for result in state.results.values())


def test_learning_requires_explicit_permission():
    store = SQLiteMemoryStore()
    state = CognitiveCore(store).run("do not persist this lesson")
    assert state.results["learning"].output["persisted"] is False
    assert store.search("lesson:", memory_type="procedural") == []
