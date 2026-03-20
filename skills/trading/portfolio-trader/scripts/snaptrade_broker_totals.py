#!/usr/bin/env python3
import argparse
from collections import defaultdict

from snaptrade_common import load_config, get_client


def get_rate(client, pair):
    # pair like USD-CAD
    resp = client.reference_data.get_currency_exchange_rate_pair(currency_pair=pair)
    body = getattr(resp, "body", resp)
    if isinstance(body, dict):
        return float(body.get("rate") or body.get("exchange_rate") or body.get("value"))
    return None


def parse_args():
    p = argparse.ArgumentParser(description="Per-broker totals with currency conversion.")
    p.add_argument("--currency", default="CAD", help="Target currency (default CAD)")
    return p.parse_args()


def main():
    args = parse_args()
    target = args.currency.upper()

    cfg = load_config()
    client = get_client(cfg)
    user_id = cfg["user_id"]
    user_secret = cfg["user_secret"]

    resp = client.account_information.list_user_accounts(user_id=user_id, user_secret=user_secret)
    accounts = getattr(resp, "body", resp)
    if not isinstance(accounts, list):
        accounts = list(accounts) if accounts is not None else []

    broker_totals = defaultdict(lambda: defaultdict(float))

    for a in accounts:
        account_id = a.get("id") if isinstance(a, dict) else getattr(a, "id", None)
        inst = a.get("institution_name") if isinstance(a, dict) else getattr(a, "institution_name", None)
        if not account_id:
            continue

        # positions
        try:
            pos_resp = client.account_information.get_user_account_positions(
                user_id=user_id, user_secret=user_secret, account_id=account_id
            )
            pos_body = getattr(pos_resp, "body", pos_resp)
            positions = pos_body if isinstance(pos_body, list) else (pos_body.get("positions") if isinstance(pos_body, dict) else [])
        except Exception:
            positions = []

        for p in positions:
            if not isinstance(p, dict):
                continue
            price = p.get("price") or 0
            units = p.get("units") or p.get("fractional_units") or 0
            cur_obj = p.get("currency") or {}
            cur = cur_obj.get("code") if isinstance(cur_obj, dict) else None
            if cur:
                broker_totals[inst][cur] += float(price) * float(units)

        # balances (cash)
        try:
            bal_resp = client.account_information.get_user_account_balance(
                user_id=user_id, user_secret=user_secret, account_id=account_id
            )
            bal_body = getattr(bal_resp, "body", bal_resp) or []
            for b in bal_body:
                if not isinstance(b, dict):
                    continue
                cur_obj = b.get("currency") or {}
                cur = cur_obj.get("code") if isinstance(cur_obj, dict) else None
                cash = b.get("cash")
                if cur and cash is not None:
                    broker_totals[inst][cur] += float(cash)
        except Exception:
            pass

    # build FX rates for needed currencies
    needed = set()
    for curmap in broker_totals.values():
        for cur in curmap.keys():
            if cur != target:
                needed.add(cur)

    rates = {}
    for cur in needed:
        # SnapTrade expects pair format like USD-CAD
        pair = f"{cur}-{target}"
        try:
            rate = get_rate(client, pair)
            if rate:
                rates[cur] = rate
                continue
        except Exception:
            pass
        # try inverse
        inv_pair = f"{target}-{cur}"
        try:
            inv_rate = get_rate(client, inv_pair)
            if inv_rate:
                rates[cur] = 1.0 / inv_rate
        except Exception:
            pass

    # output per broker totals in target currency
    results = {}
    missing_rates = defaultdict(list)
    for broker, curmap in broker_totals.items():
        total = 0.0
        for cur, amt in curmap.items():
            if cur == target:
                total += amt
            else:
                rate = rates.get(cur)
                if rate is not None:
                    total += amt * rate
                else:
                    missing_rates[broker].append(cur)
        results[broker] = round(total, 2)

    out = {"currency": target, "broker_totals": results, "rates": rates}
    if missing_rates:
        out["missing_rates"] = dict(missing_rates)
    print(out)


if __name__ == "__main__":
    main()
