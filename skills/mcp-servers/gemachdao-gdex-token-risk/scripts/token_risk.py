#!/usr/bin/env python3
"""GDEX token market + security screen, per chain. Standard library only.

Prints one JSON object per token (NDJSON). Security fields are copied from GDEX's own
back-end assessment and are OMITTED when GDEX has no value — never defaulted to false.
Absent is unknown, and unknown must never be read as safe.

Usage:
    token_risk.py                          # trending tokens on every supported chain
    token_risk.py --chain-id 1 8453        # just these chains (GDEX chain ids)
    token_risk.py --list-chains
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://trade-api.gemach.io/v1/trending/list"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Origin": "https://gdex.pro",
    "Accept": "application/json",
}
# GDEX-internal chain ids. Solana and Sui are NOT the ids those ecosystems use elsewhere;
# a wrong id silently returns an empty list, so use exactly these.
CHAINS = {1: "Ethereum", 10: "Optimism", 56: "BNB Smart Chain", 146: "Sonic", 252: "Fraxtal",
          6900: "Nibiru", 8453: "Base", 42161: "Arbitrum One", 80094: "Berachain",
          4663: "Robinhood Chain", 622112261: "Solana", 1313131213: "Sui"}
CASE_SENSITIVE = {622112261, 1313131213}  # base58 mints / Move type tags: never lowercase
ENVELOPE = "trendingTokens"


class ShapeError(RuntimeError):
    pass


def fetch(chain_id: int) -> list[dict]:
    url = API + "?" + urllib.parse.urlencode({"chainId": chain_id})
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as r:
        body = json.load(r)
    if body.get("isSuccess") is False:
        raise ShapeError(f"chain {chain_id}: upstream failure {body.get('error')!r}")
    rows = body.get(ENVELOPE)
    if not isinstance(rows, list):
        # A renamed envelope must fail loudly, not look like a quiet market.
        raise ShapeError(f"chain {chain_id}: no {ENVELOPE!r} list (keys {sorted(body)[:8]})")
    return rows


def _num(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(",", "").strip()
    return float(s) if s else None


def _flag(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    return str(v).strip().lower() in {"true", "1", "yes"}


def address(chain_id: int, addr: str) -> str:
    addr = addr.strip()
    return addr if chain_id in CASE_SENSITIVE else addr.lower()


def token(e: dict, now: datetime) -> dict:
    cid = int(e["chainId"])
    addr = address(cid, str(e["address"]))
    sec = e.get("securities") if isinstance(e.get("securities"), dict) else {}
    chg = e.get("priceChanges") if isinstance(e.get("priceChanges"), dict) else {}
    vol = e.get("volumes") if isinstance(e.get("volumes"), dict) else {}
    liq = _num(e.get("liquidityUsd"))
    clock, src = None, "fetch_time_fallback"
    for k in ("lastReserveUpdatedTimestamp", "lastCalculateVolumesAndPriceChanges",
              "lastTotalSupplyUpdatedTimestamp", "lastVolumeUpdatedTimestamp"):
        v = e.get(k)
        if isinstance(v, (int, float)) and v > 0:
            clock, src = int(v), k
            break
    rec = {
        "gemach_id": f"{cid}-{addr.replace('::', '.')}",
        "source": "gemach", "feed": "token_markets",
        "chain_id": cid, "chain_name": CHAINS.get(cid, f"chain-{cid}"),
        "token_address": addr, "symbol": str(e.get("symbol") or "").strip(),
        "is_active": bool(liq and liq > 0),
        "upstream_updated_at": clock if clock is not None else int(now.timestamp()),
        "upstream_updated_source": src,
        "ingestion_date": now.strftime("%Y-%m-%d"),
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "+00:00",
    }
    optional = {
        "token_name": (str(e["name"]).strip() if e.get("name") else None),
        "price_usd": _num(e.get("priceUsd")), "market_cap_usd": _num(e.get("marketCap")),
        "liquidity_usd": liq, "volume_24h_usd": _num(vol.get("h24")),
        "change_1h_pct": _num(chg.get("h1")), "change_24h_pct": _num(chg.get("h24")),
        # --- GDEX security assessment: percent fields are 0-100 upstream ---
        "is_honeypot": _flag(sec.get("isHoneyPot")),
        "buy_tax_pct": _num(sec.get("buyTax")), "sell_tax_pct": _num(sec.get("sellTax")),
        "lp_lock_pct": _num(sec.get("lpLockPercentage")),
        "top_holders_pct": _num(sec.get("topHoldersPercentage")),
        "is_contract_verified": _flag(sec.get("contractVerified")),
        "can_mint": _flag(sec.get("mintAbility")), "can_freeze": _flag(sec.get("freezeAbility")),
    }
    rec.update({k: v for k, v in optional.items() if v is not None})
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--chain-id", nargs="*", type=int, help="GDEX chain ids (default: all)")
    ap.add_argument("--list-chains", action="store_true")
    a = ap.parse_args(argv)
    if a.list_chains:
        for cid, name in CHAINS.items():
            print(f"{cid}\t{name}")
        return 0
    now = datetime.now(timezone.utc)
    seen = {}
    for cid in (a.chain_id or list(CHAINS)):
        for e in fetch(cid):
            r = token(e, now)
            seen[r["gemach_id"]] = r
    for gid in sorted(seen):
        sys.stdout.write(json.dumps(seen[gid], separators=(",", ":"), ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
