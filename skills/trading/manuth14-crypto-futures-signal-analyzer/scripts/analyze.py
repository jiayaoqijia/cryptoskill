#!/usr/bin/env python3
"""Read-only futures analysis using completed Binance USD-M candles."""
import argparse
import json
import math
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = 'https://fapi.binance.com/fapi/v1/klines'


def ema(values, period):
    if not values:
        raise ValueError('Empty EMA series')
    alpha = 2 / (period + 1)
    out = [float(values[0])]
    for value in values[1:]:
        out.append(alpha * float(value) + (1 - alpha) * out[-1])
    return out


def rsi(values, period=14):
    if len(values) < period + 1:
        raise ValueError('Insufficient RSI history')
    changes = [float(values[i]) - float(values[i - 1]) for i in range(1, len(values))]
    result = [None] * period
    for end in range(period, len(changes) + 1):
        window = changes[end - period:end]
        gain = sum(max(x, 0) for x in window) / period
        loss = sum(max(-x, 0) for x in window) / period
        loss = loss if loss != 0 else 0.00001
        result.append(100 - 100 / (1 + gain / loss))
    return result


def utc_timestamp(milliseconds):
    return datetime.fromtimestamp(milliseconds / 1000, timezone.utc).isoformat() if milliseconds is not None else None


def get_candles(symbol, interval, limit=150):
    query = urllib.parse.urlencode({'symbol': symbol, 'interval': interval, 'limit': limit})
    req = urllib.request.Request(BASE + '?' + query, headers={'User-Agent': 'CryptoSignalAnalyzer/1.2'})
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            rows = json.load(response)
    except urllib.error.HTTPError as exc:
        raise ValueError(f'Binance API HTTP {exc.code}') from exc
    except urllib.error.URLError as exc:
        raise ValueError(f'Binance API connection failed: {exc.reason}') from exc
    except (TimeoutError, json.JSONDecodeError) as exc:
        raise ValueError(f'Binance API response failed: {exc}') from exc
    if not isinstance(rows, list) or not rows:
        raise ValueError('Unexpected market data response')
    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    candles = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 7:
            raise ValueError('Malformed market candle')
        candles.append({'open_time': int(row[0]), 'close_time': int(row[6]),
                        'close': float(row[4]), 'volume': float(row[5])})
    return [c for c in candles if c['close_time'] < now]


def analyze(symbol, short, long):
    if len(short) < 30 or len(long) < 30:
        return {'symbol': symbol, 'signal': 'HOLD',
                'reason': 'Insufficient candles: need at least 30 completed candles per timeframe'}
    closes = [float(x['close']) for x in short]
    volumes = [float(x['volume']) for x in short]
    trend_closes = [float(x['close']) for x in long]
    if not all(math.isfinite(x) and x > 0 for x in closes + trend_closes):
        raise ValueError('Invalid close prices')
    if not all(math.isfinite(x) and x >= 0 for x in volumes):
        raise ValueError('Invalid volumes')
    e9 = ema(closes, 9)[-1]
    e21 = ema(closes, 21)[-1]
    trend_ema21 = ema(trend_closes, 21)[-1]
    close_15m = trend_closes[-1]
    bullish = close_15m > trend_ema21
    trend = 'BULLISH' if bullish else 'BEARISH'
    current_rsi = rsi(closes, 14)[-1]
    volume_ma = sum(volumes[-10:]) / 10
    volume_ok = volumes[-1] > volume_ma
    buy = bullish and e9 > e21 and current_rsi < 48 and volume_ok
    sell = (not bullish) and e9 < e21 and current_rsi > 52 and volume_ok
    signal = 'BUY' if buy else ('SELL' if sell else 'HOLD')
    conditions = {
        'buy': {'trend_bullish': bullish, 'ema9_above_ema21': e9 > e21,
                'rsi_below_48': current_rsi < 48, 'volume_above_ma10': volume_ok},
        'sell': {'trend_bearish': not bullish, 'ema9_below_ema21': e9 < e21,
                 'rsi_above_52': current_rsi > 52, 'volume_above_ma10': volume_ok}
    }
    return {
        'symbol': symbol, 'signal': signal,
        'data_source': 'Binance USD-M futures public klines',
        'as_of_utc': utc_timestamp(short[-1].get('close_time')),
        'as_of_15m_utc': utc_timestamp(long[-1].get('close_time')),
        'price': closes[-1], 'close_15m': close_15m,
        'trend_15m': trend, 'ema21_15m': trend_ema21,
        'ema9_1m': e9, 'ema21_1m': e21, 'rsi14_1m': current_rsi,
        'volume_1m': volumes[-1], 'volume_ma10_1m': volume_ma,
        'volume_confirmed': volume_ok, 'conditions': conditions,
        'illustrative_levels': None,
        'notes': ['Matches supplied original BUY/SELL/HOLD conditions, using completed candles',
                  'RSI uses simple rolling averages, not Wilder smoothing',
                  'EMA direction is tested, not a fresh crossover event',
                  'No orders placed; not financial advice']
    }


def main():
    parser = argparse.ArgumentParser(description='Read-only crypto technical analysis')
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--fixture', help='JSON containing candles_1m and candles_15m')
    args = parser.parse_args()
    symbol = args.symbol.upper()
    if not symbol.isascii() or not symbol.isalnum() or len(symbol) > 20 or not symbol.endswith('USDT'):
        parser.error('symbol must be a USDT pair such as BTCUSDT')
    try:
        if args.fixture:
            with open(args.fixture, encoding='utf-8') as f:
                data = json.load(f)
            short, long = data['candles_1m'], data['candles_15m']
        else:
            short, long = get_candles(symbol, '1m'), get_candles(symbol, '15m')
        print(json.dumps(analyze(symbol, short, long), indent=2, allow_nan=False))
    except (ValueError, KeyError, OSError, TimeoutError, TypeError, OverflowError) as exc:
        print(json.dumps({'error': str(exc), 'symbol': symbol}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
