#!/usr/bin/env python3
"""RSI + Bollinger mean reversion strategy for Maxxit lazy trading."""

import argparse
from typing import Any, Dict, List, Optional

from strategy_common import (
    VALID_INTERVALS,
    VALID_VENUES,
    bollinger_bands,
    build_config,
    closes,
    create_session,
    ensure_environment,
    execute_signal,
    fetch_binance_klines,
    load_state,
    log,
    rsi,
    save_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="RSI + Bollinger mean reversion strategy. Fades band extremes and enters on re-entry confirmation."
    )
    parser.add_argument("--symbol", type=str, default="BTCUSDT", help="Binance trading pair symbol. Default: BTCUSDT")
    parser.add_argument("--interval", type=str, default="5m", choices=VALID_INTERVALS, help="Candle interval. Default: 5m")
    parser.add_argument("--candles", type=int, default=80, help="Number of candles to fetch. Default: 80")
    parser.add_argument("--venue", type=str, default="avantis", choices=VALID_VENUES, help="DEX to trade on. Default: avantis")
    parser.add_argument("--rsi-period", type=int, default=14, help="RSI period. Default: 14")
    parser.add_argument("--bb-period", type=int, default=20, help="Bollinger lookback period. Default: 20")
    parser.add_argument("--bb-std", type=float, default=2.0, help="Bollinger standard deviation multiplier. Default: 2.0")
    parser.add_argument("--oversold-exit", type=float, default=35.0, help="Long re-entry RSI ceiling. Default: 35")
    parser.add_argument("--overbought-exit", type=float, default=65.0, help="Short re-entry RSI floor. Default: 65")
    parser.add_argument("--take-profit", type=float, default=0.02, help="Take profit percent. Default: 0.02")
    parser.add_argument("--stop-loss", type=float, default=0.012, help="Stop loss percent. Default: 0.012")
    args = parser.parse_args()
    minimum = max(args.rsi_period + 3, args.bb_period + 3)
    if args.candles < minimum:
        parser.error(f"candles must be >= {minimum} for the selected periods")
    return args


def determine_signal(
    candle_data: List[Dict[str, float]],
    rsi_values: List[Optional[float]],
    upper_band: List[Optional[float]],
    lower_band: List[Optional[float]],
    oversold_exit: float,
    overbought_exit: float,
) -> Optional[str]:
    if len(candle_data) < 3:
        return None

    prev_close = candle_data[-2]["close"]
    current_close = candle_data[-1]["close"]
    prev_upper = upper_band[-2]
    current_upper = upper_band[-1]
    prev_lower = lower_band[-2]
    current_lower = lower_band[-1]
    prev_rsi = rsi_values[-2]
    current_rsi = rsi_values[-1]

    if None in (prev_upper, current_upper, prev_lower, current_lower, prev_rsi, current_rsi):
        return None

    long_reentry = (
        prev_close < prev_lower
        and current_close > current_lower
        and current_rsi > prev_rsi
        and current_rsi <= oversold_exit
    )
    short_reentry = (
        prev_close > prev_upper
        and current_close < current_upper
        and current_rsi < prev_rsi
        and current_rsi >= overbought_exit
    )

    if long_reentry:
        return "long"
    if short_reentry:
        return "short"
    return None


def main() -> None:
    args = parse_args()
    config = build_config(
        symbol=args.symbol,
        interval=args.interval,
        candles=args.candles,
        venue=args.venue,
        strategy_slug="rsi_bollinger",
    )
    ensure_environment(config)
    state = load_state(config["state_file"])
    candles = fetch_binance_klines(config["binance_symbol"], config["interval"], config["num_candles"])
    close_values = closes(candles)
    rsi_values = rsi(close_values, args.rsi_period)
    upper_band, middle_band, lower_band = bollinger_bands(close_values, args.bb_period, args.bb_std)
    signal = determine_signal(
        candles,
        rsi_values,
        upper_band,
        lower_band,
        args.oversold_exit,
        args.overbought_exit,
    )

    latest_close = close_values[-1]
    latest_rsi = rsi_values[-1]
    latest_mid = middle_band[-1]
    log(
        f"RSI/Bollinger snapshot | close: {latest_close:.4f}, "
        f"rsi: {latest_rsi if latest_rsi is not None else 'n/a'}, "
        f"mid: {latest_mid if latest_mid is not None else 'n/a'}"
    )

    if signal is None:
        log("No RSI + Bollinger re-entry signal detected; skipping this run")
        state["last_close"] = latest_close
        state["last_rsi"] = latest_rsi
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
    state["last_rsi"] = latest_rsi
    state["last_signal"] = signal if success else "failed"
    save_state(state, config["state_file"])


if __name__ == "__main__":
    main()
