"""
AI 评分模型 - 综合技术指标判断
"""
from ai_trader.binance_api import get_klines, get_current_price, get_24h_stats
from ai_trader.indicators import ema, rsi, macd, bollinger_bands, atr

def analyze_market(coin, price_to_beat, up_odds, down_odds):
    """
    综合分析市场，返回方向和置信度
    
    返回: (direction, confidence, details)
    """
    symbol = f"{coin}USDT"
    
    # 1. 获取币安数据
    klines_1m = get_klines(symbol, "1m", 30)
    klines_5m = get_klines(symbol, "5m", 10)
    current_price = get_current_price(symbol)
    stats_24h = get_24h_stats(symbol)
    
    if not klines_1m or not current_price or not price_to_beat:
        return None, 0, {"error": "数据不足"}
    
    # 提取价格数据
    closes_1m = [k['close'] for k in klines_1m]
    highs_1m = [k['high'] for k in klines_1m]
    lows_1m = [k['low'] for k in klines_1m]
    volumes_1m = [k['volume'] for k in klines_1m]
    
    # 2. 计算技术指标
    ema9 = ema(closes_1m, 9)
    ema21 = ema(closes_1m, 21)
    rsi_val = rsi(closes_1m, 14)
    macd_val, signal_val, _ = macd(closes_1m)
    upper_bb, middle_bb, lower_bb = bollinger_bands(closes_1m, 20)
    atr_val = atr(highs_1m, lows_1m, closes_1m, 14)
    
    # 3. 综合评分
    score = 0
    details = {}
    
    # 价格位置（权重 40%）
    price_diff = (current_price - price_to_beat) / price_to_beat
    price_diff_pct = price_diff * 100
    details['price_diff_pct'] = round(price_diff_pct, 3)
    
    if abs(price_diff) > 0.001:  # 0.1%
        score += 40 * (1 if price_diff > 0 else -1)
    
    # 趋势指标（权重 25%）
    if ema9 and ema21:
        details['ema9'] = round(ema9, 2)
        details['ema21'] = round(ema21, 2)
        if ema9 > ema21:
            score += 15
        else:
            score -= 15
    
    if macd_val and signal_val:
        details['macd'] = round(macd_val, 2)
        if macd_val > signal_val:
            score += 10
        else:
            score -= 10
    
    # 动量指标（权重 20%）
    if rsi_val:
        details['rsi'] = round(rsi_val, 1)
        if 30 < rsi_val < 70:
            score += 10
        elif rsi_val > 70:
            score -= 5  # 超买
        elif rsi_val < 30:
            score += 5  # 超卖
    
    # 成交量
    avg_volume = sum(volumes_1m[-10:]) / 10
    current_volume = volumes_1m[-1]
    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
    details['volume_ratio'] = round(volume_ratio, 2)
    
    if volume_ratio > 1.5:
        score += 10 if score > 0 else -10
    
    # 市场赔率（权重 15%）
    details['up_odds'] = up_odds
    details['down_odds'] = down_odds
    
    if score > 0 and up_odds < 0.75:
        score += 15
    elif score < 0 and down_odds < 0.75:
        score += 15
    
    # 计算置信度
    confidence = min(abs(score) / 100, 1.0)
    direction = "UP" if score > 0 else "DOWN"
    
    details['score'] = score
    details['current_price'] = current_price
    details['price_to_beat'] = price_to_beat
    
    return direction, confidence, details
