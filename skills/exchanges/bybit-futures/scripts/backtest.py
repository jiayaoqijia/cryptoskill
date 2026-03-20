"""
Backtesting Engine — test strategies against historical data.
Fetches OHLCV from Bybit, runs strategy, reports metrics.
"""
import json
import ccxt
import logging
from datetime import datetime

try:
    import config
except ImportError:
    import config_template as config

log = logging.getLogger("backtest")


def fetch_candles(symbol: str, timeframe: str = "1h", limit: int = 1000) -> list:
    exchange = ccxt.bybit({"enableRateLimit": True, "options": {"defaultType": "swap"}})
    candles = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return [{"t": c[0], "o": c[1], "h": c[2], "l": c[3], "c": c[4], "v": c[5]} for c in candles]


def calc_ema(closes: list, span: int) -> list:
    ema = [closes[0]]
    k = 2 / (span + 1)
    for c in closes[1:]:
        ema.append(c * k + ema[-1] * (1 - k))
    return ema


def calc_rsi(closes: list, period: int = 14) -> list:
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    rsi = [50.0] * period
    gains = [max(d, 0) for d in deltas[:period]]
    losses = [max(-d, 0) for d in deltas[:period]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    for i in range(period, len(deltas)):
        d = deltas[i]
        avg_gain = (avg_gain * (period - 1) + max(d, 0)) / period
        avg_loss = (avg_loss * (period - 1) + max(-d, 0)) / period
        rs = avg_gain / avg_loss if avg_loss else float("inf")
        rsi.append(100 - (100 / (1 + rs)))
    return rsi


def backtest_ema(candles: list, fast: int = 12, slow: int = 26,
                 capital: float = 1000, leverage: int = 5, pos_pct: float = 0.2,
                 sl_pct: float = 0.03, tp_pct: float = 0.06) -> dict:
    """Backtest EMA crossover strategy."""
    closes = [c["c"] for c in candles]
    ema_fast = calc_ema(closes, fast)
    ema_slow = calc_ema(closes, slow)

    trades = []
    position = None
    bal = capital

    for i in range(slow + 1, len(closes)):
        price = closes[i]

        # Check SL/TP
        if position:
            if position["side"] == "long":
                if price <= position["sl"]:
                    pnl = (position["sl"] - position["entry"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "SL"})
                    position = None
                elif price >= position["tp"]:
                    pnl = (position["tp"] - position["entry"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "TP"})
                    position = None
            else:
                if price >= position["sl"]:
                    pnl = (position["entry"] - position["sl"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "SL"})
                    position = None
                elif price <= position["tp"]:
                    pnl = (position["entry"] - position["tp"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "TP"})
                    position = None

        golden = ema_fast[i - 1] <= ema_slow[i - 1] and ema_fast[i] > ema_slow[i]
        death = ema_fast[i - 1] >= ema_slow[i - 1] and ema_fast[i] < ema_slow[i]

        if position:
            if position["side"] == "long" and death:
                pnl = (price - position["entry"]) / position["entry"] * position["margin"] * leverage
                bal += pnl - position["fee"]
                trades.append({"pnl": pnl - position["fee"], "reason": "signal"})
                position = None
            elif position["side"] == "short" and golden:
                pnl = (position["entry"] - price) / position["entry"] * position["margin"] * leverage
                bal += pnl - position["fee"]
                trades.append({"pnl": pnl - position["fee"], "reason": "signal"})
                position = None
        else:
            margin = bal * pos_pct
            fee = margin * leverage * 0.0006
            if golden:
                position = {"side": "long", "entry": price, "margin": margin, "fee": fee,
                            "sl": price * (1 - sl_pct), "tp": price * (1 + tp_pct)}
            elif death:
                position = {"side": "short", "entry": price, "margin": margin, "fee": fee,
                            "sl": price * (1 + sl_pct), "tp": price * (1 - tp_pct)}

    wins = [t for t in trades if t["pnl"] > 0]
    total_pnl = sum(t["pnl"] for t in trades)
    return {
        "strategy": f"EMA({fast}/{slow})",
        "trades": len(trades), "wins": len(wins),
        "win_rate": len(wins) / len(trades) * 100 if trades else 0,
        "total_pnl": round(total_pnl, 2),
        "final_balance": round(bal, 2),
    }


def backtest_rsi(candles: list, period: int = 14, oversold: int = 30, overbought: int = 70,
                 capital: float = 1000, leverage: int = 5, pos_pct: float = 0.2,
                 sl_pct: float = 0.03, tp_pct: float = 0.06) -> dict:
    """Backtest RSI mean reversion strategy."""
    closes = [c["c"] for c in candles]
    rsi = calc_rsi(closes, period)

    trades = []
    position = None
    bal = capital

    for i in range(period + 1, len(closes)):
        price = closes[i]

        if position:
            if position["side"] == "long":
                if price <= position["sl"]:
                    pnl = (position["sl"] - position["entry"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "SL"})
                    position = None
                elif price >= position["tp"]:
                    pnl = (position["tp"] - position["entry"]) / position["entry"] * position["margin"] * leverage
                    bal += pnl - position["fee"]
                    trades.append({"pnl": pnl - position["fee"], "reason": "TP"})
                    position = None

        curr, prev = rsi[i], rsi[i - 1]

        if position:
            if position["side"] == "long" and curr > overbought:
                pnl = (price - position["entry"]) / position["entry"] * position["margin"] * leverage
                bal += pnl - position["fee"]
                trades.append({"pnl": pnl - position["fee"], "reason": "signal"})
                position = None
            elif position["side"] == "short" and curr < oversold:
                pnl = (position["entry"] - price) / position["entry"] * position["margin"] * leverage
                bal += pnl - position["fee"]
                trades.append({"pnl": pnl - position["fee"], "reason": "signal"})
                position = None
        else:
            margin = bal * pos_pct
            fee = margin * leverage * 0.0006
            if prev < oversold and curr >= oversold:
                position = {"side": "long", "entry": price, "margin": margin, "fee": fee,
                            "sl": price * (1 - sl_pct), "tp": price * (1 + tp_pct)}
            elif prev > overbought and curr <= overbought:
                position = {"side": "short", "entry": price, "margin": margin, "fee": fee,
                            "sl": price * (1 + sl_pct), "tp": price * (1 - tp_pct)}

    wins = [t for t in trades if t["pnl"] > 0]
    total_pnl = sum(t["pnl"] for t in trades)
    return {
        "strategy": f"RSI({period},{oversold}/{overbought})",
        "trades": len(trades), "wins": len(wins),
        "win_rate": len(wins) / len(trades) * 100 if trades else 0,
        "total_pnl": round(total_pnl, 2),
        "final_balance": round(bal, 2),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    for symbol in config.SYMBOLS:
        coin = symbol.split("/")[0]
        print(f"\n=== {coin} ===")
        candles = fetch_candles(symbol, "1h", 2000)
        print(f"Fetched {len(candles)} candles")

        ema_result = backtest_ema(candles)
        print(f"EMA(12/26): {ema_result['trades']} trades, {ema_result['win_rate']:.0f}% WR, PnL: ${ema_result['total_pnl']}")

        rsi_result = backtest_rsi(candles)
        print(f"RSI(14,30/70): {rsi_result['trades']} trades, {rsi_result['win_rate']:.0f}% WR, PnL: ${rsi_result['total_pnl']}")
