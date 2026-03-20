#!/usr/bin/env python3
"""VWAP Crossover bot for Maxxit Lazy Trading.
Combines Volume Weighted Average Price (VWAP) with EMA for momentum confirmation.
"""
import json
import logging
import math
import os
import sys
import argparse
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

# Configuration
BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
MAXXIT_API_URL = os.environ.get("MAXXIT_API_URL")
MAXXIT_API_KEY = os.environ.get("MAXXIT_API_KEY")

def parse_args():
    parser = argparse.ArgumentParser(description="VWAP Crossover Strategy Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTC/USD)")
    parser.add_argument("--venue", required=True, choices=["OSTIUM", "AVANTIS"], help="Trading venue (OSTIUM or AVANTIS)")
    parser.add_argument("--leverage", type=int, default=10, help="Leverage to use")
    parser.add_argument("--utilization", type=float, default=0.8, help="Collateral utilization ratio")
    return parser.parse_args()

args = parse_args()

# Global Parameters from Args
SYMBOL = args.symbol
MARKET = SYMBOL.split('/')[0]
VENUE = args.venue.upper()
COLLATERAL_UTILIZATION = args.utilization
LEVERAGE = args.leverage

# Strategy Parameters
EMA_PERIOD = 20

STATE_FILE = os.path.join(BASE_DIR, f"{VENUE.lower()}_{MARKET.lower()}_vwap_state.json")
LOG_FILE = os.path.join(LOG_DIR, f"{VENUE.lower()}_{MARKET.lower()}_vwap.log")

def log(message: str) -> None:
    logging.info(message)
    print(f"{datetime.utcnow().isoformat()} - {message}")

def ensure_environment() -> None:
    if not MAXXIT_API_URL or not MAXXIT_API_KEY:
        raise EnvironmentError("MAXXIT_API_URL and MAXXIT_API_KEY must be set")
    os.makedirs(LOG_DIR, exist_ok=True)
    if not logging.getLogger().handlers:
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

def api_post(session: requests.Session, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/{path}"
    try:
        response = session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        log(f"POST {path} failed: {exc}")
        return None

def fetch_binance_klines(market: str, interval: str = "5m", limit: int = 50) -> List[Dict[str, float]]:
    symbol = f"{market}USDT"
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        # [OpenTime, Open, High, Low, Close, Vol, CloseTime, QuoteVol, Trades, TakerBuyBase, TakerBuyQuote, Ignore]
        return [
            {
                "close": float(item[4]),
                "volume": float(item[5]),
                "high": float(item[2]),
                "low": float(item[3])
            }
            for item in resp.json()
        ]
    except Exception as exc:
        log(f"Failed to fetch Binance klines: {exc}")
        return []

def calculate_vwap(klines: List[Dict[str, float]]) -> float:
    cumulative_pv = 0
    cumulative_v = 0
    for k in klines:
        typical_price = (k['high'] + k['low'] + k['close']) / 3
        cumulative_pv += typical_price * k['volume']
        cumulative_v += k['volume']
    
    if cumulative_v == 0: return 0
    return cumulative_pv / cumulative_v

def calculate_ema(prices: List[float], period: int) -> float:
    if len(prices) < period: return prices[-1]
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return ema

def main() -> None:
    ensure_environment()
    session = requests.Session()
    session.headers.update({"X-API-KEY": MAXXIT_API_KEY, "Content-Type": "application/json"})
    
    log(f"Starting VWAP Bot | Market: {MARKET} | Venue: {VENUE}")
    
    # 1. Get Club Details
    club = requests.get(f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/user-details", headers=session.headers).json()
    user_address = club.get("user_wallet")
    agent_address = club.get("ostium_agent_address")

    # 2. Fetch Data
    klines = fetch_binance_klines(MARKET)
    if not klines: return
    
    closes = [k['close'] for k in klines]
    current_vwap = calculate_vwap(klines)
    current_ema = calculate_ema(closes, EMA_PERIOD)
    current_price = closes[-1]
    
    log(f"Price: {current_price:.2f} | VWAP: {current_vwap:.2f} | EMA({EMA_PERIOD}): {current_ema:.2f}")

    # 3. Signal Logic
    signal = None
    if current_price > current_vwap and current_price > current_ema:
        signal = "long"
    elif current_price < current_vwap and current_price < current_ema:
        signal = "short"
        
    if not signal:
        log("No VWAP/EMA crossover signal; skipping.")
        return

    # 4. Positions & Balance
    balance_path = f"{VENUE.lower()}/balance" if VENUE == "AVANTIS" else "balance"
    balance_payload = {"userAddress": user_address} if VENUE == "AVANTIS" else {"address": user_address}
    balance = api_post(session, balance_path, balance_payload)
    if not balance: return
    usdc_balance = float(balance.get("usdcBalance", 0))

    pos_path = f"{VENUE.lower()}/positions" if VENUE == "AVANTIS" else "positions"
    pos_payload = {"userAddress": user_address, "agentAddress": agent_address} if VENUE == "AVANTIS" else {"address": user_address}
    positions_resp = api_post(session, pos_path, pos_payload)
    
    if positions_resp and positions_resp.get("positions"):
        for pos in positions_resp["positions"]:
            if (pos.get("market") == MARKET or pos.get("marketFull") == SYMBOL) and pos.get("side").lower() == signal:
                log(f"Already in a {signal} position.")
                return

    # 5. Execute
    collateral = min(usdc_balance * COLLATERAL_UTILIZATION, usdc_balance)
    if collateral < 1.0: return

    open_path = f"{VENUE.lower()}/open-position" if VENUE == "AVANTIS" else "open-position"
    open_payload = {
        "agentAddress": agent_address,
        "userAddress": user_address,
        "market": MARKET,
        "side": signal,
        "collateral": round(collateral, 2),
        "leverage": LEVERAGE,
        "takeProfitPercent": 0.03, # Target 3% 
        "stopLossPercent": 0.015    # 1.5% SL
    }
    
    open_resp = api_post(session, open_path, open_payload)
    if open_resp and open_resp.get("success"):
        log(f"Opened {signal} VWAP position on {VENUE}")

if __name__ == "__main__":
    main()
