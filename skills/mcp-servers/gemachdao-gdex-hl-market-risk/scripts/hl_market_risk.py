#!/usr/bin/env python3
"""HyperLiquid core-perpetual risk snapshot via GDEX. Standard library only.

Prints one JSON object per market (NDJSON) to stdout. Every number comes from the API
response; nothing is estimated. Exit code is non-zero on any upstream or shape error, so a
caller can never mistake a failed read for an empty market.

Scope: the core HyperLiquid DEX only (the `/v1/hl/meta_and_asset_ctxs` universe). Builder-
deployed markets (equities, FX, commodities, indices) are deliberately excluded.

Usage:
    hl_market_risk.py                     # all core markets
    hl_market_risk.py --symbol BTC ETH    # just these
    hl_market_risk.py --active-only       # drop delisted markets
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone

API = "https://trade-api.gemach.io/v1/hl/meta_and_asset_ctxs"
# The GDEX API refuses non-browser clients (HTTP 403); these headers are load-bearing.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Origin": "https://gdex.pro",
    "Accept": "application/json",
}
FEED = "hl_markets"
CHAIN_ID = 999  # HyperEVM mainnet, used purely as a registry key


class ShapeError(RuntimeError):
    pass


def fetch() -> dict:
    req = urllib.request.Request(API, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _num(v) -> float:
    if v is None or isinstance(v, bool):
        raise ValueError(f"expected a number, got {v!r}")
    return float(str(v).strip())


def _pct(fraction: float) -> float:
    """Fraction -> percent, trimming the float noise that x100 introduces (e.g. ...0000004).
    12 significant digits is far beyond the precision HyperLiquid publishes."""
    return float(f"{fraction * 100.0:.12g}")


def _opt(v) -> float | None:
    return None if v is None or v == "" else _num(v)


def pairs(payload: dict):
    if not isinstance(payload, dict) or payload.get("isSuccess") is False:
        raise ShapeError(f"upstream reported failure: {str(payload)[:200]}")
    data = payload.get("data")
    if not isinstance(data, list) or len(data) != 2:
        raise ShapeError("expected data = [meta, contexts]")
    universe, ctxs = (data[0] or {}).get("universe"), data[1]
    if not isinstance(universe, list) or not isinstance(ctxs, list):
        raise ShapeError("universe or contexts is not a list")
    if len(universe) != len(ctxs):
        # Pairing is by index; misaligned arrays would attach one market's prices to another.
        raise ShapeError(f"universe has {len(universe)} entries but contexts has {len(ctxs)}")
    return zip(universe, ctxs)


def market(meta: dict, ctx: dict, now: datetime) -> dict:
    name = str(meta["name"]).strip()
    delisted = bool(meta.get("isDelisted", False))  # upstream only sends it when true
    mark, oracle, prev = _num(ctx["markPx"]), _num(ctx["oraclePx"]), _num(ctx["prevDayPx"])
    oi = _num(ctx["openInterest"])
    rec = {
        "gemach_id": f"hl-{name}",
        "source": "gemach", "feed": FEED, "product": "gdex", "deployment": "hyperliquid-core",
        "chain_id": CHAIN_ID, "chain_name": "HyperLiquid", "symbol": name,
        "is_active": not delisted, "is_delisted": delisted,
        "only_isolated": bool(meta.get("onlyIsolated", False)),
        "max_leverage": int(meta["maxLeverage"]), "sz_decimals": int(meta["szDecimals"]),
        "mark_px_usd": mark, "oracle_px_usd": oracle, "prev_day_px_usd": prev,
        # HL publishes funding and premium as decimal fractions; x100 gives percent.
        "funding_hourly_pct": _pct(_num(ctx["funding"])),
        "open_interest_base": oi, "open_interest_usd": float(f"{oi * mark:.12g}"),
        "volume_24h_usd": _num(ctx["dayNtlVlm"]), "volume_24h_base": _num(ctx["dayBaseVlm"]),
        "change_24h_pct": _pct(mark / prev - 1.0) if prev > 0 else 0.0,
        "upstream_updated_at": int(now.timestamp()), "upstream_updated_source": "api_snapshot_time",
        "ingestion_date": now.strftime("%Y-%m-%d"),
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "+00:00",
    }
    # Delisted markets have no book: upstream nulls these two. Active ones must have them.
    mid, prem = _opt(ctx.get("midPx")), _opt(ctx.get("premium"))
    if mid is not None:
        rec["mid_px_usd"] = mid
    if prem is not None:
        rec["premium_pct"] = _pct(prem)
    if not delisted and (mid is None or prem is None):
        raise ShapeError(f"active market {name} has no mid/premium; upstream shape changed")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--symbol", nargs="*", help="only these symbols (case-sensitive, e.g. BTC kPEPE)")
    ap.add_argument("--active-only", action="store_true", help="drop delisted markets")
    a = ap.parse_args(argv)
    now = datetime.now(timezone.utc)
    rows = [market(m, c, now) for m, c in pairs(fetch())]
    if a.symbol:
        want = set(a.symbol)
        rows = [r for r in rows if r["symbol"] in want]
    if a.active_only:
        rows = [r for r in rows if r["is_active"]]
    for r in rows:
        sys.stdout.write(json.dumps(r, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
