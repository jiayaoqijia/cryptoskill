from openclaw_trading_suite.adapters import (
    ADAPTER_SPECS,
    AdapterType,
    ResolutionMode,
    resolve_adapter_target,
)


def test_catalog_contains_requested_core_and_optional_providers() -> None:
    names = {spec.provider for spec in ADAPTER_SPECS}
    assert "alpaca" in names
    assert "binance" in names
    assert "taapi" in names
    assert "kraken" in names
    assert "ibkr" in names
    assert "x-sentiment" in names
    assert "weibo-sentiment" in names
    assert "brave-search" in names


def test_resolution_prefers_skill_when_alias_matches() -> None:
    result = resolve_adapter_target(
        provider="alpaca",
        adapter_type=AdapterType.EXECUTION,
        available_skill_names=["my-alpaca-mcp-skill"],
        prefer_skill=True,
    )
    assert result.mode == ResolutionMode.SKILL_BACKED


def test_resolution_falls_back_to_direct_adapter() -> None:
    result = resolve_adapter_target(
        provider="taapi",
        adapter_type=AdapterType.MARKET_DATA,
        available_skill_names=["some-other-skill"],
        prefer_skill=True,
    )
    assert result.mode == ResolutionMode.DIRECT_ADAPTER

