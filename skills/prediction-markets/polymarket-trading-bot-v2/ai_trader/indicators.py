"""
技术指标计算模块（纯 Python 实现）
"""

def ema(prices, period):
    """指数移动平均"""
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema_val = sum(prices[:period]) / period
    for price in prices[period:]:
        ema_val = (price - ema_val) * multiplier + ema_val
    return ema_val

def rsi(prices, period=14):
    """相对强弱指标"""
    if len(prices) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(prices, fast=12, slow=26, signal=9):
    """MACD 指标"""
    if len(prices) < slow:
        return None, None, None
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    if ema_fast is None or ema_slow is None:
        return None, None, None
    macd_line = ema_fast - ema_slow
    # 简化：用最后几个值计算 signal
    return macd_line, 0, macd_line

def bollinger_bands(prices, period=20, std_dev=2):
    """布林带"""
    if len(prices) < period:
        return None, None, None
    sma = sum(prices[-period:]) / period
    variance = sum((p - sma) ** 2 for p in prices[-period:]) / period
    std = variance ** 0.5
    upper = sma + (std_dev * std)
    lower = sma - (std_dev * std)
    return upper, sma, lower

def atr(highs, lows, closes, period=14):
    """平均真实波幅"""
    if len(highs) < period + 1:
        return None
    trs = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
            abs(lows[i] - closes[i-1])
        )
        trs.append(tr)
    return sum(trs[-period:]) / period
