#!/usr/bin/env python3
"""
pump.fun Token Sniper Scorer
Scores a new token 0-100 for snipe safety based on on-chain signals.
"""

import requests
import time
import os
import json
from dataclasses import dataclass, field
from typing import Optional

HELIUS_KEY = os.environ.get("HELIUS_API_KEY", "")
RPC_ENDPOINTS = (
    [f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"] if HELIUS_KEY else []
) + ["https://api.mainnet-beta.solana.com"]

HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


@dataclass
class ScoreResult:
    ca: str
    total_score: int = 0          # 0 (danger) – 100 (safe)
    verdict: str = "UNKNOWN"      # SNIPE / CAUTION / AVOID
    breakdown: dict = field(default_factory=dict)
    signals: list = field(default_factory=list)
    token_meta: dict = field(default_factory=dict)


def rpc(method, params):
    for url in RPC_ENDPOINTS:
        try:
            r = requests.post(url, json={"jsonrpc": "2.0", "id": 1,
                                          "method": method, "params": params},
                              headers=HEADERS, timeout=8)
            if r.status_code == 200:
                data = r.json()
                if "error" not in data:
                    return data.get("result")
        except Exception:
            continue
    return None


# ── Data fetchers ─────────────────────────────────────────────────────────────

def fetch_pumpfun_meta(ca: str) -> dict:
    """Get token metadata from pump.fun frontend API"""
    urls = [
        f"https://client-api-2-74b1891ee9f9.herokuapp.com/coins/{ca}",
        f"https://frontend-api.pump.fun/coins/{ca}",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=6)
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return {}


def fetch_dex_data(ca: str) -> dict:
    """Get price/liquidity/volume from DexScreener"""
    try:
        r = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{ca}",
                         headers=HEADERS, timeout=6)
        if r.status_code == 200:
            data = r.json()
            if data.get("pairs"):
                return max(data["pairs"], key=lambda x: x.get("liquidity", {}).get("usd", 0))
    except Exception:
        pass
    return {}


def fetch_wallet_tx_history(wallet: str, limit: int = 20) -> list:
    """Get recent transaction signatures for a wallet via Helius"""
    if not HELIUS_KEY:
        return []
    try:
        url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions?api-key={HELIUS_KEY}&limit={limit}"
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def fetch_token_largest_accounts(ca: str) -> list:
    res = rpc("getTokenLargestAccounts", [ca])
    if res and "value" in res:
        return res["value"]
    return []


def get_sol_balance(address: str) -> float:
    res = rpc("getBalance", [address])
    if res and "value" in res:
        return res["value"] / 1e9
    return -1


# ── Scoring modules ───────────────────────────────────────────────────────────

def score_dev_wallet(meta: dict, helius_txs: list) -> tuple[int, list]:
    """
    Score: 0–30
    Check if dev wallet has a history of launching rugs.
    """
    score = 15  # neutral start
    signals = []

    creator = meta.get("creator", "")
    if not creator:
        return 5, ["⚠️ Dev wallet unknown"]

    sol_bal = get_sol_balance(creator)
    if sol_bal != -1:
        if sol_bal < 0.1:
            score -= 10
            signals.append(f"🚨 Dev wallet near empty ({sol_bal:.3f} SOL) — likely burner")
        elif sol_bal > 50:
            score += 10
            signals.append(f"✅ Dev has significant SOL ({sol_bal:.1f} SOL)")
        else:
            signals.append(f"ℹ️ Dev SOL balance: {sol_bal:.2f}")

    # Check if dev has many recent token launches (serial rugger pattern)
    if helius_txs:
        token_creates = [t for t in helius_txs
                         if t.get("type") in ("TOKEN_MINT", "CREATE_TOKEN", "INIT_MINT")]
        if len(token_creates) > 5:
            score -= 8
            signals.append(f"🚨 Dev launched {len(token_creates)}+ tokens recently — serial launcher")
        elif len(token_creates) > 2:
            score -= 3
            signals.append(f"⚠️ Dev launched {len(token_creates)} tokens recently")

    return max(0, min(30, score)), signals


def score_social_validity(meta: dict) -> tuple[int, list]:
    """
    Score: 0–20
    Check if token has real social links.
    """
    score = 0
    signals = []

    name = meta.get("name", "")
    symbol = meta.get("symbol", "")
    description = meta.get("description", "")
    twitter = meta.get("twitter", "")
    telegram = meta.get("telegram", "")
    website = meta.get("website", "")

    if name and symbol:
        score += 5
        signals.append(f"✅ Token: ${symbol} — {name}")

    if len(description) > 20:
        score += 5
        signals.append("✅ Has description")
    else:
        signals.append("⚠️ No description")

    if twitter:
        score += 5
        signals.append(f"✅ Twitter: {twitter}")
    else:
        signals.append("⚠️ No Twitter")

    if telegram:
        score += 3
        signals.append(f"✅ Telegram: {telegram}")

    if website:
        score += 2
        signals.append(f"✅ Website: {website}")

    return min(20, score), signals


def score_liquidity_and_market(dex: dict) -> tuple[int, list]:
    """
    Score: 0–25
    Check liquidity, buy/sell ratio, volume.
    """
    score = 0
    signals = []

    if not dex:
        return 0, ["⚠️ Not yet on DexScreener (very new or not launched)"]

    liq = dex.get("liquidity", {}).get("usd", 0)
    vol_h1 = dex.get("volume", {}).get("h1", 0)
    price_change_m5 = dex.get("priceChange", {}).get("m5", 0)
    txns = dex.get("txns", {})
    buys_m5 = txns.get("m5", {}).get("buys", 0)
    sells_m5 = txns.get("m5", {}).get("sells", 0)

    # Liquidity check
    if liq > 50000:
        score += 10
        signals.append(f"✅ Strong liquidity: ${liq:,.0f}")
    elif liq > 10000:
        score += 6
        signals.append(f"ℹ️ Liquidity: ${liq:,.0f}")
    elif liq > 1000:
        score += 2
        signals.append(f"⚠️ Low liquidity: ${liq:,.0f}")
    else:
        signals.append(f"🚨 Very low liquidity: ${liq:,.0f}")

    # Buy/sell ratio
    total_txns = buys_m5 + sells_m5
    if total_txns > 0:
        buy_ratio = buys_m5 / total_txns
        if buy_ratio > 0.65:
            score += 10
            signals.append(f"✅ Strong buy pressure: {buys_m5}B / {sells_m5}S (5m)")
        elif buy_ratio > 0.5:
            score += 5
            signals.append(f"ℹ️ Balanced txns: {buys_m5}B / {sells_m5}S (5m)")
        else:
            signals.append(f"🚨 Sell pressure: {buys_m5}B / {sells_m5}S (5m)")

    # Volume
    if vol_h1 > 10000:
        score += 5
        signals.append(f"✅ 1h volume: ${vol_h1:,.0f}")
    elif vol_h1 > 1000:
        score += 2
        signals.append(f"ℹ️ 1h volume: ${vol_h1:,.0f}")

    return min(25, score), signals


def score_holder_concentration(ca: str, meta: dict) -> tuple[int, list]:
    """
    Score: 0–25
    Check if top holders are clustered (coordinated dump risk).
    """
    score = 12  # neutral
    signals = []

    holders = fetch_token_largest_accounts(ca)
    if not holders:
        return 5, ["⚠️ Could not fetch holder data"]

    total_supply_res = rpc("getTokenSupply", [ca])
    if not total_supply_res or "value" not in total_supply_res:
        return 5, ["⚠️ Could not fetch supply"]

    total_supply = float(total_supply_res["value"]["uiAmountString"])
    if total_supply == 0:
        return 5, ["⚠️ Supply is 0"]

    creator = meta.get("creator", "")
    top5_pct = 0
    dev_holds_pct = 0

    for i, h in enumerate(holders[:5]):
        pct = float(h["uiAmountString"]) / total_supply * 100
        top5_pct += pct
        if h["address"] == creator:
            dev_holds_pct = pct

    if dev_holds_pct > 10:
        score -= 10
        signals.append(f"🚨 Dev holds {dev_holds_pct:.1f}% of supply")
    elif dev_holds_pct > 5:
        score -= 5
        signals.append(f"⚠️ Dev holds {dev_holds_pct:.1f}%")
    elif dev_holds_pct == 0:
        score += 5
        signals.append("✅ Dev wallet not in top holders")

    if top5_pct > 60:
        score -= 8
        signals.append(f"🚨 Top 5 holders control {top5_pct:.1f}%")
    elif top5_pct > 40:
        score -= 3
        signals.append(f"⚠️ Top 5 hold {top5_pct:.1f}%")
    else:
        score += 5
        signals.append(f"✅ Healthy distribution — top 5 hold {top5_pct:.1f}%")

    return max(0, min(25, score)), signals


# ── Main scorer ───────────────────────────────────────────────────────────────

def score_token(ca: str) -> ScoreResult:
    result = ScoreResult(ca=ca)

    # Fetch all data
    meta = fetch_pumpfun_meta(ca)
    dex = fetch_dex_data(ca)
    creator = meta.get("creator", "")
    helius_txs = fetch_wallet_tx_history(creator) if creator else []

    # Store token metadata
    result.token_meta = {
        "name": meta.get("name", "Unknown"),
        "symbol": meta.get("symbol", "???"),
        "creator": creator,
        "description": meta.get("description", ""),
        "twitter": meta.get("twitter", ""),
        "telegram": meta.get("telegram", ""),
        "website": meta.get("website", ""),
        "price_usd": dex.get("priceUsd", "0") if dex else "0",
        "liquidity_usd": dex.get("liquidity", {}).get("usd", 0) if dex else 0,
        "market_cap": dex.get("marketCap", 0) if dex else 0,
    }

    # Run scoring modules
    s1, sig1 = score_dev_wallet(meta, helius_txs)
    s2, sig2 = score_social_validity(meta)
    s3, sig3 = score_liquidity_and_market(dex)
    s4, sig4 = score_holder_concentration(ca, meta)

    result.breakdown = {
        "dev_wallet":    {"score": s1, "max": 30},
        "social":        {"score": s2, "max": 20},
        "liquidity":     {"score": s3, "max": 25},
        "concentration": {"score": s4, "max": 25},
    }
    result.total_score = s1 + s2 + s3 + s4
    result.signals = sig1 + sig2 + sig3 + sig4

    # Verdict
    if result.total_score >= 70:
        result.verdict = "SNIPE"
    elif result.total_score >= 45:
        result.verdict = "CAUTION"
    else:
        result.verdict = "AVOID"

    return result


if __name__ == "__main__":
    import sys
    ca = sys.argv[1] if len(sys.argv) > 1 else input("Token CA: ").strip()
    r = score_token(ca)
    print(f"\n{'='*50}")
    print(f"  {r.token_meta.get('symbol','?')} — Snipe Score: {r.total_score}/100  [{r.verdict}]")
    print(f"{'='*50}")
    for s in r.signals:
        print(f"  {s}")
    print(f"\nBreakdown:")
    for k, v in r.breakdown.items():
        bar = "█" * v["score"] + "░" * (v["max"] - v["score"])
        print(f"  {k:15} {bar} {v['score']}/{v['max']}")
