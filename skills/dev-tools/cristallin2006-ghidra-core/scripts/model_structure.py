#!/usr/bin/env python3
"""Check two common CTF answer-uniqueness traps without guessing a flag.

length: report unchecked input positions from the actual comparison coverage.
matrix: test invertibility of a square integer matrix modulo an integer.
For a composite modulus, determinant gcd != 1 proves non-uniqueness when
solutions exist; it does not itself prove that a particular target is soluble.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def determinant(rows: list[list[int]]) -> int:
    if len(rows) == 1:
        return rows[0][0]
    # Fraction-free Bareiss elimination avoids floating-point rank errors.
    a = [r[:] for r in rows]
    sign, denom, n = 1, 1, len(a)
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if a[i][k]), None)
            if swap is None:
                return 0
            a[k], a[swap] = a[swap], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) // denom
            a[i][k] = 0
        denom = pivot
    return sign * a[-1][-1]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("length")
    q.add_argument("--required", type=int, required=True)
    q.add_argument("--checked", required=True,
                   help="comma-separated zero-based indices or ranges, e.g. 0-18,21")
    q = sub.add_parser("matrix")
    q.add_argument("--rows", required=True,
                   help='JSON square matrix, e.g. "[[1,-1],[1,1]]"')
    q.add_argument("--modulus", type=int, required=True)
    args = p.parse_args()
    try:
        if args.command == "length":
            if args.required <= 0:
                raise ValueError("required length must be positive")
            checked = set()
            for part in args.checked.split(","):
                bounds = [int(x) for x in part.strip().split("-")]
                if len(bounds) == 1:
                    checked.add(bounds[0])
                elif len(bounds) == 2 and bounds[0] <= bounds[1]:
                    checked.update(range(bounds[0], bounds[1] + 1))
                else:
                    raise ValueError("bad checked range")
            if any(i < 0 or i >= args.required for i in checked):
                raise ValueError("checked index outside required input")
            free = sorted(set(range(args.required)) - checked)
            result = {"required": args.required, "checked_count": len(checked),
                      "free_indices": free, "full_coverage": not free,
                      "note": "full coverage alone does not prove a unique solution"}
            code = 2 if free else 0
        else:
            rows = json.loads(args.rows)
            n = len(rows)
            if (args.modulus <= 1 or n < 1 or
                    any(not isinstance(r, list) or len(r) != n for r in rows) or
                    any(type(x) is not int for r in rows for x in r)):
                raise ValueError("need a nonempty square integer matrix and modulus > 1")
            det = determinant(rows)
            gcd = math.gcd(det, args.modulus)
            result = {"equations": n, "unknowns": n, "determinant": det,
                      "modulus": args.modulus, "gcd": gcd,
                      "invertible": gcd == 1,
                      "note": "noninvertible means multiple solutions if a solution exists" if gcd != 1 else "unique solution for every target"}
            code = 0 if gcd == 1 else 2
        print(json.dumps(result, ensure_ascii=False))
        return code
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
