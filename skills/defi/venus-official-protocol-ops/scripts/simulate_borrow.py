#!/usr/bin/env python3
"""Borrow what-if calculator with conservative health target."""
import argparse


def classify(health: float) -> str:
    if health < 1.15:
        return "HIGH"
    if health < 1.35:
        return "MEDIUM"
    return "LOW"


def main():
    p = argparse.ArgumentParser(description="Simulate post-borrow health")
    p.add_argument("--weighted-collateral", type=float, required=True)
    p.add_argument("--current-debt", type=float, required=True)
    p.add_argument("--extra-borrow", type=float, required=True)
    p.add_argument("--target-health", type=float, default=1.30)
    args = p.parse_args()

    new_debt = args.current_debt + args.extra_borrow
    if new_debt <= 0:
        print("post_health=inf risk=LOW max_extra_borrow_for_target=inf")
        return

    post_health = args.weighted_collateral / new_debt

    # Maximum additional borrow still satisfying target health
    max_debt_for_target = args.weighted_collateral / args.target_health
    max_extra = max(0.0, max_debt_for_target - args.current_debt)

    print(
        f"post_health={post_health:.4f} "
        f"risk={classify(post_health)} "
        f"max_extra_borrow_for_target={max_extra:.2f}"
    )


if __name__ == "__main__":
    main()
