#!/usr/bin/env python3
import argparse
import time
from datetime import datetime, timezone

from snaptrade_common import load_config, get_client


def parse_args():
    p = argparse.ArgumentParser(description="Place a SnapTrade order and optionally monitor for fill.")
    p.add_argument("action", choices=["buy", "sell"], help="buy or sell")
    p.add_argument("symbol", help="Ticker symbol, e.g., AAPL or VXC.TO")
    p.add_argument("units", type=float, help="Number of units (shares). Use whole numbers when required by broker.")
    p.add_argument("--account-id", required=True, help="SnapTrade account id")
    p.add_argument("--order-type", default="market", choices=["market", "limit"], help="market (default) or limit")
    p.add_argument("--limit-price", type=float, help="Limit price (required if order-type=limit)")
    p.add_argument("--tif", default="Day", choices=["Day", "GTC", "IOC", "FOK"], help="Time in force")
    p.add_argument("--watch", action="store_true", help="Monitor for fill after placing")
    p.add_argument("--watch-interval", type=int, default=10, help="Seconds between checks (default 10)")
    p.add_argument("--watch-seconds", type=int, default=120, help="Max seconds to watch (default 120)")
    return p.parse_args()


def normalize_order_type(o):
    return "Market" if o.lower() == "market" else "Limit"


def main():
    args = parse_args()
    if args.order_type == "limit" and args.limit_price is None:
        raise SystemExit("--limit-price is required for limit orders")

    cfg = load_config()
    client = get_client(cfg)
    user_id = cfg["user_id"]
    user_secret = cfg["user_secret"]

    resp = client.trading.place_force_order(
        user_id=user_id,
        user_secret=user_secret,
        account_id=args.account_id,
        action=args.action.upper(),
        order_type=normalize_order_type(args.order_type),
        time_in_force=args.tif,
        symbol=args.symbol,
        units=args.units,
        price=args.limit_price if args.order_type == "limit" else None,
    )
    body = getattr(resp, "body", resp)
    order_id = body.get("brokerage_order_id") if isinstance(body, dict) else None
    print({"status": "placed", "order": body})

    if not args.watch or not order_id:
        return

    deadline = time.time() + args.watch_seconds
    last = None
    while time.time() < deadline:
        try:
            oresp = client.account_information.get_user_account_orders(
                user_id=user_id,
                user_secret=user_secret,
                account_id=args.account_id,
            )
            orders = getattr(oresp, "body", oresp) or []
            match = None
            for o in orders:
                if (o.get("brokerage_order_id") if isinstance(o, dict) else None) == order_id:
                    match = o
                    break
            if match:
                status = match.get("status") if isinstance(match, dict) else None
                if status != last:
                    last = status
                    print({"status": "update", "order_id": order_id, "order_status": status, "time": datetime.now(timezone.utc).isoformat()})
                if status in ("EXECUTED", "FILLED"):
                    return
        except Exception:
            pass
        time.sleep(args.watch_interval)

    print({"status": "timeout", "order_id": order_id})


if __name__ == "__main__":
    main()
