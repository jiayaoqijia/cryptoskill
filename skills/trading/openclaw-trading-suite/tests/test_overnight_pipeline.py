from openclaw_trading_suite.adapters import AdapterRegistry
from openclaw_trading_suite.adapters.mock import (
    MockExecutionAdapter,
    MockMarketDataAdapter,
    MockNewsAdapter,
)
from openclaw_trading_suite.db import SQLiteStore
from openclaw_trading_suite.research import OvernightResearchConfig, run_overnight_research


def test_overnight_pipeline_creates_report_and_db_record(tmp_path) -> None:
    db_path = tmp_path / "suite.sqlite3"
    store = SQLiteStore(db_path)
    store.init_schema()

    registry = AdapterRegistry()
    registry.register(MockExecutionAdapter())
    registry.register(MockMarketDataAdapter())
    registry.register(MockNewsAdapter())

    cfg = OvernightResearchConfig(
        report_dir=tmp_path / "reports",
        report_date="2026-02-27",
        autonomy_level="balanced",
        market_symbols=["SPY", "BTCUSD"],
        research_topics=["asia markets"],
        strategy_focus=["swing_baseline"],
    )
    report_path = run_overnight_research(cfg, registry, store)
    text = report_path.read_text(encoding="utf-8")
    json_text = (tmp_path / "reports" / "while-you-were-sleeping-2026-02-27.json").read_text(
        encoding="utf-8"
    )

    assert report_path.exists()
    assert "While You Were Sleeping Report" in text
    assert "asia markets" in text
    assert '"topic": "asia markets"' in json_text
