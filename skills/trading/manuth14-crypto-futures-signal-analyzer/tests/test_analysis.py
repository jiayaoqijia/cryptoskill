import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('analyzer',Path(__file__).resolve().parents[1]/'scripts'/'analyze.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

def candles(closes, volumes=None):
    if volumes is None: volumes=[10.0]*len(closes)
    return [{'close':c,'volume':v,'close_time':(i+1)*60000} for i,(c,v) in enumerate(zip(closes,volumes))]

class Tests(unittest.TestCase):
    def test_ema_matches_pandas_initialization(self):
        self.assertAlmostEqual(a.ema([10,20,30],9)[-1],15.6)
    def test_rsi_up_matches_original_zero_loss_epsilon(self):
        self.assertGreater(a.rsi(list(range(40)))[-1],99.9)
        self.assertLess(a.rsi(list(range(40)))[-1],100)
    def test_hold_constant(self):
        rows=candles([100.0]*50)
        self.assertEqual(a.analyze('BTCUSDT',rows,rows)['signal'],'HOLD')
    def test_buy_without_fresh_cross(self):
        # Long term trend bullish, short-term pullback, but EMA9 still > EMA21
        long=candles([100+i for i in range(50)])
        short=candles([100+i*.5 for i in range(42)]+[120,119,118,117,116,115,114,113], [10]*49+[100])
        result=a.analyze('BTCUSDT',short,long)
        self.assertEqual(result['signal'],'BUY')
    def test_sell(self):
        long=candles([150-i for i in range(50)])
        short=candles([150-i*.5 for i in range(42)]+[130,131,132,133,134,135,136,137], [10]*49+[100])
        self.assertEqual(a.analyze('BTCUSDT',short,long)['signal'],'SELL')
    def test_volume_ma_includes_current(self):
        long=candles([100+i for i in range(50)])
        short=candles([100+i for i in range(50)],[10]*49+[100])
        self.assertAlmostEqual(a.analyze('BTCUSDT',short,long)['volume_ma10_1m'],19)
    def test_insufficient_history(self):
        self.assertEqual(a.analyze('BTCUSDT',candles([100]*29),candles([100]*50))['signal'],'HOLD')
if __name__=='__main__': unittest.main()


class FuturesSourceTests(unittest.TestCase):
    def test_futures_endpoint(self):
        self.assertEqual(a.BASE, "https://fapi.binance.com/fapi/v1/klines")

    def test_futures_source_label(self):
        candles = [{"close": 100.0, "volume": 1.0, "close_time": 1700000000000} for _ in range(35)]
        self.assertIn("futures", a.analyze("BTCUSDT", candles, candles)["data_source"].lower())
