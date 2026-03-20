#!/usr/bin/env python3
"""Binance Spot Trader — LLM-enhanced autonomous trading bot."""
import os, sys, json, time, logging, hmac, hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from dotenv import load_dotenv
import httpx

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("trader")

API_KEY = os.environ["BINANCE_API_KEY"]
SECRET_KEY = os.environ["BINANCE_SECRET_KEY"]
LLM_API_KEY = os.environ["LLM_API_KEY"]
PAIRS = os.getenv("PAIRS", "BTCUSDT").split(",")
STRATEGY = os.getenv("STRATEGY", "momentum")
TRADE_SIZE_PCT = float(os.getenv("TRADE_SIZE_PCT", "5"))
MAX_POSITIONS = int(os.getenv("MAX_POSITIONS", "5"))
TP_PCT = float(os.getenv("TAKE_PROFIT_PCT", "5"))
SL_PCT = float(os.getenv("STOP_LOSS_PCT", "3"))
USE_LLM = os.getenv("USE_LLM", "true").lower() == "true"
DCA_AMOUNT = float(os.getenv("DCA_AMOUNT_USDT", "50"))

BASE = "https://api.binance.com"
TRADES_LOG = Path("trades.jsonl")

def sign(params: dict) -> dict:
    params["timestamp"] = int(time.time() * 1000)
    query = urlencode(params)
    params["signature"] = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return params

def api_get(path, params=None):
    with httpx.Client(timeout=15) as c:
        if params and "signature" in params:
            r = c.get(f"{BASE}{path}", params=params, headers={"X-MBX-APIKEY": API_KEY})
        else:
            r = c.get(f"{BASE}{path}", params=params or {})
        return r.json()

def api_post(path, params):
    with httpx.Client(timeout=15) as c:
        r = c.post(f"{BASE}{path}", params=sign(params), headers={"X-MBX-APIKEY": API_KEY})
        return r.json()

def get_klines(symbol, interval="1h", limit=50):
    data = api_get("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": limit})
    return [{"t": k[0], "o": float(k[1]), "h": float(k[2]), "l": float(k[3]), "c": float(k[4]), "v": float(k[5])} for k in data]

def ema(prices, period):
    k = 2 / (period + 1)
    e = prices[0]
    for p in prices[1:]:
        e = p * k + e * (1 - k)
    return e

def rsi(prices, period=14):
    deltas = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def bollinger(prices, period=20, std_mult=2):
    sma = sum(prices[-period:]) / period
    variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
    std = variance ** 0.5
    return sma - std_mult * std, sma, sma + std_mult * std

def llm_sentiment(symbol, klines):
    if not USE_LLM: return 0.5
    prices = [k["c"] for k in klines[-10:]]
    vol = [k["v"] for k in klines[-10:]]
    prompt = f"""Rate market sentiment for {symbol} (0.0=very bearish, 1.0=very bullish):
Last 10 closes: {[round(p,2) for p in prices]}
Volume trend: {'increasing' if vol[-1] > sum(vol[:-1])/len(vol[:-1]) else 'decreasing'}
Current RSI: {rsi(prices):.0f}
Reply ONLY a number."""

    with httpx.Client(timeout=30) as c:
        resp = c.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": LLM_API_KEY, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
            json={"model": "claude-3-5-haiku-20241022", "max_tokens": 20, "messages": [{"role": "user", "content": prompt}]})
        text = resp.json().get("content", [{}])[0].get("text", "0.5").strip()
        try: return float(text.split()[0].strip(".,"))
        except: return 0.5

def get_balance(asset="USDT"):
    info = api_get("/api/v3/account", sign({}))
    for b in info.get("balances", []):
        if b["asset"] == asset:
            return float(b["free"])
    return 0

def place_order(symbol, side, quantity):
    params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": f"{quantity:.6f}"}
    result = api_post("/api/v3/order", params)
    log.info(f"ORDER {side}: {symbol} qty={quantity:.6f} -> {result.get('status', 'UNKNOWN')}")
    with open(TRADES_LOG, "a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "symbol": symbol,
            "side": side, "qty": quantity, "result": result.get("status", "UNKNOWN"),
            "price": float(result.get("fills", [{}])[0].get("price", 0)) if result.get("fills") else 0
        }) + "\n")
    return result

def momentum_signal(klines):
    prices = [k["c"] for k in klines]
    ema20 = ema(prices, 20)
    current = prices[-1]
    avg_vol = sum(k["v"] for k in klines[-20:]) / 20
    vol_spike = klines[-1]["v"] > avg_vol * 1.5
    if current > ema20 and vol_spike: return "BUY"
    if current < ema20: return "SELL"
    return "HOLD"

def mean_reversion_signal(klines):
    prices = [k["c"] for k in klines]
    r = rsi(prices)
    lower, mid, upper = bollinger(prices)
    current = prices[-1]
    if r < 30 and current <= lower * 1.02: return "BUY"
    if r > 70 or current >= upper * 0.98: return "SELL"
    return "HOLD"

def run():
    log.info(f"Strategy: {STRATEGY} | Pairs: {PAIRS} | LLM: {USE_LLM}")
    balance = get_balance("USDT")
    log.info(f"USDT balance: ${balance:.2f}")

    if balance < 10:
        log.error("Insufficient USDT balance")
        return

    for symbol in PAIRS:
        try:
            klines = get_klines(symbol, "1h", 50)
            if not klines: continue

            if STRATEGY == "momentum":
                signal = momentum_signal(klines)
            elif STRATEGY == "mean_reversion":
                signal = mean_reversion_signal(klines)
            elif STRATEGY == "dca":
                signal = "BUY"  # DCA always buys
            else:
                signal = "HOLD"

            current_price = klines[-1]["c"]
            log.info(f"{symbol}: price=${current_price:.2f} signal={signal}")

            if signal == "BUY":
                if USE_LLM:
                    sentiment = llm_sentiment(symbol, klines)
                    log.info(f"  LLM sentiment: {sentiment:.2f}")
                    if sentiment < 0.35:
                        log.info(f"  LLM VETO — bearish sentiment")
                        continue

                if STRATEGY == "dca":
                    trade_usdt = DCA_AMOUNT
                else:
                    trade_usdt = balance * (TRADE_SIZE_PCT / 100)

                qty = trade_usdt / current_price
                if trade_usdt >= 10:  # Binance minimum
                    place_order(symbol, "BUY", qty)
                else:
                    log.info(f"  Skip: trade size ${trade_usdt:.2f} below $10 minimum")

            elif signal == "SELL":
                # Check if we hold this asset
                base_asset = symbol.replace("USDT", "")
                held = get_balance(base_asset)
                if held * current_price > 10:
                    place_order(symbol, "SELL", held)
                else:
                    log.info(f"  No {base_asset} position to sell")

        except Exception as e:
            log.error(f"{symbol} error: {e}")

    log.info("=== Cycle complete ===")

if __name__ == "__main__":
    run()
