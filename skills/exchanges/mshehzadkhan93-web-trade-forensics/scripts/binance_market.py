
import json
import urllib.error
import urllib.parse
import urllib.request


SPOT_BASE_URL = "https://api.binance.com"
FUTURES_BASE_URL = "https://fapi.binance.com"
TIMEOUT_SECONDS = 10


def _get_json(base_url: str, path: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    url = f"{base_url}{path}?{query}"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "trade-forensics-agent/1.0"},
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT_SECONDS,
        ) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Binance HTTP error: {exc.code}"
        ) from exc

    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Binance connection error: {exc.reason}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Binance returned invalid JSON."
        ) from exc


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    symbol = symbol.replace("/", "")
    symbol = symbol.replace("-", "")

    if not symbol:
        raise ValueError("symbol cannot be empty")

    return symbol


def get_spot_book_ticker(symbol: str) -> dict:
    symbol = normalize_symbol(symbol)

    data = _get_json(
        SPOT_BASE_URL,
        "/api/v3/ticker/bookTicker",
        {"symbol": symbol},
    )

    bid = float(data["bidPrice"])
    ask = float(data["askPrice"])

    if bid <= 0 or ask <= 0:
        raise RuntimeError("Invalid bid/ask data received.")

    mid = (bid + ask) / 2
    spread = ask - bid
    spread_pct = (spread / mid) * 100

    return {
        "symbol": symbol,
        "bid": bid,
        "ask": ask,
        "mid_price": mid,
        "spread": spread,
        "spread_pct": spread_pct,
    }


def get_spot_24h(symbol: str) -> dict:
    symbol = normalize_symbol(symbol)

    data = _get_json(
        SPOT_BASE_URL,
        "/api/v3/ticker/24hr",
        {"symbol": symbol},
    )

    return {
        "symbol": symbol,
        "last_price": float(data["lastPrice"]),
        "price_change_pct": float(data["priceChangePercent"]),
        "high_24h": float(data["highPrice"]),
        "low_24h": float(data["lowPrice"]),
        "base_volume_24h": float(data["volume"]),
        "quote_volume_24h": float(data["quoteVolume"]),
    }


def get_futures_funding(symbol: str) -> dict:
    symbol = normalize_symbol(symbol)

    data = _get_json(
        FUTURES_BASE_URL,
        "/fapi/v1/premiumIndex",
        {"symbol": symbol},
    )

    return {
        "symbol": symbol,
        "mark_price": float(data["markPrice"]),
        "index_price": float(data["indexPrice"]),
        "last_funding_rate": float(data["lastFundingRate"]),
        "next_funding_time": int(data["nextFundingTime"]),
    }


def get_futures_open_interest(symbol: str) -> dict:
    symbol = normalize_symbol(symbol)

    data = _get_json(
        FUTURES_BASE_URL,
        "/fapi/v1/openInterest",
        {"symbol": symbol},
    )

    return {
        "symbol": symbol,
        "open_interest": float(data["openInterest"]),
        "timestamp": int(data["time"]),
    }


def get_market_snapshot(symbol: str) -> dict:
    symbol = normalize_symbol(symbol)

    snapshot = {
        "symbol": symbol,
        "spot": None,
        "futures": None,
        "errors": [],
    }

    try:
        book = get_spot_book_ticker(symbol)
        ticker = get_spot_24h(symbol)

        snapshot["spot"] = {
            **book,
            **ticker,
        }

    except (RuntimeError, KeyError, ValueError) as exc:
        snapshot["errors"].append(
            f"Spot data unavailable: {exc}"
        )

    try:
        funding = get_futures_funding(symbol)
        open_interest = get_futures_open_interest(symbol)

        snapshot["futures"] = {
            **funding,
            **open_interest,
        }

    except (RuntimeError, KeyError, ValueError) as exc:
        snapshot["errors"].append(
            f"Futures data unavailable: {exc}"
        )

    return snapshot


if __name__ == "__main__":
    result = get_market_snapshot("BTCUSDT")
    print(json.dumps(result, indent=2))
