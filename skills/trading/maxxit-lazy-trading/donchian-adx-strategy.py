#!/usr/bin/env python3
"""Donchian breakout with ADX trend filter for Maxxit lazy trading."""

import argparse
from typing import Any, Dict, List, Optional

from strategy_common import (
    VALID_INTERVALS,
    VALID_VENUES,
    adx,
    build_config,
    closes,
    create_session,
    ema,
    ensure_environment,
    execute_signal,
    fetch_binance_klines,
    highs,
    load_state,
    log,
    lows,
    save_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Donchian breakout strategy with ADX confirmation. Trades only when trend strength is above threshold."
    )
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="Binance trading pair symbol. Default: BTCUSDT")
    parser.add_argument("--interval", type=str, default="15m", choices=VALID_INTERVALS, help="Candle interval. Default: 15m")
    parser.add_argument("--candles", type=int, default=120, help="Number of candles to fetch. Default: 120")
    parser.add_argument("--venue", type=str, default="avantis", choices=VALID_VENUES, help="DEX to trade on. Default: avantis")
    parser.add_argument("--donchian-period", type=int, default=20, help="Breakout lookback period. Default: 20")
    parser.add_argument("--adx-period", type=int, default=14, help="ADX period. Default: 14")
    parser.add_argument("--adx-threshold", type=float, default=25.0, help="Minimum ADX required to trade. Default: 25")
    parser.add_argument("--trend-ema", type=int, default=50, help="EMA trend filter period. Default: 50")
    parser.add_argument("--take-profit", type=float, default=0.03, help="Take profit percent. Default: 0.03")
    parser.add_argument("--stop-loss", type=float, default=0.015, help="Stop loss percent. Default: 0.015")
    args = parser.parse_args()
    minimum = max(args.donchian_period + 2, (args.adx_period * 2) + 2, args.trend_ema + 1)
    if args.candles < minimum:
        parser.error(f"candles must be >= {minimum} for the selected periods")
    return args


def determine_signal(
    candle_data: List[Dict[str, float]],
    adx_values: List[Optional[float]],
    trend_ema: List[Optional[float]],
    donchian_period: int,
    adx_threshold: float,
) -> Optional[str]:
    if len(candle_data) < donchian_period + 2:
        return None

    current_close = candle_data[-1]["close"]
    prior_highs = [row["high"] for row in candle_data[-1 - donchian_period : -1]]
    prior_lows = [row["low"] for row in candle_data[-1 - donchian_period : -1]]
    if not prior_highs or not prior_lows:
        return None

    upper_breakout = max(prior_highs)
    lower_breakout = min(prior_lows)
    current_adx = adx_values[-1]
    current_trend = trend_ema[-1]
    if current_adx is None or current_trend is None or current_adx < adx_threshold:
        return None

    if current_close > upper_breakout and current_close > current_trend:
        return "long"
    if current_close < lower_breakout and current_close < current_trend:
        return "short"
    return None


def main() -> None:
    args = parse_args()
    config = build_config(
        symbol=args.symbol,
        interval=args.interval,
        candles=args.candles,
        venue=args.venue,
        strategy_slug="donchian_adx",
    )
    ensure_environment(config)
    state = load_state(config["state_file"])
    candles = fetch_binance_klines(config["binance_symbol"], config["interval"], config["num_candles"])
    close_values = closes(candles)
    high_values = highs(candles)
    low_values = lows(candles)
    adx_values = adx(high_values, low_values, close_values, args.adx_period)
    trend_values = ema(close_values, args.trend_ema)
    signal = determine_signal(candles, adx_values, trend_values, args.donchian_period, args.adx_threshold)

    latest_close = close_values[-1]
    latest_adx = adx_values[-1]
    latest_trend = trend_values[-1]
    log(
        f"Donchian/ADX snapshot | close: {latest_close:.4f}, "
        f"adx: {latest_adx if latest_adx is not None else 'n/a'}, "
        f"trend_ema: {latest_trend if latest_trend is not None else 'n/a'}"
    )

    if signal is None:
        log("No Donchian breakout with ADX confirmation detected; skipping this run")
        state["last_close"] = latest_close
        state["last_adx"] = latest_adx
        state["last_signal"] = None
        save_state(state, config["state_file"])
        return

    session = create_session()
    success = execute_signal(
        session=session,
        config=config,
        signal=signal,
        reference_price=latest_close,
        take_profit=args.take_profit,
        stop_loss=args.stop_loss,
    )
    state["last_close"] = latest_close
    state["last_adx"] = latest_adx
    state["last_signal"] = signal if success else "failed"
    save_state(state, config["state_file"])


if __name__ == "__main__":
    main()
