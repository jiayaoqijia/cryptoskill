import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from local_agent import deterministic_report, extract_symbol


class V13Tests(unittest.TestCase):
    def sample(self):
        return {"symbol": "BTCUSDT", "signal": "HOLD", "as_of_utc": "2026-11-16T19:52:59+00:00",
                "as_of_15m_utc": "2026-11-16T19:44:59+00:00", "trend_15m": "BULLISH",
                "close_15m": 64787.4, "ema21_15m": 64760.05, "ema9_1m": 64865.45,
                "ema21_1m": 64842.14, "rsi14_1m": 71.78, "volume_1m": 42.48,
                "volume_ma10_1m": 48.97,
                "conditions": {"buy": {"trend_bullish": True, "ema9_above_ema21": True,
                                       "rsi_below_48": False, "volume_above_ma10": False},
                               "sell": {"trend_bearish": False, "ema9_below_ema21": False,
                                        "rsi_above_52": True, "volume_above_ma10": False}}}

    def test_report_has_correct_timeframes(self):
        result = deterministic_report(self.sample())
        self.assertIn("15m trend: BULLISH", result)
        self.assertIn("1m EMA9", result)
        self.assertIn("PASS: ema9_above_ema21", result)
        self.assertIn("FAIL: volume_above_ma10", result)

    def test_inconsistent_signal_rejected(self):
        data = self.sample()
        data["signal"] = "BUY"
        with self.assertRaises(ValueError):
            deterministic_report(data)

    def test_insufficient_data_fallback(self):
        self.assertIn("Insufficient", deterministic_report({"symbol": "BTCUSDT", "signal": "HOLD", "reason": "Insufficient candles"}))

    def test_symbol_extraction(self):
        self.assertEqual(extract_symbol("Analyze ETH/USDT"), "ETHUSDT")


if __name__ == "__main__":
    unittest.main()
