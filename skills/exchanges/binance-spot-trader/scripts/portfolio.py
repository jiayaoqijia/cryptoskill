#!/usr/bin/env python3
"""Portfolio tracker for Binance Spot Trader."""
import os, json, hmac, hashlib, time
from urllib.parse import urlencode
from dotenv import load_dotenv
import httpx

load_dotenv()
API_KEY = os.environ["BINANCE_API_KEY"]
SECRET_KEY = os.environ["BINANCE_SECRET_KEY"]
BASE = "https://api.binance.com"

def sign(params):
    params["timestamp"] = int(time.time() * 1000)
    query = urlencode(params)
    params["signature"] = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return params

with httpx.Client(timeout=15) as c:
    info = c.get(f"{BASE}/api/v3/account", params=sign({}), headers={"X-MBX-APIKEY": API_KEY}).json()
    total = 0
    print(f"{'Asset':>8} {'Free':>12} {'Locked':>12} {'USD Value':>12}")
    print("=" * 48)
    for b in info.get("balances", []):
        free = float(b["free"])
        locked = float(b["locked"])
        if free + locked < 0.00001: continue
        # Get price
        usd = 0
        if b["asset"] == "USDT":
            usd = free + locked
        else:
            try:
                p = c.get(f"{BASE}/api/v3/ticker/price", params={"symbol": f"{b['asset']}USDT"}).json()
                usd = (free + locked) * float(p.get("price", 0))
            except: pass
        total += usd
        print(f"{b['asset']:>8} {free:>12.4f} {locked:>12.4f} ${usd:>11.2f}")
    print("=" * 48)
    print(f"{'TOTAL':>8} {'':>12} {'':>12} ${total:>11.2f}")
