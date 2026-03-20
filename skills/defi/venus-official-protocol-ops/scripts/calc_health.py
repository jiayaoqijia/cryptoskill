#!/usr/bin/env python3
import argparse


def main():
    p = argparse.ArgumentParser(description="Calculate health and buffer from collateral/debt")
    p.add_argument("--weighted-collateral", type=float, required=True, help="Weighted collateral USD")
    p.add_argument("--debt", type=float, required=True, help="Debt USD")
    args = p.parse_args()

    if args.debt <= 0:
        print("health=inf buffer_pct=inf")
        return

    health = args.weighted_collateral / args.debt
    buffer_pct = (health - 1.0) * 100
    print(f"health={health:.4f} buffer_pct={buffer_pct:.2f}")


if __name__ == "__main__":
    main()
