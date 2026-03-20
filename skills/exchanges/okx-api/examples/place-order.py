"""
Place a limit buy order on OKX.

Usage:
    OKX_DEMO=1 python place-order.py
    OKX_DEMO=1 python place-order.py ETH-USDT buy limit 2000 0.01

Arguments (all optional, defaults shown):
    instId   — instrument ID (default: BTC-USDT)
    side     — buy or sell (default: buy)
    ordType  — limit, market, post_only, fok, ioc (default: limit)
    px       — price in quote currency (default: 40000)
    sz       — size in base currency (default: 0.001)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from okx_auth import make_request


def place_order(inst_id: str, side: str, ord_type: str, px: str, sz: str):
    body = {
        "instId": inst_id,
        "tdMode": "cash",   # cash = spot; use "cross" or "isolated" for margin/derivatives
        "side": side,
        "ordType": ord_type,
        "sz": sz,
    }

    if ord_type != "market":
        body["px"] = px

    print(f"Placing {side} {ord_type} order: {sz} {inst_id} @ {px}")
    data = make_request("POST", "/api/v5/trade/order", body=body)

    for result in data:
        ord_id = result.get("ordId", "")
        cl_ord_id = result.get("clOrdId", "")
        s_code = result.get("sCode", "")
        s_msg = result.get("sMsg", "")

        if s_code == "0":
            print(f"Order placed successfully!")
            print(f"  Order ID:    {ord_id}")
            if cl_ord_id:
                print(f"  Client ID:   {cl_ord_id}")
        else:
            print(f"Order failed: [{s_code}] {s_msg}")


def cancel_order(inst_id: str, ord_id: str):
    data = make_request("POST", "/api/v5/trade/cancel-order", body={
        "instId": inst_id,
        "ordId": ord_id,
    })
    for result in data:
        s_code = result.get("sCode", "")
        s_msg = result.get("sMsg", "")
        if s_code == "0":
            print(f"Order {ord_id} cancelled successfully.")
        else:
            print(f"Cancel failed: [{s_code}] {s_msg}")


def main():
    args = sys.argv[1:]
    inst_id = args[0] if len(args) > 0 else "BTC-USDT"
    side    = args[1] if len(args) > 1 else "buy"
    ord_type = args[2] if len(args) > 2 else "limit"
    px      = args[3] if len(args) > 3 else "40000"
    sz      = args[4] if len(args) > 4 else "0.001"

    demo = os.environ.get("OKX_DEMO", "0") == "1"
    if not demo:
        confirm = input("WARNING: OKX_DEMO is not set. This will place a REAL order. Continue? [y/N] ")
        if confirm.lower() != "y":
            print("Aborted.")
            return

    place_order(inst_id, side, ord_type, px, sz)


if __name__ == "__main__":
    main()
