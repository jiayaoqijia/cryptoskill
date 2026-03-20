#!/usr/bin/env python3
"""Shared helpers for Maxxit lazy trading strategy scripts."""

import json
import logging
import math
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests

BASE_DIR = "/home/ubuntu/.openclaw/workspace"
LOG_DIR = os.path.join(BASE_DIR, "logs")
MAXXIT_API_URL = os.environ.get("MAXXIT_API_URL")
MAXXIT_API_KEY = os.environ.get("MAXXIT_API_KEY")

COLLATERAL_UTILIZATION = 0.8
MIN_COLLATERAL = 1.0
MIN_NOTIONAL = 100.0
REQUEST_TIMEOUT = 60
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
VALID_INTERVALS = (
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M",
)
VALID_VENUES = ("ostium", "aster", "avantis")


def log(message: str) -> None:
    logging.info(message)
    print(f"{datetime.utcnow().isoformat()} - {message}")


def build_config(
    *,
    symbol: str,
    interval: str,
    candles: int,
    venue: str,
    strategy_slug: str,
) -> Dict[str, Any]:
    binance_symbol = symbol.strip().upper()
    if not binance_symbol.endswith("USDT"):
        binance_symbol = f"{binance_symbol}USDT"
    base = binance_symbol.replace("USDT", "")
    safe_strategy = strategy_slug.replace("-", "_")
    return {
        "binance_symbol": binance_symbol,
        "market": base,
        "symbol": f"{base}/USD",
        "interval": interval,
        "num_candles": candles,
        "venue": venue.strip().lower(),
        "state_file": os.path.join(BASE_DIR, f"{venue}_{base.lower()}_{safe_strategy}_state.json"),
        "log_file": os.path.join(LOG_DIR, f"{venue}_{base.lower()}_{safe_strategy}.log"),
        "strategy_slug": safe_strategy,
    }


def ensure_environment(config: Dict[str, Any]) -> None:
    if not MAXXIT_API_URL or not MAXXIT_API_KEY:
        raise EnvironmentError("MAXXIT_API_URL and MAXXIT_API_KEY must be set")
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = config.get("log_file")
    if log_file and not logging.getLogger().handlers:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def load_state(state_file: str) -> Dict[str, Any]:
    if not os.path.isfile(state_file):
        return {}
    try:
        with open(state_file, "r") as handle:
            return json.load(handle)
    except (ValueError, IOError):
        return {}


def save_state(state: Dict[str, Any], state_file: str) -> None:
    with open(state_file, "w") as handle:
        json.dump(state, handle)


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"X-API-KEY": MAXXIT_API_KEY, "Content-Type": "application/json"})
    return session


def api_get(session: requests.Session, path: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    url = f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/{path}"
    try:
        response = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        log(f"GET {path} failed: {exc}")
        return None


def api_post(session: requests.Session, path: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    url = f"{MAXXIT_API_URL}/api/lazy-trading/programmatic/{path}"
    try:
        response = session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        log(f"POST {path} failed: {exc}")
        return None


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def fetch_binance_klines(symbol: str, interval: str, limit: int) -> List[Dict[str, float]]:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(BINANCE_KLINES_URL, params=params, timeout=10)
    response.raise_for_status()
    raw = response.json()
    candles: List[Dict[str, float]] = []
    for item in raw:
        volume = safe_float(item[5])
        quote_volume = safe_float(item[7])
        taker_buy_base = safe_float(item[9])
        taker_buy_quote = safe_float(item[10])
        candles.append(
            {
                "open_time": float(item[0]),
                "open": safe_float(item[1]),
                "high": safe_float(item[2]),
                "low": safe_float(item[3]),
                "close": safe_float(item[4]),
                "volume": volume,
                "close_time": float(item[6]),
                "quote_volume": quote_volume,
                "num_trades": safe_float(item[8]),
                "taker_buy_base_volume": taker_buy_base,
                "taker_buy_quote_volume": taker_buy_quote,
                "taker_buy_ratio": taker_buy_base / volume if volume > 0 else 0.0,
                "vwap": quote_volume / volume if volume > 0 else safe_float(item[4]),
            }
        )
    return candles


def closes(candles: List[Dict[str, float]]) -> List[float]:
    return [candle["close"] for candle in candles]


def highs(candles: List[Dict[str, float]]) -> List[float]:
    return [candle["high"] for candle in candles]


def lows(candles: List[Dict[str, float]]) -> List[float]:
    return [candle["low"] for candle in candles]


def sma(values: List[float], period: int) -> List[Optional[float]]:
    result: List[Optional[float]] = [None] * len(values)
    if period <= 0:
        return result
    running = 0.0
    for index, value in enumerate(values):
        running += value
        if index >= period:
            running -= values[index - period]
        if index >= period - 1:
            result[index] = running / period
    return result


def ema(values: List[float], period: int) -> List[Optional[float]]:
    result: List[Optional[float]] = [None] * len(values)
    if not values or period <= 0 or len(values) < period:
        return result
    seed = sum(values[:period]) / period
    alpha = 2 / (period + 1)
    current = seed
    result[period - 1] = seed
    for index in range(period, len(values)):
        current = values[index] * alpha + current * (1 - alpha)
        result[index] = current
    return result


def rolling_stddev(values: List[float], period: int) -> List[Optional[float]]:
    result: List[Optional[float]] = [None] * len(values)
    if period <= 1:
        return result
    for index in range(period - 1, len(values)):
        window = values[index - period + 1 : index + 1]
        mean = sum(window) / period
        variance = sum((value - mean) ** 2 for value in window) / period
        result[index] = math.sqrt(variance)
    return result


def bollinger_bands(values: List[float], period: int, std_mult: float) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    middle = sma(values, period)
    std = rolling_stddev(values, period)
    upper: List[Optional[float]] = [None] * len(values)
    lower: List[Optional[float]] = [None] * len(values)
    for index in range(len(values)):
        if middle[index] is None or std[index] is None:
            continue
        upper[index] = middle[index] + std_mult * std[index]
        lower[index] = middle[index] - std_mult * std[index]
    return upper, middle, lower


def rsi(values: List[float], period: int) -> List[Optional[float]]:
    result: List[Optional[float]] = [None] * len(values)
    if period <= 0 or len(values) <= period:
        return result
    gains: List[float] = []
    losses: List[float] = []
    for index in range(1, len(values)):
        delta = values[index] - values[index - 1]
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    if avg_loss == 0:
        result[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        result[period] = 100 - (100 / (1 + rs))
    for index in range(period + 1, len(values)):
        gain = gains[index - 1]
        loss = losses[index - 1]
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        if avg_loss == 0:
            result[index] = 100.0
        else:
            rs = avg_gain / avg_loss
            result[index] = 100 - (100 / (1 + rs))
    return result


def adx(high_values: List[float], low_values: List[float], close_values: List[float], period: int) -> List[Optional[float]]:
    size = len(close_values)
    result: List[Optional[float]] = [None] * size
    if period <= 0 or size <= period * 2:
        return result

    true_ranges: List[float] = [0.0] * size
    plus_dm: List[float] = [0.0] * size
    minus_dm: List[float] = [0.0] * size
    for index in range(1, size):
        high_diff = high_values[index] - high_values[index - 1]
        low_diff = low_values[index - 1] - low_values[index]
        true_ranges[index] = max(
            high_values[index] - low_values[index],
            abs(high_values[index] - close_values[index - 1]),
            abs(low_values[index] - close_values[index - 1]),
        )
        plus_dm[index] = high_diff if high_diff > low_diff and high_diff > 0 else 0.0
        minus_dm[index] = low_diff if low_diff > high_diff and low_diff > 0 else 0.0

    tr_sum = sum(true_ranges[1 : period + 1])
    plus_sum = sum(plus_dm[1 : period + 1])
    minus_sum = sum(minus_dm[1 : period + 1])

    dx_values: List[Optional[float]] = [None] * size
    for index in range(period, size):
        if index > period:
            tr_sum = tr_sum - (tr_sum / period) + true_ranges[index]
            plus_sum = plus_sum - (plus_sum / period) + plus_dm[index]
            minus_sum = minus_sum - (minus_sum / period) + minus_dm[index]
        if tr_sum == 0:
            continue
        plus_di = 100 * (plus_sum / tr_sum)
        minus_di = 100 * (minus_sum / tr_sum)
        denominator = plus_di + minus_di
        if denominator == 0:
            continue
        dx_values[index] = 100 * abs(plus_di - minus_di) / denominator

    initial_dx = [value for value in dx_values[period : period * 2] if value is not None]
    if len(initial_dx) < period:
        return result

    adx_value = sum(initial_dx[:period]) / period
    result[period * 2 - 1] = adx_value
    for index in range(period * 2, size):
        dx = dx_values[index]
        if dx is None:
            continue
        adx_value = ((adx_value * (period - 1)) + dx) / period
        result[index] = adx_value
    return result


def highest(values: List[float]) -> float:
    return max(values) if values else 0.0


def lowest(values: List[float]) -> float:
    return min(values) if values else 0.0


def fetch_balance(
    session: requests.Session,
    venue: str,
    user_address: str,
    agent_address: Optional[str],
) -> Optional[Dict[str, Any]]:
    if venue == "ostium":
        return api_post(session, "balance", {"address": user_address})
    if venue == "aster":
        return api_post(session, "aster/balance", {"userAddress": user_address})
    if venue == "avantis":
        return api_post(session, "avantis/balance", {"userAddress": user_address})
    return None


def usdc_balance_from_response(venue: str, balance_resp: Optional[Dict[str, Any]]) -> float:
    if not balance_resp:
        return 0.0
    if venue == "aster":
        return safe_float(balance_resp.get("availableBalance") or balance_resp.get("balance"))
    return safe_float(balance_resp.get("usdcBalance"))


def fetch_market_data_and_max_leverage(
    session: requests.Session,
    venue: str,
    symbol: str,
    market: str,
) -> float:
    if venue in ("ostium", "avantis"):
        data = api_get(session, "market-data")
        for row in (data or {}).get("data", []):
            if row.get("symbol") == symbol:
                return safe_float(row.get("maxLeverage"), 15.0)
        return 15.0
    if venue == "aster":
        data = api_get(session, "aster/market-data", {"symbol": market})
        if data and isinstance(data.get("maxLeverage"), (int, float)):
            return float(data["maxLeverage"])
        return 20.0
    return 15.0


def fetch_positions(
    session: requests.Session,
    venue: str,
    user_address: str,
    agent_address: Optional[str],
) -> Optional[Dict[str, Any]]:
    if venue == "ostium":
        return api_post(session, "positions", {"address": user_address})
    if venue == "aster":
        return api_post(session, "aster/positions", {"userAddress": user_address})
    if venue == "avantis":
        return api_post(session, "avantis/positions", {"userAddress": user_address, "agentAddress": agent_address})
    return None


def find_existing_position(positions_resp: Optional[Dict[str, Any]], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    positions = (positions_resp or {}).get("positions") or []
    symbol = config["symbol"]
    market = config["market"]
    binance_symbol = config["binance_symbol"]
    venue = config["venue"]
    for pos in positions:
        if venue == "aster":
            pos_symbol = str(pos.get("symbol") or "")
            if pos_symbol == binance_symbol or pos_symbol.replace("USDT", "") == market:
                return pos
        else:
            if pos.get("market") == market or pos.get("marketFull") == symbol:
                return pos
    return None


def get_ostium_pair_index(session: requests.Session, symbol: str) -> Optional[int]:
    data = api_get(session, "symbols")
    symbols = (data or {}).get("symbols") or []
    for row in symbols:
        if row.get("symbol") == symbol:
            return row.get("id")
    return None


def fetch_trading_identity(session: requests.Session, venue: str) -> Tuple[Optional[str], Optional[str]]:
    user_details = api_get(session, "user-details")
    if not user_details:
        return None, None
    user_address = user_details.get("user_wallet")
    agent_address = user_details.get("ostium_agent_address")
    if not user_address:
        log("User details missing user wallet")
        return None, None
    if venue != "aster" and not agent_address:
        log("User details missing agent address (required for Ostium/Avantis)")
        return None, None
    return user_address, agent_address


def enforce_notional(collateral: float, leverage: float, max_leverage: float, usdc_balance: float) -> Tuple[float, float, float]:
    notional = collateral * leverage
    if notional < MIN_NOTIONAL and collateral > 0:
        needed_leverage = math.ceil(MIN_NOTIONAL / collateral)
        leverage = min(max_leverage, max(leverage, needed_leverage))
        notional = collateral * leverage
    if notional < MIN_NOTIONAL and leverage > 0:
        potential_collateral = min(usdc_balance, MIN_NOTIONAL / leverage)
        if potential_collateral > collateral and potential_collateral >= MIN_COLLATERAL:
            collateral = potential_collateral
            notional = collateral * leverage
    return collateral, leverage, notional


def execute_signal(
    *,
    session: requests.Session,
    config: Dict[str, Any],
    signal: str,
    reference_price: float,
    take_profit: float,
    stop_loss: float,
) -> bool:
    venue = config["venue"]
    symbol = config["symbol"]
    market = config["market"]
    user_address, agent_address = fetch_trading_identity(session, venue)
    if not user_address:
        return False

    max_leverage = fetch_market_data_and_max_leverage(session, venue, symbol, market)
    balance_resp = fetch_balance(session, venue, user_address, agent_address)
    usdc_balance = usdc_balance_from_response(venue, balance_resp)
    if not balance_resp:
        log("Failed to fetch balance")
        return False

    collateral = min(usdc_balance * COLLATERAL_UTILIZATION, usdc_balance)
    if collateral < MIN_COLLATERAL:
        log(f"Not enough balance ({usdc_balance}) to allocate collateral")
        return False

    leverage = min(15.0, max_leverage)
    collateral, leverage, notional = enforce_notional(collateral, leverage, max_leverage, usdc_balance)
    if notional < MIN_NOTIONAL:
        log(f"Notional ({notional:.2f}) is below the {MIN_NOTIONAL} requirement -> skipping")
        return False

    log(
        f"Signal: {signal}, venue: {venue}, leverage: {leverage}, "
        f"collateral: {collateral:.4f}, notional: {notional:.2f}"
    )

    positions_resp = fetch_positions(session, venue, user_address, agent_address)
    existing_position = find_existing_position(positions_resp, config)
    if existing_position:
        existing_side = str(existing_position.get("side", "")).lower()
        if existing_side != signal:
            close_resp: Optional[Dict[str, Any]]
            if venue == "ostium":
                close_resp = api_post(
                    session,
                    "close-position",
                    {
                        "agentAddress": agent_address,
                        "userAddress": user_address,
                        "market": market,
                        "actualTradeIndex": existing_position.get("tradeIndex"),
                    },
                )
            elif venue == "aster":
                close_resp = api_post(
                    session,
                    "aster/close-position",
                    {"userAddress": user_address, "symbol": market},
                )
            else:
                close_resp = api_post(
                    session,
                    "avantis/close-position",
                    {
                        "agentAddress": agent_address,
                        "userAddress": user_address,
                        "market": market,
                        "actualTradeIndex": existing_position.get("tradeIndex"),
                    },
                )
            if not (close_resp and close_resp.get("success")):
                log("Failed to close existing position")
                return False
        else:
            return update_existing_protection(
                session=session,
                config=config,
                existing_position=existing_position,
                user_address=user_address,
                agent_address=agent_address,
                take_profit=take_profit,
                stop_loss=stop_loss,
            )

    open_resp: Optional[Dict[str, Any]]
    if venue == "ostium":
        open_resp = api_post(
            session,
            "open-position",
            {
                "agentAddress": agent_address,
                "userAddress": user_address,
                "market": market,
                "side": signal,
                "collateral": round(collateral, 4),
                "leverage": leverage,
            },
        )
        if open_resp and open_resp.get("success"):
            trade_index = open_resp.get("actualTradeIndex")
            entry_price = safe_float(open_resp.get("entryPrice"), reference_price)
            pair_index = get_ostium_pair_index(session, symbol)
            if pair_index is not None:
                api_post(
                    session,
                    "set-take-profit",
                    {
                        "agentAddress": agent_address,
                        "userAddress": user_address,
                        "market": market,
                        "tradeIndex": trade_index,
                        "takeProfitPercent": take_profit,
                        "entryPrice": entry_price,
                        "pairIndex": pair_index,
                        "side": signal,
                    },
                )
                api_post(
                    session,
                    "set-stop-loss",
                    {
                        "agentAddress": agent_address,
                        "userAddress": user_address,
                        "market": market,
                        "tradeIndex": trade_index,
                        "stopLossPercent": stop_loss,
                        "entryPrice": entry_price,
                        "pairIndex": pair_index,
                        "side": signal,
                    },
                )
    elif venue == "aster":
        if reference_price <= 0:
            log("Invalid price for quantity calculation")
            return False
        quantity = notional / reference_price
        if quantity <= 0:
            log("Invalid quantity calculation")
            return False
        open_resp = api_post(
            session,
            "aster/open-position",
            {
                "userAddress": user_address,
                "symbol": market,
                "side": signal,
                "quantity": round(quantity, 6),
                "leverage": leverage,
            },
        )
        if open_resp and open_resp.get("success"):
            entry_price = safe_float(open_resp.get("avgPrice"), reference_price)
            api_post(
                session,
                "aster/set-take-profit",
                {
                    "userAddress": user_address,
                    "symbol": market,
                    "takeProfitPercent": take_profit,
                    "entryPrice": entry_price,
                    "side": signal,
                },
            )
            api_post(
                session,
                "aster/set-stop-loss",
                {
                    "userAddress": user_address,
                    "symbol": market,
                    "stopLossPercent": stop_loss,
                    "entryPrice": entry_price,
                    "side": signal,
                },
            )
    else:
        open_resp = api_post(
            session,
            "avantis/open-position",
            {
                "agentAddress": agent_address,
                "userAddress": user_address,
                "market": market,
                "side": signal,
                "collateral": round(collateral, 4),
                "leverage": leverage,
                "takeProfitPercent": take_profit,
                "stopLossPercent": stop_loss,
            },
        )

    if open_resp and open_resp.get("success"):
        entry = open_resp.get("entryPrice") or open_resp.get("avgPrice")
        log(f"Opened {signal} position | entry: {safe_float(entry, reference_price):.2f}, TP% {take_profit:.2%}, SL% {stop_loss:.2%}")
        return True

    log("Open-position call failed")
    return False


def update_existing_protection(
    *,
    session: requests.Session,
    config: Dict[str, Any],
    existing_position: Dict[str, Any],
    user_address: str,
    agent_address: Optional[str],
    take_profit: float,
    stop_loss: float,
) -> bool:
    venue = config["venue"]
    symbol = config["symbol"]
    market = config["market"]
    existing_side = str(existing_position.get("side", "")).lower()
    if venue == "ostium":
        trade_index = existing_position.get("tradeIndex")
        entry_price = safe_float(existing_position.get("entryPrice"))
        pair_index = get_ostium_pair_index(session, symbol)
        if pair_index is not None:
            api_post(
                session,
                "set-take-profit",
                {
                    "agentAddress": agent_address,
                    "userAddress": user_address,
                    "market": market,
                    "tradeIndex": trade_index,
                    "takeProfitPercent": take_profit,
                    "entryPrice": entry_price,
                    "pairIndex": pair_index,
                    "side": existing_side,
                },
            )
            api_post(
                session,
                "set-stop-loss",
                {
                    "agentAddress": agent_address,
                    "userAddress": user_address,
                    "market": market,
                    "tradeIndex": trade_index,
                    "stopLossPercent": stop_loss,
                    "entryPrice": entry_price,
                    "pairIndex": pair_index,
                    "side": existing_side,
                },
            )
            log("Updated TP/SL for the existing position")
            return True
    elif venue == "aster":
        entry_price = safe_float(existing_position.get("entryPrice"))
        api_post(
            session,
            "aster/set-take-profit",
            {
                "userAddress": user_address,
                "symbol": market,
                "takeProfitPercent": take_profit,
                "entryPrice": entry_price,
                "side": existing_side,
            },
        )
        api_post(
            session,
            "aster/set-stop-loss",
            {
                "userAddress": user_address,
                "symbol": market,
                "stopLossPercent": stop_loss,
                "entryPrice": entry_price,
                "side": existing_side,
            },
        )
        log("Updated TP/SL for the existing position")
        return True
    else:
        update_resp = api_post(
            session,
            "avantis/update-sl-tp",
            {
                "agentAddress": agent_address,
                "userAddress": user_address,
                "market": market,
                "takeProfitPercent": take_profit,
                "stopLossPercent": stop_loss,
                "tradeIndex": existing_position.get("tradeIndex"),
            },
        )
        if update_resp and update_resp.get("success"):
            log("Updated TP/SL for the existing position")
            return True
    return False
