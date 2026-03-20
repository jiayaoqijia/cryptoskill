#!/usr/bin/env python3
"""
binance_signal_engine - Multi-Timeframe Technical Analysis Signal Generator

Architecture
────────────
  1D  (high)  → Trend regime   (EMA structure, ADX)
  4H  (mid)   → Momentum       (MACD, Stochastic)
  15m (low)   → Entry trigger   (RSI reclaim, BB re-entry, volume)

Outputs a JSON report with: signal, trade plan, position size,
and an optional flat record suitable for backtest ingestion.
"""

import ccxt
import pandas as pd
import numpy as np
import ta
import sys
import json
import time
import logging
import argparse
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────────────────────
class Regime(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class Bias(str, Enum):
    STRONG_BULLISH = "STRONG BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    STRONG_BEARISH = "STRONG BEARISH"

class PlanStatus(str, Enum):
    READY = "ready"
    WAITING = "waiting"
    NONE = "none"
    REJECT = "reject"
    INVALID = "invalid"

class Side(str, Enum):
    LONG = "long"
    SHORT = "short"


# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────
@dataclass
class Config:
    exchange_id: str = "binance"
    market_type: str = "spot"  # "spot" | "futures"

    timeframes: Dict[str, str] = field(default_factory=lambda: {"high": "1d", "mid": "4h", "low": "15m"})
    limits: Dict[str, int] = field(default_factory=lambda: {"high": 200, "mid": 200, "low": 200})

    ema_fast: int = 9
    ema_slow: int = 21
    ema_trend: int = 50
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    adx_period: int = 14
    adx_trend_threshold: float = 25.0
    rsi_period: int = 14
    rsi_oversold: float = 35.0
    rsi_overbought: float = 65.0
    stoch_window: int = 14
    stoch_smooth: int = 3
    stoch_oversold: float = 20.0
    stoch_overbought: float = 80.0
    bb_window: int = 20
    bb_std: float = 2.0
    atr_period: int = 14
    volume_ma_period: int = 20
    volume_spike_threshold: float = 1.5

    sr_lookback: int = 20
    sr_entry_buffer_atr: float = 0.10
    sr_stop_buffer_atr: float = 0.25
    sr_target_buffer_atr: float = 0.10
    max_entry_distance_atr: float = 1.0

    weak_signal_threshold: float = 10.0
    strong_signal_threshold: float = 30.0

    weight_trend_ema_position: float = 15.0
    weight_trend_ema_cross: float = 10.0
    weight_trend_adx: float = 10.0
    weight_momentum_macd_cross: float = 10.0
    weight_momentum_macd_hist: float = 5.0
    weight_momentum_stoch_primary: float = 8.0
    weight_momentum_stoch_secondary: float = 4.0
    weight_trigger_rsi: float = 15.0
    weight_trigger_bb: float = 10.0
    weight_trigger_volume: float = 5.0

    atr_sl_multiplier: float = 1.5
    risk_reward_ratio: float = 2.0
    min_acceptable_rr: float = 1.2
    slippage_buffer_pct: float = 0.05  

    account_balance: float = 10_000.0
    account_risk_pct: float = 1.0
    max_position_notional_pct: float = 100.0
    leverage: float = 1.0
    cooldown_bars: int = 4  

    @property
    def is_futures(self) -> bool:
        return self.market_type.lower() in {"future", "futures"}

    @classmethod
    def from_json(cls, path: str) -> "Config":
        with open(path) as f:
            data = json.load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ──────────────────────────────────────────────────────────────
# Utility helpers
# ──────────────────────────────────────────────────────────────
def safe_float(value: Any) -> Optional[float]:
    if value is None: return None
    try:
        if pd.isna(value): return None
        return float(value)
    except (TypeError, ValueError):
        return None

def sanitize_for_json(obj: Any) -> Any:
    if isinstance(obj, dict): return {k: sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)): return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, pd.Timestamp): return obj.isoformat()
    if isinstance(obj, np.integer): return int(obj)
    if isinstance(obj, np.floating):
        v = float(obj)
        return None if np.isnan(v) else v
    if isinstance(obj, Enum): return obj.value
    if obj is None: return None
    try:
        if pd.isna(obj): return None
    except (TypeError, ValueError): pass
    if isinstance(obj, (str, int, float, bool)): return obj
    return str(obj)


# ──────────────────────────────────────────────────────────────
# Exchange Wrapper
# ──────────────────────────────────────────────────────────────
class ExchangeClient:
    def __init__(self, cfg: Config, max_retries: int = 3):
        exchange_kwargs: Dict[str, Any] = {"enableRateLimit": True}
        if cfg.exchange_id == "binance":
            default_type = "future" if cfg.is_futures else "spot"
            exchange_kwargs["options"] = {"defaultType": default_type}

        self.exchange: ccxt.Exchange = getattr(ccxt, cfg.exchange_id)(exchange_kwargs)
        self.exchange.load_markets()
        self.max_retries = max_retries
        self.cfg = cfg

    def _drop_open_candle(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        if df.empty: return df
        try:
            tf_seconds = self.exchange.parse_timeframe(timeframe)
        except Exception: return df
        now = pd.Timestamp.now(tz="UTC")
        candle_close_time = df.index[-1] + pd.Timedelta(seconds=tf_seconds)
        if candle_close_time > now:
            return df.iloc[:-1].copy()
        return df

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        numeric_cols = ["open", "high", "low", "close", "volume"]
        for attempt in range(1, self.max_retries + 1):
            try:
                raw = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                if not raw: raise ValueError(f"Empty OHLCV for {symbol} {timeframe}")
                df = pd.DataFrame(raw, columns=["timestamp"] + numeric_cols)
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
                for col in numeric_cols: df[col] = pd.to_numeric(df[col], errors="coerce")
                df.dropna(subset=numeric_cols, inplace=True)
                df.set_index("timestamp", inplace=True)
                df = df[~df.index.duplicated(keep="last")].sort_index()
                df = self._drop_open_candle(df, timeframe)
                if len(df) < 3: raise ValueError(f"Not enough closed candles for {symbol} {timeframe}")
                return df
            except ccxt.NetworkError as exc:
                logger.warning("Network error (attempt %d/%d): %s", attempt, self.max_retries, exc)
                time.sleep(2 ** attempt)
            except ccxt.ExchangeError as exc:
                logger.error("Exchange error: %s", exc)
                raise
        raise ConnectionError(f"Failed to fetch {symbol} {timeframe} after {self.max_retries} retries")

    def format_price(self, symbol: str, value: Optional[float]) -> Optional[float]:
        if value is None: return None
        try: return float(self.exchange.price_to_precision(symbol, float(value)))
        except Exception: return round(float(value), 8)

    def apply_lot_size(self, symbol: str, units: float) -> float:
        try:
            market = self.exchange.market(symbol)
            step = market.get("precision", {}).get("amount")
            if step is not None: return float(self.exchange.amount_to_precision(symbol, units))
        except Exception: pass
        return units

    def get_min_notional(self, symbol: str) -> Optional[float]:
        try:
            market = self.exchange.market(symbol)
            return market.get("limits", {}).get("cost", {}).get("min")
        except Exception: return None


# ──────────────────────────────────────────────────────────────
# Indicator Calculations
# ──────────────────────────────────────────────────────────────
class Indicators:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def enrich(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = self._add_trend(df)
        df = self._add_momentum(df)
        df = self._add_volatility(df)
        df = self._add_volume(df)
        df = self._add_support_resistance(df)
        
        df.dropna(inplace=True)
        return df

    def _add_trend(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        df["ema_fast"] = ta.trend.EMAIndicator(df["close"], window=c.ema_fast).ema_indicator()
        df["ema_slow"] = ta.trend.EMAIndicator(df["close"], window=c.ema_slow).ema_indicator()
        df["ema_trend"] = ta.trend.EMAIndicator(df["close"], window=c.ema_trend).ema_indicator()

        macd = ta.trend.MACD(df["close"], window_fast=c.macd_fast, window_slow=c.macd_slow, window_sign=c.macd_signal)
        df["macd"] = macd.macd()
        df["macd_signal"] = macd.macd_signal()
        df["macd_hist"] = macd.macd_diff()

        adx = ta.trend.ADXIndicator(df["high"], df["low"], df["close"], window=c.adx_period)
        df["adx"] = adx.adx()
        df["di_plus"] = adx.adx_pos()
        df["di_minus"] = adx.adx_neg()
        return df

    def _add_momentum(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=c.rsi_period).rsi()
        stoch = ta.momentum.StochasticOscillator(df["high"], df["low"], df["close"], window=c.stoch_window, smooth_window=c.stoch_smooth)
        df["stoch_k"] = stoch.stoch()
        df["stoch_d"] = stoch.stoch_signal()
        return df

    def _add_volatility(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        bb = ta.volatility.BollingerBands(df["close"], window=c.bb_window, window_dev=c.bb_std)
        df["bb_upper"] = bb.bollinger_hband()
        df["bb_lower"] = bb.bollinger_lband()
        df["bb_mid"] = bb.bollinger_mavg()
        df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / df["bb_mid"].replace(0, np.nan)

        atr_ind = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"], window=c.atr_period)
        df["atr"] = atr_ind.average_true_range()
        return df

    def _add_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        df["vol_ma"] = df["volume"].shift(1).rolling(window=c.volume_ma_period).mean()
        df["vol_ratio"] = df["volume"] / df["vol_ma"].replace(0, np.nan)
        return df

    def _add_support_resistance(self, df: pd.DataFrame) -> pd.DataFrame:
        c = self.cfg
        df["sr_support"] = df["low"].shift(1).rolling(window=c.sr_lookback, min_periods=c.sr_lookback).min()
        df["sr_resistance"] = df["high"].shift(1).rolling(window=c.sr_lookback, min_periods=c.sr_lookback).max()
        df["dist_to_support_atr"] = (df["close"] - df["sr_support"]) / df["atr"].replace(0, np.nan)
        df["dist_to_resistance_atr"] = (df["sr_resistance"] - df["close"]) / df["atr"].replace(0, np.nan)
        return df


# ──────────────────────────────────────────────────────────────
# Divergence Detector
# ──────────────────────────────────────────────────────────────
class DivergenceDetector:
    def __init__(self, lookback: int = 20):
        self.lookback = lookback

    def detect(self, df: pd.DataFrame) -> Tuple[Optional[str], str]:
        if len(df) < self.lookback:
            return None, "Insufficient data for divergence check"
        
        window = df.iloc[-self.lookback:]
        close = window["close"]
        rsi = window["rsi"]
        
        if rsi.isna().sum() > self.lookback // 2: 
            return None, "Too many NaN RSI values"

        current_close = close.iloc[-1]
        current_rsi = rsi.iloc[-1]

        # Check Bullish Divergence
        price_low_idx = close.idxmin()
        price_at_low = close.loc[price_low_idx]
        rsi_at_low = rsi.loc[price_low_idx]

        if price_low_idx != close.index[-1] and current_close < price_at_low and current_rsi > rsi_at_low:
            return "bullish", f"Bullish RSI divergence: price {current_close:.2f} vs {price_at_low:.2f}, RSI {current_rsi:.1f} vs {rsi_at_low:.1f}"

        # Check Bearish Divergence (FIXED UNBOUND ERROR HERE)
        price_high_idx = close.idxmax()
        price_at_high = close.loc[price_high_idx]
        rsi_at_high = rsi.loc[price_high_idx]

        if price_high_idx != close.index[-1] and current_close > price_at_high and current_rsi < rsi_at_high:
            return "bearish", f"Bearish RSI divergence: price {current_close:.2f} vs {price_at_high:.2f}, RSI {current_rsi:.1f} vs {rsi_at_high:.1f}"

        return None, "No divergence detected"


# ──────────────────────────────────────────────────────────────
# Signal Scoring Engine
# ──────────────────────────────────────────────────────────────
class SignalEngine:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.divergence = DivergenceDetector()

    def _regime(self, score: float) -> Regime:
        if score >= self.cfg.weak_signal_threshold: return Regime.BULLISH
        if score <= -self.cfg.weak_signal_threshold: return Regime.BEARISH
        return Regime.NEUTRAL

    def score_trend(self, df_high: pd.DataFrame) -> Tuple[float, List[str]]:
        c, row, score, reasons = self.cfg, df_high.iloc[-1], 0.0, []
        if row["close"] > row["ema_trend"]: score += c.weight_trend_ema_position; reasons.append("Price > EMA50 (1D)")
        else: score -= c.weight_trend_ema_position; reasons.append("Price < EMA50 (1D)")

        if row["ema_fast"] > row["ema_slow"]: score += c.weight_trend_ema_cross; reasons.append("EMA9 > EMA21 (1D)")
        else: score -= c.weight_trend_ema_cross; reasons.append("EMA9 < EMA21 (1D)")

        adx_val = row["adx"]
        if adx_val > c.adx_trend_threshold:
            if row["di_plus"] > row["di_minus"]: score += c.weight_trend_adx; reasons.append(f"ADX={adx_val:.1f} strong bullish trend")
            elif row["di_plus"] < row["di_minus"]: score -= c.weight_trend_adx; reasons.append(f"ADX={adx_val:.1f} strong bearish trend")
            else: reasons.append(f"ADX={adx_val:.1f} strong but DI mixed")
        else: reasons.append(f"ADX={adx_val:.1f} weak / ranging")
        return score, reasons

    def score_momentum(self, df_mid: pd.DataFrame, regime: Regime) -> Tuple[float, List[str]]:
        c, row, prev, score, reasons = self.cfg, df_mid.iloc[-1], df_mid.iloc[-2], 0.0, []
        if row["macd"] > row["macd_signal"]: score += c.weight_momentum_macd_cross; reasons.append("MACD > Signal (4H)")
        else: score -= c.weight_momentum_macd_cross; reasons.append("MACD < Signal (4H)")

        if row["macd_hist"] > prev["macd_hist"]: score += c.weight_momentum_macd_hist; reasons.append("MACD histogram rising (4H)")
        else: score -= c.weight_momentum_macd_hist; reasons.append("MACD histogram falling (4H)")

        bull_cross = prev["stoch_k"] <= prev["stoch_d"] and row["stoch_k"] > row["stoch_d"]
        bear_cross = prev["stoch_k"] >= prev["stoch_d"] and row["stoch_k"] < row["stoch_d"]

        if regime == Regime.BULLISH:
            if bull_cross and row["stoch_k"] < 30: score += c.weight_momentum_stoch_primary; reasons.append(f"Stoch bullish cross from pullback (%K={row['stoch_k']:.1f})")
            elif bear_cross and row["stoch_k"] > c.stoch_overbought: score -= c.weight_momentum_stoch_secondary; reasons.append(f"Stoch bearish cross from OB (%K={row['stoch_k']:.1f})")
        elif regime == Regime.BEARISH:
            if bear_cross and row["stoch_k"] > 70: score -= c.weight_momentum_stoch_primary; reasons.append(f"Stoch bearish cross from rally (%K={row['stoch_k']:.1f})")
            elif bull_cross and row["stoch_k"] < c.stoch_oversold: score += c.weight_momentum_stoch_secondary; reasons.append(f"Stoch bullish bounce from OS (%K={row['stoch_k']:.1f})")
        else:
            if bull_cross and row["stoch_k"] < c.stoch_oversold: score += c.weight_momentum_stoch_primary; reasons.append(f"Stoch bullish cross from OS")
            elif bear_cross and row["stoch_k"] > c.stoch_overbought: score -= c.weight_momentum_stoch_primary; reasons.append(f"Stoch bearish cross from OB")
        return score, reasons

    def score_trigger(self, df_low: pd.DataFrame, regime: Regime) -> Tuple[float, List[str]]:
        c, row, prev, score, reasons = self.cfg, df_low.iloc[-1], df_low.iloc[-2], 0.0, []
        bullish_rsi_reclaim, bearish_rsi_reject = prev["rsi"] < c.rsi_oversold <= row["rsi"], prev["rsi"] > c.rsi_overbought >= row["rsi"]
        bullish_bb_reentry, bearish_bb_reentry = prev["close"] < prev["bb_lower"] and row["close"] >= row["bb_lower"], prev["close"] > prev["bb_upper"] and row["close"] <= row["bb_upper"]

        if regime == Regime.BULLISH:
            if bullish_rsi_reclaim: score += c.weight_trigger_rsi; reasons.append(f"RSI reclaimed above oversold ({row['rsi']:.1f})")
            elif row["rsi"] < c.rsi_oversold: reasons.append(f"RSI still oversold ({row['rsi']:.1f}) — waiting for reclaim")
            if bullish_bb_reentry: score += c.weight_trigger_bb; reasons.append("Price re-entered above lower BB")
        elif regime == Regime.BEARISH:
            if bearish_rsi_reject: score -= c.weight_trigger_rsi; reasons.append(f"RSI rolled below overbought ({row['rsi']:.1f})")
            elif row["rsi"] > c.rsi_overbought: reasons.append(f"RSI still overbought ({row['rsi']:.1f}) — waiting")
            if bearish_bb_reentry: score -= c.weight_trigger_bb; reasons.append("Price re-entered below upper BB")
        else:
            if bullish_rsi_reclaim: score += c.weight_trigger_rsi
            elif bearish_rsi_reject: score -= c.weight_trigger_rsi
            if bullish_bb_reentry: score += c.weight_trigger_bb
            elif bearish_bb_reentry: score -= c.weight_trigger_bb

        if row["vol_ratio"] > c.volume_spike_threshold:
            if row["close"] > row["open"]: score += c.weight_trigger_volume; reasons.append(f"Bullish volume spike ({row['vol_ratio']:.2f}x)")
            elif row["close"] < row["open"]: score -= c.weight_trigger_volume; reasons.append(f"Bearish volume spike ({row['vol_ratio']:.2f}x)")
            
        div_type, div_desc = self.divergence.detect(df_low)
        if div_type == "bullish": score += 5; reasons.append(div_desc)
        elif div_type == "bearish": score -= 5; reasons.append(div_desc)

        return score, reasons

    def evaluate(self, df_high: pd.DataFrame, df_mid: pd.DataFrame, df_low: pd.DataFrame) -> Dict[str, Any]:
        c = self.cfg
        trend_score, trend_reasons = self.score_trend(df_high)
        regime = self._regime(trend_score)
        momentum_score, momentum_reasons = self.score_momentum(df_mid, regime)
        trigger_score, trigger_reasons = self.score_trigger(df_low, regime)
        total, reasons = trend_score + momentum_score + trigger_score, trend_reasons + momentum_reasons + trigger_reasons

        if total >= c.strong_signal_threshold: bias, action, entry_ready = Bias.STRONG_BULLISH, "BUY", True
        elif total >= c.weak_signal_threshold: bias, action, entry_ready = Bias.BULLISH, "WATCH LONG", False
        elif total <= -c.strong_signal_threshold:
            bias = Bias.STRONG_BEARISH
            action, entry_ready = ("SELL (SHORT)", True) if c.is_futures else ("SELL / EXIT", False)
        elif total <= -c.weak_signal_threshold:
            bias = Bias.BEARISH
            action, entry_ready = ("WATCH SHORT" if c.is_futures else "WATCH / EXIT BIAS"), False
        else: bias, action, entry_ready = Bias.NEUTRAL, "WAIT", False

        return {
            "score": round(total, 1), "trend_score": round(trend_score, 1),
            "momentum_score": round(momentum_score, 1), "trigger_score": round(trigger_score, 1),
            "bias": bias.value, "action": action, "entry_ready": entry_ready,
            "regime": regime.value, "reasons": reasons,
        }


# ──────────────────────────────────────────────────────────────
# Trade Planner
# ──────────────────────────────────────────────────────────────
class TradePlanner:
    def __init__(self, cfg: Config): self.cfg = cfg

    @staticmethod
    def _empty_plan(**kwargs) -> Dict[str, Any]:
        base = {"side": None, "entry_type": None, "entry_ready": False, "tradeable": False, "plan_status": "none", "entry": None, "current_price": None, "support": None, "resistance": None, "stop_loss": None, "take_profit": None, "target_rr": None, "target_sr": None, "effective_risk_reward": None, "notes": []}
        base.update(kwargs)
        return base

    def _infer_side(self, signal: Dict[str, Any]) -> Optional[str]:
        bias = signal.get("bias", "")
        if bias in [Bias.STRONG_BULLISH.value, Bias.BULLISH.value]: return "long"
        if bias in [Bias.STRONG_BEARISH.value, Bias.BEARISH.value] and self.cfg.is_futures: return "short"
        return None

    def plan(self, df_low: pd.DataFrame, signal: Dict[str, Any]) -> Dict[str, Any]:
        c, row = self.cfg, df_low.iloc[-1]
        price, atr, support, resistance = safe_float(row["close"]), safe_float(row["atr"]), safe_float(row.get("sr_support")), safe_float(row.get("sr_resistance"))

        if price is None or atr is None or atr <= 0:
            return self._empty_plan(price=price, support=support, resistance=resistance, status="invalid", notes=["Invalid price or ATR"])

        side = self._infer_side(signal)
        if side is None:
            return self._empty_plan(price=price, support=support, resistance=resistance, notes=["No actionable side / Spot restrictions applied"])

        slippage = price * (c.slippage_buffer_pct / 100.0)
        
        if side == "long": return self._plan_long(price, atr, support, resistance, signal, slippage, c)
        return self._plan_short(price, atr, support, resistance, signal, slippage, c)

    def _plan_long(self, price, atr, support, resistance, signal, slippage, c):
        notes, entry_buffer, stop_buffer, target_buffer = [], c.sr_entry_buffer_atr * atr, c.sr_stop_buffer_atr * atr, c.sr_target_buffer_atr * atr
        if support is not None:
            planned_entry, near_support = support + entry_buffer, 0 <= (price - support) <= (c.max_entry_distance_atr * atr)
        else:
            planned_entry, near_support, notes = price, True, ["Support unavailable — using current price + ATR fallback"]

        entry_ready = bool(signal.get("entry_ready", False) and near_support)
        entry = (price + slippage) if entry_ready else planned_entry
        stop_from_atr, stop_from_sr = entry - (c.atr_sl_multiplier * atr), (support - stop_buffer) if support is not None else None
        stop_loss = min(stop_from_atr, stop_from_sr) if stop_from_sr is not None else stop_from_atr

        risk_per_unit = entry - stop_loss
        if risk_per_unit <= 0: return self._empty_plan(side="long", price=price, status="invalid", notes=notes + ["Non-positive risk distance (long)"])

        target_rr = entry + (risk_per_unit * c.risk_reward_ratio)
        target_sr = (resistance - target_buffer) if resistance is not None and resistance > entry else None
        take_profit = target_sr if target_sr is not None else target_rr
        return self._finalise("long", entry_ready, entry, price, support, resistance, stop_loss, take_profit, target_rr, target_sr, (take_profit - entry) / risk_per_unit, notes)

    def _plan_short(self, price, atr, support, resistance, signal, slippage, c):
        notes, entry_buffer, stop_buffer, target_buffer = [], c.sr_entry_buffer_atr * atr, c.sr_stop_buffer_atr * atr, c.sr_target_buffer_atr * atr
        if resistance is not None:
            planned_entry, near_resistance = resistance - entry_buffer, 0 <= (resistance - price) <= (c.max_entry_distance_atr * atr)
        else:
            planned_entry, near_resistance, notes = price, True, ["Resistance unavailable — using current price + ATR fallback"]

        entry_ready = bool(signal.get("entry_ready", False) and near_resistance)
        entry = (price - slippage) if entry_ready else planned_entry
        stop_from_atr, stop_from_sr = entry + (c.atr_sl_multiplier * atr), (resistance + stop_buffer) if resistance is not None else None
        stop_loss = max(stop_from_atr, stop_from_sr) if stop_from_sr is not None else stop_from_atr

        risk_per_unit = stop_loss - entry
        if risk_per_unit <= 0: return self._empty_plan(side="short", price=price, status="invalid", notes=notes + ["Non-positive risk distance (short)"])

        target_rr = entry - (risk_per_unit * c.risk_reward_ratio)
        target_sr = (support + target_buffer) if support is not None and support < entry else None
        take_profit = target_sr if target_sr is not None else target_rr
        return self._finalise("short", entry_ready, entry, price, support, resistance, stop_loss, take_profit, target_rr, target_sr, (entry - take_profit) / risk_per_unit, notes)

    def _finalise(self, side, entry_ready, entry, price, support, resistance, stop_loss, take_profit, target_rr, target_sr, effective_rr, notes):
        tradeable = effective_rr is not None and effective_rr >= self.cfg.min_acceptable_rr
        if not tradeable: notes.append(f"Rejected: effective RR < min {self.cfg.min_acceptable_rr:.2f}")
        return {
            "side": side, "entry_type": "market" if entry_ready else "limit", "entry_ready": entry_ready,
            "tradeable": tradeable, "plan_status": PlanStatus.READY.value if (tradeable and entry_ready) else PlanStatus.WAITING.value if tradeable else PlanStatus.REJECT.value,
            "entry": entry, "current_price": price, "support": support, "resistance": resistance,
            "stop_loss": stop_loss, "take_profit": take_profit, "target_rr": target_rr,
            "target_sr": target_sr, "effective_risk_reward": round(effective_rr, 2) if effective_rr is not None else None, "notes": notes,
        }


# ──────────────────────────────────────────────────────────────
# Position Sizer
# ──────────────────────────────────────────────────────────────
class PositionSizer:
    def __init__(self, cfg: Config, exchange: Optional[ExchangeClient] = None):
        self.cfg, self.exchange = cfg, exchange

    def size(self, plan: Dict[str, Any], symbol: Optional[str] = None) -> Dict[str, Any]:
        c = self.cfg
        if not plan.get("tradeable", False): return {"units": None, "notional": None, "risk_budget": None, "actual_risk": None, "potential_reward": None, "position_pct_of_account": None, "capped_by_notional_limit": None}

        entry, stop_loss, take_profit = safe_float(plan.get("entry")), safe_float(plan.get("stop_loss")), safe_float(plan.get("take_profit"))
        if None in (entry, stop_loss, take_profit) or (stop_distance := abs(entry - stop_loss)) <= 0: return {"units": None, "notional": None, "risk_budget": None, "actual_risk": None, "potential_reward": None, "position_pct_of_account": None, "capped_by_notional_limit": None}

        risk_budget = c.account_balance * (c.account_risk_pct / 100.0)
        units = min(risk_budget / stop_distance, (c.account_balance * (c.max_position_notional_pct / 100.0) * c.leverage) / entry if entry > 0 else 0.0)
        
        if self.exchange and symbol: units = self.exchange.apply_lot_size(symbol, units)
        notional = units * entry
        
        if self.exchange and symbol and (min_not := self.exchange.get_min_notional(symbol)) and notional < min_not:
            logger.warning("Position notional %.2f below exchange minimum %.2f for %s", notional, min_not, symbol)

        return {
            "units": round(units, 8), "notional": round(notional, 2), "risk_budget": round(risk_budget, 2),
            "actual_risk": round(units * stop_distance, 2), "potential_reward": round(units * abs(take_profit - entry), 2),
            "position_pct_of_account": round((notional / c.account_balance) * 100, 2) if c.account_balance > 0 else None,
            "capped_by_notional_limit": (risk_budget / stop_distance) > units,
        }


# ──────────────────────────────────────────────────────────────
# Backtest Formatter
# ──────────────────────────────────────────────────────────────
class BacktestFormatter:
    @classmethod
    def build(cls, symbol, cfg, df_high, df_mid, df_low, signal, plan, size) -> Dict[str, Any]:
        row_h, row_m, row_l = df_high.iloc[-1], df_mid.iloc[-1], df_low.iloc[-1]
        return {
            "timestamp": row_l.name.isoformat(), "symbol": symbol, "close_15m": safe_float(row_l["close"]),
            "score_total": signal.get("score"), "bias": signal.get("bias"),
            "plan_side": plan.get("side"), "plan_tradeable": plan.get("tradeable"),
            "plan_effective_rr": plan.get("effective_risk_reward"), "size_units": size.get("units"),
        }


# ──────────────────────────────────────────────────────────────
# Orchestrator
# ──────────────────────────────────────────────────────────────
class Analyzer:
    def __init__(self, cfg: Config):
        self.cfg, self.client = cfg, ExchangeClient(cfg)
        self.indicators, self.signal_engine = Indicators(cfg), SignalEngine(cfg)
        self.planner, self.sizer = TradePlanner(cfg), PositionSizer(cfg, self.client)

    def _fetch_and_enrich(self, symbol: str, tier: str) -> pd.DataFrame:
        df = self.client.fetch_ohlcv(symbol, self.cfg.timeframes[tier], self.cfg.limits[tier])
        return self.indicators.enrich(df)

    def analyze(self, symbol: str) -> Dict[str, Any]:
        try:
            df_high = self._fetch_and_enrich(symbol, "high")
            time.sleep(0.3)
            df_mid = self._fetch_and_enrich(symbol, "mid")
            time.sleep(0.3)
            df_low = self._fetch_and_enrich(symbol, "low")

            signal = self.signal_engine.evaluate(df_high, df_mid, df_low)
            plan = self.planner.plan(df_low, signal)
            sizing = self.sizer.size(plan, symbol)

            for key in ("entry", "stop_loss", "take_profit", "target_rr", "target_sr", "support", "resistance"):
                if plan.get(key) is not None: plan[key] = self.client.format_price(symbol, plan[key])

            return {
                "symbol": symbol, "market_type": self.cfg.market_type, "timeframes": self.cfg.timeframes,
                "signal": signal, "trade_plan": plan, "position_size": sizing,
                "backtest_row": BacktestFormatter.build(symbol, self.cfg, df_high, df_mid, df_low, signal, plan, sizing),
            }
        except Exception as exc:
            logger.error(f"Failed to analyze {symbol}: {exc}")
            return {"symbol": symbol, "error": str(exc)}

    def analyze_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        results = []
        for sym in symbols:
            results.append(self.analyze(sym))
            time.sleep(0.5)
        return results


# ──────────────────────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-Timeframe Technical Analysis Signal Generator")
    parser.add_argument("symbols", nargs="+", help="Trading pair(s), e.g. BTC/USDT ETH/USDT")
    parser.add_argument("--market", "-m", choices=["spot", "futures"], default="spot")
    parser.add_argument("--exchange", "-e", default="binance")
    parser.add_argument("--balance", "-b", type=float, default=10_000.0)
    parser.add_argument("--risk", "-r", type=float, default=1.0)
    parser.add_argument("--leverage", "-l", type=float, default=1.0)
    parser.add_argument("--config", "-c", type=str, default=None)
    parser.add_argument("--output", "-o", choices=["json", "summary"], default="summary")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def print_summary(report: Dict[str, Any]) -> None:
    if "error" in report:
        print(f"\n{'='*60}\n  {report['symbol']}  —  ERROR: {report['error']}\n{'='*60}")
        return

    sig, plan, size = report["signal"], report["trade_plan"], report["position_size"]
    print(f"\n{'='*60}\n  {report['symbol']}  |  {report['market_type'].upper()}  |  Score: {sig['score']}\n{'='*60}")
    print(f"  Regime : {sig['regime']}\n  Bias   : {sig['bias']}\n  Action : {sig['action']}")
    print(f"  Trend  : {sig['trend_score']:+.1f}  |  Momentum: {sig['momentum_score']:+.1f}  |  Trigger: {sig['trigger_score']:+.1f}\n")
    
    print("  Signal Reasons:")
    for r in sig["reasons"]: print(f"    • {r}")
    print()

    if plan["tradeable"]:
        print(f"  Trade Plan ({plan['plan_status'].upper()}):")
        for k in ['side', 'entry_type', 'entry', 'stop_loss', 'take_profit', 'effective_risk_reward']:
            print(f"    {k.capitalize():11}: {plan[k]}")
        print()
        if size["units"]:
            print("  Position Size:")
            print(f"    Units      : {size['units']}\n    Notional   : ${size['notional']:,.2f}\n    Risk Budget: ${size['risk_budget']:,.2f}")
    else:
        print(f"  Trade Plan: {plan['plan_status'].upper()}")
        for n in plan["notes"]: print(f"    — {n}")
    print(f"{'='*60}")


def main() -> None:
    args = parse_args()
    if args.debug: logging.getLogger().setLevel(logging.DEBUG)

    cfg = Config.from_json(args.config) if args.config else Config()
    cfg.exchange_id, cfg.market_type, cfg.account_balance, cfg.account_risk_pct, cfg.leverage = args.exchange, args.market, args.balance, args.risk, args.leverage

    reports = Analyzer(cfg).analyze_multiple(args.symbols)

    if args.output == "json": print(json.dumps(sanitize_for_json(reports), indent=2))
    else:
        for r in reports: print_summary(r)


if __name__ == "__main__":
    main()
