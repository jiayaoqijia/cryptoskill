import importlib.util
import unittest
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("analyzer_v12", root / "scripts" / "analyze.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def candles(closes):
    return [{"close": c, "volume": 10.0, "close_time": (i + 1) * 60000} for i, c in enumerate(closes)]


class V12Tests(unittest.TestCase):
    def test_15m_trend_close_is_exposed(self):
        short = candles([100.0] * 50)
        long = candles([100 + i for i in range(50)])
        result = a.analyze("BTCUSDT", short, long)
        self.assertEqual(result["close_15m"], 149)
        self.assertEqual(result["trend_15m"], "BULLISH")
        self.assertGreater(result["close_15m"], result["ema21_15m"])
        self.assertIsNotNone(result["as_of_15m_utc"])

    def test_invalid_close_rejected(self):
        short = candles([100.0] * 49 + [float("nan")])
        with self.assertRaisesRegex(ValueError, "Invalid close"):
            a.analyze("BTCUSDT", short, candles([100.0] * 50))

    def test_15m_bearish_when_equal(self):
        data = candles([100.0] * 50)
        self.assertEqual(a.analyze("BTCUSDT", data, data)["trend_15m"], "BEARISH")


if __name__ == "__main__":
    unittest.main()
