#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "references" / "trader-registry.json"
SNAPSHOT_SCRIPT = ROOT.parent / "hyperliquid-public-trader-watch" / "scripts" / "fetch_trader_snapshot.py"


def load_registry():
    return json.loads(REGISTRY_PATH.read_text())


def load_snapshot(name, address):
    cmd = [
        "python3",
        str(SNAPSHOT_SCRIPT),
        "--address",
        address,
        "--name",
        name,
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def confidence_penalty(label):
    mapping = {
        "high": 0,
        "medium": -2,
        "low-medium": -4,
        "low": -6,
    }
    return mapping.get(label, -3)


def score_snapshot(item, snapshot):
    positions = snapshot.get("positions", [])
    fills = snapshot.get("fills", {}).get("recent", [])
    week = snapshot.get("portfolio", {}).get("week", {})

    total_position_value = sum(abs(p.get("position_value", 0.0)) for p in positions)
    total_unrealized = sum(p.get("unrealized_pnl", 0.0) for p in positions)
    max_leverage = max([p.get("leverage", 0) or 0 for p in positions], default=0)
    volume = week.get("volume") or 0.0

    score = 0.0
    if positions:
        score += 40
        score += min(total_position_value / 1_000_000, 40)
        score += min(abs(total_unrealized) / 100_000, 10)
    else:
        score += 5

    if fills:
        score += min(len(fills), 10)

    if volume:
        score += min(volume / 10_000_000, 10)

    if max_leverage >= 20:
        score += 5

    score += confidence_penalty(item.get("attribution_confidence", "medium"))

    return {
        "score": round(score, 2),
        "active": bool(positions),
        "position_count": len(positions),
        "total_position_value": round(total_position_value, 2),
        "total_unrealized_pnl": round(total_unrealized, 2),
        "max_leverage": max_leverage,
        "recent_fill_count": len(fills),
        "week_volume": round(volume, 2),
    }


def build_watch_reason(snapshot, metrics):
    if metrics["active"]:
        positions = snapshot.get("positions", [])
        top = positions[0] if positions else {}
        return f"当前有实盘风险，主仓 {top.get('coin', '?')}，杠杆上到 {top.get('leverage', '?')}x。"
    if metrics["recent_fill_count"]:
        return "当前空仓，但最近还有可复盘的真实成交。"
    return "当前公开信号很弱，更适合暂时忽略。"


def build_learn_takeaway(snapshot, metrics):
    style = snapshot.get("style_inference", [])
    if style:
        return style[0]
    if metrics["active"]:
        return "可以观察他怎么用仓位表达主观点。"
    return "当前更适合作为历史样本，不适合作为实时模板。"


def build_copy_warning(metrics):
    if metrics["active"] and metrics["max_leverage"] >= 20:
        return "高杠杆重仓，晚到的人复制的是劣化后的盈亏比。"
    if metrics["active"]:
        return "有活跃仓位也不等于适合照抄，尤其是入场价已经错位。"
    return "现在没有实时仓位，拿不到当下方向，别硬抄。"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ranked = []
    for item in load_registry():
        snapshot = load_snapshot(item["name"], item["address"])
        metrics = score_snapshot(item, snapshot)
        ranked.append(
            {
                "name": item["name"],
                "address": item["address"],
                "attribution_confidence": item["attribution_confidence"],
                "tags": item.get("tags", []),
                "score": metrics["score"],
                "watch_reason": build_watch_reason(snapshot, metrics),
                "learn_takeaway": build_learn_takeaway(snapshot, metrics),
                "copy_warning": build_copy_warning(metrics),
                "metrics": metrics,
                "top_positions": snapshot.get("positions", [])[:3],
                "recent_fills": snapshot.get("fills", {}).get("recent", [])[:5],
            }
        )

    ranked.sort(key=lambda x: x["score"], reverse=True)
    if args.top is not None:
        ranked = ranked[: args.top]

    if args.json:
        json.dump(ranked, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    for idx, item in enumerate(ranked, start=1):
        print(f"{idx}. {item['name']}  score={item['score']}")
        print(f"   当前在干什么: {item['watch_reason']}")
        print(f"   能学什么: {item['learn_takeaway']}")
        print(f"   别怎么抄: {item['copy_warning']}")
        if item["top_positions"]:
            pos = item["top_positions"][0]
            print(
                f"   主仓: {pos.get('coin')} value={pos.get('position_value')} "
                f"uPnL={pos.get('unrealized_pnl')} lev={pos.get('leverage')}"
            )
        print(f"   地址: {item['address']}  归因置信度: {item['attribution_confidence']}")


if __name__ == "__main__":
    main()
