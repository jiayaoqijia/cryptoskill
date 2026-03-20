"""
Real-time OKX ticker via WebSocket.

Subscribes to the `tickers` channel and prints live price updates.
Press Ctrl+C to stop.

Usage:
    pip install websocket-client
    python websocket-ticker.py BTC-USDT ETH-USDT

For private channels (orders, positions), set env vars:
    OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE
"""

import hashlib
import hmac
import json
import os
import sys
import time
from base64 import b64encode
from datetime import datetime, timezone

import websocket


WS_PUBLIC_URL = "wss://ws.okx.com:8443/ws/v5/public"
WS_PRIVATE_URL = "wss://ws.okx.com:8443/ws/v5/private"


def _ws_sign(secret: str, timestamp: str) -> str:
    pre_sign = timestamp + "GET" + "/users/self/verify"
    mac = hmac.new(secret.encode(), pre_sign.encode(), hashlib.sha256)
    return b64encode(mac.digest()).decode()


def run_public_ticker(inst_ids: list[str]):
    """Subscribe to public ticker channel for given instrument IDs."""

    def on_open(ws):
        args = [{"channel": "tickers", "instId": i} for i in inst_ids]
        ws.send(json.dumps({"op": "subscribe", "args": args}))
        print(f"Subscribed to tickers: {', '.join(inst_ids)}")
        print("Press Ctrl+C to stop.\n")

    def on_message(ws, message):
        msg = json.loads(message)

        # Handle subscription confirmation
        if msg.get("event") == "subscribe":
            return
        if msg.get("event") == "error":
            print(f"Error: {msg.get('msg')}")
            return

        data_list = msg.get("data", [])
        for ticker in data_list:
            inst_id = ticker.get("instId", "")
            last = float(ticker.get("last", 0))
            open24h = float(ticker.get("open24h", 0))
            change_pct = ((last - open24h) / open24h * 100) if open24h else 0
            bid = float(ticker.get("bidPx", 0))
            ask = float(ticker.get("askPx", 0))
            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(
                f"[{ts}] {inst_id:<14} last={last:>12,.4f}  "
                f"change={change_pct:>+7.2f}%  "
                f"bid={bid:>12,.4f}  ask={ask:>12,.4f}"
            )

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"Connection closed: {close_status_code} {close_msg}")

    ws = websocket.WebSocketApp(
        WS_PUBLIC_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(ping_interval=20, ping_timeout=10)


def run_private_orders():
    """Subscribe to private orders channel (requires API credentials)."""
    api_key = os.environ["OKX_API_KEY"]
    secret = os.environ["OKX_SECRET_KEY"]
    passphrase = os.environ["OKX_PASSPHRASE"]
    demo = os.environ.get("OKX_DEMO", "0") == "1"

    logged_in = False

    def on_open(ws):
        ts = str(int(time.time()))
        sign = _ws_sign(secret, ts)
        login_msg = {
            "op": "login",
            "args": [{
                "apiKey": api_key,
                "passphrase": passphrase,
                "timestamp": ts,
                "sign": sign,
            }],
        }
        if demo:
            login_msg["args"][0]["simulated"] = "1"
        ws.send(json.dumps(login_msg))

    def on_message(ws, message):
        nonlocal logged_in
        msg = json.loads(message)

        if msg.get("event") == "login":
            if msg.get("code") == "0":
                logged_in = True
                print("Logged in. Subscribing to orders channel...")
                ws.send(json.dumps({
                    "op": "subscribe",
                    "args": [{"channel": "orders", "instType": "ANY"}],
                }))
            else:
                print(f"Login failed: {msg.get('msg')}")
            return

        if msg.get("event") == "subscribe":
            print("Subscribed to orders channel. Waiting for order events...\n")
            return

        data_list = msg.get("data", [])
        for order in data_list:
            ts = datetime.now().strftime("%H:%M:%S")
            print(
                f"[{ts}] ORDER UPDATE  "
                f"instId={order.get('instId')}  "
                f"side={order.get('side')}  "
                f"ordType={order.get('ordType')}  "
                f"state={order.get('state')}  "
                f"px={order.get('px')}  "
                f"sz={order.get('sz')}  "
                f"fillSz={order.get('fillSz')}  "
                f"ordId={order.get('ordId')}"
            )

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"Connection closed.")

    ws = websocket.WebSocketApp(
        WS_PRIVATE_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(ping_interval=20, ping_timeout=10)


def main():
    args = sys.argv[1:]

    if "--private" in args:
        run_private_orders()
    else:
        inst_ids = [a for a in args if not a.startswith("--")] or ["BTC-USDT"]
        run_public_ticker(inst_ids)


if __name__ == "__main__":
    main()
