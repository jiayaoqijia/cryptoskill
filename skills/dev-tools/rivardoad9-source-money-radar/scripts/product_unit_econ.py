#!/usr/bin/env python3
"""Per-unit economics for a physical product. Stdlib only.

Example:
  python product_unit_econ.py --price 129000 --cogs 35000 \
    --fee-pct 10 --ad-pct 15 --ship 8000 --packaging 2000 \
    --returns-pct 2 --units 150 --capital 7250000

Returns JSON. Contribution is conservative: returns are charged at the
full selling price (lost revenue) with no recovery of COGS.
"""
import argparse
import json
import math


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--price", type=float, required=True, help="selling price per unit")
    p.add_argument("--cogs", type=float, required=True, help="cost of goods incl. label")
    p.add_argument("--fee-pct", type=float, default=10.0, help="marketplace/payment fee %% of price")
    p.add_argument("--ad-pct", type=float, default=0.0, help="ad spend %% of price")
    p.add_argument("--ship", type=float, default=0.0, help="shipping subsidy per unit")
    p.add_argument("--packaging", type=float, default=0.0, help="packaging per unit")
    p.add_argument("--returns-pct", type=float, default=0.0, help="return/write-off rate %%")
    p.add_argument("--units", type=float, default=0.0, help="units sold per month")
    p.add_argument("--capital", type=float, default=0.0, help="total test capital")
    p.add_argument("--wholesale", type=float, default=None, help="optional wholesale price per unit")
    p.add_argument("--wholesale-ship", type=float, default=0.0, help="shipping per wholesale unit")
    a = p.parse_args()

    if a.price <= 0:
        raise SystemExit("price must be > 0")

    returns_cost = a.price * a.returns_pct / 100.0
    fees = a.price * (a.fee_pct + a.ad_pct) / 100.0
    contribution = a.price - a.cogs - fees - a.ship - a.packaging - returns_cost
    margin_pct = contribution / a.price * 100.0

    out = {
        "price": round(a.price),
        "cogs": round(a.cogs),
        "fees_and_ads": round(fees),
        "returns_cost": round(returns_cost),
        "contribution": round(contribution),
        "margin_pct": round(margin_pct, 1),
    }

    if a.units > 0:
        monthly_profit = contribution * a.units
        out["units_per_month"] = a.units
        out["monthly_profit"] = round(monthly_profit)
        if a.capital > 0:
            out["break_even_units"] = math.ceil(a.capital / contribution) if contribution > 0 else None
            out["payback_months"] = round(a.capital / monthly_profit, 1) if monthly_profit > 0 else None

    if a.wholesale is not None:
        w_contrib = a.wholesale - a.cogs - a.packaging - a.wholesale_ship
        out["wholesale"] = {
            "price": round(a.wholesale),
            "contribution": round(w_contrib),
            "margin_pct": round(w_contrib / a.wholesale * 100.0, 1) if a.wholesale > 0 else None,
        }

    out["passes_35pct"] = margin_pct >= 35.0
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
