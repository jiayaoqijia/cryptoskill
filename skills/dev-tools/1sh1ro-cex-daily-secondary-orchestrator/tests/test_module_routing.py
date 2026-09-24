from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cex_daily_modules.market import collect  # noqa: E402
from cex_daily_modules.registry import MODULES, MODULE_SOURCES  # noqa: E402


class DailyModuleRoutingTests(unittest.TestCase):
    def test_registry_has_stable_module_contract(self) -> None:
        self.assertEqual(set(MODULES), {"market", "derivatives", "yields", "rwa", "sentiment"})
        self.assertEqual(set(MODULE_SOURCES), set(MODULES))

    def test_market_module_returns_standard_envelope(self) -> None:
        engine = SimpleNamespace(
            _fetch_market_day=lambda target, gaps, lookback_days: {"market_cap": 100.0, "btc_dom": 50.0},
            _fetch_top_assets=lambda gaps: ([{"symbol": "BTC", "mcap": 50.0}], {"status": "ok", "used": "demo"}),
            _fetch_exchanges=lambda gaps: [],
            _fetch_top2_24h_trend=lambda gaps: {},
            _fetch_top2_1h_series=lambda target, gaps, hours: {},
            _build_breadth_snapshot=lambda market_cap, btc_dom, assets: {"btc_share": btc_dom},
        )
        result = collect(engine, date(2026, 7, 26))
        self.assertEqual(result.module, "market")
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.data["market"]["market_cap"], 100.0)
        self.assertIn("top_assets", result.sources)


if __name__ == "__main__":
    unittest.main()
