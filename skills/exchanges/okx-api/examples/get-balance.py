"""
Get OKX account balance.

Usage:
    OKX_API_KEY=... OKX_SECRET_KEY=... OKX_PASSPHRASE=... python get-balance.py
    OKX_DEMO=1 python get-balance.py   # sandbox mode
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from okx_auth import make_request


def main():
    data = make_request("GET", "/api/v5/account/balance")

    for account in data:
        total_eq = account.get("totalEq", "0")
        imr = account.get("imr", "0")        # Initial margin requirement
        mmr = account.get("mmr", "0")        # Maintenance margin requirement
        print(f"Total equity (USD):  {float(total_eq):,.2f}")
        print(f"Initial margin req:  {float(imr):,.2f}")
        print(f"Maintenance margin:  {float(mmr):,.2f}")
        print()

        details = account.get("details", [])
        non_zero = [d for d in details if float(d.get("eq", 0) or 0) > 0]
        if non_zero:
            print(f"{'Currency':<10} {'Equity':>16} {'Available':>16} {'Frozen':>16}")
            print("-" * 62)
            for d in non_zero:
                ccy = d.get("ccy", "")
                eq = float(d.get("eq", 0) or 0)
                avail = float(d.get("availEq", 0) or 0)
                frozen = float(d.get("frozenBal", 0) or 0)
                print(f"{ccy:<10} {eq:>16.6f} {avail:>16.6f} {frozen:>16.6f}")
        else:
            print("No non-zero balances found.")


if __name__ == "__main__":
    main()
