#!/usr/bin/env python3
"""Aggressive Taker (Order Flow) bot for Maxxit Lazy Trading.
Uses Binance Taker Buy/Sell volume as a leading indicator for HFT scalping.
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
    parser = argparse.ArgumentParser(description="Aggressive Taker Strategy Bot")
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
TAKER_RATIO_THRESHOLD = float(os.environ.get("TAKER_RATIO_THRESHOLD", "0.60"))
MIN_COLLATERAL = 1.0

STATE_FILE = os.path.join(BASE_DIR, f"{VENUE.lower()}_{MARKET.lower()}_taker_state.json")
LOG_FILE = os.path.join(LOG_DIR, f"{VENUE.lower()}_{MARKET.lower()}_taker.log")

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

def load_state() -> Dict[str, Any]:
    if not os.path.isfile(STATE_FILE):
        return {"last_direction": None, "last_ratio": None}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (ValueError, IOError):
        return {"last_direction": None, "last_ratio": None}

def save_state(state: Dict[str, Any]) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def api_get(session: requests.Session, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    url = f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/{path}"
    try:
        response = session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        log(f"GET {path} failed: {exc}")
        return None

def api_post(session: requests.Session, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/{path}"
    try:
        response = session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        log(f"POST {path} failed: {exc}")
        return None

def fetch_binance_klines(market: str, interval: str = "5m", limit: int = 5) -> List[Dict[str, float]]:
    """Fetches klines and extracts Taker Volume data."""
    symbol = f"{market}USDT"
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # [OpenTime, Open, High, Low, Close, Vol, CloseTime, QuoteVol, Trades, TakerBuyBase, TakerBuyQuote, Ignore]
        return [
            {
                "close": float(item[4]),
                "volume": float(item[5]),
                "taker_buy_volume": float(item[9])
            }
            for item in data
        ]
    except Exception as exc:
        log(f"Failed to fetch Binance klines: {exc}")
        return []

def determine_signal(klines: List[Dict[str, float]]) -> Optional[str]:
    if not klines:
        return None
    
    # Calculate average taker ratio over the last few candles
    total_vol = sum(k['volume'] for k in klines)
    total_taker_buy = sum(k['taker_buy_volume'] for k in klines)
    
    if total_vol == 0:
        return None
        
    ratio = total_taker_buy / total_vol
    log(f"Taker Buy Ratio: {ratio:.4f}")
    
    if ratio > TAKER_RATIO_THRESHOLD:
        return "long"
    elif ratio < (1 - TAKER_RATIO_THRESHOLD):
        return "short"
    return None

def main() -> None:
    ensure_environment()
    session = requests.Session()
    session.headers.update({"X-API-KEY": MAXXIT_API_KEY, "Content-Type": "application/json"})
    
    state = load_state()
    log(f"Starting Aggressive Taker Bot | Market: {MARKET} | Venue: {VENUE}")

    # 1. Get Club Details
    club = api_get(session, "user-details")
    if not club:
        return
    user_address = club.get("user_wallet")
    agent_address = club.get("ostium_agent_address")
    
    # 2. Fetch Order Flow Data
    klines = fetch_binance_klines(MARKET)
    signal = determine_signal(klines)
    
    if signal is None:
        log("No strong order flow signal detected; skipping.")
        return

    # 3. Get Account Balance (Venue Specific)
    balance_path = f"{VENUE.lower()}/balance" if VENUE == "AVANTIS" else "balance"
    balance_payload = {"userAddress": user_address} if VENUE == "AVANTIS" else {"address": user_address}
    
    balance = api_post(session, balance_path, balance_payload)
    if not balance:
        return
    usdc_balance = float(balance.get("usdcBalance", 0))
    
    # 4. Check for Existing Position
    pos_path = f"{VENUE.lower()}/positions" if VENUE == "AVANTIS" else "positions"
    pos_payload = {"userAddress": user_address, "agentAddress": agent_address} if VENUE == "AVANTIS" else {"address": user_address}
    
    positions_resp = api_post(session, pos_path, pos_payload)
    existing_position = None
    if positions_resp and positions_resp.get("positions"):
        for pos in positions_resp["positions"]:
            if pos.get("market") == MARKET or pos.get("marketFull") == SYMBOL:
                existing_position = pos
                break

    # 5. Execute Logic
    if existing_position:
        existing_side = existing_position.get("side", "").lower()
        if existing_side == signal:
            log(f"Already in a {signal} position. No action needed.")
            return
        else:
            # Flip Position: Close old one
            log(f"Signal flipped to {signal}. Closing existing {existing_side} position.")
            close_path = f"{VENUE.lower()}/close-position" if VENUE == "AVANTIS" else "close-position"
            close_payload = {
                "agentAddress": agent_address,
                "userAddress": user_address,
                "market": MARKET,
                "actualTradeIndex": existing_position.get("tradeIndex")
            }
            api_post(session, close_path, close_payload)

    # Calculate collateral
    collateral = min(usdc_balance * COLLATERAL_UTILIZATION, usdc_balance)
    if collateral < MIN_COLLATERAL:
        log("Insufficient balance to open position.")
        return

    # Open Position
    open_path = f"{VENUE.lower()}/open-position" if VENUE == "AVANTIS" else "open-position"
    open_payload = {
        "agentAddress": agent_address,
        "userAddress": user_address,
        "market": MARKET,
        "side": signal,
        "collateral": round(collateral, 2),
        "leverage": LEVERAGE,
        "takeProfitPercent": 0.02, # 2% TP for scalping
        "stopLossPercent": 0.01    # 1% SL for scalping
    }
    
    open_resp = api_post(session, open_path, open_payload)
    if open_resp and open_resp.get("success"):
        log(f"Opened {signal} position on {VENUE} for {MARKET}")
    
    state["last_direction"] = signal
    save_state(state)

if __name__ == "__main__":
    main()
