"""
AI 评分模型 v2 - 针对 5 分钟 Price to Beat 预测优化

核心逻辑：
  PTB = 市场开始时 Chainlink 快照价格
  结束时价格 >= PTB → UP 赢
  结束时价格 <  PTB → DOWN 赢
  
  我们在结束前约 40 秒做决策
  关键：预测的不是"BTC会涨还是跌"，而是"5分钟结束时价格相对PTB的位置"

策略原则：
  1. 当前价格 vs PTB 的差距是最强信号（已经领先/落后多少）
  2. 短期动量（最近 1-2 分钟趋势）决定剩余 40 秒的走向
  3. 波动率决定翻盘概率
  4. 赔率决定是否有下注价值（期望值 > 0）
"""
from ai_trader.binance_api import get_klines, get_current_price
from ai_trader.indicators import ema, rsi, atr


def analyze_market(coin, price_to_beat, up_odds, down_odds):
    """
    v2 分析：专门针对 5 分钟 PTB 预测

    返回: (direction, confidence, details)
    """
    symbol = f"{coin}USDT"

    # ── 数据采集 ──
    klines_1m = get_klines(symbol, "1m", 15)  # 最近 15 根 1 分钟 K 线
    current_price = get_current_price(symbol)

    if not klines_1m or not current_price or not price_to_beat:
        return None, 0, {"error": "数据不足"}

    closes = [k["close"] for k in klines_1m]
    highs  = [k["high"]  for k in klines_1m]
    lows   = [k["low"]   for k in klines_1m]
    volumes = [k["volume"] for k in klines_1m]

    details = {
        "current_price": current_price,
        "price_to_beat": price_to_beat,
    }

    # ═══════════════════════════════════════
    # 信号 1：价格位置（核心信号，权重 50）
    # ═══════════════════════════════════════
    # 当前价 vs PTB 的偏离度
    price_diff = current_price - price_to_beat
    price_diff_pct = (price_diff / price_to_beat) * 100
    details["price_diff"] = round(price_diff, 2)
    details["price_diff_pct"] = round(price_diff_pct, 4)

    # 用 ATR 归一化偏离度（相对波动率的倍数）
    atr_val = atr(highs, lows, closes, min(14, len(highs) - 1))
    if atr_val and atr_val > 0:
        diff_in_atr = abs(price_diff) / atr_val  # 偏离了几倍 ATR
        details["diff_in_atr"] = round(diff_in_atr, 2)
    else:
        diff_in_atr = 0
        atr_val = abs(current_price * 0.001)  # fallback

    # 偏离越大，翻盘越难，置信度越高
    # 注意：只剩 40 秒，1 分钟 ATR 的偏离已经非常难翻盘
    if diff_in_atr > 3.0:
        position_score = 60  # 几乎不可能翻盘
    elif diff_in_atr > 2.0:
        position_score = 55
    elif diff_in_atr > 1.5:
        position_score = 50
    elif diff_in_atr > 1.0:
        position_score = 45  # 1 ATR 偏离，40 秒内翻盘概率很低
    elif diff_in_atr > 0.5:
        position_score = 35
    elif diff_in_atr > 0.3:
        position_score = 25
    elif diff_in_atr > 0.15:
        position_score = 15
    else:
        position_score = 3  # 几乎平盘，不值得赌

    # 方向
    position_direction = 1 if price_diff > 0 else -1
    details["position_score"] = position_score
    details["position_dir"] = "UP" if position_direction > 0 else "DOWN"

    # ═══════════════════════════════════════
    # 信号 2：短期动量（权重 30）
    # ═══════════════════════════════════════
    # 最近 3 根 K 线的趋势（3 分钟内的动量）
    momentum_score = 0

    if len(closes) >= 4:
        # 近 3 分钟的价格变化
        recent_change = closes[-1] - closes[-4]
        recent_pct = (recent_change / closes[-4]) * 100
        details["recent_3m_pct"] = round(recent_pct, 4)

        # 短 EMA 斜率
        ema3 = ema(closes[-5:], 3) if len(closes) >= 5 else None
        ema3_prev = ema(closes[-6:-1], 3) if len(closes) >= 6 else None

        if ema3 and ema3_prev:
            ema_slope = (ema3 - ema3_prev) / ema3_prev * 100
            details["ema3_slope_pct"] = round(ema_slope, 4)
        else:
            ema_slope = recent_pct

        # 最近 1 分钟的微观动量
        micro_change = closes[-1] - closes[-2]
        micro_pct = (micro_change / closes[-2]) * 100
        details["micro_1m_pct"] = round(micro_pct, 4)

        # 动量方向和强度
        momentum_direction = 1 if recent_change > 0 else -1
        micro_direction = 1 if micro_change > 0 else -1

        # 综合动量：3 分钟趋势 + 最近 1 分钟加权
        if momentum_direction == micro_direction:
            # 动量一致，信号强
            momentum_score = 25
        else:
            # 动量分歧（可能反转），信号弱
            momentum_score = 10
            momentum_direction = micro_direction  # 以最近方向为准

        details["momentum_dir"] = "UP" if momentum_direction > 0 else "DOWN"
    else:
        momentum_direction = position_direction
        momentum_score = 5

    details["momentum_score"] = momentum_score

    # ═══════════════════════════════════════
    # 信号 3：RSI 极端值（权重 10）
    # ═══════════════════════════════════════
    rsi_val = rsi(closes, min(14, len(closes) - 1))
    rsi_score = 0
    rsi_direction = 0

    if rsi_val is not None:
        details["rsi"] = round(rsi_val, 1)
        if rsi_val > 75:
            # 严重超买 → 可能回调
            rsi_score = 10
            rsi_direction = -1
            details["rsi_signal"] = "overbought"
        elif rsi_val < 25:
            # 严重超卖 → 可能反弹
            rsi_score = 10
            rsi_direction = 1
            details["rsi_signal"] = "oversold"
        elif rsi_val > 65:
            rsi_score = 5
            rsi_direction = -1
            details["rsi_signal"] = "slightly_overbought"
        elif rsi_val < 35:
            rsi_score = 5
            rsi_direction = 1
            details["rsi_signal"] = "slightly_oversold"
        else:
            details["rsi_signal"] = "neutral"

    details["rsi_score"] = rsi_score

    # ═══════════════════════════════════════
    # 信号 4：成交量异常（权重 10）
    # ═══════════════════════════════════════
    vol_score = 0
    if len(volumes) >= 5:
        avg_vol = sum(volumes[-5:]) / 5
        curr_vol = volumes[-1]
        vol_ratio = curr_vol / avg_vol if avg_vol > 0 else 1
        details["vol_ratio"] = round(vol_ratio, 2)

        if vol_ratio > 2.0:
            # 放量 → 趋势可能延续
            vol_score = 10
            details["vol_signal"] = "high_volume"
        elif vol_ratio > 1.5:
            vol_score = 5
            details["vol_signal"] = "above_avg"
        else:
            details["vol_signal"] = "normal"

    details["vol_score"] = vol_score

    # ═══════════════════════════════════════
    # 综合决策
    # ═══════════════════════════════════════
    # 核心逻辑：
    # - 价格位置 + 动量方向一致 → 强信号
    # - 价格位置 + 动量方向矛盾 → 弱信号 / 不下注
    # - RSI 极端 + 动量可能修正位置判断

    # 判定最终方向
    if position_score >= 30:
        # 位置信号强，以位置为主
        final_direction = position_direction
        if momentum_direction == position_direction:
            # 动量确认，加分
            total_score = position_score + momentum_score + vol_score
        else:
            # 动量反向，但位置优势大
            total_score = position_score - momentum_score * 0.5 + vol_score * 0.3
    elif position_score >= 10:
        # 位置信号中等
        if momentum_direction == position_direction:
            final_direction = position_direction
            total_score = position_score + momentum_score + vol_score
        else:
            # 信号矛盾，极不确定
            final_direction = momentum_direction
            total_score = max(momentum_score - position_score, 5)
    else:
        # 几乎平盘，完全看动量
        final_direction = momentum_direction
        total_score = momentum_score + vol_score

    # RSI 修正：在边界情况下 RSI 可以翻转方向
    if rsi_score > 0 and rsi_direction != 0:
        if rsi_direction != final_direction and total_score < 40:
            total_score -= rsi_score  # RSI 与方向矛盾，减分
        elif rsi_direction == final_direction:
            total_score += rsi_score  # RSI 确认，加分

    # 计算置信度
    confidence = min(max(total_score / 80, 0), 1.0)  # 归一化到 0-1
    direction = "UP" if final_direction > 0 else "DOWN"

    details["total_score"] = round(total_score, 1)
    details["direction"] = direction
    details["confidence"] = round(confidence, 3)

    # ═══════════════════════════════════════
    # 赔率价值分析（不影响方向，影响是否下注）
    # ═══════════════════════════════════════
    target_odds = up_odds if direction == "UP" else down_odds
    # 期望值 = confidence * (1/odds - 1) - (1 - confidence)
    if target_odds > 0:
        payout = 1 / target_odds  # 赔率倍数
        ev = confidence * (payout - 1) - (1 - confidence)
        details["target_odds"] = target_odds
        details["expected_value"] = round(ev, 3)
        details["ev_positive"] = ev > 0
    else:
        details["expected_value"] = 0
        details["ev_positive"] = False

    return direction, confidence, details
