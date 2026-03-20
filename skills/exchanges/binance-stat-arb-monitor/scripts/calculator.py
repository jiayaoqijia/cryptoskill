#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
z-score 计算模块
"""


def calculate_zscore(current, mean, std):
    """
    计算 z-score
    
    Args:
        current: 当前值
        mean: 均值
        std: 标准差
    
    Returns:
        float: z-score
    """
    if std == 0:
        return 0
    return (current - mean) / std


def determine_signal(zscore, entry_threshold, exit_threshold, stop_loss):
    """
    判断交易信号
    
    Args:
        zscore: 当前 z-score
        entry_threshold: 开仓阈值
        exit_threshold: 平仓阈值
        stop_loss: 止损阈值
    
    Returns:
        tuple: (signal_type, direction, reason)
            - signal_type: OPEN / CLOSE / HOLD
            - direction: LONG_ETH_SHORT_BTC / SHORT_ETH_LONG_BTC / CLOSE_ALL
            - reason: 说明
    """
    if zscore is None:
        return "HOLD", "UNKNOWN", "数据不足"
    
    # 开仓条件
    if zscore < -entry_threshold:
        return "OPEN", "LONG_ETH_SHORT_BTC", f"z-score {zscore:.2f} 低于 -{entry_threshold}，ETH 相对低估"
    
    if zscore > entry_threshold:
        return "OPEN", "SHORT_ETH_LONG_BTC", f"z-score {zscore:.2f} 高于 +{entry_threshold}，ETH 相对高估"
    
    # 止盈条件（z-score 回归）
    if -exit_threshold < zscore < exit_threshold:
        return "CLOSE", "CLOSE_ALL", f"z-score {zscore:.2f} 回归至均值，平仓获利"
    
    # 止损条件
    if zscore < -stop_loss:
        return "CLOSE", "CLOSE_ALL", f"z-score {zscore:.2f} 触及止损线"
    
    if zscore > stop_loss:
        return "CLOSE", "CLOSE_ALL", f"z-score {zscore:.2f} 触及止损线"
    
    return "HOLD", "UNKNOWN", f"z-score {zscore:.2f} 在阈值内，观望"


def calculate_expected_pnl(eth_price, btc_price, position_size_usd=1000):
    """
    预估收益（简化计算）
    
    Args:
        eth_price: ETH 价格
        btc_price: BTC 价格
        position_size_usd: 每边仓位大小（USD）
    
    Returns:
        dict: 预估收益信息
    """
    # 手续费估算 (taker fee x4: 开多+开空+平多+平空)
    taker_fee_rate = 0.0004
    total_fee_rate = taker_fee_rate * 4
    
    fees = position_size_usd * total_fee_rate
    
    # 简化假设：z-score 回归到 0 时的预期收益
    # 实际收益取决于价差回归幅度
    expected_return_rate = 0.001  # 0.1%
    
    gross_pnl = position_size_usd * expected_return_rate
    net_pnl = gross_pnl - fees
    
    return {
        "gross_pnl": gross_pnl,
        "fees": fees,
        "net_pnl": net_pnl,
        "return_pct": expected_return_rate * 100
    }
