"""Arithmetic facts only. No technical ratings, risk labels or trade signals."""
from __future__ import annotations

from common import asset_key, instant, number


def change(start, end):
    a, b = number(start), number(end)
    if a is None or b is None or a == 0:
        return None
    return (b / a - 1) * 100


def concentration(document: dict) -> dict:
    supply = number(document.get("total_supply"))
    if supply is None or supply <= 0:
        raise ValueError("Positive supply with a stated unit is required")
    rows, seen = [], set()
    for holder in document["holders"]:
        key = asset_key({"chain": document["chain"], "address": holder["address"]})
        if key in seen:
            raise ValueError("Duplicate holder address")
        seen.add(key)
        balance = number(holder["balance"])
        if balance is None or balance < 0:
            raise ValueError("Holder balances must be nonnegative")
        if holder.get("exclude") and not holder.get("label_source"):
            raise ValueError("Excluding a technical/custodial address requires a label source")
        rows.append({**holder, "balance": balance})
    if sum(row["balance"] for row in rows) > supply * (1 + 1e-9):
        raise ValueError("Holder balances exceed stated total supply")
    excluded = sum(row["balance"] for row in rows if row.get("exclude"))
    eligible = supply - excluded
    def top(n, adjusted):
        chosen = [r["balance"] for r in rows if not adjusted or not r.get("exclude")]
        denominator = eligible if adjusted else supply
        return sum(sorted(chosen, reverse=True)[:n]) / denominator * 100 if denominator > 0 else None
    return {"raw_top10_pct": top(10, False), "adjusted_top10_pct": top(10, True),
            "observed_address_count": len(rows), "excluded_supply": excluded,
            "adjusted_denominator": eligible, "coverage": document.get("coverage", "partial"),
            "note": "Partial samples are lower bounds, not full ownership distribution; adjusted addresses are not beneficial owners or free float."}


def candles(document: dict) -> dict:
    rows = document["candles"]
    if not rows:
        raise ValueError("No candles")
    times = [instant(row["time"]) for row in rows]
    if times != sorted(set(times)):
        raise ValueError("Candles must have unique ascending timestamps")
    closes = [number(row["close"]) for row in rows]
    if any(x is None or x <= 0 for x in closes):
        raise ValueError("Positive closes required")
    result = {"count": len(rows), "from": rows[0]["time"], "to": rows[-1]["time"],
              "return_pct": change(closes[0], closes[-1]), "last_close": closes[-1],
              "instrument": document["instrument"], "interval": document["interval"]}
    for period in (20, 50, 200):
        result[f"sma_{period}"] = sum(closes[-period:]) / period if len(closes) >= period else None
    # Wilder RSI: seed from 14 price differences, then recursive smoothing.
    if len(closes) < 15:
        result["rsi14_wilder"] = None
    else:
        differences = [b - a for a, b in zip(closes, closes[1:])]
        gain = sum(max(x, 0) for x in differences[:14]) / 14
        loss = sum(max(-x, 0) for x in differences[:14]) / 14
        for delta in differences[14:]:
            gain, loss = (gain * 13 + max(delta, 0)) / 14, (loss * 13 + max(-delta, 0)) / 14
        result["rsi14_wilder"] = 50 if gain == loss == 0 else (100 if loss == 0 else 100 - 100 / (1 + gain / loss))
    return result


def depth(document: dict) -> dict:
    amount = number(document["quote_amount"])
    if amount is None or amount <= 0:
        raise ValueError("Positive quote_amount required")
    bids = sorted([(float(p), float(q)) for p, q in document["bids"]], reverse=True)
    asks = sorted([(float(p), float(q)) for p, q in document["asks"]])
    if not bids or not asks or any(p <= 0 or q < 0 for p, q in bids + asks) or bids[0][0] >= asks[0][0]:
        raise ValueError("Noncrossed, positive order book required")
    remaining, base = amount, 0.0
    for price, quantity in asks:
        take = min(remaining, price * quantity)
        base += take / price
        remaining -= take
        if remaining <= 1e-9:
            break
    buy_vwap = amount / base if remaining <= 1e-9 else None
    remaining_base, proceeds = base, 0.0
    if buy_vwap is not None:
        for price, quantity in bids:
            take = min(remaining_base, quantity)
            proceeds += take * price
            remaining_base -= take
            if remaining_base <= 1e-9:
                break
    return {"spread_pct": (asks[0][0] / bids[0][0] - 1) * 100,
            "quote_amount": amount, "buy_vwap": buy_vwap,
            "buy_impact_pct": (buy_vwap / asks[0][0] - 1) * 100 if buy_vwap else None,
            "roundtrip_quote_return_pct": (proceeds / amount - 1) * 100 if buy_vwap and remaining_base <= 1e-9 else None,
            "note": "Displayed snapshot only; ignores fees, queue changes and hidden liquidity; not an execution guarantee."}


def delta(document: dict) -> dict:
    before, after = document["before"], document["after"]
    if asset_key(before["asset"]) != asset_key(after["asset"]):
        raise ValueError("Snapshot asset mismatch")
    if instant(after["observed_at"]) <= instant(before["observed_at"]):
        raise ValueError("After timestamp must be later")
    result = {}
    for key in before["metrics"].keys() & after["metrics"].keys():
        a, b = before["metrics"][key], after["metrics"][key]
        if a["unit"] != b["unit"] or a["scope"] != b["scope"]:
            raise ValueError(f"Metric scope/unit mismatch: {key}")
        left, right = number(a["value"]), number(b["value"])
        result[key] = {"before": left, "after": right, "delta": right-left if left is not None and right is not None else None,
                       "change_pct": change(left, right), "unit": a["unit"], "scope": a["scope"]}
    return {"before": before["observed_at"], "after": after["observed_at"], "metrics": result}


def calculate(document: dict) -> dict:
    dispatch = {"concentration": concentration, "candles": candles, "depth": depth, "delta": delta}
    return dispatch[document["operation"]](document)
