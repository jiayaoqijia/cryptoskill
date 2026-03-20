#!/usr/bin/env python3
"""Health-factor monitor with customizable safety line and assistant alert text."""
import argparse
import json
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent


def run_wallet(wallet: str, scan_limit: int, strategy: str):
    cmd = [
        "python3", str(ROOT / "wallet_onchain_exposure.py"),
        "--wallet", wallet,
        "--scan-limit", str(scan_limit),
        "--strategy", strategy,
    ]
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def main():
    p = argparse.ArgumentParser(description="HF monitor")
    p.add_argument("--wallet", required=True)
    p.add_argument("--safe-hf", type=float, default=1.2, help="Customizable safety line")
    p.add_argument("--warn-hf", type=float, default=1.35)
    p.add_argument("--critical-hf", type=float, default=1.15)
    p.add_argument("--scan-limit", type=int, default=120)
    p.add_argument("--strategy", choices=["auto", "all"], default="auto")
    args = p.parse_args()

    obj = run_wallet(args.wallet, args.scan_limit, args.strategy)
    s = obj.get("summary", {})
    health = s.get("health")

    status = "OK"
    advice = ["No urgent action."]
    assistant_alert = None

    if health != "inf":
        h = float(health)
        if h < args.critical_hf:
            status = "CRITICAL"
            advice = [
                "Repay debt immediately or add collateral.",
                "Avoid new borrows until health recovers.",
            ]
        elif h < args.warn_hf:
            status = "WARN"
            advice = [
                "Increase safety buffer (repay or add collateral).",
                "Avoid increasing borrow exposure.",
            ]

        if h < args.safe_hf:
            assistant_alert = (
                f"ACCOUNT_UNHEALTHY: HF {h:.6f} is below safety line {args.safe_hf}. "
                "Withdrawals can increase liquidation risk."
            )

    out = {
        "wallet": args.wallet,
        "health": health,
        "risk": s.get("risk"),
        "status": status,
        "safeLine": args.safe_hf,
        "safe": (health == "inf" or float(health) >= args.safe_hf),
        "totalSupplyUsd": s.get("totalSupplyUsd"),
        "totalBorrowUsd": s.get("totalBorrowUsd"),
        "advice": advice,
        "assistantAlert": assistant_alert,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
