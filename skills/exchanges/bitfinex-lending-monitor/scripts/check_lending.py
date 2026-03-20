#!/usr/bin/env python3
"""Bitfinex funding monitor.

Fetches funding wallet, active credits, and recent funding ledger entries,
then prints compact收益 summary.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API_BASE = "https://api.bitfinex.com"


def bfx_post(path: str, body: dict, api_key: str, api_secret: str):
    nonce = str(int(time.time() * 1000 * 1000))
    raw_body = json.dumps(body, separators=(",", ":"))
    signature_payload = f"/api{path}{nonce}{raw_body}".encode("utf-8")
    signature = hmac.new(
        api_secret.encode("utf-8"), signature_payload, hashlib.sha384
    ).hexdigest()

    req = urllib.request.Request(
        API_BASE + path,
        method="POST",
        data=raw_body.encode("utf-8"),
        headers={
            "content-type": "application/json",
            "bfx-apikey": api_key,
            "bfx-nonce": nonce,
            "bfx-signature": signature,
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_args():
    p = argparse.ArgumentParser(description="Check Bitfinex funding收益")
    p.add_argument("--currency", default="USD", help="Funding currency, e.g. USD, USDT (USDT auto-mapped to UST)")
    p.add_argument("--days", type=int, default=7, help="Lookback days for ledger summary")
    p.add_argument("--json", action="store_true", help="Print raw summary as JSON")
    return p.parse_args()


def safe_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def normalize_currency(raw: str) -> str:
    c = raw.upper()
    # Bitfinex commonly represents Tether USD as UST in wallet/funding APIs.
    if c == "USDT":
        return "UST"
    return c


def main():
    args = parse_args()
    currency = normalize_currency(args.currency)
    symbol = f"f{currency}"

    api_key = os.getenv("BITFINEX_API_KEY")
    api_secret = os.getenv("BITFINEX_API_SECRET")
    if not api_key or not api_secret:
        raise SystemExit("Missing BITFINEX_API_KEY / BITFINEX_API_SECRET")

    try:
        wallets = bfx_post("/v2/auth/r/wallets", {}, api_key, api_secret)
        credits = bfx_post(f"/v2/auth/r/funding/credits/{symbol}", {}, api_key, api_secret)

        now_ms = int(time.time() * 1000)
        start_dt = datetime.now(timezone.utc) - timedelta(days=max(1, args.days))
        start_ms = int(start_dt.timestamp() * 1000)

        ledgers = bfx_post(
            f"/v2/auth/r/ledgers/{currency}/hist",
            {
                "start": start_ms,
                "end": now_ms,
                "limit": 2500,
                "wallet": "funding",
            },
            api_key,
            api_secret,
        )
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Bitfinex API error: HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e}")

    funding_wallet = None
    for w in wallets:
        # [TYPE, CURRENCY, BALANCE, UNSETTLED_INTEREST, AVAILABLE_BALANCE, ...]
        if len(w) >= 5 and str(w[0]).lower() == "funding" and str(w[1]).upper() == currency:
            funding_wallet = w
            break

    wallet_balance = safe_float(funding_wallet[2]) if funding_wallet else 0.0
    unsettled_interest = safe_float(funding_wallet[3]) if funding_wallet else 0.0
    available_balance = safe_float(funding_wallet[4]) if funding_wallet else 0.0

    active_credit_amount = 0.0
    weighted_rate_sum = 0.0
    active_count = 0
    for c in credits:
        # [.., AMOUNT=5, .., STATUS=7, .., RATE=11]
        if len(c) < 12:
            continue
        amount = safe_float(c[5])
        status = str(c[7]).upper()
        rate = safe_float(c[11])
        if status == "ACTIVE":
            active_count += 1
            active_credit_amount += amount
            weighted_rate_sum += amount * rate

    avg_rate = (weighted_rate_sum / active_credit_amount) if active_credit_amount > 0 else 0.0

    # Ledger tuple: [ID, CURRENCY, WALLET, MTS, .., AMOUNT(5), BALANCE(6), .., DESCRIPTION(8)]
    interest_like = []
    for row in ledgers:
        if len(row) < 9:
            continue
        amt = safe_float(row[5])
        mts = int(row[3]) if row[3] is not None else 0
        desc = str(row[8]).lower()

        # Heuristic: funding interest收益常见于描述包含 interest / funding / swap。
        if amt > 0 and ("interest" in desc or "funding" in desc or "swap" in desc):
            interest_like.append((mts, amt, row[8]))

    total_interest_window = sum(x[1] for x in interest_like)

    today_utc = datetime.now(timezone.utc).date()
    interest_today = 0.0
    for mts, amt, _ in interest_like:
        if datetime.fromtimestamp(mts / 1000, timezone.utc).date() == today_utc:
            interest_today += amt

    summary = {
        "currency": currency,
        "wallet_balance": wallet_balance,
        "available_balance": available_balance,
        "unsettled_interest": unsettled_interest,
        "active_credits": active_count,
        "active_credit_amount": active_credit_amount,
        "avg_active_rate_decimal": avg_rate,
        "interest_today_utc": interest_today,
        "interest_last_n_days": total_interest_window,
        "window_days": max(1, args.days),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        return

    print(f"Bitfinex Funding Summary ({currency})")
    print(f"- Wallet balance: {wallet_balance:.8f}")
    print(f"- Available: {available_balance:.8f}")
    print(f"- Unsettled interest: {unsettled_interest:.8f}")
    print(f"- Active credits: {active_count} (amount {active_credit_amount:.8f})")
    print(f"- Avg active rate: {avg_rate * 100:.4f}%")
    print(f"- Interest today (UTC): {interest_today:.8f}")
    print(f"- Interest last {max(1, args.days)} day(s): {total_interest_window:.8f}")


if __name__ == "__main__":
    main()
