#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from openclaw_trading_suite.adapters import AdapterRegistry
from openclaw_trading_suite.adapters.mock import (
    MockExecutionAdapter,
    MockMarketDataAdapter,
    MockNewsAdapter,
)
from openclaw_trading_suite.db import SQLiteStore
from openclaw_trading_suite.research import OvernightResearchConfig, run_overnight_research_safe
from openclaw_trading_suite.security import redact_sensitive, redact_structure


def _load_config(path: Path | None) -> dict:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return path.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Run overnight research and generate report.")
    parser.add_argument("--config", type=Path, default=None, help="Optional JSON config path.")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=ROOT / "runtime" / "data" / "openclaw_trading.sqlite3",
        help="SQLite database path.",
    )
    args = parser.parse_args()

    cfg_json = _load_config(args.config)
    report_date = cfg_json.get("report_date") or datetime.now(UTC).date().isoformat()
    cfg = OvernightResearchConfig(
        report_dir=ROOT / "runtime" / "reports",
        report_date=report_date,
        autonomy_level=cfg_json.get("autonomy_level", "balanced"),
        market_symbols=cfg_json.get("market_symbols", ["SPY", "QQQ", "BTCUSD"]),
        research_topics=cfg_json.get(
            "research_topics",
            ["international macro", "crypto regulation", "rates and inflation"],
        ),
        strategy_focus=cfg_json.get("strategy_focus", ["swing_baseline", "contrarian_skew"]),
        preferred_market_adapter=cfg_json.get("preferred_market_adapter"),
        preferred_news_adapter=cfg_json.get("preferred_news_adapter"),
        fallback_market_adapters=cfg_json.get("fallback_market_adapters"),
        fallback_news_adapters=cfg_json.get("fallback_news_adapters"),
    )

    store = SQLiteStore(args.db_path)
    store.init_schema()

    registry = AdapterRegistry()
    registry.register(MockExecutionAdapter())
    registry.register(MockMarketDataAdapter())
    registry.register(MockNewsAdapter())

    report_path, error = run_overnight_research_safe(cfg, registry, store)
    if error:
        log_payload = redact_structure(
            {
                "event": "overnight_report_failed",
                "db_path": _display_path(args.db_path),
                "autonomy_level": cfg.autonomy_level,
                "error": error,
            }
        )
        print(redact_sensitive(str(log_payload)))
        return 1
    log_payload = redact_structure(
        {
            "event": "overnight_report_generated",
            "report_path": _display_path(report_path),
            "db_path": _display_path(args.db_path),
            "autonomy_level": cfg.autonomy_level,
        }
    )
    print(redact_sensitive(str(log_payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
