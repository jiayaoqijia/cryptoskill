#!/usr/bin/env python3
"""Fetch Venus markets from official API and output normalized risk-friendly fields."""
import argparse
import json
import math
import urllib.parse
import urllib.request
from pathlib import Path

FILTER_CFG = Path(__file__).resolve().parent.parent / "references" / "pool-filter.json"

DEFAULT_BASE = "https://api.venus.io"


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "venus-skill/1.1"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def to_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def normalize_market(m: dict):
    supply = to_float(m.get("totalSupplyUnderlyingCents")) / 100.0
    borrows = to_float(m.get("totalBorrowCents")) / 100.0
    liquidity = to_float(m.get("liquidityCents")) / 100.0
    util = (borrows / supply) if supply > 0 else 0.0

    return {
        "symbol": m.get("symbol") or m.get("underlyingSymbol"),
        "marketAddress": m.get("address"),
        "poolComptroller": m.get("poolComptrollerAddress"),
        "isListed": m.get("isListed"),
        "isBorrowable": m.get("isBorrowable"),
        "canBeCollateral": m.get("canBeCollateral"),
        "supplyApy": to_float(m.get("supplyApy")),
        "borrowApy": to_float(m.get("borrowApy")),
        "totalSupplyUsd": round(supply, 2),
        "totalBorrowUsd": round(borrows, 2),
        "liquidityUsd": round(liquidity, 2),
        "utilization": round(util, 6),
        "collateralFactor": to_float(m.get("collateralFactorMantissa")),
        "liquidationThreshold": to_float(m.get("liquidationThresholdMantissa")),
        "borrowCap": to_float(m.get("borrowCapsMantissa")),
        "supplyCap": to_float(m.get("supplyCapsMantissa")),
        "priceInvalid": bool(m.get("isPriceInvalid")),
    }


def load_filter_config(path: str | None):
    cfg_path = Path(path) if path else FILTER_CFG
    if not cfg_path.exists():
        return {"defaultScope": "all", "coreComptrollersByChain": {}}
    try:
        return json.loads(cfg_path.read_text())
    except Exception:
        return {"defaultScope": "all", "coreComptrollersByChain": {}}


def filter_markets(markets: list[dict], chain_id: int, scope: str, cfg: dict):
    if scope == "all":
        return markets
    core = {x.lower() for x in (cfg.get("coreComptrollersByChain", {}).get(str(chain_id), []) or [])}
    if not core:
        return markets
    return [m for m in markets if (m.get("poolComptrollerAddress") or "").lower() in core]


def main():
    p = argparse.ArgumentParser(description="Fetch Venus market snapshot")
    p.add_argument("--base-url", default=DEFAULT_BASE)
    p.add_argument("--chain-id", type=int, default=56)
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--page", type=int, default=0)
    p.add_argument("--symbol", default=None, help="Optional market symbol filter")
    p.add_argument("--pool-scope", choices=["core", "all"], default=None, help="Default from config; core recommended")
    p.add_argument("--pool-filter-config", default=None, help="Path to pool filter config JSON")
    args = p.parse_args()

    cfg = load_filter_config(args.pool_filter_config)
    scope = args.pool_scope or cfg.get("defaultScope", "all")

    query = {
        "chainId": args.chain_id,
        "limit": args.limit,
        "page": args.page,
    }
    if args.symbol:
        query["symbol"] = args.symbol

    url = args.base_url.rstrip("/") + "/markets?" + urllib.parse.urlencode(query)
    data = fetch_json(url)
    raw_markets = data.get("result", [])
    filtered = filter_markets(raw_markets, args.chain_id, scope, cfg)
    rows = [normalize_market(x) for x in filtered]

    out = {
        "source": url,
        "scope": scope,
        "total": data.get("total", len(raw_markets)),
        "returned": len(rows),
        "markets": rows,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
