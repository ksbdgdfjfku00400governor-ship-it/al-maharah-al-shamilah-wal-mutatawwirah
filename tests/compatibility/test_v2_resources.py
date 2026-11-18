from acns.resource_intelligence import PermissionManager, Resource, ResourceIntelligenceEngine, ResourceRegistry
from acns.version_manager import VersionInfo, VersionManager


def test_resource_engine_scores_and_selects_permitted_resource():
    registry = ResourceRegistry()
    registry.register(Resource("local-a", "local", "A", frozenset({"search", "parse"}), 0.9, 0.9, 0.8, 0.1, 0.1))
    registry.register(Resource("remote-a", "remote", "Remote", frozenset({"search", "parse"}), 1, 1, 1, 0, 0))
    engine = ResourceIntelligenceEngine(registry, permission=PermissionManager({"local"}))
    selected = engine.best({"search", "parse"})
    assert selected is not None
    assert selected.resource.resource_id == "local-a"


def test_resource_engine_fallback_excludes_failed_candidate():
    registry = ResourceRegistry()
    registry.register(Resource("a", "local", "A", frozenset({"parse"}), 0.9, 0.9, 0.9, 0.1, 0.1))
    registry.register(Resource("b", "local", "B", frozenset({"parse"}), 0.8, 0.8, 0.8, 0.2, 0.2))
    engine = ResourceIntelligenceEngine(registry)
    assert engine.best({"parse"}, excluded={"a"}).resource.resource_id == "b"


def test_version_manager_keeps_versions_independent():
    manager = VersionManager()
    manager.register(VersionInfo("1.0", "Cognitive Core", frozenset({"core"})))
    manager.register(VersionInfo("2.0", "Resource Intelligence", frozenset({"core", "resources"})))
    assert manager.select("1.0").version == "1.0"
    assert manager.current().version == "1.0"
    assert manager.compatibility("2.0", {"resources"}) is True
    assert manager.compatibility("1.0", {"resources"}) is False
