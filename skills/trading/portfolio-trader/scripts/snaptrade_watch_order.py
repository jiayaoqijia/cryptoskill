#!/usr/bin/env python3
import argparse
import time
from datetime import datetime, timezone

from snaptrade_common import load_config, get_client


def parse_args():
    p = argparse.ArgumentParser(description="Watch a SnapTrade order by ID for fill status.")
    p.add_argument("--account-id", required=True, help="SnapTrade account id")
    p.add_argument("--order-id", required=True, help="brokerage_order_id to watch")
    p.add_argument("--watch-interval", type=int, default=10, help="Seconds between checks (default 10)")
    p.add_argument("--watch-seconds", type=int, default=120, help="Max seconds to watch (default 120)")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config()
    client = get_client(cfg)
    user_id = cfg["user_id"]
    user_secret = cfg["user_secret"]

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
                if (o.get("brokerage_order_id") if isinstance(o, dict) else None) == args.order_id:
                    match = o
                    break
            if match:
                status = match.get("status") if isinstance(match, dict) else None
                if status != last:
                    last = status
                    print({"status": "update", "order_id": args.order_id, "order_status": status, "time": datetime.now(timezone.utc).isoformat()})
                if status in ("EXECUTED", "FILLED"):
                    return
        except Exception:
            pass
        time.sleep(args.watch_interval)

    print({"status": "timeout", "order_id": args.order_id})


if __name__ == "__main__":
    main()
