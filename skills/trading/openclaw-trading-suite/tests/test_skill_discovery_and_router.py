from pathlib import Path

from openclaw_trading_suite.adapters import (
    AdapterRouter,
    AdapterType,
    ResolutionMode,
    SkillDiscoveryService,
)


def _write_skill(root: Path, folder: str, name: str) -> None:
    skill_dir = root / folder
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: test\n---\n",
        encoding="utf-8",
    )


def test_discovery_refreshes_and_finds_new_skills(tmp_path) -> None:
    root = tmp_path / "skills"
    _write_skill(root, "a1", "alpaca-mcp")
    discovery = SkillDiscoveryService(skill_roots=[root], ttl_seconds=3600)
    first = discovery.refresh(force=True)
    assert "alpaca-mcp" in first

    _write_skill(root, "a2", "binance-api")
    cached = discovery.refresh(force=False)
    assert "binance-api" not in cached

    refreshed = discovery.refresh(force=True)
    assert "binance-api" in refreshed


def test_router_can_switch_between_skill_and_direct(tmp_path) -> None:
    root = tmp_path / "skills"
    _write_skill(root, "x1", "alpaca-mcp")
    router = AdapterRouter(discovery=SkillDiscoveryService(skill_roots=[root], ttl_seconds=3600))

    skill_route = router.resolve("alpaca", AdapterType.EXECUTION, force_refresh_skills=True)
    assert skill_route.mode == ResolutionMode.SKILL_BACKED

    router.set_preference("alpaca", prefer_skill=False)
    direct_route = router.resolve("alpaca", AdapterType.EXECUTION, force_refresh_skills=False)
    assert direct_route.mode == ResolutionMode.DIRECT_ADAPTER

