#!/usr/bin/env python3
"""EMA crossover bot for trading on Ostium, Aster, or Avantis."""

import argparse
from typing import Any, Dict, List, Optional

from strategy_common import (
    VALID_INTERVALS,
    VALID_VENUES,
    build_config,
    closes,
    create_session,
    ema,
    ensure_environment,
    execute_signal,
    fetch_binance_klines,
    load_state,
    log,
    save_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="EMA crossover strategy. Pass token symbol, candle interval, candle count, and fast/slow EMA periods."
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="BTCUSDT",
        help="Binance trading pair symbol (e.g. BTCUSDT, ETHUSDT). Default: BTCUSDT",
    )
    parser.add_argument(
        "--interval",
        type=str,
        default="5m",
        choices=VALID_INTERVALS,
        help="Candle interval. Default: 5m",
    )
    parser.add_argument(
        "--candles",
        type=int,
        default=40,
        help="Number of candles to fetch and use for EMA calculation. Must be >= slow_period + 2. Default: 40",
    )
    parser.add_argument(
        "--fast",
        type=int,
        default=5,
        dest="fast_period",
        help="Fast EMA period. Default: 5",
    )
    parser.add_argument(
        "--slow",
        type=int,
        default=20,
        dest="slow_period",
        help="Slow EMA period. Default: 20",
    )
    parser.add_argument(
        "--venue",
        type=str,
        default="avantis",
        choices=VALID_VENUES,
        help="DEX to trade on: ostium (Arbitrum), aster (BNB Chain), avantis (Base). Default: avantis",
    )
    parser.add_argument(
        "--take-profit",
        type=float,
        default=0.025,
        help="Take profit percent. Default: 0.025",
    )
    parser.add_argument(
        "--stop-loss",
        type=float,
        default=0.015,
        help="Stop loss percent. Default: 0.015",
    )
    args = parser.parse_args()
    if args.candles < args.slow_period + 2:
        parser.error(f"candles must be >= slow_period + 2 (got candles={args.candles}, slow_period={args.slow_period})")
    if args.fast_period >= args.slow_period:
        parser.error("fast_period must be less than slow_period")
    return args


def determine_signal(fast_values: List[Optional[float]], slow_values: List[Optional[float]]) -> Optional[str]:
    if len(fast_values) < 2 or len(slow_values) < 2:
        return None
    previous_fast = fast_values[-2]
    current_fast = fast_values[-1]
    previous_slow = slow_values[-2]
    current_slow = slow_values[-1]
    if None in (previous_fast, current_fast, previous_slow, current_slow):
        return None
    if previous_fast <= previous_slow and current_fast > current_slow:
        return "long"
    if previous_fast >= previous_slow and current_fast < current_slow:
        return "short"
    return None


def main() -> None:
    args = parse_args()
    config = build_config(
        symbol=args.symbol,
        interval=args.interval,
        candles=args.candles,
        venue=args.venue,
        strategy_slug="ema",
    )
    config["fast_period"] = args.fast_period
    config["slow_period"] = args.slow_period

    ensure_environment(config)
    state = load_state(config["state_file"])
    candles = fetch_binance_klines(config["binance_symbol"], config["interval"], config["num_candles"])
    price_values = closes(candles)
    fast_ema = ema(price_values, args.fast_period)
    slow_ema = ema(price_values, args.slow_period)
    signal = determine_signal(fast_ema, slow_ema)

    latest_price = price_values[-1]
    log(
        f"EMA snapshot | close: {latest_price:.4f}, "
        f"fast_ema: {fast_ema[-1] if fast_ema[-1] is not None else 'n/a'}, "
        f"slow_ema: {slow_ema[-1] if slow_ema[-1] is not None else 'n/a'}"
    )

    if signal is None:
        log("No EMA crossover signal detected; skipping this run")
        state["last_fast"] = fast_ema[-1]
        state["last_slow"] = slow_ema[-1]
        state["last_direction"] = None
        save_state(state, config["state_file"])
        return

    session = create_session()
    success = execute_signal(
        session=session,
        config=config,
        signal=signal,
        reference_price=latest_price,
        take_profit=args.take_profit,
        stop_loss=args.stop_loss,
    )
    state["last_fast"] = fast_ema[-1]
    state["last_slow"] = slow_ema[-1]
    state["last_direction"] = signal if success else "failed"
    save_state(state, config["state_file"])


if __name__ == "__main__":
    main()
