from openclaw_trading_suite.adapters import AdapterRegistry, AdapterType
from openclaw_trading_suite.adapters.mock import (
    MockExecutionAdapter,
    MockMarketDataAdapter,
    MockNewsAdapter,
)


def test_registry_registers_and_lists_adapters() -> None:
    registry = AdapterRegistry()
    registry.register(MockExecutionAdapter())
    registry.register(MockMarketDataAdapter())
    registry.register(MockNewsAdapter())

    assert registry.list_names(AdapterType.EXECUTION) == ["mock-execution"]
    assert registry.list_names(AdapterType.MARKET_DATA) == ["mock-market-data"]
    assert registry.list_names(AdapterType.NEWS) == ["mock-news"]


def test_registry_capability_snapshot() -> None:
    registry = AdapterRegistry()
    registry.register(MockExecutionAdapter())
    snap = registry.capability_snapshot()
    assert "execution" in snap
    assert snap["execution"] == ["mock-execution"]

