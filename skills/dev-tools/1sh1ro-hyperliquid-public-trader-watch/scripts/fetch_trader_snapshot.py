#!/usr/bin/env python3
import argparse
import json
import statistics
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from urllib.error import URLError


API_URL = "https://api.hyperliquid.xyz/info"


def post(payload):
    last_error = None
    for attempt in range(3):
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except URLError as exc:
            last_error = exc
            if attempt == 2:
                raise
            time.sleep(1.0 + attempt)
    raise last_error


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_snapshot(address):
    return {
        "state": post({"type": "clearinghouseState", "user": address}),
        "fills": post({"type": "userFills", "user": address}),
        "portfolio": post({"type": "portfolio", "user": address}),
    }


def summarize_positions(state):
    positions = []
    for item in state.get("assetPositions", []):
        pos = item.get("position", {})
        if not pos:
            continue
        positions.append(
            {
                "coin": pos.get("coin"),
                "size": to_float(pos.get("szi")),
                "entry_px": to_float(pos.get("entryPx")),
                "position_value": to_float(pos.get("positionValue")),
                "unrealized_pnl": to_float(pos.get("unrealizedPnl")),
                "roe": to_float(pos.get("returnOnEquity")),
                "liq_px": pos.get("liquidationPx"),
                "margin_used": to_float(pos.get("marginUsed")),
                "leverage": (pos.get("leverage") or {}).get("value"),
            }
        )
    positions.sort(key=lambda x: abs(x["position_value"]), reverse=True)
    return positions


def summarize_fills(fills, limit):
    top_coins = Counter()
    dir_counter = Counter()
    pnl_by_coin = defaultdict(float)
    recent = []

    for fill in fills[:limit]:
        coin = fill.get("coin", "?")
        direction = fill.get("dir", "?")
        pnl = to_float(fill.get("closedPnl"))
        size = to_float(fill.get("sz"))
        top_coins[coin] += abs(size)
        dir_counter[direction] += 1
        pnl_by_coin[coin] += pnl
        recent.append(
            {
                "coin": coin,
                "dir": direction,
                "px": fill.get("px"),
                "sz": fill.get("sz"),
                "closedPnl": fill.get("closedPnl"),
                "time": fill.get("time"),
            }
        )

    return {
        "recent": recent,
        "top_coins_by_fill_size": top_coins.most_common(5),
        "direction_counts": dict(dir_counter),
        "closed_pnl_by_coin": {
            coin: round(value, 4) for coin, value in sorted(pnl_by_coin.items(), key=lambda x: -abs(x[1]))
        },
    }


def summarize_portfolio(portfolio):
    out = {}
    for label, series in portfolio:
        account_values = [to_float(v) for _, v in series.get("accountValueHistory", [])]
        pnl_values = [to_float(v) for _, v in series.get("pnlHistory", [])]
        out[label] = {
            "points": len(account_values),
            "last_account_value": account_values[-1] if account_values else None,
            "last_pnl": pnl_values[-1] if pnl_values else None,
            "account_value_volatility": round(statistics.pstdev(account_values), 4) if len(account_values) > 1 else 0.0,
            "volume": to_float(series.get("vlm")),
        }
    return out


def infer_style(positions, fill_summary):
    notes = []

    if not positions:
        notes.append("当前无持仓，更像阶段性休息或已平仓后的观察窗口。")
    elif len(positions) == 1:
        notes.append("当前高度单一标的集中，偏强 conviction 交易。")
    else:
        top = positions[0]["position_value"]
        total = sum(abs(p["position_value"]) for p in positions)
        if total and abs(top) / total > 0.7:
            notes.append("虽然有多腿，但风险仍集中在主仓，属于主观点驱动。")
        else:
            notes.append("当前更像多腿组合或轮动管理，不是纯单边孤注一掷。")

    leverages = [p["leverage"] for p in positions if p.get("leverage") is not None]
    if leverages:
        max_lev = max(leverages)
        if max_lev >= 20:
            notes.append("使用高杠杆，说明容忍波动但对方向和时机要求极高。")
        elif max_lev <= 5:
            notes.append("杠杆并不夸张，更像中等频率的结构交易。")

    dirs = fill_summary["direction_counts"]
    opens = sum(v for k, v in dirs.items() if "Open" in k)
    closes = sum(v for k, v in dirs.items() if "Close" in k)
    if opens and not closes:
        notes.append("最近动作以开仓为主，处在建立观点阶段。")
    elif closes > opens:
        notes.append("最近动作以减仓/平仓为主，偏兑现或止损后的重整。")

    return notes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--fills-limit", type=int, default=30)
    args = parser.parse_args()

    snapshot = load_snapshot(args.address)
    positions = summarize_positions(snapshot["state"])
    fill_summary = summarize_fills(snapshot["fills"], args.fills_limit)
    portfolio = summarize_portfolio(snapshot["portfolio"])
    style = infer_style(positions, fill_summary)

    output = {
        "name": args.name or args.address,
        "address": args.address,
        "withdrawable": snapshot["state"].get("withdrawable"),
        "positions": positions,
        "fills": fill_summary,
        "portfolio": portfolio,
        "style_inference": style,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
