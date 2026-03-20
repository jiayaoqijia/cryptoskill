#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取模块 - Binance API
"""
import requests
import logging
import random
import datetime

logger = logging.getLogger(__name__)


def get_klines(base_url, symbol, interval, limit, timeout=10):
    """
    获取 K 线数据
    
    Args:
        base_url: Binance API 地址
        symbol: 交易对（如 ETHUSDT）
        interval: K线间隔（1h, 4h, 1d）
        limit: 获取数量
        timeout: 超时时间
    
    Returns:
        list: K线数据列表
    """
    url = f"{base_url}/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"获取 K线失败 {symbol}: {e}")
        # 如果是 451 错误（地区限制），使用模拟数据
        if "451" in str(e):
            logger.warning(f"⚠️ 地区限制，使用模拟数据")
            return get_mock_klines(symbol, interval, limit)
        return None


def get_ticker_price(base_url, symbol, timeout=10):
    """
    获取当前价格
    
    Args:
        base_url: Binance API 地址
        symbol: 交易对
        timeout: 超时时间
    
    Returns:
        float: 当前价格
    """
    url = f"{base_url}/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except requests.exceptions.RequestException as e:
        logger.error(f"获取价格失败 {symbol}: {e}")
        # 尝试使用模拟数据
        if "451" in str(e):
            return get_mock_price(symbol)
        return None


def get_mock_klines(symbol, interval, limit):
    """
    生成模拟 K 线数据（用于测试或 API 不可用时）
    """
    import time
    
    # 基础价格
    if "ETH" in symbol:
        base_price = 2050.0
    elif "BTC" in symbol:
        base_price = 70000.0
    else:
        base_price = 1000.0
    
    # 生成模拟数据
    klines = []
    current_time = int(time.time() * 1000) - (limit * 3600 * 1000)
    
    for i in range(limit):
        variation = random.uniform(-0.02, 0.02)
        close = base_price * (1 + variation)
        open_price = close * random.uniform(0.995, 1.005)
        high = max(open_price, close) * random.uniform(1.0, 1.01)
        low = min(open_price, close) * random.uniform(0.99, 1.0)
        volume = random.uniform(1000, 10000)
        
        kline = [
            current_time + (i * 3600 * 1000),
            str(open_price),
            str(high),
            str(low),
            str(close),
            str(volume),
            current_time + (i * 3600 * 1000) + 3599999,
            str(volume * close),
            str(int(random.uniform(100, 1000))),
            str(volume * 0.5),
            str(volume * 0.5 * close),
            "0"
        ]
        klines.append(kline)
    
    return klines


def get_mock_price(symbol):
    """获取模拟价格"""
    if "ETH" in symbol:
        return 2050.0
    elif "BTC" in symbol:
        return 70000.0
    return 1000.0


def get_market_data(config, symbol1, symbol2, lookback_period, interval):
    """
    获取市场数据并计算比率
    
    Args:
        config: Binance 配置
        symbol1: 分子交易对（ETHUSDT）
        symbol2: 分母交易对（BTCUSDT）
        lookback_period: 回看周期
        interval: K线间隔
    
    Returns:
        dict: 包含价格、比率、z-score 等
    """
    base_url = config.get("base_url", "https://fapi.binance.com")
    timeout = config.get("timeout", 10)
    
    # 获取历史 K 线
    klines1 = get_klines(base_url, symbol1, interval, lookback_period, timeout)
    klines2 = get_klines(base_url, symbol2, interval, lookback_period, timeout)
    
    if not klines1 or not klines2:
        raise Exception("无法获取 K 线数据")
    
    # 提取收盘价
    closes1 = [float(k[4]) for k in klines1]  # 收盘价
    closes2 = [float(k[4]) for k in klines2]
    
    # 计算比率序列
    ratios = [c1 / c2 for c1, c2 in zip(closes1, closes2)]
    
    # 获取当前价格（最新收盘价）
    current_price1 = closes1[-1]
    current_price2 = closes2[-1]
    current_ratio = ratios[-1]
    
    # 计算统计值
    import statistics
    
    mean = statistics.mean(ratios)
    std = statistics.stdev(ratios) if len(ratios) > 1 else 0
    
    # 计算 z-score
    if std > 0:
        zscore = (current_ratio - mean) / std
    else:
        zscore = 0
    
    return {
        "prices": {
            "eth": current_price1,
            "btc": current_price2
        },
        "ratios": ratios,
        "current_ratio": current_ratio,
        "mean": mean,
        "std": std,
        "zscore": zscore,
        "timestamp": datetime.datetime.now().isoformat()
    }


# 导入 datetime 以支持时间戳
import datetime
