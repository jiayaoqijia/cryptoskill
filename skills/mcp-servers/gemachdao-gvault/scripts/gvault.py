#!/usr/bin/env python3
"""GVault (GMACL, an Enzyme vault) NAV, share price and return. Standard library only.

Figures come from Enzyme's own accounting on the vault's comptroller, not from summing token
balances (the vault holds stETH as well as USDC; a balance sweep understates NAV badly).
Return is printed both cumulative and annualised: a multi-year cumulative figure alone
reads as an annual rate and overstates performance several-fold.

Usage:  gvault.py
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone

VAULT = "0x740cbfefb9ca9c1c99d95b711e959dd960f8bdb6"
INCEPTION = "2022-07-31"  # first code at block 15250173; the first shares minted at 1.0
LAUNCH_SHARE_PRICE = 1.0
# cloudflare-eth.com and rpc.ankr.com/eth return an EMPTY result for contracts that exist,
# which reads as "not deployed"; they are deliberately not used.
RPCS = ["https://ethereum-rpc.publicnode.com", "https://eth.drpc.org"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
SEL = {"symbol": "0x95d89b41", "decimals": "0x313ce567", "totalSupply": "0x18160ddd",
       "getAccessor": "0x5a53e348", "getTrackedAssets": "0xc4b97370",
       "getDenominationAsset": "0xe269c3d6", "calcGav": "0x56cff99f",
       "calcGrossShareValue": "0xda72503c"}


def rpc(method: str, params: list):
    last = None
    for url in RPCS:
        req = urllib.request.Request(url, data=json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
            headers={"Content-Type": "application/json", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = json.load(r)
        except Exception as exc:  # transport failure: try the next endpoint
            last = exc
            continue
        err = body.get("error")
        if err:
            if err.get("code") == 3 or "revert" in str(err.get("message", "")).lower():
                return None  # the contract answered: it reverted
            last = RuntimeError(f"{url}: {err.get('message')}")  # node failure: fail over
            continue
        return body.get("result")
    raise RuntimeError(f"{method} failed on every endpoint: {last}")


def call(to: str, data: str, block: str):
    r = rpc("eth_call", [{"to": to, "data": data}, block])
    return None if r in (None, "", "0x") else r


def uint(h):
    return None if not h or len(h) < 66 else int(h[2:66], 16)


def addr(h):
    return None if not h or len(h) < 66 else "0x" + h[26:66]


def string(h):
    if not h or len(h) < 130:
        return None
    b = bytes.fromhex(h[2:])
    off = int.from_bytes(b[:32], "big")
    n = int.from_bytes(b[off:off + 32], "big")
    return b[off + 32:off + 32 + n].decode("utf-8", "replace").strip()


def addr_array(h):
    if not h or len(h) < 130:
        return []
    b = h[2:]
    off = int(b[:64], 16) * 2
    n = int(b[off:off + 64], 16)
    return ["0x" + b[off + 64 + i * 64 + 24: off + 64 + (i + 1) * 64] for i in range(n)]


def main() -> int:
    now = datetime.now(timezone.utc)
    blk = hex(int(rpc("eth_blockNumber", []), 16) - 3)  # every read at ONE block
    comp = addr(call(VAULT, SEL["getAccessor"], blk))
    if not comp:
        raise RuntimeError("getAccessor() reverted — cannot reach the vault comptroller")
    denom = addr(call(comp, SEL["getDenominationAsset"], blk))
    dec = uint(call(denom, SEL["decimals"], blk)) if denom else 18
    gav, share = uint(call(comp, SEL["calcGav"], blk)), uint(call(comp, SEL["calcGrossShareValue"], blk))
    if gav is None or share is None:
        raise RuntimeError("calcGav/calcGrossShareValue reverted")
    shares = uint(call(VAULT, SEL["totalSupply"], blk))
    price = share / 10 ** dec
    start = datetime.strptime(INCEPTION, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    years = max((now - start).days / 365.25, 1e-9)
    ratio = price / LAUNCH_SHARE_PRICE
    held = sorted({s for s in (string(call(a, SEL["symbol"], blk))
                               for a in addr_array(call(VAULT, SEL["getTrackedAssets"], blk))) if s})
    rec = {
        "gemach_id": "gvault-gmacl", "source": "gemach", "feed": "gvault", "product": "gvault",
        "deployment": "gvault-gmacl", "chain_id": 1, "chain_name": "Ethereum",
        "vault_address": VAULT, "symbol": string(call(VAULT, SEL["symbol"], blk)) or "GMACL",
        "is_active": bool(shares), "nav_usd": gav / 10 ** dec, "share_price_usd": price,
        "all_time_return_pct": float(f"{(ratio - 1) * 100:.10g}"),
        "annualised_return_pct": float(f"{(ratio ** (1 / years) - 1) * 100:.10g}") if ratio > 0 else -100.0,
        "inception_date": INCEPTION, "age_years": round(years, 2),
        "observed_block": int(blk, 16),
        "upstream_updated_at": int(now.timestamp()), "upstream_updated_source": "chain_read_time",
        "ingestion_date": now.strftime("%Y-%m-%d"),
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%S.%f") + "+00:00",
    }
    if shares is not None:
        rec["shares_outstanding"] = shares / 1e18
    if denom:
        rec["denomination_symbol"] = string(call(denom, SEL["symbol"], blk))
    if held:
        rec["tracked_assets"] = held
    sys.stdout.write(json.dumps(rec, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
