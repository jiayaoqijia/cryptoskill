#!/usr/bin/env python3
"""Wallet exposure checker.

Mode A (API): query a compatible endpoint that returns weighted collateral/debt.
Mode B (manual): compute health from provided numbers.
"""
import argparse
import json
import urllib.request


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "venus-skill/1.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def classify(health: float) -> str:
    if health < 1.15:
        return "HIGH"
    if health < 1.35:
        return "MEDIUM"
    return "LOW"


def main():
    p = argparse.ArgumentParser(description="Check wallet exposure")
    p.add_argument("--wallet", help="Wallet address")
    p.add_argument("--api-url", help="Optional full endpoint URL returning exposure JSON")
    p.add_argument("--weighted-collateral", type=float, help="Manual weighted collateral USD")
    p.add_argument("--debt", type=float, help="Manual debt USD")
    args = p.parse_args()

    if args.api_url:
        data = fetch_json(args.api_url)
        wc = float(data.get("weighted_collateral_usd", 0.0))
        debt = float(data.get("debt_usd", 0.0))
        health = (wc / debt) if debt > 0 else float("inf")
        out = {
            "wallet": args.wallet,
            "source": args.api_url,
            "weightedCollateralUsd": wc,
            "debtUsd": debt,
            "health": health,
            "risk": classify(health) if health != float("inf") else "LOW",
        }
        print(json.dumps(out, indent=2))
        return

    if args.weighted_collateral is None or args.debt is None:
        raise SystemExit("Provide either --api-url or both --weighted-collateral and --debt")

    health = (args.weighted_collateral / args.debt) if args.debt > 0 else float("inf")
    out = {
        "wallet": args.wallet,
        "source": "manual",
        "weightedCollateralUsd": args.weighted_collateral,
        "debtUsd": args.debt,
        "health": health,
        "risk": classify(health) if health != float("inf") else "LOW",
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
