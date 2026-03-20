#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息格式化模块
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import calculator


def format_signal_json(signal_type, direction, zscore, ratio, mean, std,
                      eth_price, btc_price, strength, reason, threshold, position_size):
    """
    格式化为 JSON 信号
    
    Returns:
        dict: 信号数据
    """
    # 计算预估收益
    estimate = calculator.calculate_expected_pnl(eth_price, btc_price, position_size)
    
    # 动作描述
    if signal_type == "OPEN":
        if direction == "LONG_ETH_SHORT_BTC":
            action = "LONG ETH-PERP + SHORT BTC-PERP"
            eth_action = f"LONG ETH-PERP @ ${eth_price:,.2f}"
            btc_action = f"SHORT BTC-PERP @ ${btc_price:,.2f}"
        else:
            action = "SHORT ETH-PERP + LONG BTC-PERP"
            eth_action = f"SHORT ETH-PERP @ ${eth_price:,.2f}"
            btc_action = f"LONG BTC-PERP @ ${btc_price:,.2f}"
    elif signal_type == "CLOSE":
        action = "平仓全部对冲头寸"
        eth_action = "市价平仓 ETH 多/空仓"
        btc_action = "市价平仓 BTC 多/空仓"
    else:
        action = "观望"
        eth_action = "无操作"
        btc_action = "无操作"
    
    # 信号强度星级
    stars = "★" * strength + "☆" * (5 - strength)
    
    # 波动率评估（简化）
    volatility = "normal"
    
    return {
        "timestamp": get_timestamp(),
        "signal_type": signal_type,
        "direction": direction,
        "zscore": round(zscore, 4),
        "ratio": round(ratio, 6),
        "mean": round(mean, 6),
        "std": round(std, 6),
        "threshold": {
            "entry": threshold["entry_threshold"],
            "exit": threshold["exit_threshold"],
            "stop_loss": threshold["stop_loss"]
        },
        "prices": {
            "eth": eth_price,
            "btc": btc_price
        },
        "recommendation": {
            "action": action,
            "eth_action": eth_action,
            "btc_action": btc_action,
            "position_size_usd": position_size
        },
        "estimate": {
            "expected_return": round(estimate["gross_pnl"], 4),
            "fees_taker": round(estimate["fees"], 4),
            "net_pnl": round(estimate["net_pnl"], 4),
            "return_pct": round(estimate["return_pct"], 3)
        },
        "strength": strength,
        "reason": reason,
        "volatility": volatility
    }


def format_signal_message(signal_data):
    """
    格式化为 Telegram/飞书 推送消息
    """
    signal_type = signal_data["signal_type"]
    zscore = signal_data["zscore"]
    ratio = signal_data["ratio"]
    mean = signal_data["mean"]
    strength = signal_data["strength"]
    reason = signal_data["reason"]
    prices = signal_data["prices"]
    recommendation = signal_data["recommendation"]
    estimate = signal_data["estimate"]
    threshold = signal_data["threshold"]
    
    # Emoji
    if signal_type == "OPEN":
        emoji = "🟢"
        status = "开仓信号"
    elif signal_type == "CLOSE":
        emoji = "🔴"
        status = "平仓信号"
    else:
        emoji = "⚪️"
        status = "观望"
    
    # 信号强度星级
    stars = "★" * strength + "☆" * (5 - strength)
    
    # 波动率
    volatility = signal_data.get("volatility", "normal")
    volatility_emoji = "正常" if volatility == "normal" else "异常"
    
    msg = f"""{emoji} [{signal_type}] 统计套利{status}

ETH/BTC z-score: {zscore:.2f} ({reason})
比率: {ratio:.6f} (均值: {mean:.6f})
动态阈值: 开仓 ±{threshold['entry']} / 止损 ±{threshold['stop_loss']}
z波动率: {volatility_emoji}

建议操作:"""

    if signal_type == "OPEN":
        msg += f"\n • {recommendation['eth_action']}"
        msg += f"\n • {recommendation['btc_action']}"
    elif signal_type == "CLOSE":
        msg += "\n • 市价平仓全部对冲头寸"
        msg += "\n • ⚠️ 提醒: BTC 和 ETH 两边都要平!"

    msg += f"""

预估 (每腿 ${recommendation['position_size_usd']}):
 预期利润: ${estimate['expected_return']:.2f} ({estimate['return_pct']:.3f}%)
 手续费: ${estimate['fees_taker']:.2f} (taker x4)
 净利润: ${estimate['net_pnl']:.2f}

信号强度: {stars}"""

    return msg


def get_timestamp():
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
