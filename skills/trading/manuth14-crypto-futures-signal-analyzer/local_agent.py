#!/usr/bin/env python3
"""Read-only local Ollama explanation of deterministic futures signals."""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "llama3.1:8b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
ROOT = Path(__file__).resolve().parent
SUPPORTED = {"BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"}


def extract_symbol(prompt):
    match = re.search(r"\b(BTC|ETH|SOL|BNB)(?:[/\s-]?USDT)?\b", prompt.upper())
    if not match:
        raise ValueError("Specify a supported pair: BTCUSDT, ETHUSDT, SOLUSDT, or BNBUSDT")
    return match.group(1) + "USDT"


def analyze_market(symbol):
    if symbol not in SUPPORTED:
        raise ValueError("Unsupported symbol")
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "analyze.py"), "--symbol", symbol],
        cwd=ROOT, capture_output=True, text=True, timeout=45, check=False
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Analysis failed")
    return json.loads(completed.stdout)


def deterministic_report(data):
    """Authoritative explanation; no language-model calculations."""
    symbol = data["symbol"]
    signal = data["signal"]
    if signal not in {"BUY", "SELL", "HOLD"}:
        raise ValueError("Invalid engine signal")
    if "conditions" not in data:
        return (f"{symbol}: {signal}. " + data.get("reason", "Insufficient analysis data."))

    conditions = data["conditions"]
    buy = conditions["buy"]
    sell = conditions["sell"]
    expected = "BUY" if all(buy.values()) else ("SELL" if all(sell.values()) else "HOLD")
    if signal != expected:
        raise ValueError("Engine signal and condition flags disagree")

    def flag(value):
        if not isinstance(value, bool):
            raise ValueError("Non-boolean condition flag")
        return "PASS" if value else "FAIL"

    lines = [
        f"{symbol} | Engine signal: {signal}",
        f"1m candle closed (UTC): {data.get('as_of_utc')}",
        f"15m candle closed (UTC): {data.get('as_of_15m_utc')}",
        f"15m trend: {data['trend_15m']} | close: {data['close_15m']:.4f} | EMA21: {data['ema21_15m']:.4f}",
        f"1m EMA9: {data['ema9_1m']:.4f} | EMA21: {data['ema21_1m']:.4f}",
        f"1m RSI14: {data['rsi14_1m']:.4f}",
        f"1m volume: {data['volume_1m']:.4f} | MA10: {data['volume_ma10_1m']:.4f}",
        "BUY conditions (all required):",
    ]
    for key, value in buy.items():
        lines.append(f"  {flag(value)}: {key}")
    lines.append("SELL conditions (all required):")
    for key, value in sell.items():
        lines.append(f"  {flag(value)}: {key}")
    if signal == "HOLD":
        lines.append("Reason: Neither the complete BUY nor SELL rule set passed.")
    else:
        lines.append(f"Reason: All {signal} conditions passed.")
    lines.append("Educational indicator analysis only; not financial advice. No orders placed.")
    return "\n".join(lines)


def explain_with_ai(data):
    """Optional educational glossary, never a source of market facts or signals."""
    prompt = ("Give a short general educational explanation of what EMA, RSI, and "
              "volume moving average mean in technical analysis. Do NOT mention "
              "any trading pair, market prices, numbers, current signals, timestamps, "
              "trading recommendations, or BUY/SELL/HOLD. Plain language only.")
    payload = {"model": MODEL, "prompt": prompt, "stream": False,
               "options": {"temperature": 0}}
    request = urllib.request.Request(
        OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError("Cannot reach Ollama. Start Ollama and check installed model.") from exc
    explanation = result.get("response")
    if not isinstance(explanation, str) or not explanation.strip():
        raise RuntimeError("Ollama returned an empty explanation")
    # Suppress unexpected numerical claims, signal calls, and trading advice.
    if re.search(r"\d|\b(?:BUY|SELL|HOLD|LONG|SHORT|LEVERAGE)\b", explanation, re.I):
        return "EMA describes smoothed price trends; RSI measures recent price momentum; volume MA compares current trading activity with a recent average."
    return explanation.strip()

def main():
    print(f"Crypto Futures Local AI Agent ({MODEL}) — read-only")
    print("Ask: Analyze BTCUSDT | exit to quit")
    while True:
        try:
            prompt = input("\nYou: ").strip()
            if prompt.lower() in {"exit", "quit"}:
                break
            if not prompt:
                continue
            symbol = extract_symbol(prompt)
            data = analyze_market(symbol)
            print("\nVerified engine explanation:\n" + deterministic_report(data))
            try:
                print("\nOptional AI indicator glossary (not signal analysis):\n" + explain_with_ai(data))
            except RuntimeError as exc:
                print("\nAI glossary unavailable:", exc)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except (ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as exc:
            print("Error:", exc)


if __name__ == "__main__":
    main()
