#!/usr/bin/env python3
"""Mean Reversion (RSI + Bollinger Bands) bot for Maxxit Lazy Trading.
Identifies oversold/overbought conditions in ranging markets for quick scalping.
"""
import json
import logging
import math
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import argparse

# Configuration
BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
MAXXIT_API_URL = os.environ.get("MAXXIT_API_URL")
MAXXIT_API_KEY = os.environ.get("MAXXIT_API_KEY")

def parse_args():
    parser = argparse.ArgumentParser(description="Mean Reversion Strategy Bot")
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
RSI_PERIOD = 7
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
BB_PERIOD = 20
BB_STD = 2.0

STATE_FILE = os.path.join(BASE_DIR, f"{VENUE.lower()}_{MARKET.lower()}_mean_state.json")
LOG_FILE = os.path.join(LOG_DIR, f"{VENUE.lower()}_{MARKET.lower()}_mean.log")

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

def fetch_binance_klines(market: str, interval: str = "5m", limit: int = 50) -> List[float]:
    symbol = f"{market}USDT"
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return [float(item[4]) for item in resp.json()] # Just close prices
    except Exception as exc:
        log(f"Failed to fetch Binance klines: {exc}")
        return []

def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
    if len(prices) < period + 1:
        return None
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gain = [d if d > 0 else 0 for d in deltas]
    loss = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gain[:period]) / period
    avg_loss = sum(loss[:period]) / period
    
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gain[i]) / period
        avg_loss = (avg_loss * (period - 1) + loss[i]) / period
        
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Dict[str, float]:
    if len(prices) < period:
        return {}
    sma = sum(prices[-period:]) / period
    variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
    stdev = math.sqrt(variance)
    return {
        "upper": sma + (std_dev * stdev),
        "lower": sma - (std_dev * stdev),
        "middle": sma
    }

def main() -> None:
    ensure_environment()
    session = requests.Session()
    session.headers.update({"X-API-KEY": MAXXIT_API_KEY, "Content-Type": "application/json"})
    
    log(f"Starting Mean Reversion Bot | Market: {MARKET} | Venue: {VENUE}")
    
    # 1. Get Club Details
    club = requests.get(f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/user-details", headers=session.headers).json()
    user_address = club.get("user_wallet")
    agent_address = club.get("ostium_agent_address")

    # 2. Fetch Price Data & Calculate Indicators
    prices = fetch_binance_klines(MARKET)
    if not prices: return
    
    rsi = calculate_rsi(prices, RSI_PERIOD)
    bb = calculate_bollinger_bands(prices, BB_PERIOD, BB_STD)
    current_price = prices[-1]
    
    if rsi is None or not bb: 
        log("Insufficient data for indicators")
        return
        
    log(f"Price: {current_price:.2f} | RSI: {rsi:.2f} | BB: L={bb['lower']:.2f}, U={bb['upper']:.2f}")

    # 3. Determine Signal
    signal = None
    if current_price < bb['lower'] and rsi < RSI_OVERSOLD:
        signal = "long"
    elif current_price > bb['upper'] and rsi > RSI_OVERBOUGHT:
        signal = "short"
        
    if not signal:
        log("No mean reversion signal; skipping.")
        return

    # 4. Check Balance & Positions
    balance_path = f"{VENUE.lower()}/balance" if VENUE == "AVANTIS" else "balance"
    balance_payload = {"userAddress": user_address} if VENUE == "AVANTIS" else {"address": user_address}
    balance = api_post(session, balance_path, balance_payload)
    if not balance: return
    usdc_balance = float(balance.get("usdcBalance", 0))

    pos_path = f"{VENUE.lower()}/positions" if VENUE == "AVANTIS" else "positions"
    pos_payload = {"userAddress": user_address, "agentAddress": agent_address} if VENUE == "AVANTIS" else {"address": user_address}
    positions_resp = api_post(session, pos_path, pos_payload)
    
    # Simple logic: If in a position, don't open another of the same side.
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
        "takeProfitPercent": 0.015, # Tight TP for mean reversion
        "stopLossPercent": 0.01      # Tight SL
    }
    
    open_resp = api_post(session, open_path, open_payload)
    if open_resp and open_resp.get("success"):
        log(f"Opened {signal} mean-reversion position on {VENUE}")

if __name__ == "__main__":
    main()
