from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_cex_daily_orchestrator.py"
SPEC = importlib.util.spec_from_file_location("cex_daily_test_module", MODULE_PATH)
assert SPEC and SPEC.loader
daily = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = daily
SPEC.loader.exec_module(daily)


class BinanceSmartMoneyTests(unittest.TestCase):
    def test_success_without_match_is_not_zero_signal(self) -> None:
        gaps: list[str] = []
        with patch.object(
            daily,
            "_http_post_json",
            return_value={"success": True, "data": []},
        ):
            result = daily._fetch_binance_smart_money_signals(
                {"56"}, {"Accept-Encoding": "identity"}, gaps
            )

        self.assertEqual(result["56"]["status"], "available")
        self.assertEqual(result["56"]["signals"], {})
        self.assertEqual(gaps, [])

    def test_source_failure_is_structured_and_recorded(self) -> None:
        gaps: list[str] = []
        with patch.object(daily, "_http_post_json", side_effect=TimeoutError("timed out")):
            result = daily._fetch_binance_smart_money_signals(
                {"56"}, {"Accept-Encoding": "identity"}, gaps
            )

        self.assertEqual(result["56"]["status"], "source_unavailable")
        self.assertEqual(result["56"]["signals"], {})
        self.assertEqual(len(gaps), 1)
        self.assertIn("Binance Web3 BSC 聪明钱信号获取失败", gaps[0])

    def test_unsupported_chain_does_not_call_source(self) -> None:
        gaps: list[str] = []
        with patch.object(daily, "_http_post_json") as post:
            result = daily._fetch_binance_smart_money_signals(
                {"1"}, {"Accept-Encoding": "identity"}, gaps
            )

        post.assert_not_called()
        self.assertEqual(result["1"]["status"], "unsupported_chain")
        self.assertEqual(gaps, [])


if __name__ == "__main__":
    unittest.main()
