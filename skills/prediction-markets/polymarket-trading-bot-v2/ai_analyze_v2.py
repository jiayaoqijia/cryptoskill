#!/usr/bin/env python3
"""
AI 分析和下注决策 v2
- 使用 ai_model_v2 的新策略
- 用期望值（EV）决定是否下注，而不是固定阈值
"""
import sys
import json
from datetime import datetime, timezone

sys.path.insert(0, "/root/.openclaw/workspace/polymarket-arb-bot")

from ai_trader.ai_model_v2 import analyze_market
import subprocess


def log_decision(slug, coin, ptb, direction, confidence, up_odds, down_odds, details):
    """记录决策到统计文件"""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "coin": coin,
        "ptb": ptb,
        "direction": direction,
        "confidence": confidence,
        "up_odds": up_odds,
        "down_odds": down_odds,
        "ev": details.get("expected_value", 0),
        "price_diff_pct": details.get("price_diff_pct", 0),
        "diff_in_atr": details.get("diff_in_atr", 0),
        "current_price": details.get("current_price", 0),
        "total_score": details.get("total_score", 0),
    }

    with open("logs/decisions_v2.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")


def analyze_and_decide(coin, price_to_beat, up_odds, down_odds, slug):
    """
    执行 AI 分析并返回决策

    返回: (should_bet, direction, confidence, details)
    """
    direction, confidence, details = analyze_market(
        coin, price_to_beat, up_odds, down_odds
    )

    if not direction:
        return False, None, 0, details

    # 记录决策
    log_decision(slug, coin, price_to_beat, direction, confidence, up_odds, down_odds, details)

    # ── 下注条件（基于期望值） ──
    # 1. 置信度 >= 55%（基本面）
    # 2. EV > 0.05（期望值为正且有足够边际）
    # 3. 赔率 < 0.90（不买太贵的）
    target_odds = up_odds if direction == "UP" else down_odds
    ev = details.get("expected_value", 0)

    should_bet = (
        confidence >= 0.55
        and ev > 0.05
        and target_odds < 0.90
    )

    details["should_bet"] = should_bet
    details["bet_reason"] = (
        f"conf={confidence:.0%} ev={ev:+.3f} odds={target_odds:.3f}"
    )

    return should_bet, direction, confidence, details


def execute_bet(slug, direction, amount=10):
    """执行下注（通过 Polymarket CLI）"""
    outcome_index = 0 if direction == "UP" else 1

    cmd = [
        "polymarket", "clob", "market-order",
        "--slug", slug,
        "--outcome", str(outcome_index),
        "--amount", str(amount),
        "--side", "BUY",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return (
        result.returncode == 0,
        result.stdout if result.returncode == 0 else result.stderr,
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        coin = sys.argv[1]
        ptb = float(sys.argv[2])
        up_odds = float(sys.argv[3])
        down_odds = float(sys.argv[4])

        should_bet, direction, confidence, details = analyze_and_decide(
            coin, ptb, up_odds, down_odds, "test"
        )

        print(f"Direction: {direction}")
        print(f"Confidence: {confidence*100:.1f}%")
        print(f"Should bet: {should_bet}")
        print(f"EV: {details.get('expected_value', 0):+.3f}")
        print(f"Details: {json.dumps(details, indent=2)}")
