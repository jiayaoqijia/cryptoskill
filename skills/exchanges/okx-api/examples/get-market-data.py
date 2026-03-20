"""
Get OKX market data: ticker price and recent candlesticks.

Usage:
    python get-market-data.py BTC-USDT
    python get-market-data.py ETH-USDT 4H   # 4-hour candles
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from okx_auth import make_request


def get_ticker(inst_id: str):
    data = make_request("GET", "/api/v5/market/ticker", params={"instId": inst_id})
    if not data:
        print(f"No ticker data for {inst_id}")
        return

    t = data[0]
    last = float(t.get("last", 0))
    open24h = float(t.get("open24h", 0))
    high24h = float(t.get("high24h", 0))
    low24h = float(t.get("low24h", 0))
    vol24h = float(t.get("vol24h", 0))
    change_pct = ((last - open24h) / open24h * 100) if open24h else 0

    print(f"=== {inst_id} Ticker ===")
    print(f"Last price:    {last:,.4f}")
    print(f"24h change:    {change_pct:+.2f}%")
    print(f"24h high:      {high24h:,.4f}")
    print(f"24h low:       {low24h:,.4f}")
    print(f"24h volume:    {vol24h:,.2f}")
    print()


def get_candles(inst_id: str, bar: str = "1H", limit: int = 10):
    data = make_request(
        "GET",
        "/api/v5/market/candles",
        params={"instId": inst_id, "bar": bar, "limit": str(limit)},
    )

    print(f"=== {inst_id} Candlesticks ({bar}, last {len(data)}) ===")
    print(f"{'Time':<22} {'Open':>12} {'High':>12} {'Low':>12} {'Close':>12} {'Volume':>14}")
    print("-" * 90)

    for candle in reversed(data):
        # candle: [ts, open, high, low, close, vol, volCcy, volCcyQuote, confirm]
        ts = int(candle[0]) / 1000
        dt = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        o, h, l, c, vol = float(candle[1]), float(candle[2]), float(candle[3]), float(candle[4]), float(candle[5])
        print(f"{dt:<22} {o:>12,.2f} {h:>12,.2f} {l:>12,.2f} {c:>12,.2f} {vol:>14,.4f}")


def main():
    inst_id = sys.argv[1] if len(sys.argv) > 1 else "BTC-USDT"
    bar = sys.argv[2] if len(sys.argv) > 2 else "1H"

    get_ticker(inst_id)
    get_candles(inst_id, bar)


if __name__ == "__main__":
    main()
