#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import hmac
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import warnings
import zipfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Patch, Wedge

CMC_GLOBAL_HIST = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"
CMC_EXCHANGE_QUOTES = "https://api.coinmarketcap.com/data-api/v3/exchange/quotes/latest"
CMC_FNG = "https://api.coinmarketcap.com/data-api/v3/fear-greed/chart"
CG_BASE_PRO = "https://pro-api.coingecko.com/api/v3"
CG_BASE_DEMO = "https://api.coingecko.com/api/v3"
COINPAPRIKA_TICKERS = "https://api.coinpaprika.com/v1/tickers"
ALT_FNG = "https://api.alternative.me/fng/"
DERIBIT_RPC = "https://www.deribit.com/api/v2"
BINANCE_24H = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_KLINES = "https://api.binance.com/api/v3/klines"
BINANCE_US_24H = "https://api.binance.us/api/v3/ticker/24hr"
BINANCE_US_KLINES = "https://api.binance.us/api/v3/klines"
BINANCE_FAPI_PREMIUM_INDEX = "https://fapi.binance.com/fapi/v1/premiumIndex"
BINANCE_FAPI_OPEN_INTEREST = "https://fapi.binance.com/fapi/v1/openInterest"
OKX_TICKER = "https://www.okx.com/api/v5/market/ticker"
OKX_FUNDING = "https://www.okx.com/api/v5/public/funding-rate"
OKX_OPEN_INTEREST = "https://www.okx.com/api/v5/public/open-interest"
BINANCE_MARGIN_INFO = "https://www.binance.com/bapi/margin/v1/public/margin/vip/spec/list-all"
OKX_MARGIN_INFO = "https://www.okx.com/api/v5/public/interest-rate-loan-quota"
BYBIT_MARGIN_INFO = "https://api.bybit.com/v5/spot-margin-trade/data"
KUCOIN_MARGIN_INFO = "https://api.kucoin.com/api/v3/margin/currencies"
BACKPACK_BORROW_MARKETS = "https://api.backpack.exchange/api/v1/borrowLend/markets"
DEFILLAMA_YIELDS = "https://yields.llama.fi/pools"
BITCOMPARE_LENDING_RATES = "https://bitcompare.net/lending-rates"
AAVE_V3_GRAPHQL = "https://api.v3.aave.com/graphql"
MORPHO_GRAPHQL = "https://api.morpho.org/graphql"
COMPOUND_V3_SUMMARY = "https://v3-api.compound.finance/market/all-networks/all-contracts/summary"
COMPOUND_V3_REWARDS = "https://v3-api.compound.finance/market/all-networks/all-contracts/rewards/dapp-data"
RWA_APP_BASE = "https://app.rwa.xyz"
BINANCE_RWA_STOCK_LIST = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/rwa/stock/detail/list/ai"
BINANCE_RWA_DYNAMIC = "https://www.binance.com/bapi/defi/v2/public/wallet-direct/buw/wallet/market/token/rwa/dynamic/ai"
BINANCE_RWA_KLINE = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/kline/ai"
BINANCE_TOKEN_DYNAMIC = "https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info"
BINANCE_SMART_MONEY_SIGNAL = "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money"

DEFAULT_RWA_EQUITY_WATCHLIST = [
    "AAPL", "AMZN", "AMD", "AVGO", "COIN", "CRCL", "GOOGL", "HOOD", "IBIT", "MARA",
    "META", "MSFT", "MSTR", "NFLX", "NVDA", "PLTR", "QQQ", "RIOT", "SPY", "TSLA",
]

# These assets are valid market-cap constituents, but they are not evidence of
# directional crypto risk participation.  Keep them in concentration charts and
# exclude them from the report's risk-breadth counts.
RISK_BREADTH_EXCLUDED_SYMBOLS = {
    "USDT", "USDC", "DAI", "USDS", "FDUSD", "TUSD", "PYUSD", "USDE", "USDP",
    "STETH", "WSTETH", "RETH", "CBETH", "WBETH", "WEETH", "EZETH", "FIGR_HELOC",
}

EXCHANGE_SLUGS = [
    "binance",
    "coinbase-exchange",
    "upbit",
    "okx",
    "bybit",
    "bitget",
    "gate",
    "kucoin",
    "mexc",
    "htx",
]

STABLE_YIELD_PROJECTS = {
    "aave-v3": "Aave",
    "sparklend": "Spark",
    "spark-savings": "Spark",
    "compound-v3": "Compound",
    "morpho-v1": "Morpho",
}
STABLE_YIELD_PROJECT_PRIORITY = {
    "aave-v3": 1,
    "sparklend": 2,
    "spark-savings": 2,
    "compound-v3": 3,
    "morpho-v1": 4,
}
STABLE_YIELD_PROTOCOL_RISK_NOTE = {
    "aave-v3": "审计成熟/头部流动性",
    "sparklend": "Aave系改造/审计覆盖",
    "spark-savings": "Aave系改造/审计覆盖",
    "compound-v3": "成熟协议/资金利用率驱动",
    "morpho-v1": "需关注金库与奖励口径差异",
}
STABLE_YIELD_ASSETS = {"USDC", "USDT", "DAI", "USDS", "SUSDS", "PYUSD"}
STABLE_YIELD_CHAINS = {"ethereum", "base", "arbitrum"}
STABLE_CHAIN_ID_MAP = {1: "Ethereum", 42161: "Arbitrum", 8453: "Base"}
STABLE_EXTENDED_EXCLUDED_PROJECTS = {
    "aave-v3",
    "spark-savings",
    "sparklend",
    "compound-v3",
    "morpho-v1",
    "merkl",
    "curve-dex",
    "uniswap-v3",
    "convex-finance",
    "beefy",
    "pendle",
}
STABLE_EXTENDED_MIN_TVL_USD = 30_000_000.0
STABLE_EXTENDED_MIN_APY_PCT = 0.2
STABLE_EXTENDED_MAX_APY_PCT = 20.0
STABLE_EXTENDED_DISPLAY_ROWS = 20
BITCOMPARE_MAX_PAGES = 12
STABLE_CEFI_ASSETS = {
    "USDT",
    "USDC",
    "DAI",
    "USDE",
    "USDS",
    "SUSDS",
    "PYUSD",
    "USDP",
    "TUSD",
    "BUSD",
    "USD0",
    "USDD",
    "FRAX",
    "LUSD",
}
OKX_SMARTMONEY_TOP_TRADERS = 10
OKX_SMARTMONEY_INSTS = {"BTC": "BTC-USDT-SWAP", "ETH": "ETH-USDT-SWAP"}
OKX_SENTIMENT_COINS = ["BTC", "ETH", "SOL"]
BINANCE_SMART_MONEY_CHAINS = {"56": "BSC", "CT_501": "Solana"}
RWA_PUBLIC_ASSET_CLASSES = [
    {"asset_class": "U.S. Treasuries", "slug": "treasuries", "source": "https://app.rwa.xyz/treasuries"},
    {"asset_class": "Credit", "slug": "credit", "source": "https://app.rwa.xyz/credit"},
    {"asset_class": "Tokenized Stocks", "slug": "stocks", "source": "https://app.rwa.xyz/stocks"},
    {"asset_class": "Non-U.S. Government Debt", "slug": "government-bonds", "source": "https://app.rwa.xyz/government-bonds"},
    {"asset_class": "Active Strategies", "slug": "active-strategies", "source": "https://app.rwa.xyz/active-strategies"},
    {"asset_class": "Real Estate", "slug": "real-estate", "source": "https://app.rwa.xyz/real-estate"},
]


def _configure_cjk_font_fallback() -> None:
    # Prefer macOS CJK fonts first; fallback to broadly available Unicode fonts.
    preferred = [
        "Hiragino Sans GB",
        "Songti SC",
        "STHeiti",
        "Heiti TC",
        "Arial Unicode MS",
        "PingFang HK",
        "Noto Sans CJK SC",
        "SimHei",
        "Microsoft YaHei",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    chain = [name for name in preferred if name in available]
    chain.append("DejaVu Sans")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = chain
    plt.rcParams["axes.unicode_minus"] = False


_configure_cjk_font_fallback()


THEME = {
    "bg": "#FFFFFF",
    "panel": "#F8FAFC",
    "grid": "#DFE6F1",
    "axis": "#CAD4E2",
    "text": "#1F2A44",
    "primary": "#2563EB",
    "secondary": "#60A5FA",
    "accent": "#F59E0B",
    "positive": "#16A34A",
    "negative": "#DC2626",
    "muted": "#94A3B8",
    "btc": "#F59E0B",
    "eth": "#3B82F6",
}

plt.rcParams.update(
    {
        "figure.facecolor": THEME["bg"],
        "axes.facecolor": THEME["panel"],
        "axes.edgecolor": THEME["axis"],
        "axes.labelcolor": THEME["text"],
        "axes.titlecolor": THEME["text"],
        "xtick.color": THEME["text"],
        "ytick.color": THEME["text"],
        "text.color": THEME["text"],
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.labelsize": 10,
        "axes.titleweight": "bold",
        "grid.color": THEME["grid"],
    }
)


@dataclass
class ExchangeRow:
    rank: Optional[int]
    name: str
    slug: str
    volume24h: Optional[float]
    pct24h: Optional[float]
    spot24h: Optional[float]
    deriv24h: Optional[float]


@dataclass
class DailyContext:
    target_date: date
    generated_at_shanghai: str
    market_as_of: Optional[str]
    market_lag_days: Optional[int]
    market_cap: Optional[float]
    prev_market_cap: Optional[float]
    volume_24h: Optional[float]
    prev_volume_24h: Optional[float]
    btc_dom: Optional[float]
    prev_btc_dom: Optional[float]
    market_history: List[Dict[str, Any]]
    breadth_snapshot: Dict[str, Any]
    top_assets: List[Dict[str, Any]]
    exchanges: List[ExchangeRow]
    deribit: Dict[str, Any]
    dvol: Dict[str, Any]
    dvol_history: Dict[str, List[Dict[str, Any]]]
    fng: Dict[str, Any]
    fng_series: List[Dict[str, Any]]
    top2_trend: Dict[str, Dict[str, Any]]
    top2_intraday: Dict[str, List[Dict[str, Any]]]
    nondefi_carry: List[Dict[str, Any]]
    borrow_rates: List[Dict[str, Any]]
    coingecko_capability: Dict[str, Any]
    stablecoin_yields: List[Dict[str, Any]]
    stablecoin_yields_extended: List[Dict[str, Any]]
    stablecoin_cefi_rates: List[Dict[str, Any]]
    rwa_asset_classes: List[Dict[str, Any]]
    rwa_token_movers: List[Dict[str, Any]]
    rwa_smartmoney: Dict[str, Any]
    taoli_binance_margin_rates: List[Dict[str, Any]]
    smartmoney_traders: List[Dict[str, Any]]
    smartmoney_signals: Dict[str, Dict[str, Any]]
    smartmoney_signal_attempted: bool
    smartmoney_positions: Dict[str, Any]
    okx_news_sentiment: Dict[str, Any]
    module_status: Dict[str, str]
    data_gaps: List[str]
    source_warnings: List[str]


def _safe_float(v: Any) -> Optional[float]:
    try:
        return float(v)
    except Exception:
        return None


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def _normalize_asset_symbol(v: Any) -> str:
    raw = str(v or "").upper().strip()
    if not raw:
        return ""
    norm = re.sub(r"[^A-Z0-9]", "", raw)
    aliases = {
        "USD0PP": "USD0",
        "USDCE": "USDC",
        "USDTE": "USDT",
    }
    return aliases.get(norm, norm)


def _fmt_usd(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    x = abs(v)
    if x >= 1e12:
        s = f"${x/1e12:.2f}T"
    elif x >= 1e9:
        s = f"${x/1e9:.2f}B"
    elif x >= 1e6:
        s = f"${x/1e6:.2f}M"
    else:
        s = f"${x:,.0f}"
    return f"-{s}" if v < 0 else s


def _fmt_pct(v: Optional[float], signed: bool = True) -> str:
    if v is None:
        return "N/A"
    return f"{v:+.2f}%" if signed else f"{v:.2f}%"


def _fmt_price_usd(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    return f"${v:,.2f}"


def _fmt_num(v: Optional[float], digits: int = 1) -> str:
    return "N/A" if v is None else f"{v:.{digits}f}"


def _trim_cn_sentence(s: str) -> str:
    return (s or "").strip().rstrip("。")


def _append_md_image(lines: List[str], alt: str, path: str) -> None:
    # Keep images in their own paragraph so GitBook does not collapse them
    # into left-right mixed layouts with the following text.
    lines.append(f"![{alt}]({path})")
    lines.append("")


def _dvol_regime(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    if v < 45:
        return "Complacency（低波动定价）"
    if v < 60:
        return "Neutral（中性波动定价）"
    return "Panic（高波动溢价）"


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _prefer_curl_transport() -> bool:
    configured = (os.getenv("CEX_HTTP_TRANSPORT") or "auto").strip().lower()
    if configured == "curl":
        return True
    if configured == "urllib":
        return False
    proxy_keys = ("https_proxy", "http_proxy", "all_proxy", "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY")
    return any((os.getenv(key) or "").strip() for key in proxy_keys)


def _curl_request(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    method: str = "GET",
    payload: Optional[Dict[str, Any]] = None,
) -> bytes:
    curl_bin = shutil.which("curl")
    if not curl_bin:
        raise RuntimeError("curl is unavailable")
    full = url if not params else f"{url}?{urlencode({k: v for k, v in params.items() if v is not None})}"
    cmd = [curl_bin, "--fail", "--silent", "--show-error", "--location", "--compressed", "--max-time", str(timeout), "--request", method]
    for key, value in (headers or {}).items():
        cmd.extend(["--header", f"{key}: {value}"])
    if payload is not None:
        cmd.extend(["--header", "Content-Type: application/json", "--data-binary", json.dumps(payload, separators=(",", ":"))])
    cmd.append(full)
    proc = subprocess.run(cmd, capture_output=True, timeout=timeout + 5, check=False)
    if proc.returncode != 0:
        message = proc.stderr.decode("utf-8", errors="ignore").strip() or f"curl exit {proc.returncode}"
        raise RuntimeError(message)
    return proc.stdout


def _http_get_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Any:
    from cex_daily_modules.mihomo_route import optional_url_route

    full = url if not params else f"{url}?{urlencode({k: v for k, v in params.items() if v is not None})}"
    req_headers = {
        "User-Agent": "cex-daily-secondary-orchestrator/1.0",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, identity",
    }
    if "coinmarketcap" in full:
        cmc_key = (os.getenv("CMC_API_KEY") or "").strip()
        if cmc_key:
            req_headers.setdefault("X-CMC_PRO_API_KEY", cmc_key)
    if headers:
        req_headers.update(headers)
    with optional_url_route(full):
        if _prefer_curl_transport():
            raw = _curl_request(full, headers=req_headers, timeout=timeout)
            return json.loads(raw.decode("utf-8"))
        req = Request(full, headers=req_headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                enc = (resp.headers.get("Content-Encoding") or "").lower()
                if enc == "gzip":
                    import gzip

                    raw = gzip.decompress(raw)
                elif enc == "deflate":
                    import zlib

                    raw = zlib.decompress(raw)
                return json.loads(raw.decode("utf-8"))
        except Exception as urllib_error:
            try:
                raw = _curl_request(full, headers=req_headers, timeout=timeout)
                return json.loads(raw.decode("utf-8"))
            except Exception as curl_error:
                raise RuntimeError(f"urllib={urllib_error}; curl={curl_error}") from curl_error


def _http_get_text(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> str:
    from cex_daily_modules.mihomo_route import optional_url_route

    full = url if not params else f"{url}?{urlencode({k: v for k, v in params.items() if v is not None})}"
    req_headers = {
        "User-Agent": "cex-daily-secondary-orchestrator/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, identity",
    }
    if headers:
        req_headers.update(headers)
    with optional_url_route(full):
        if _prefer_curl_transport():
            raw = _curl_request(full, headers=req_headers, timeout=timeout)
            return raw.decode("utf-8", errors="ignore")
        req = Request(full, headers=req_headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                enc = (resp.headers.get("Content-Encoding") or "").lower()
                if enc == "gzip":
                    import gzip

                    raw = gzip.decompress(raw)
                elif enc == "deflate":
                    import zlib

                    raw = zlib.decompress(raw)
                return raw.decode("utf-8", errors="ignore")
        except Exception as urllib_error:
            try:
                raw = _curl_request(full, headers=req_headers, timeout=timeout)
                return raw.decode("utf-8", errors="ignore")
            except Exception as curl_error:
                raise RuntimeError(f"urllib={urllib_error}; curl={curl_error}") from curl_error


def _http_get_json_retry(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    attempts: int = 3,
    backoff_sec: float = 1.2,
) -> Any:
    last_err: Optional[Exception] = None
    for i in range(max(1, attempts)):
        try:
            return _http_get_json(url, params=params, headers=headers, timeout=timeout)
        except Exception as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(backoff_sec * float(i + 1))
    if last_err is not None:
        raise last_err
    raise RuntimeError("unexpected retry failure")


def _http_post_json(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = 45) -> Any:
    from cex_daily_modules.mihomo_route import optional_url_route

    req_headers = {"User-Agent": "cex-daily-secondary-orchestrator/1.0", "Accept": "application/json", "Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    with optional_url_route(url):
        if _prefer_curl_transport():
            raw = _curl_request(url, headers=req_headers, timeout=timeout, method="POST", payload=payload)
            return json.loads(raw.decode("utf-8"))
        req = Request(url, data=json.dumps(payload).encode("utf-8"), headers=req_headers, method="POST")
        try:
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as urllib_error:
            try:
                raw = _curl_request(url, headers=req_headers, timeout=timeout, method="POST", payload=payload)
                return json.loads(raw.decode("utf-8"))
            except Exception as curl_error:
                raise RuntimeError(f"urllib={urllib_error}; curl={curl_error}") from curl_error


def _coingecko_auth_candidates(data_gaps: List[str]) -> Optional[List[Tuple[str, Dict[str, str], str]]]:
    key = (os.getenv("COINGECKO_API_KEY") or "").strip()
    if not key:
        return None

    tier = (os.getenv("COINGECKO_API_TIER") or "demo").strip().lower()
    pro = (CG_BASE_PRO, {"x-cg-pro-api-key": key}, "pro")
    demo = (CG_BASE_DEMO, {"x-cg-demo-api-key": key}, "demo")

    if tier == "demo":
        return [demo]
    if tier == "pro":
        return [pro]
    if tier == "auto":
        return [pro, demo]

    data_gaps.append(f"COINGECKO_API_TIER={tier} 非法，已按 demo 处理。")
    return [demo]


def _fetch_coinpaprika_top_assets() -> List[Dict[str, Any]]:
    payload = _http_get_json(COINPAPRIKA_TICKERS, {"quotes": "USD", "limit": "25"})
    rows: List[Dict[str, Any]] = []
    for item in payload if isinstance(payload, list) else []:
        if not isinstance(item, dict):
            continue
        rank = _safe_int(item.get("rank"))
        quote = ((item.get("quotes") or {}).get("USD") or {}) if isinstance(item.get("quotes"), dict) else {}
        if rank is None or rank < 1 or rank > 10 or not isinstance(quote, dict):
            continue
        rows.append(
            {
                "rank": rank,
                "symbol": str(item.get("symbol") or "").upper(),
                "name": str(item.get("name") or ""),
                "price": _safe_float(quote.get("price")),
                "mcap": _safe_float(quote.get("market_cap")),
                "chg24": _safe_float(quote.get("percent_change_24h")),
                "source": "CoinPaprika",
                "as_of": item.get("last_updated"),
            }
        )
    rows.sort(key=lambda row: int(row.get("rank") or 999))
    return rows[:10]


def _rpc(method: str, params: Dict[str, Any]) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": int(datetime.now(tz=timezone.utc).timestamp() * 1000) % 1_000_000_000,
        "method": method,
        "params": params,
    }
    try:
        out = _http_post_json(DERIBIT_RPC, payload, timeout=30)
    except Exception as post_error:
        try:
            out = _http_get_json(f"{DERIBIT_RPC}/{method}", params=params, timeout=30)
        except Exception as get_error:
            raise RuntimeError(f"Deribit POST={post_error}; GET={get_error}") from get_error
    if isinstance(out, dict) and out.get("error"):
        raise RuntimeError(str(out.get("error")))
    return out.get("result") if isinstance(out, dict) else None


def _fetch_market_day(target: date, data_gaps: List[str], lookback_days: int = 14) -> Dict[str, Any]:
    start = target - timedelta(days=max(lookback_days, 2))
    end = target + timedelta(days=1)
    try:
        payload = _http_get_json(
            CMC_GLOBAL_HIST,
            {
                "interval": "1d",
                "convertId": "2781",
                "timeStart": f"{start.isoformat()}T00:00:00.000Z",
                "timeEnd": f"{end.isoformat()}T00:00:00.000Z",
            },
        )
        quotes = ((payload.get("data") or {}).get("quotes") or []) if isinstance(payload, dict) else []
        by_day: Dict[date, Dict[str, Optional[float]]] = {}
        for q in quotes:
            if not isinstance(q, dict):
                continue
            ts = q.get("timestamp")
            if not isinstance(ts, str):
                continue
            try:
                d = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
            except Exception:
                continue
            qq = q.get("quote")
            qq0 = qq[0] if isinstance(qq, list) and qq and isinstance(qq[0], dict) else {}
            mc = _safe_float(qq0.get("totalMarketCap"))
            vol = _safe_float(qq0.get("totalVolume24H"))
            dom = _safe_float(q.get("btcDominance"))
            by_day[d] = {"mc": mc, "vol": vol, "dom": dom}

        available_days = sorted(d for d in by_day if d <= target)
        selected_day = available_days[-1] if available_days else None
        lag_days = (target - selected_day).days if selected_day else None
        if lag_days is not None and lag_days > 2:
            selected_day = None
            lag_days = None
        previous_days = [d for d in available_days if selected_day is not None and d < selected_day]
        previous_day = previous_days[-1] if previous_days else None
        t = by_day.get(selected_day) if selected_day else None
        p = by_day.get(previous_day) if previous_day else None
        hist: List[Dict[str, Any]] = []
        for d in sorted(by_day.keys()):
            if d < target - timedelta(days=lookback_days - 1) or d > target:
                continue
            row = by_day[d]
            hist.append({"date": d, "market_cap": row.get("mc"), "volume_24h": row.get("vol"), "btc_dom": row.get("dom")})
        return {
            "as_of": selected_day.isoformat() if selected_day else None,
            "lag_days": lag_days,
            "market_cap": t.get("mc") if t else None,
            "prev_market_cap": p.get("mc") if p else None,
            "volume_24h": t.get("vol") if t else None,
            "prev_volume_24h": p.get("vol") if p else None,
            "btc_dom": t.get("dom") if t else None,
            "prev_btc_dom": p.get("dom") if p else None,
            "history": hist,
        }
    except Exception as e:
        data_gaps.append(f"CMC 全市场历史数据获取失败: {e}")
        return {
            "as_of": None,
            "lag_days": None,
            "market_cap": None,
            "prev_market_cap": None,
            "volume_24h": None,
            "prev_volume_24h": None,
            "btc_dom": None,
            "prev_btc_dom": None,
            "history": [],
        }


def _fetch_top_assets(data_gaps: List[str]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    configured_tier = (os.getenv("COINGECKO_API_TIER") or "demo").strip().lower()
    capability: Dict[str, Any] = {
        "status": "unknown",
        "configured_tier": configured_tier,
        "attempted": [],
        "used": None,
        "endpoint": "/coins/markets",
        "key_required": True,
        "key_present": False,
        "errors": [],
    }
    candidates = _coingecko_auth_candidates(data_gaps)
    if candidates is None:
        capability["status"] = "fallback_pending"
        capability["errors"] = ["COINGECKO_API_KEY is not configured"]
        try:
            fallback_rows = _fetch_coinpaprika_top_assets()
            if fallback_rows:
                capability.update(
                    {
                        "status": "fallback",
                        "used": "coinpaprika",
                        "fallback_provider": "CoinPaprika",
                        "fallback_endpoint": "/v1/tickers",
                    }
                )
                return fallback_rows, capability
            capability["errors"].append("CoinPaprika: empty response")
        except Exception as e:
            capability["errors"].append(f"CoinPaprika: {e}")
        capability["status"] = "failed"
        data_gaps.append(f"Top10 资产数据获取失败：{' | '.join(capability['errors'])}")
        return [], capability
    capability["key_present"] = True
    capability["attempted"] = [c[2] for c in candidates]
    errs: List[str] = []
    for base, headers, tier in candidates:
        try:
            arr = _http_get_json(
                f"{base}/coins/markets",
                {
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": "10",
                    "page": "1",
                    "sparkline": "false",
                    "price_change_percentage": "24h",
                },
                headers=headers,
            )
            out: List[Dict[str, Any]] = []
            if isinstance(arr, list):
                for x in arr:
                    if not isinstance(x, dict):
                        continue
                    out.append(
                        {
                            "symbol": str(x.get("symbol") or "").upper(),
                            "name": str(x.get("name") or ""),
                            "price": _safe_float(x.get("current_price")),
                            "mcap": _safe_float(x.get("market_cap")),
                            "chg24": _safe_float(x.get("price_change_percentage_24h_in_currency") or x.get("price_change_percentage_24h")),
                            "source": f"CoinGecko {tier}",
                        }
                    )
            if out:
                capability["status"] = "ok"
                capability["used"] = tier
                return out, capability
            errs.append(f"{tier}: empty response")
        except Exception as e:
            errs.append(f"{tier}: {e}")

    capability["errors"] = errs
    try:
        fallback_rows = _fetch_coinpaprika_top_assets()
        if fallback_rows:
            capability.update(
                {
                    "status": "fallback",
                    "used": "coinpaprika",
                    "fallback_provider": "CoinPaprika",
                    "fallback_endpoint": "/v1/tickers",
                }
            )
            return fallback_rows, capability
        errs.append("CoinPaprika: empty response")
    except Exception as e:
        errs.append(f"CoinPaprika: {e}")
    capability["status"] = "failed"
    capability["errors"] = errs
    data_gaps.append(f"Top10 资产数据获取失败：{' | '.join(errs)}")
    return [], capability


def _fetch_exchanges(data_gaps: List[str]) -> List[ExchangeRow]:
    try:
        payload = _http_get_json(CMC_EXCHANGE_QUOTES, {"slug": ",".join(EXCHANGE_SLUGS), "convert": "USD"})
        data = payload.get("data") if isinstance(payload, dict) else []
        rows: List[ExchangeRow] = []
        for item in data if isinstance(data, list) else []:
            if not isinstance(item, dict):
                continue
            q = {}
            quote = item.get("quote")
            if isinstance(quote, list) and quote and isinstance(quote[0], dict):
                q = quote[0]
            rows.append(
                ExchangeRow(
                    rank=_safe_int(item.get("rank")),
                    name=str(item.get("name") or ""),
                    slug=str(item.get("slug") or ""),
                    volume24h=_safe_float(q.get("volume24h")),
                    pct24h=_safe_float(q.get("percentChangeVolume24h")),
                    spot24h=_safe_float(q.get("spotVolumeUsd")),
                    deriv24h=_safe_float(q.get("derivativeVolumeUsd")),
                )
            )
        rows.sort(key=lambda r: (r.rank is None, r.rank if r.rank is not None else 9999, r.name))
        return rows
    except Exception as e:
        data_gaps.append(f"CMC 交易所报价数据获取失败: {e}")
        return []


def _is_risk_breadth_asset(row: Dict[str, Any]) -> bool:
    symbol = str(row.get("symbol") or "").upper()
    name = str(row.get("name") or "").lower()
    if symbol in RISK_BREADTH_EXCLUDED_SYMBOLS:
        return False
    return not any(marker in name for marker in ("stablecoin", "staked ether", "wrapped steth", "heloc"))


def _build_breadth_snapshot(total_market_cap: Optional[float], btc_dom: Optional[float], top_assets: List[Dict[str, Any]]) -> Dict[str, Any]:
    risk_assets = [x for x in top_assets if _is_risk_breadth_asset(x)]
    excluded = [str(x.get("symbol") or "").upper() for x in top_assets if not _is_risk_breadth_asset(x)]
    metadata: Dict[str, Any] = {
        "definition": "market_cap_concentration_top10_including_stable_and_staked_assets",
        "risk_breadth_definition": "top_market_cap_directional_assets_excluding_stablecoins_staked_and_credit_mappings",
        "risk_asset_symbols": [str(x.get("symbol") or "").upper() for x in risk_assets],
        "risk_asset_count": len(risk_assets),
        "excluded_symbols": excluded,
    }
    if total_market_cap is None or total_market_cap <= 0:
        return metadata | {
            "top10_share": None,
            "outside_top10_share": None,
            "btc_share": btc_dom,
            "top2_to_10_share": None,
        }

    top10_sum = sum(float(x.get("mcap") or 0.0) for x in top_assets if x.get("mcap") is not None)
    top10_share = _clamp(top10_sum / total_market_cap * 100.0, 0.0, 100.0)
    outside = _clamp(100.0 - top10_share, 0.0, 100.0)
    btc_share = _clamp(float(btc_dom or 0.0), 0.0, 100.0)
    top2_10 = _clamp(100.0 - outside - btc_share, 0.0, 100.0)
    return metadata | {
        "top10_share": top10_share,
        "outside_top10_share": outside,
        "btc_share": btc_share,
        "top2_to_10_share": top2_10,
    }


def _fetch_okx_perp_snapshot(asset: str) -> Dict[str, Any]:
    inst_id = f"{asset.upper()}-USDT-SWAP"
    funding_payload = _http_get_json(OKX_FUNDING, {"instId": inst_id})
    oi_payload = _http_get_json(OKX_OPEN_INTEREST, {"instType": "SWAP", "instId": inst_id})
    funding_rows = funding_payload.get("data") if isinstance(funding_payload, dict) else []
    oi_rows = oi_payload.get("data") if isinstance(oi_payload, dict) else []
    funding_row = funding_rows[0] if isinstance(funding_rows, list) and funding_rows and isinstance(funding_rows[0], dict) else {}
    oi_row = oi_rows[0] if isinstance(oi_rows, list) and oi_rows and isinstance(oi_rows[0], dict) else {}
    funding = _safe_float(funding_row.get("fundingRate"))
    funding_time = _safe_int(funding_row.get("fundingTime"))
    prev_funding_time = _safe_int(funding_row.get("prevFundingTime"))
    if funding is not None and funding_time is not None and prev_funding_time is not None:
        interval_hours = (funding_time - prev_funding_time) / 3_600_000.0
        if not 7.5 <= interval_hours <= 8.5:
            funding = None
    return {
        "funding_8h": funding,
        "open_interest_usd": _safe_float(oi_row.get("oiUsd")),
        "as_of_ms": _safe_int(funding_row.get("ts") or oi_row.get("ts")),
        "source": "OKX public API",
        "instrument": inst_id,
    }


def _fetch_deribit(data_gaps: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "btc_funding_8h": None,
        "eth_funding_8h": None,
        "btc_open_interest": None,
        "eth_open_interest": None,
        "btc_source": None,
        "eth_source": None,
        "fallbacks": [],
        "source_errors": [],
    }
    for c, inst in [("btc", "BTC-PERPETUAL"), ("eth", "ETH-PERPETUAL")]:
        try:
            res = _rpc("public/ticker", {"instrument_name": inst}) or {}
            out[f"{c}_funding_8h"] = _safe_float(res.get("funding_8h"))
            out[f"{c}_open_interest"] = _safe_float(res.get("open_interest"))
            out[f"{c}_source"] = "Deribit public/ticker"
        except Exception as e:
            out["source_errors"].append(f"Deribit {inst}: {e}")
            try:
                fallback = _fetch_okx_perp_snapshot(c)
                out[f"{c}_funding_8h"] = fallback.get("funding_8h")
                out[f"{c}_open_interest"] = fallback.get("open_interest_usd")
                out[f"{c}_source"] = fallback.get("source")
                out["fallbacks"].append(
                    {
                        "metric": f"{c.upper()} perpetual funding/OI",
                        "provider": fallback.get("source"),
                        "instrument": fallback.get("instrument"),
                        "as_of_ms": fallback.get("as_of_ms"),
                    }
                )
                if out[f"{c}_funding_8h"] is None or out[f"{c}_open_interest"] is None:
                    raise RuntimeError("OKX fallback returned incomplete funding/OI")
            except Exception as fallback_error:
                data_gaps.append(f"{inst} funding/OI 获取失败：Deribit={e} | OKX fallback={fallback_error}")
    return out


def _fetch_dvol(target: date, data_gaps: List[str], lookback_days: int = 30) -> Tuple[Dict[str, Any], Dict[str, List[Dict[str, Any]]]]:
    out: Dict[str, Any] = {"btc_dvol_close": None, "eth_dvol_close": None, "btc_source": None, "eth_source": None}
    history: Dict[str, List[Dict[str, Any]]] = {"btc": [], "eth": []}
    start_day = target - timedelta(days=max(lookback_days - 1, 0))
    start_ts = int(datetime(start_day.year, start_day.month, start_day.day, tzinfo=timezone.utc).timestamp() * 1000)
    end_ts = int(datetime(target.year, target.month, target.day, 23, 59, 59, tzinfo=timezone.utc).timestamp() * 1000)

    for c in ["BTC", "ETH"]:
        try:
            result = _rpc(
                "public/get_volatility_index_data",
                {
                    "currency": c,
                    "start_timestamp": start_ts,
                    "end_timestamp": end_ts,
                    "resolution": 3600,
                },
            )
            data = result.get("data") if isinstance(result, dict) else []
            by_day_close: Dict[date, float] = {}
            for row in data if isinstance(data, list) else []:
                if not (isinstance(row, list) and len(row) >= 5 and isinstance(row[0], (int, float)) and isinstance(row[4], (int, float))):
                    continue
                d = datetime.fromtimestamp(float(row[0]) / 1000.0, tz=timezone.utc).date()
                by_day_close[d] = float(row[4])

            series = [{"date": d, "value": by_day_close[d]} for d in sorted(by_day_close.keys()) if start_day <= d <= target]
            history[c.lower()] = series
            if series:
                out[f"{c.lower()}_dvol_close"] = float(series[-1]["value"])
                out[f"{c.lower()}_source"] = "Deribit public/get_volatility_index_data"
            else:
                data_gaps.append(f"Deribit DVOL {c} 返回为空：未使用非等价波动率代理填充。")
        except Exception as e:
            data_gaps.append(f"Deribit DVOL {c} 获取失败: {e}")
    return out, history


def _run_okx_cli_json(args: List[str], data_gaps: List[str], tag: str) -> Optional[Any]:
    profile = os.getenv("OKX_PROFILE", "oauth").strip() or "oauth"
    cmd = ["okx", "--profile", profile] + args + ["--json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=25, check=False)
    except FileNotFoundError:
        data_gaps.append("OKX 聪明钱数据获取失败：未安装 okx CLI。")
        return None
    except Exception as e:
        data_gaps.append(f"OKX 聪明钱数据获取失败（{tag}）: {e}")
        return None
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        data_gaps.append(f"OKX 聪明钱数据获取失败（{tag}）: {err or 'unknown error'}")
        return None
    try:
        return json.loads(proc.stdout)
    except Exception as e:
        data_gaps.append(f"OKX 聪明钱数据解析失败（{tag}）: {e}")
        return None


def _fetch_okx_news_sentiment(data_gaps: List[str]) -> Dict[str, Any]:
    payload = _run_okx_cli_json(
        ["news", "coin-sentiment", "--coins", ",".join(OKX_SENTIMENT_COINS)],
        data_gaps,
        "news:coin-sentiment",
    )
    details = payload.get("details") if isinstance(payload, dict) else []
    details = details if isinstance(details, list) else []
    rows: List[Dict[str, Any]] = []
    for row in details:
        if not isinstance(row, dict):
            continue
        coin = str(row.get("coin") or "").upper().strip()
        if not coin:
            continue
        sentiment = row.get("sentiment") if isinstance(row.get("sentiment"), dict) else {}
        rows.append(
            {
                "coin": coin,
                "label": sentiment.get("label"),
                "bullish_ratio": _safe_float(sentiment.get("bullishRatio")),
                "bearish_ratio": _safe_float(sentiment.get("bearishRatio")),
                "mention_count": _safe_int(row.get("mentionCount")),
                "score": _safe_float(row.get("score")),
            }
        )
    rows.sort(key=lambda x: ((x.get("mention_count") or -1), (x.get("score") or -1.0)), reverse=True)
    if not rows:
        data_gaps.append("OKX 新闻情绪快照为空：coin-sentiment 未返回有效样本。")
    return {"rows": rows}


def _fetch_okx_smartmoney(
    data_gaps: List[str],
) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]], bool, Dict[str, Any]]:
    enabled = (os.getenv("OKX_SMARTMONEY_ENABLED", "0").strip() or "0").lower()
    if enabled in {"0", "false", "no", "off"}:
        return [], {}, False, {"trader_count": 0, "position_count": 0, "rows": []}
    traders_payload = _run_okx_cli_json(
        ["smartmoney", "traders", "--period", "30", "--sortType", "pnl", "--limit", str(OKX_SMARTMONEY_TOP_TRADERS)],
        data_gaps,
        "traders",
    )
    traders = traders_payload if isinstance(traders_payload, list) else []
    by_inst: Dict[str, Dict[str, Any]] = {}
    trader_count = 0
    for t in traders:
        if not isinstance(t, dict):
            continue
        author_id = t.get("authorId")
        if not author_id:
            continue
        detail = _run_okx_cli_json(["smartmoney", "trader", "--authorId", str(author_id)], data_gaps, f"trader:{author_id}")
        if not isinstance(detail, dict):
            continue
        positions = detail.get("positions") if isinstance(detail.get("positions"), list) else []
        trader_count += 1
        for p in positions:
            if not isinstance(p, dict):
                continue
            pos_data = p.get("posData") if isinstance(p.get("posData"), list) else []
            for slot in pos_data:
                if not isinstance(slot, dict):
                    continue
                inst_id = str(slot.get("instId") or "").strip()
                notional = _safe_float(slot.get("notionalUsd"))
                pos = _safe_float(slot.get("pos"))
                if not inst_id or notional is None or notional <= 0 or pos is None:
                    continue
                rec = by_inst.setdefault(
                    inst_id,
                    {"inst_id": inst_id, "long_usd": 0.0, "short_usd": 0.0, "net_usd": 0.0, "long_traders": 0, "short_traders": 0},
                )
                if pos >= 0:
                    rec["long_usd"] += notional
                    rec["long_traders"] += 1
                    rec["net_usd"] += notional
                else:
                    rec["short_usd"] += notional
                    rec["short_traders"] += 1
                    rec["net_usd"] -= notional
    position_rows = sorted(by_inst.values(), key=lambda x: abs(float(x.get("net_usd") or 0.0)), reverse=True)
    smartmoney_positions = {
        "trader_count": trader_count,
        "position_count": len(position_rows),
        "rows": position_rows,
    }
    fetch_signal = (os.getenv("OKX_SMARTMONEY_FETCH_SIGNAL", "0").strip() or "0").lower() in {"1", "true", "yes", "on"}
    if not fetch_signal:
        return traders, {}, False, smartmoney_positions
    signals: Dict[str, Dict[str, Any]] = {}
    for symbol, inst_id in OKX_SMARTMONEY_INSTS.items():
        payload = _run_okx_cli_json(["smartmoney", "signal", "--instId", inst_id], data_gaps, f"signal:{inst_id}")
        row: Optional[Dict[str, Any]] = None
        if isinstance(payload, list) and payload and isinstance(payload[0], dict):
            row = payload[0]
        elif isinstance(payload, dict):
            if isinstance(payload.get("data"), list) and payload.get("data") and isinstance(payload["data"][0], dict):
                row = payload["data"][0]
            elif isinstance(payload.get("data"), dict):
                row = payload["data"]
        if row:
            signals[symbol] = row
    return traders, signals, True, smartmoney_positions


def _fetch_fng(target: date, data_gaps: List[str], lookback_days: int = 30) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    out: Dict[str, Any] = {"value": None, "prev": None, "delta": None, "source": None, "fallback": False, "source_errors": []}
    by_day: Dict[date, int] = {}
    selected_day: Optional[date] = None
    try:
        payload = _http_get_json(ALT_FNG, {"limit": "120"})
        arr = payload.get("data") if isinstance(payload, dict) else []
        for row in arr if isinstance(arr, list) else []:
            if not isinstance(row, dict):
                continue
            ts = _safe_int(row.get("timestamp"))
            value = _safe_int(row.get("value"))
            if ts is None or value is None:
                continue
            by_day[datetime.fromtimestamp(ts, tz=timezone.utc).date()] = value
        candidates = [day for day in by_day if day <= target]
        selected_day = max(candidates) if candidates else None
        if selected_day is None or (target - selected_day).days > 2:
            raise RuntimeError(f"no observation within 2 days of {target.isoformat()}")
        out["source"] = "Alternative.me /fng/"
    except Exception as primary_error:
        out["source_errors"].append(f"Alternative.me: {primary_error}")
        by_day = {}
        start_day = target - timedelta(days=max(lookback_days + 3, 7))
        start_ts = int(datetime(start_day.year, start_day.month, start_day.day, tzinfo=timezone.utc).timestamp())
        end_ts = int(datetime(target.year, target.month, target.day, 23, 59, 59, tzinfo=timezone.utc).timestamp())
        try:
            payload = _http_get_json(CMC_FNG, {"start": str(start_ts), "end": str(end_ts)})
            arr = ((payload.get("data") or {}).get("dataList") or []) if isinstance(payload, dict) else []
            for row in arr if isinstance(arr, list) else []:
                if not isinstance(row, dict):
                    continue
                ts = _safe_int(row.get("timestamp"))
                value = _safe_int(row.get("score"))
                if ts is None or value is None:
                    continue
                by_day[datetime.fromtimestamp(ts, tz=timezone.utc).date()] = value
            candidates = [day for day in by_day if day <= target]
            selected_day = max(candidates) if candidates else None
            if selected_day is None or (target - selected_day).days > 2:
                raise RuntimeError(f"no observation within 2 days of {target.isoformat()}")
            out["source"] = "CoinMarketCap Fear & Greed fallback"
            out["fallback"] = True
        except Exception as fallback_error:
            out["source_errors"].append(f"CoinMarketCap: {fallback_error}")
            data_gaps.append(f"F&G 获取失败：{' | '.join(out['source_errors'])}")
            return out, []

    if selected_day is None:
        data_gaps.append("F&G 获取失败：未找到可用日期。")
        return out, []
    current = by_day.get(selected_day)
    previous = by_day.get(selected_day - timedelta(days=1))
    out["value"] = float(current) if current is not None else None
    out["prev"] = float(previous) if previous is not None else None
    out["delta"] = float(current - previous) if (current is not None and previous is not None) else None
    out["as_of"] = selected_day.isoformat()
    out["lag_days"] = (target - selected_day).days
    start_day = target - timedelta(days=max(lookback_days - 1, 0))
    series = [{"date": day, "value": float(by_day[day])} for day in sorted(by_day.keys()) if start_day <= day <= target]
    return out, series


def _classify_top2_24h(change_pct: Optional[float], range_pos_pct: Optional[float]) -> str:
    if change_pct is None:
        return "数据不足"
    if range_pos_pct is None:
        if change_pct <= -2.0:
            return "偏弱，下行主导"
        if change_pct <= -1.0:
            return "偏弱震荡"
        if change_pct >= 2.0:
            return "偏强，上行主导"
        if change_pct >= 1.0:
            return "偏强震荡"
        return "区间震荡"

    if change_pct <= -3.0 or (change_pct <= -2.0 and range_pos_pct <= 30.0):
        return "偏弱，下行主导"
    if change_pct <= -1.0:
        return "偏弱震荡"
    if change_pct >= 3.0 or (change_pct >= 2.0 and range_pos_pct >= 70.0):
        return "偏强，上行主导"
    if change_pct >= 1.0:
        return "偏强震荡"
    return "区间震荡"


def _fetch_top2_24h_trend(data_gaps: List[str]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    symbols = ["BTCUSDT", "ETHUSDT"]
    source_errors: List[str] = []

    def _ingest_row(row: Dict[str, Any], source: str) -> None:
        symbol = str(row.get("symbol") or "").upper()
        key = "BTC" if symbol == "BTCUSDT" else ("ETH" if symbol == "ETHUSDT" else None)
        if key is None:
            return
        price = _safe_float(row.get("lastPrice"))
        open_price = _safe_float(row.get("openPrice"))
        high = _safe_float(row.get("highPrice"))
        low = _safe_float(row.get("lowPrice"))
        change_pct = _safe_float(row.get("priceChangePercent"))
        range_pos_pct = None
        if price is not None and high is not None and low is not None and high > low:
            range_pos_pct = (price - low) / (high - low) * 100.0
        out[key] = {
            "symbol": symbol,
            "price": price,
            "open": open_price,
            "high": high,
            "low": low,
            "change_pct": change_pct,
            "range_pos_pct": range_pos_pct,
            "trend": _classify_top2_24h(change_pct, range_pos_pct),
            "source": source,
        }

    try:
        payload = _http_get_json(BINANCE_24H, {"symbols": json.dumps(symbols, separators=(",", ":"))})
        rows = payload if isinstance(payload, list) else []
        for row in rows:
            if isinstance(row, dict):
                _ingest_row(row, "Binance global")
    except Exception as e:
        source_errors.append(f"Binance global: {e}")

    for sym in symbols:
        key = "BTC" if sym == "BTCUSDT" else "ETH"
        if key in out:
            continue
        try:
            row = _http_get_json(BINANCE_US_24H, {"symbol": sym})
            if isinstance(row, dict):
                _ingest_row(row, "Binance.US fallback")
        except Exception as e:
            source_errors.append(f"Binance.US {sym}: {e}")

    for sym in symbols:
        key = "BTC" if sym == "BTCUSDT" else "ETH"
        if key not in out:
            try:
                row = _http_get_json(BINANCE_24H, {"symbol": sym})
                if isinstance(row, dict):
                    _ingest_row(row, "Binance global single-symbol retry")
            except Exception as e:
                source_errors.append(f"Binance global {sym}: {e}")
        if key not in out:
            data_gaps.append(f"{sym} 24h 行情获取失败：{' | '.join(source_errors)}")
    return out


def _fetch_top2_1h_series(target: date, data_gaps: List[str], hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {"BTC": [], "ETH": []}
    now_utc = datetime.now(tz=timezone.utc)
    target_end = datetime(target.year, target.month, target.day, 23, 59, 59, tzinfo=timezone.utc)
    end_dt = target_end if target_end < now_utc else now_utc
    end_ms = int(end_dt.timestamp() * 1000)
    start_ms = int((end_dt - timedelta(hours=max(hours - 1, 1))).timestamp() * 1000)
    symbols = {"BTC": "BTCUSDT", "ETH": "ETHUSDT"}

    for asset, symbol in symbols.items():
        errors: List[str] = []
        for endpoint, source in [(BINANCE_KLINES, "Binance global"), (BINANCE_US_KLINES, "Binance.US fallback")]:
            try:
                rows = _http_get_json(
                    endpoint,
                    {
                        "symbol": symbol,
                        "interval": "1h",
                        "startTime": start_ms,
                        "endTime": end_ms,
                        "limit": str(max(hours + 8, 32)),
                    },
                )
            except Exception as e:
                errors.append(f"{source}: {e}")
                continue
            series: List[Dict[str, Any]] = []
            for row in rows if isinstance(rows, list) else []:
                if not (isinstance(row, list) and len(row) >= 5):
                    continue
                ts = _safe_int(row[0])
                if ts is None:
                    continue
                dt = datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
                if dt.timestamp() * 1000 < start_ms or dt.timestamp() * 1000 > end_ms:
                    continue
                series.append(
                    {
                        "ts": dt,
                        "open": _safe_float(row[1]),
                        "high": _safe_float(row[2]),
                        "low": _safe_float(row[3]),
                        "close": _safe_float(row[4]),
                        "source": source,
                    }
                )
            series.sort(key=lambda x: x.get("ts") or datetime.min.replace(tzinfo=timezone.utc))
            if len(series) >= 2:
                out[asset] = series[-hours:]
                break
            errors.append(f"{source}: insufficient rows ({len(series)})")
        if len(out[asset]) < 2:
            data_gaps.append(f"{symbol} 1h K线获取失败：{' | '.join(errors)}")
    return out


def _parse_ms(v: Any) -> Optional[int]:
    i = _safe_int(v)
    if i is None:
        return None
    # Normalize seconds timestamps to ms
    if i < 10_000_000_000:
        return i * 1000
    return i


def _fetch_nondefi_carry(data_gaps: List[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    assets = ["BTC", "ETH"]

    # Binance: spot 24h + futures premium/funding + OI
    for a in assets:
        sym = f"{a}USDT"
        try:
            spot_row = _http_get_json(BINANCE_24H, {"symbol": sym})
            prem_row = _http_get_json(BINANCE_FAPI_PREMIUM_INDEX, {"symbol": sym})
            oi_row = _http_get_json(BINANCE_FAPI_OPEN_INTEREST, {"symbol": sym})

            spot = _safe_float((spot_row or {}).get("lastPrice") if isinstance(spot_row, dict) else None)
            index = _safe_float((prem_row or {}).get("indexPrice") if isinstance(prem_row, dict) else None)
            mark = _safe_float((prem_row or {}).get("markPrice") if isinstance(prem_row, dict) else None)
            funding = _safe_float((prem_row or {}).get("lastFundingRate") if isinstance(prem_row, dict) else None)
            oi = _safe_float((oi_row or {}).get("openInterest") if isinstance(oi_row, dict) else None)
            basis_pct = ((mark - index) / index * 100.0) if (mark is not None and index and index != 0) else None
            # Binance USDT perpetual funding interval is typically 8h.
            annual_funding_pct = funding * 3.0 * 365.0 * 100.0 if funding is not None else None
            out.append(
                {
                    "exchange": "Binance",
                    "asset": a,
                    "spot_price": spot,
                    "index_price": index,
                    "mark_price": mark,
                    "funding_rate_pct": funding * 100.0 if funding is not None else None,
                    "funding_interval_hours": 8.0,
                    "annual_funding_pct": annual_funding_pct,
                    "basis_pct": basis_pct,
                    "open_interest_contracts": oi,
                    "quote_ccy": "USDT",
                }
            )
        except Exception as e:
            data_gaps.append(f"Binance 非DeFi期现数据获取失败 {a}: {e}")

    # OKX: spot ticker + swap ticker + funding + OI
    for a in assets:
        spot_inst = f"{a}-USDT"
        swap_inst = f"{a}-USDT-SWAP"
        try:
            spot_payload = _http_get_json(OKX_TICKER, {"instId": spot_inst})
            swap_payload = _http_get_json(OKX_TICKER, {"instId": swap_inst})
            fund_payload = _http_get_json(OKX_FUNDING, {"instId": swap_inst})
            oi_payload = _http_get_json(OKX_OPEN_INTEREST, {"instType": "SWAP", "instId": swap_inst})

            spot_data = (spot_payload.get("data") or [None])[0] if isinstance(spot_payload, dict) else None
            swap_data = (swap_payload.get("data") or [None])[0] if isinstance(swap_payload, dict) else None
            fund_data = (fund_payload.get("data") or [None])[0] if isinstance(fund_payload, dict) else None
            oi_data = (oi_payload.get("data") or [None])[0] if isinstance(oi_payload, dict) else None

            spot = _safe_float((spot_data or {}).get("last") if isinstance(spot_data, dict) else None)
            mark = _safe_float((swap_data or {}).get("last") if isinstance(swap_data, dict) else None)
            index = _safe_float((swap_data or {}).get("idxPx") if isinstance(swap_data, dict) else None)
            funding = _safe_float((fund_data or {}).get("fundingRate") if isinstance(fund_data, dict) else None)
            f_time = _parse_ms((fund_data or {}).get("fundingTime") if isinstance(fund_data, dict) else None)
            n_time = _parse_ms((fund_data or {}).get("nextFundingTime") if isinstance(fund_data, dict) else None)
            interval_h = ((n_time - f_time) / 3_600_000.0) if (f_time is not None and n_time is not None and n_time > f_time) else 8.0
            annual_funding_pct = funding * (24.0 / interval_h) * 365.0 * 100.0 if (funding is not None and interval_h > 0) else None
            basis_pct = ((mark - index) / index * 100.0) if (mark is not None and index and index != 0) else None
            oi = _safe_float((oi_data or {}).get("oiCcy") if isinstance(oi_data, dict) else None)

            out.append(
                {
                    "exchange": "OKX",
                    "asset": a,
                    "spot_price": spot,
                    "index_price": index,
                    "mark_price": mark,
                    "funding_rate_pct": funding * 100.0 if funding is not None else None,
                    "funding_interval_hours": interval_h,
                    "annual_funding_pct": annual_funding_pct,
                    "basis_pct": basis_pct,
                    "open_interest_contracts": oi,
                    "quote_ccy": "USDT",
                }
            )
        except Exception as e:
            data_gaps.append(f"OKX 非DeFi期现数据获取失败 {a}: {e}")

    if not out:
        data_gaps.append("非DeFi期现数据为空：未获取到 Binance/OKX 的可用样本。")
    return out


def _extract_rwa_next_data(html: str) -> Dict[str, Any]:
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except Exception:
        return {}


def _metric_pct(v: Any) -> Optional[float]:
    x = _safe_float(v)
    if x is None:
        return None
    return x * 100.0 if abs(x) <= 1.0 else x


def _fetch_rwa_asset_classes(data_gaps: List[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in RWA_PUBLIC_ASSET_CLASSES:
        url = str(spec["source"])
        try:
            html = _http_get_text(url, timeout=35)
            payload = _extract_rwa_next_data(html)
            page_props = ((payload.get("props") or {}).get("pageProps") or {}) if isinstance(payload, dict) else {}
            aggregates = page_props.get("aggregates") if isinstance(page_props, dict) else None
            primary = (aggregates or [None])[0] if isinstance(aggregates, list) and aggregates else None
            if not isinstance(primary, dict):
                raise ValueError("missing pageProps.aggregates[0]")

            value = _safe_float(primary.get("value"))
            change_7d = _metric_pct(((primary.get("percentChange") or {}) if isinstance(primary.get("percentChange"), dict) else {}).get("value"))
            as_of = None
            reviewed = re.search(r'"lastReviewed"\s*:\s*"([^"]+)"', html)
            if reviewed:
                as_of = reviewed.group(1)[:10]

            if value is None:
                raise ValueError("missing aggregate value")
            rows.append(
                {
                    "asset_class": spec["asset_class"],
                    "value_usd": value,
                    "change_7d_pct": change_7d,
                    "as_of": as_of,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "freshness_status": "source_dated" if as_of else "source_date_unavailable",
                    "source": url,
                    "source_type": "RWA.xyz public page (undocumented page payload)",
                }
            )
        except Exception as e:
            data_gaps.append(f"RWA.xyz {spec['asset_class']} 快照获取失败: {e}")

    rows.sort(key=lambda r: float(r.get("value_usd") or 0.0), reverse=True)
    if not rows:
        data_gaps.append("RWA 资产类别快照为空：RWA.xyz 公开页未返回可解析数据。")
    return rows


def _rsi14(closes: List[float]) -> Optional[float]:
    if len(closes) < 15:
        return None
    diffs = [closes[i] - closes[i - 1] for i in range(len(closes) - 14, len(closes))]
    gains = sum(max(x, 0.0) for x in diffs) / 14.0
    losses = sum(max(-x, 0.0) for x in diffs) / 14.0
    if losses == 0:
        return 100.0 if gains > 0 else 50.0
    return 100.0 - 100.0 / (1.0 + gains / losses)


def _fetch_binance_smart_money_signals(
    chain_ids: set[str], headers: Dict[str, str], data_gaps: List[str]
) -> Dict[str, Dict[str, Any]]:
    """Fetch public Binance Web3 signals without coupling collection to a wallet login."""
    coverage: Dict[str, Dict[str, Any]] = {}
    for chain_id in sorted(chain_ids):
        if chain_id not in BINANCE_SMART_MONEY_CHAINS:
            coverage[chain_id] = {"status": "unsupported_chain", "signals": {}}
            continue
        try:
            payload = _http_post_json(
                BINANCE_SMART_MONEY_SIGNAL,
                {"smartSignalType": "", "page": 1, "pageSize": 100, "chainId": chain_id},
                headers=headers,
                timeout=20,
            )
            if not isinstance(payload, dict) or payload.get("success") is False:
                raise RuntimeError(str(payload.get("message") or payload.get("messageDetail") or "invalid response"))
            by_address: Dict[str, Dict[str, Any]] = {}
            for signal in payload.get("data") or []:
                if not isinstance(signal, dict):
                    continue
                address = str(signal.get("contractAddress") or "").lower()
                if address:
                    by_address[address] = signal
            coverage[chain_id] = {"status": "available", "signals": by_address}
        except Exception as exc:
            coverage[chain_id] = {"status": "source_unavailable", "signals": {}}
            data_gaps.append(
                f"Binance Web3 {BINANCE_SMART_MONEY_CHAINS[chain_id]} 聪明钱信号获取失败: {exc}"
            )
    return coverage


def _fetch_rwa_token_movers(target: date, data_gaps: List[str]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Screen a focused tokenized-equity universe, then enrich the largest movers."""
    raw_watchlist = os.getenv("RWA_EQUITY_TICKERS") or ",".join(DEFAULT_RWA_EQUITY_WATCHLIST)
    watchlist = {x.strip().upper() for x in raw_watchlist.split(",") if x.strip()}
    try:
        payload = _http_get_json(BINANCE_RWA_STOCK_LIST, params={"type": 1}, timeout=30)
        universe = payload.get("data") or []
    except Exception as e:
        data_gaps.append(f"RWA tokenized stocks 列表获取失败: {e}")
        return [], {"source": "Binance Web3 Smart Money", "covered_assets": 0, "active_signals": 0, "rows": []}

    # Prefer BSC because the on-chain flow endpoint and smart-money holder fields support it.
    selected: Dict[str, Dict[str, Any]] = {}
    for item in universe:
        ticker = str(item.get("ticker") or "").upper()
        if ticker not in watchlist:
            continue
        old = selected.get(ticker)
        if old is None or (str(item.get("chainId")) == "56" and str(old.get("chainId")) != "56"):
            selected[ticker] = item

    screened: List[Dict[str, Any]] = []
    headers = {"User-Agent": "binance-web3/1.1 (Skill)", "Accept-Encoding": "identity"}
    for ticker, item in selected.items():
        chain_id = str(item.get("chainId") or "")
        address = str(item.get("contractAddress") or "")
        try:
            dynamic = _http_get_json(
                BINANCE_RWA_DYNAMIC,
                params={"chainId": chain_id, "contractAddress": address},
                headers=headers,
                timeout=15,
            ).get("data") or {}
            token = dynamic.get("tokenInfo") or {}
            stock = dynamic.get("stockInfo") or {}
            status = dynamic.get("statusInfo") or {}
            token_multiplier = _safe_float(token.get("sharesMultiplier"))
            item_multiplier = _safe_float(item.get("multiplier"))
            multiplier = token_multiplier if token_multiplier is not None and token_multiplier > 0 else item_multiplier
            if multiplier is not None and multiplier <= 0:
                multiplier = None
            token_price = _safe_float(token.get("price"))
            stock_price = _safe_float(stock.get("price"))
            reference_price = token_price / multiplier if token_price is not None and multiplier else None
            market_status = str(status.get("marketStatus") or "").lower()
            premium_is_live = market_status in {"trading", "open"}
            premium = ((reference_price / stock_price - 1.0) * 100.0) if premium_is_live and reference_price and stock_price else None
            if not premium_is_live:
                premium_status = "unavailable_reference_frozen"
            elif multiplier is None:
                premium_status = "unavailable_multiplier"
            elif premium is None:
                premium_status = "unavailable_price"
            else:
                premium_status = "live"
            screened.append({
                "ticker": ticker,
                "symbol": dynamic.get("symbol") or item.get("symbol"),
                "chain_id": chain_id,
                "contract_address": address,
                "price_usd": token_price,
                "change_24h_pct": _safe_float(token.get("priceChangePct24h")),
                "holders": _safe_int(token.get("totalHolders")),
                "market_cap_usd": _safe_float(token.get("marketCap")),
                "shares_multiplier": multiplier,
                "shares_multiplier_source": (
                    "dynamic.tokenInfo.sharesMultiplier" if token_multiplier is not None and token_multiplier > 0
                    else "stock_list.multiplier" if item_multiplier is not None and item_multiplier > 0
                    else None
                ),
                "stock_price_usd": stock_price,
                "reference_price_usd": reference_price,
                "premium_pct": premium,
                "premium_status": premium_status,
                "market_status": status.get("marketStatus"),
                "reason_code": status.get("reasonCode"),
                "reason_msg": status.get("reasonMsg"),
                "pe_ttm": _safe_float(stock.get("priceToEarnings")),
                "kline_1h": [],
            })
        except Exception as e:
            data_gaps.append(f"RWA {ticker} 行情获取失败: {e}")

    screened.sort(key=lambda r: abs(float(r.get("change_24h_pct") or 0.0)), reverse=True)
    movers = screened[:5]
    smart_coverage = _fetch_binance_smart_money_signals(
        {str(row.get("chain_id") or "") for row in movers}, headers, data_gaps
    )
    for row in movers:
        chain_id = str(row["chain_id"])
        address = str(row["contract_address"])
        chain_coverage = smart_coverage.get(chain_id) or {"status": "unsupported_chain", "signals": {}}
        signal = (chain_coverage.get("signals") or {}).get(address.lower())
        if signal:
            signal_coverage = "active_signal"
        elif chain_coverage.get("status") == "available":
            signal_coverage = "no_matching_signal"
        else:
            signal_coverage = str(chain_coverage.get("status") or "source_unavailable")
        row.update({
            "smart_signal_source": "Binance Web3 Smart Money",
            "smart_signal_coverage": signal_coverage,
            "smart_signal_direction": signal.get("direction") if signal else None,
            "smart_signal_count": _safe_int(signal.get("smartMoneyCount")) if signal else None,
            "smart_signal_value_usd": _safe_float(signal.get("totalTokenValue")) if signal else None,
            "smart_signal_time_ms": _safe_int(signal.get("signalTriggerTime")) if signal else None,
            "smart_signal_status": signal.get("status") if signal else None,
        })
        try:
            kpayload = _http_get_json(
                BINANCE_RWA_KLINE,
                params={"chainId": chain_id, "contractAddress": address, "interval": "1h", "limit": 48},
                headers=headers,
                timeout=20,
            )
            candles = ((kpayload.get("data") or {}).get("klineInfos") or [])
            series = [
                {"timestamp_ms": _safe_int(x[0]), "open": _safe_float(x[1]), "high": _safe_float(x[2]), "low": _safe_float(x[3]), "close": _safe_float(x[4])}
                for x in candles if isinstance(x, list) and len(x) >= 5 and _safe_float(x[4]) is not None
            ]
            closes = [float(x["close"]) for x in series]
            row["kline_1h"] = series
            row["rsi14"] = _rsi14(closes)
            row["sma6"] = sum(closes[-6:]) / 6.0 if len(closes) >= 6 else None
            row["sma24"] = sum(closes[-24:]) / 24.0 if len(closes) >= 24 else None
            row["range_24h_pct"] = ((max(closes[-24:]) / min(closes[-24:]) - 1.0) * 100.0) if len(closes) >= 24 and min(closes[-24:]) > 0 else None
        except Exception as e:
            data_gaps.append(f"RWA {row['ticker']} 1h K线获取失败: {e}")

        if chain_id == "56":
            try:
                flow = _http_get_json(
                    BINANCE_TOKEN_DYNAMIC,
                    params={"chainId": chain_id, "contractAddress": address},
                    headers=headers,
                    timeout=20,
                ).get("data") or {}
                raw_volume = _safe_float(flow.get("volume24h"))
                raw_buy = _safe_float(flow.get("volume24hBuy"))
                raw_sell = _safe_float(flow.get("volume24hSell"))
                market_cap = _safe_float(row.get("market_cap_usd"))
                components_match = (
                    raw_volume is not None and raw_volume >= 0
                    and raw_buy is not None and raw_buy >= 0
                    and raw_sell is not None and raw_sell >= 0
                    and (raw_volume == 0 or 0.5 <= (raw_buy + raw_sell) / raw_volume <= 2.0)
                )
                plausible_scale = not (
                    raw_volume is not None and market_cap is not None and market_cap > 0
                    and raw_volume / market_cap > 50.0
                )
                flow_units_validated = bool(components_match and plausible_scale)
                flow_status = "validated_internal_consistency" if flow_units_validated else "raw_unit_unverified"
                anomaly_reason = None
                if not plausible_scale:
                    flow_status = "anomalous_scale"
                    anomaly_reason = "reported_volume_exceeds_50x_market_cap"
                elif raw_volume is not None and raw_volume > 0 and raw_buy == 0 and raw_sell == 0:
                    anomaly_reason = "positive_volume_with_zero_buy_sell_components"
                row.update({
                    "onchain_volume_24h_raw": raw_volume,
                    "buy_volume_24h_raw": raw_buy,
                    "sell_volume_24h_raw": raw_sell,
                    "flow_unit_status": flow_status,
                    "flow_anomaly_reason": anomaly_reason,
                    "onchain_volume_24h_usd": raw_volume if flow_units_validated else None,
                    "buy_volume_24h_usd": raw_buy if flow_units_validated else None,
                    "sell_volume_24h_usd": raw_sell if flow_units_validated else None,
                    "net_buy_24h_usd": (raw_buy - raw_sell) if flow_units_validated else None,
                    "liquidity_usd": _safe_float(flow.get("liquidity")),
                    "top10_holders_pct": _safe_float(flow.get("top10HoldersPercentage")),
                    "smart_money_holders": _safe_int(flow.get("smartMoneyHolders")),
                    "smart_money_holding_pct": _safe_float(flow.get("smartMoneyHoldingPercent")),
                })
            except Exception as e:
                data_gaps.append(f"RWA {row['ticker']} 链上流向获取失败: {e}")
    coverage_rows = [
        {
            "ticker": row.get("ticker"),
            "chain_id": row.get("chain_id"),
            "contract_address": row.get("contract_address"),
            "coverage_status": row.get("smart_signal_coverage"),
            "direction": row.get("smart_signal_direction"),
            "smart_money_count": row.get("smart_signal_count"),
            "total_value_usd": row.get("smart_signal_value_usd"),
            "signal_time_ms": row.get("smart_signal_time_ms"),
            "signal_status": row.get("smart_signal_status"),
        }
        for row in movers
    ]
    return movers, {
        "source": "Binance Web3 Smart Money",
        "auth": "public_no_wallet_auth",
        "agentic_wallet_role": "account_monitoring_and_execution_only",
        "covered_assets": sum(1 for row in coverage_rows if row["coverage_status"] in {"active_signal", "no_matching_signal"}),
        "active_signals": sum(1 for row in coverage_rows if row["coverage_status"] == "active_signal"),
        "rows": coverage_rows,
    }


def _kucoin_signed_headers(api_path: str) -> Optional[Dict[str, str]]:
    key = (os.getenv("KUCOIN_API_KEY") or "").strip()
    secret = (os.getenv("KUCOIN_API_SECRET") or "").strip()
    passphrase = (os.getenv("KUCOIN_API_PASSPHRASE") or "").strip()
    if not (key and secret and passphrase):
        return None
    ts = str(int(time.time() * 1000))
    prehash = f"{ts}GET{api_path}"
    sign = base64.b64encode(hmac.new(secret.encode("utf-8"), prehash.encode("utf-8"), hashlib.sha256).digest()).decode("utf-8")
    pass_sig = base64.b64encode(hmac.new(secret.encode("utf-8"), passphrase.encode("utf-8"), hashlib.sha256).digest()).decode("utf-8")
    return {
        "KC-API-KEY": key,
        "KC-API-SIGN": sign,
        "KC-API-TIMESTAMP": ts,
        "KC-API-PASSPHRASE": pass_sig,
        "KC-API-KEY-VERSION": (os.getenv("KUCOIN_API_KEY_VERSION") or "2").strip(),
    }


def _fetch_borrow_rates(data_gaps: List[str]) -> List[Dict[str, Any]]:
    target_assets = ["USDT", "USDC", "DAI", "USDE", "BTC", "ETH"]
    asset_rank = {a: i for i, a in enumerate(target_assets)}
    source_rank = {"Binance": 1, "OKX": 2, "Bybit": 3, "Backpack": 4, "KuCoin": 5}
    out: List[Dict[str, Any]] = []
    errors: List[str] = []

    def _append(source: str, asset: str, daily_rate: Optional[float], borrow_limit: Optional[float], tier: str, rate_basis: str) -> None:
        if daily_rate is None:
            return
        if borrow_limit is not None and borrow_limit <= 0:
            return
        out.append(
            {
                "source": source,
                "asset": asset,
                "daily_rate_pct": daily_rate * 100.0,
                "annual_rate_pct": daily_rate * 365.0 * 100.0,
                "borrow_limit": borrow_limit,
                "tier": tier,
                "rate_basis": rate_basis,
                "updated_at": datetime.now(tz=timezone.utc).isoformat(),
            }
        )

    # Binance VIP0 daily borrow rates.
    try:
        payload = _http_get_json(BINANCE_MARGIN_INFO, timeout=45)
        rows = payload.get("data") if isinstance(payload, dict) else []
        for asset in target_assets:
            row = next((r for r in rows if isinstance(r, dict) and str(r.get("assetName") or "").upper() == asset), None)
            if not row:
                continue
            specs = row.get("specs") if isinstance(row.get("specs"), list) else []
            vip0 = next((s for s in specs if isinstance(s, dict) and str(s.get("vipLevel") or "") == "0"), None)
            if not isinstance(vip0, dict):
                continue
            _append(
                "Binance",
                asset,
                _safe_float(vip0.get("dailyInterestRate")),
                _safe_float(vip0.get("borrowLimit")),
                "VIP0",
                "daily",
            )
    except Exception as e:
        errors.append(f"Binance: {e}")

    # OKX public loan quota + rate.
    try:
        payload = _http_get_json(OKX_MARGIN_INFO, timeout=45)
        basic = ((payload.get("data") or [None])[0] or {}).get("basic") if isinstance(payload, dict) else []
        for asset in target_assets:
            row = next((r for r in basic if isinstance(r, dict) and str(r.get("ccy") or "").upper() == asset), None)
            if not row:
                continue
            _append(
                "OKX",
                asset,
                _safe_float(row.get("rate")),
                _safe_float(row.get("quota")),
                "Public",
                "daily",
            )
    except Exception as e:
        errors.append(f"OKX: {e}")

    # Bybit spot margin hourly rates (convert to daily/annual).
    try:
        payload = _http_get_json(BYBIT_MARGIN_INFO, timeout=45)
        vip_coin_list = (((payload or {}).get("result") or {}).get("vipCoinList") or []) if isinstance(payload, dict) else []
        if isinstance(vip_coin_list, list) and vip_coin_list:
            bucket = next(
                (
                    b
                    for b in vip_coin_list
                    if isinstance(b, dict) and str(b.get("vipLevel") or "").strip().lower() in {"no vip", "vip0", "0"}
                ),
                vip_coin_list[0] if isinstance(vip_coin_list[0], dict) else None,
            )
            coins = bucket.get("list") if isinstance(bucket, dict) and isinstance(bucket.get("list"), list) else []
            tier = str(bucket.get("vipLevel") or "No VIP") if isinstance(bucket, dict) else "No VIP"
            for asset in target_assets:
                row = next((r for r in coins if isinstance(r, dict) and str(r.get("currency") or "").upper() == asset), None)
                if not row:
                    continue
                hourly = _safe_float(row.get("hourlyBorrowRate"))
                daily = (hourly * 24.0) if hourly is not None else None
                _append("Bybit", asset, daily, _safe_float(row.get("maxBorrowingAmount")), tier, "hourly")
    except Exception as e:
        errors.append(f"Bybit: {e}")

    # Backpack borrow/lend market rates.
    try:
        payload = _http_get_json(BACKPACK_BORROW_MARKETS, timeout=45)
        rows = payload if isinstance(payload, list) else []
        for asset in target_assets:
            row = next((r for r in rows if isinstance(r, dict) and str(r.get("symbol") or "").upper() == asset), None)
            if not row:
                continue
            annual = _safe_float(row.get("borrowInterestRate"))
            daily = (annual / 365.0) if annual is not None else None
            _append(
                "Backpack",
                asset,
                daily,
                _safe_float(row.get("openBorrowLendLimit")),
                "Public",
                "annual",
            )
    except Exception as e:
        errors.append(f"Backpack: {e}")

    # KuCoin signed API (optional, key-based).
    kucoin_headers = _kucoin_signed_headers("/api/v3/margin/currencies")
    if kucoin_headers is not None:
        try:
            payload = _http_get_json(KUCOIN_MARGIN_INFO, headers=kucoin_headers, timeout=45)
            rows = payload.get("data") if isinstance(payload, dict) else []
            for asset in target_assets:
                row = next((r for r in rows if isinstance(r, dict) and str(r.get("currency") or "").upper() == asset), None)
                if not row:
                    continue
                daily = None
                for k in ["dailyIntRate", "dailyBorrowRate", "dailyInterestRate", "interestRate", "borrowRate"]:
                    daily = _safe_float(row.get(k))
                    if daily is not None:
                        break
                if daily is None:
                    hourly = _safe_float(row.get("hourlyBorrowRate"))
                    if hourly is not None:
                        daily = hourly * 24.0
                limit = None
                for k in ["borrowMaxAmount", "maxBorrowSize", "maxBorrowAmount", "holdMaxAmount", "buyMaxAmount"]:
                    limit = _safe_float(row.get(k))
                    if limit is not None:
                        break
                _append("KuCoin", asset, daily, limit, "API Key", "daily")
        except Exception as e:
            errors.append(f"KuCoin: {e}")
    else:
        if (
            (os.getenv("KUCOIN_API_KEY") or "").strip()
            or (os.getenv("KUCOIN_API_SECRET") or "").strip()
            or (os.getenv("KUCOIN_API_PASSPHRASE") or "").strip()
        ):
            data_gaps.append("KuCoin 借币数据未启用：请同时设置 KUCOIN_API_KEY / KUCOIN_API_SECRET / KUCOIN_API_PASSPHRASE。")

    if not out:
        data_gaps.append(f"借币成本多源数据获取失败: {' | '.join(errors) if errors else 'empty'}")
        return []
    if errors:
        data_gaps.append(f"借币成本部分数据源不可用: {' | '.join(errors)}")

    out.sort(
        key=lambda x: (
            asset_rank.get(str(x.get("asset") or "").upper(), 99),
            source_rank.get(str(x.get("source") or ""), 99),
            float(x.get("daily_rate_pct") or 9999.0),
        )
    )
    return out


def _normalize_chain(chain: Optional[str]) -> str:
    c = (chain or "").strip()
    if not c:
        return "Unknown"
    low = c.lower()
    if "arbitrum" in low:
        return "Arbitrum"
    if "ethereum" in low:
        return "Ethereum"
    if "base" in low:
        return "Base"
    return c


def _normalize_chain_id(chain_id: Optional[int]) -> str:
    if chain_id is None:
        return "Unknown"
    return _normalize_chain(STABLE_CHAIN_ID_MAP.get(chain_id, str(chain_id)))


def _rate_to_pct(v: Optional[float], ratio_threshold: float = 2.0) -> Optional[float]:
    if v is None:
        return None
    if abs(v) <= ratio_threshold:
        return v * 100.0
    return v


def _util_to_pct(v: Optional[float]) -> Optional[float]:
    if v is None:
        return None
    if abs(v) <= 1.0:
        return v * 100.0
    return v


def _append_source_tag(row: Dict[str, Any], tag: str) -> None:
    tags = row.get("source_tags")
    cur: List[str] = tags if isinstance(tags, list) else []
    if tag not in cur:
        cur.append(tag)
    row["source_tags"] = cur
    if cur:
        row["source_primary"] = "+".join(cur)


def _stable_safety_rank(protocol_key: str, chain: str, rewards_apy: Optional[float]) -> int:
    chain_penalty = 0 if chain.strip().lower() == "ethereum" else 1
    rewards_penalty = 1 if (rewards_apy or 0.0) > 0.0 else 0
    return int(STABLE_YIELD_PROJECT_PRIORITY.get(protocol_key, 99)) + chain_penalty + rewards_penalty


def _pick_better_stable_row(a: Optional[Dict[str, Any]], b: Dict[str, Any]) -> Dict[str, Any]:
    if a is None:
        return b
    a_score = int(a.get("data_completeness") or 0)
    b_score = int(b.get("data_completeness") or 0)
    if b_score != a_score:
        return b if b_score > a_score else a
    return b if float(b.get("tvl_usd") or 0.0) > float(a.get("tvl_usd") or 0.0) else a


def _dedupe_stable_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for r in rows:
        protocol = str(r.get("protocol") or "").strip()
        chain = str(r.get("chain") or "").strip()
        asset = str(r.get("asset") or "").upper().strip()
        if not protocol or not chain or not asset:
            continue
        key = (protocol, chain, asset)
        cur = best.get(key)
        if cur is None:
            best[key] = r
            continue
        picked = _pick_better_stable_row(cur, r)
        other = r if picked is cur else cur
        tags_a = picked.get("source_tags") if isinstance(picked.get("source_tags"), list) else []
        tags_b = other.get("source_tags") if isinstance(other.get("source_tags"), list) else []
        tags = []
        for t in [*tags_a, *tags_b]:
            ts = str(t)
            if ts and ts not in tags:
                tags.append(ts)
        if tags:
            picked["source_tags"] = tags
            picked["source_primary"] = "+".join(tags)
        best[key] = picked
    return list(best.values())


def _stable_row_completeness_score(
    supply_apy: Optional[float],
    borrow_apy: Optional[float],
    rewards_apy: Optional[float],
    utilization_pct: Optional[float],
    total_supply_usd: Optional[float],
    total_borrow_usd: Optional[float],
) -> int:
    score = 0
    if supply_apy is not None:
        score += 2
    if borrow_apy is not None:
        score += 2
    if rewards_apy is not None:
        score += 1
    if utilization_pct is not None:
        score += 2
    if total_supply_usd is not None:
        score += 1
    if total_borrow_usd is not None:
        score += 1
    return score


def _fetch_stablecoin_yields(data_gaps: List[str]) -> List[Dict[str, Any]]:
    try:
        payload = _http_get_json(DEFILLAMA_YIELDS, timeout=60)
        rows = payload.get("data") if isinstance(payload, dict) else []
        if not isinstance(rows, list):
            rows = []
    except Exception as e:
        data_gaps.append(f"DefiLlama 稳定币收益数据获取失败: {e}")
        return []

    best_by_key: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("stablecoin") is not True:
            continue
        project_key = str(row.get("project") or "").strip().lower()
        if project_key not in STABLE_YIELD_PROJECTS:
            continue
        symbol = str(row.get("symbol") or "").strip().upper()
        if symbol not in STABLE_YIELD_ASSETS:
            continue
        chain_name = _normalize_chain(str(row.get("chain") or ""))
        if chain_name.lower() not in STABLE_YIELD_CHAINS:
            continue

        tvl = _safe_float(row.get("tvlUsd"))
        native_apy = _safe_float(row.get("apyBase"))
        rewards_apy = _safe_float(row.get("apyReward"))
        total_apy = _safe_float(row.get("apy"))
        if total_apy is None and (native_apy is not None or rewards_apy is not None):
            total_apy = float(native_apy or 0.0) + float(rewards_apy or 0.0)
        borrow_apy = _safe_float(row.get("apyBaseBorrow"))
        total_supply = _safe_float(row.get("totalSupplyUsd"))
        total_borrow = _safe_float(row.get("totalBorrowUsd"))
        utilization = _safe_float(row.get("utilization"))
        util_pct = _util_to_pct(utilization)
        if util_pct is None and total_supply is not None and total_borrow is not None and total_supply > 0:
            util_pct = total_borrow / total_supply * 100.0
        completeness = _stable_row_completeness_score(native_apy, borrow_apy, rewards_apy, util_pct, total_supply, total_borrow)
        key = (project_key, chain_name, symbol)
        candidate = {
            "protocol": STABLE_YIELD_PROJECTS[project_key],
            "protocol_key": project_key,
            "chain": chain_name,
            "asset": symbol,
            "supply_apy": native_apy,
            "borrow_apy": borrow_apy,
            "rewards_apy": rewards_apy,
            "total_apy": total_apy,
            "tvl_usd": tvl,
            "total_supply_usd": total_supply,
            "total_borrow_usd": total_borrow,
            "utilization_pct": util_pct,
            "data_completeness": completeness,
            "pool_id": str(row.get("pool") or ""),
            "risk_note": STABLE_YIELD_PROTOCOL_RISK_NOTE.get(project_key, "待复核"),
            "updated_at": datetime.now(tz=timezone.utc).isoformat(),
            "source_tags": ["DefiLlama"],
            "source_primary": "DefiLlama",
        }
        best_by_key[key] = _pick_better_stable_row(best_by_key.get(key), candidate)

    out = list(best_by_key.values())
    _augment_stablecoin_yields_with_official(out, data_gaps)
    for r in out:
        if r.get("supply_apy") is not None or r.get("rewards_apy") is not None:
            r["total_apy"] = float(r.get("supply_apy") or 0.0) + float(r.get("rewards_apy") or 0.0)
            r["total_apy_method"] = "supply_plus_rewards"
        r["data_completeness"] = _stable_row_completeness_score(
            _safe_float(r.get("supply_apy")),
            _safe_float(r.get("borrow_apy")),
            _safe_float(r.get("rewards_apy")),
            _safe_float(r.get("utilization_pct")),
            _safe_float(r.get("total_supply_usd")),
            _safe_float(r.get("total_borrow_usd")),
        )
        protocol_key = str(r.get("protocol_key") or "")
        chain = str(r.get("chain") or "")
        r["safety_rank"] = _stable_safety_rank(protocol_key, chain, _safe_float(r.get("rewards_apy")))
        if not r.get("source_tags"):
            _append_source_tag(r, "DefiLlama")

    out = _dedupe_stable_rows(out)
    out.sort(
        key=lambda x: (
            int(x.get("safety_rank") or 99),
            -(int(x.get("data_completeness") or 0)),
            -(float(x.get("tvl_usd") or 0.0)),
            -(float(x.get("supply_apy") or 0.0)),
        )
    )
    if not out:
        data_gaps.append("稳定币收益面板为空：DefiLlama 未返回符合筛选条件的池。")
    return out


def _fetch_stablecoin_yields_extended(data_gaps: List[str]) -> List[Dict[str, Any]]:
    try:
        payload = _http_get_json(DEFILLAMA_YIELDS, timeout=60)
        rows = payload.get("data") if isinstance(payload, dict) else []
        if not isinstance(rows, list):
            rows = []
    except Exception as e:
        data_gaps.append(f"DefiLlama 扩展稳定币样本获取失败: {e}")
        return []

    best: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("stablecoin") is not True:
            continue
        protocol = str(row.get("project") or "").strip().lower()
        if not protocol or protocol in STABLE_EXTENDED_EXCLUDED_PROJECTS:
            continue
        asset = _normalize_asset_symbol(row.get("symbol"))
        if not asset:
            continue
        chain = _normalize_chain(str(row.get("chain") or ""))
        tvl = _safe_float(row.get("tvlUsd"))
        if tvl is None or tvl < STABLE_EXTENDED_MIN_TVL_USD:
            continue

        base_apy = _safe_float(row.get("apyBase"))
        rewards_apy = _safe_float(row.get("apyReward"))
        total_apy = _safe_float(row.get("apy"))
        if total_apy is None and (base_apy is not None or rewards_apy is not None):
            total_apy = float(base_apy or 0.0) + float(rewards_apy or 0.0)
        if total_apy is not None and (total_apy < STABLE_EXTENDED_MIN_APY_PCT or total_apy > STABLE_EXTENDED_MAX_APY_PCT):
            continue

        key = (asset, protocol, chain)
        candidate = {
            "asset": asset,
            "protocol": protocol,
            "chain": chain,
            "base_apy_pct": base_apy,
            "rewards_apy_pct": rewards_apy,
            "total_apy_pct": total_apy,
            "tvl_usd": tvl,
            "source": "DefiLlama API",
        }
        cur = best.get(key)
        if cur is None:
            best[key] = candidate
            continue
        cur_tvl = _safe_float(cur.get("tvl_usd")) or 0.0
        cur_apy = _safe_float(cur.get("total_apy_pct")) or -10**9
        cand_apy = _safe_float(candidate.get("total_apy_pct")) or -10**9
        if tvl > cur_tvl or (tvl == cur_tvl and cand_apy > cur_apy):
            best[key] = candidate

    out = list(best.values())
    out.sort(key=lambda r: (-(float(r.get("tvl_usd") or 0.0)), -(float(r.get("total_apy_pct") or 0.0))))
    if not out:
        data_gaps.append("DefiLlama 扩展稳定币样本为空：筛选后无有效记录。")
    return out


class _BitcompareTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: List[List[Dict[str, Any]]] = []
        self._row: Optional[List[Dict[str, Any]]] = None
        self._cell: Optional[Dict[str, Any]] = None

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = {"text": [], "hrefs": []}
        elif tag == "a" and self._cell is not None:
            href = dict(attrs).get("href")
            if href:
                self._cell["hrefs"].append(href)

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._row is not None and self._cell is not None:
            self._cell["text"] = " ".join("".join(self._cell["text"]).split())
            self._row.append(self._cell)
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
            self._cell = None


def _extract_bitcompare_rows(html: str) -> List[Dict[str, Any]]:
    parser = _BitcompareTableParser()
    parser.feed(html)
    out: List[Dict[str, Any]] = []
    for cells in parser.rows:
        if len(cells) < 3:
            continue
        asset_text = str(cells[0].get("text") or "")
        provider = str(cells[1].get("text") or "").strip()
        rate_text = str(cells[2].get("text") or "")
        sym_match = re.search(r"\(\s*([A-Za-z0-9.\-]+)\s*\)", asset_text)
        apy_match = re.search(r"(?:最高可达|up to)?\s*([0-9]+(?:\.[0-9]+)?)%\s*(?:APY)?", rate_text, flags=re.I)
        provider_links = [str(v) for v in cells[1].get("hrefs") or []]
        if not (sym_match and apy_match and provider and any(v.startswith("/go/") for v in provider_links)):
            continue
        asset = _normalize_asset_symbol(sym_match.group(1))
        apy = _safe_float(apy_match.group(1))
        if asset and apy is not None:
            out.append(
                {
                    "asset": asset,
                    "provider": provider,
                    "apy_pct": apy,
                    "source": "Bitcompare (CeFi/DeFi/Hybrid)",
                    "source_url": BITCOMPARE_LENDING_RATES,
                    "retrieved_at": datetime.now(tz=timezone.utc).isoformat(),
                    "verification_status": "aggregator_quote_unverified",
                    "is_extreme_apy": apy >= 20.0,
                }
            )
    return out


def _fetch_stablecoin_cefi_rates(data_gaps: List[str]) -> List[Dict[str, Any]]:
    best_by_asset: Dict[str, Dict[str, Any]] = {}
    any_page_ok = False
    deadline = time.time() + 25.0
    for page in range(1, BITCOMPARE_MAX_PAGES + 1):
        if time.time() >= deadline:
            data_gaps.append("Bitcompare 平台 APY 获取超时：已跳过剩余分页。")
            break
        try:
            html = _http_get_text(BITCOMPARE_LENDING_RATES, params={"page": page}, timeout=8)
            any_page_ok = True
        except Exception as e:
            if page == 1:
                data_gaps.append(f"Bitcompare 平台 APY 获取失败: {e}")
            else:
                data_gaps.append(f"Bitcompare 平台 APY 获取中断：第 {page} 页失败，已保留已抓取样本。")
            break
        parsed_rows = _extract_bitcompare_rows(html)
        if not parsed_rows:
            break
        for row in parsed_rows:
            asset = str(row.get("asset") or "").upper()
            if asset not in STABLE_CEFI_ASSETS:
                continue
            cur = best_by_asset.get(asset)
            if cur is None or float(row.get("apy_pct") or -10**9) > float(cur.get("apy_pct") or -10**9):
                best_by_asset[asset] = row
        if f"page={page + 1}" not in html:
            break

    out = sorted(best_by_asset.values(), key=lambda r: str(r.get("asset") or ""))
    if any_page_ok and not out:
        data_gaps.append("Bitcompare 稳定币平台 APY 样本为空：未匹配到稳定币资产。")
    return out


def _build_taoli_binance_margin_rates(borrow_rates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in borrow_rates:
        if str(row.get("source") or "") != "Binance":
            continue
        asset = _normalize_asset_symbol(row.get("asset"))
        if not asset:
            continue
        out.append(
            {
                "asset": asset,
                "daily_rate_pct": _safe_float(row.get("daily_rate_pct")),
                "annual_rate_pct": _safe_float(row.get("annual_rate_pct")),
                "borrow_limit": _safe_float(row.get("borrow_limit")),
                "source": "taoli",
                "updated_at": str(row.get("updated_at") or datetime.now(tz=timezone.utc).isoformat()),
            }
        )
    out.sort(key=lambda r: str(r.get("asset") or ""))
    return out


def _fetch_aave_official_reserve_map(data_gaps: List[str]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    endpoint = AAVE_V3_GRAPHQL
    market_by_chain: Dict[int, str] = {}
    reserve_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    try:
        q_markets = {
            "query": """
            query Markets {
              markets(request:{ chainIds:[1,42161,8453] }) {
                name
                address
                chain { chainId name }
              }
            }
            """
        }
        payload = _http_post_json(endpoint, q_markets, timeout=45)
        markets = ((payload or {}).get("data") or {}).get("markets") or []
        for m in markets if isinstance(markets, list) else []:
            if not isinstance(m, dict):
                continue
            name = str(m.get("name") or "")
            chain = m.get("chain") if isinstance(m.get("chain"), dict) else {}
            chain_id = _safe_int(chain.get("chainId"))
            addr = str(m.get("address") or "")
            if chain_id is None or not addr:
                continue
            if name in {"AaveV3Ethereum", "AaveV3Arbitrum", "AaveV3Base"}:
                market_by_chain[chain_id] = addr
    except Exception as e:
        data_gaps.append(f"Aave API markets 获取失败: {e}")
        return reserve_map

    for chain_id, addr in market_by_chain.items():
        try:
            q_reserves = {
                "query": """
                query MarketReserves($chainId: ChainId!, $address: EvmAddress!) {
                  market(request:{ chainId:$chainId, address:$address }) {
                    chain { name chainId }
                    reserves(request:{ reserveType:BOTH, orderBy:{ tokenName:ASC } }) {
                      underlyingToken { symbol }
                      supplyInfo {
                        apy { value }
                        canBeCollateral
                        supplyCap { usd }
                      }
                      borrowInfo {
                        apy { value }
                        utilizationRate { value }
                        availableLiquidity { usd }
                        borrowCap { usd }
                      }
                      isPaused
                      isFrozen
                    }
                  }
                }
                """,
                "variables": {"chainId": chain_id, "address": addr},
            }
            payload = _http_post_json(endpoint, q_reserves, timeout=45)
            market = ((payload or {}).get("data") or {}).get("market") or {}
            chain_obj = market.get("chain") if isinstance(market, dict) and isinstance(market.get("chain"), dict) else {}
            chain_name = _normalize_chain(str(chain_obj.get("name") or ""))
            reserves = market.get("reserves") if isinstance(market, dict) else []
            for r in reserves if isinstance(reserves, list) else []:
                if not isinstance(r, dict):
                    continue
                tok = r.get("underlyingToken") if isinstance(r.get("underlyingToken"), dict) else {}
                symbol = str(tok.get("symbol") or "").upper()
                if symbol not in STABLE_YIELD_ASSETS:
                    continue
                s_info = r.get("supplyInfo") if isinstance(r.get("supplyInfo"), dict) else {}
                b_info = r.get("borrowInfo") if isinstance(r.get("borrowInfo"), dict) else {}
                s_apy_raw = _safe_float((s_info.get("apy") or {}).get("value") if isinstance(s_info.get("apy"), dict) else None)
                b_apy_raw = _safe_float((b_info.get("apy") or {}).get("value") if isinstance(b_info.get("apy"), dict) else None)
                s_apy = s_apy_raw * 100.0 if s_apy_raw is not None else None
                b_apy = b_apy_raw * 100.0 if b_apy_raw is not None else None
                util = _safe_float((b_info.get("utilizationRate") or {}).get("value") if isinstance(b_info.get("utilizationRate"), dict) else None)
                cap_s = _safe_float((s_info.get("supplyCap") or {}).get("usd") if isinstance(s_info.get("supplyCap"), dict) else None)
                cap_b = _safe_float((b_info.get("borrowCap") or {}).get("usd") if isinstance(b_info.get("borrowCap"), dict) else None)
                avail = _safe_float((b_info.get("availableLiquidity") or {}).get("usd") if isinstance(b_info.get("availableLiquidity"), dict) else None)
                reserve_map[(chain_name, symbol)] = {
                    "supply_apy": s_apy,
                    "borrow_apy": b_apy,
                    "utilization_pct": util * 100.0 if util is not None else None,
                    "supply_cap_usd": cap_s,
                    "borrow_cap_usd": cap_b,
                    "available_liquidity_usd": avail,
                    "can_be_collateral": bool(s_info.get("canBeCollateral")) if s_info.get("canBeCollateral") is not None else None,
                    "is_paused": bool(r.get("isPaused")) if r.get("isPaused") is not None else None,
                    "is_frozen": bool(r.get("isFrozen")) if r.get("isFrozen") is not None else None,
                }
        except Exception as e:
            data_gaps.append(f"Aave API reserves 获取失败 chain_id={chain_id}: {e}")
    return reserve_map


def _fetch_compound_official_reserve_map(data_gaps: List[str]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    reserve_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    try:
        summary_rows = _http_get_json_retry(COMPOUND_V3_SUMMARY, timeout=45, attempts=3, backoff_sec=1.0)
        rewards_rows = _http_get_json_retry(COMPOUND_V3_REWARDS, timeout=45, attempts=3, backoff_sec=1.0)
    except Exception as e:
        data_gaps.append(f"Compound API 获取失败: {e}")
        return reserve_map

    rewards_map: Dict[Tuple[int, str], Dict[str, Any]] = {}
    for row in rewards_rows if isinstance(rewards_rows, list) else []:
        if not isinstance(row, dict):
            continue
        chain_id = _safe_int(row.get("chain_id"))
        comet = row.get("comet") if isinstance(row.get("comet"), dict) else {}
        addr = str(comet.get("address") or "").lower()
        base_asset = row.get("base_asset") if isinstance(row.get("base_asset"), dict) else {}
        symbol = str(base_asset.get("symbol") or "").upper()
        if chain_id not in STABLE_CHAIN_ID_MAP or symbol not in STABLE_YIELD_ASSETS or not addr:
            continue
        rewards_map[(chain_id, addr)] = {
            "asset": symbol,
            "rewards_apy": _rate_to_pct(_safe_float(row.get("earn_rewards_apr"))),
        }

    for row in summary_rows if isinstance(summary_rows, list) else []:
        if not isinstance(row, dict):
            continue
        chain_id = _safe_int(row.get("chain_id"))
        if chain_id not in STABLE_CHAIN_ID_MAP:
            continue
        comet = row.get("comet") if isinstance(row.get("comet"), dict) else {}
        addr = str(comet.get("address") or "").lower()
        if not addr:
            continue
        reward_meta = rewards_map.get((chain_id, addr))
        symbol = str((reward_meta or {}).get("asset") or "").upper()
        if symbol not in STABLE_YIELD_ASSETS:
            continue

        util_raw = _safe_float(row.get("utilization"))
        if util_raw is not None and util_raw > 1_000:
            util_raw = util_raw / 1e18
        util_pct = _util_to_pct(util_raw)
        total_supply = _safe_float(row.get("total_supply_value"))
        total_borrow = _safe_float(row.get("total_borrow_value"))
        supply_apy = _rate_to_pct(_safe_float(row.get("supply_apr")))
        borrow_apy = _rate_to_pct(_safe_float(row.get("borrow_apr")))
        rewards_apy = _safe_float((reward_meta or {}).get("rewards_apy"))
        total_apy = (float(supply_apy or 0.0) + float(rewards_apy or 0.0)) if (supply_apy is not None or rewards_apy is not None) else None
        chain_name = _normalize_chain_id(chain_id)
        candidate = {
            "supply_apy": supply_apy,
            "borrow_apy": borrow_apy,
            "rewards_apy": rewards_apy,
            "total_apy": total_apy,
            "tvl_usd": total_supply,
            "total_supply_usd": total_supply,
            "total_borrow_usd": total_borrow,
            "utilization_pct": util_pct,
            "pool_id": addr,
            "updated_at": datetime.now(tz=timezone.utc).isoformat(),
            "data_completeness": _stable_row_completeness_score(supply_apy, borrow_apy, rewards_apy, util_pct, total_supply, total_borrow),
        }
        key = (chain_name, symbol)
        reserve_map[key] = _pick_better_stable_row(reserve_map.get(key), candidate)

    return reserve_map


def _fetch_morpho_official_reserve_map(data_gaps: List[str]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    reserve_map: Dict[Tuple[str, str], Dict[str, Any]] = {}
    query = """
    query Markets($first:Int!, $skip:Int!) {
      markets(first:$first, skip:$skip) {
        items {
          uniqueKey
          loanAsset { symbol }
          morphoBlue { chain { id network } }
          state {
            supplyApy
            borrowApy
            utilization
            supplyAssetsUsd
            borrowAssetsUsd
            rewards { supplyApr borrowApr asset { symbol } }
          }
        }
        pageInfo { count countTotal }
      }
    }
    """
    skip = 0
    first = 200
    max_pages = 30
    pages = 0
    while pages < max_pages:
        pages += 1
        try:
            payload = _http_post_json(MORPHO_GRAPHQL, {"query": query, "variables": {"first": first, "skip": skip}}, timeout=45)
        except Exception as e:
            data_gaps.append(f"Morpho API 获取失败: {e}")
            break
        market_obj = ((payload or {}).get("data") or {}).get("markets") or {}
        items = market_obj.get("items") if isinstance(market_obj, dict) else []
        if not isinstance(items, list) or not items:
            break
        for item in items:
            if not isinstance(item, dict):
                continue
            loan_asset = item.get("loanAsset") if isinstance(item.get("loanAsset"), dict) else {}
            symbol = str(loan_asset.get("symbol") or "").upper()
            if symbol not in STABLE_YIELD_ASSETS:
                continue
            morpho_blue = item.get("morphoBlue") if isinstance(item.get("morphoBlue"), dict) else {}
            chain_obj = morpho_blue.get("chain") if isinstance(morpho_blue.get("chain"), dict) else {}
            chain_id = _safe_int(chain_obj.get("id"))
            chain_name = _normalize_chain_id(chain_id)
            if chain_name.lower() not in STABLE_YIELD_CHAINS:
                continue
            state = item.get("state") if isinstance(item.get("state"), dict) else {}
            supply_apy = _rate_to_pct(_safe_float(state.get("supplyApy")))
            borrow_apy = _rate_to_pct(_safe_float(state.get("borrowApy")))
            util_pct = _util_to_pct(_safe_float(state.get("utilization")))
            total_supply = _safe_float(state.get("supplyAssetsUsd"))
            total_borrow = _safe_float(state.get("borrowAssetsUsd"))
            rewards = state.get("rewards") if isinstance(state.get("rewards"), list) else []
            rewards_vals = [_rate_to_pct(_safe_float(r.get("supplyApr")) if isinstance(r, dict) else None) for r in rewards]
            rewards_apy = sum(v for v in rewards_vals if v is not None) if any(v is not None for v in rewards_vals) else None

            # Filter out tiny or extreme pools to keep safety-first comparability.
            if total_supply is None or total_supply < 100_000:
                continue
            if supply_apy is not None and (supply_apy < -1.0 or supply_apy > 50.0):
                continue
            if borrow_apy is not None and (borrow_apy < -1.0 or borrow_apy > 80.0):
                continue
            if util_pct is not None and (util_pct < 0.0 or util_pct > 100.5):
                continue

            total_apy = (float(supply_apy or 0.0) + float(rewards_apy or 0.0)) if (supply_apy is not None or rewards_apy is not None) else None
            candidate = {
                "supply_apy": supply_apy,
                "borrow_apy": borrow_apy,
                "rewards_apy": rewards_apy,
                "total_apy": total_apy,
                "tvl_usd": total_supply,
                "total_supply_usd": total_supply,
                "total_borrow_usd": total_borrow,
                "utilization_pct": util_pct,
                "pool_id": str(item.get("uniqueKey") or ""),
                "updated_at": datetime.now(tz=timezone.utc).isoformat(),
                "data_completeness": _stable_row_completeness_score(supply_apy, borrow_apy, rewards_apy, util_pct, total_supply, total_borrow),
            }
            key = (chain_name, symbol)
            reserve_map[key] = _pick_better_stable_row(reserve_map.get(key), candidate)

        page_info = market_obj.get("pageInfo") if isinstance(market_obj, dict) else {}
        count = _safe_int(page_info.get("count")) if isinstance(page_info, dict) else None
        total = _safe_int(page_info.get("countTotal")) if isinstance(page_info, dict) else None
        step = count if (count is not None and count > 0) else len(items)
        skip += step
        if total is not None and skip >= total:
            break
        if len(items) < first:
            break

    return reserve_map


def _merge_stable_official_map(
    rows: List[Dict[str, Any]],
    protocol_key: str,
    protocol_label: str,
    source_tag: str,
    official_map: Dict[Tuple[str, str], Dict[str, Any]],
) -> None:
    if not official_map:
        return
    existing: Dict[Tuple[str, str], Dict[str, Any]] = {
        (str(r.get("chain") or ""), str(r.get("asset") or "").upper()): r for r in rows if str(r.get("protocol_key") or "") == protocol_key
    }
    for key, extra in official_map.items():
        chain, symbol = key
        row = existing.get((chain, symbol))
        if row is None:
            row = {
                "protocol": protocol_label,
                "protocol_key": protocol_key,
                "chain": chain,
                "asset": symbol,
                "risk_note": STABLE_YIELD_PROTOCOL_RISK_NOTE.get(protocol_key, "待复核"),
                "updated_at": datetime.now(tz=timezone.utc).isoformat(),
            }
            rows.append(row)
            existing[(chain, symbol)] = row

        for field in [
            "supply_apy",
            "borrow_apy",
            "rewards_apy",
            "total_apy",
            "tvl_usd",
            "total_supply_usd",
            "total_borrow_usd",
            "utilization_pct",
            "supply_cap_usd",
            "borrow_cap_usd",
            "available_liquidity_usd",
            "can_be_collateral",
            "is_paused",
            "is_frozen",
            "pool_id",
            "updated_at",
        ]:
            if extra.get(field) is not None:
                row[field] = extra.get(field)
        _append_source_tag(row, source_tag)


def _augment_stablecoin_yields_with_official(rows: List[Dict[str, Any]], data_gaps: List[str]) -> None:
    aave_map = _fetch_aave_official_reserve_map(data_gaps)
    compound_map = _fetch_compound_official_reserve_map(data_gaps)
    morpho_map = _fetch_morpho_official_reserve_map(data_gaps)

    _merge_stable_official_map(rows, "aave-v3", "Aave", "Aave API", aave_map)
    _merge_stable_official_map(rows, "compound-v3", "Compound", "Compound API", compound_map)
    _merge_stable_official_map(rows, "morpho-v1", "Morpho", "Morpho API", morpho_map)


def _ensure_dirs(outdir: Path) -> Tuple[Path, Path]:
    charts = outdir / "charts"
    data = outdir / "data"
    charts.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    return charts, data


def _cleanup_legacy_outputs(charts_dir: Path, data_dir: Path) -> None:
    # Every run owns its dated chart directory; remove stale conditional charts before rendering.
    for p in charts_dir.glob("chart_*.png"):
        if p.is_file():
            p.unlink()
    for name in ["market_history_14d.csv", "fng_30d.csv", "dvol_btc_30d.csv", "dvol_eth_30d.csv", "rwa_asset_class_snapshot.csv", "rwa_token_movers.csv"]:
        p = data_dir / name
        if p.exists():
            p.unlink()


def _write_csv_top_assets(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["symbol", "name", "price_usd", "market_cap_usd", "change_24h_pct", "source", "as_of"])
        for r in rows:
            w.writerow([r.get("symbol"), r.get("name"), r.get("price"), r.get("mcap"), r.get("chg24"), r.get("source"), r.get("as_of")])


def _write_csv_exchanges(path: Path, rows: List[ExchangeRow]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "name", "slug", "volume24h_usd", "change_24h_pct", "spot24h_usd", "deriv24h_usd"])
        for r in rows:
            w.writerow([r.rank, r.name, r.slug, r.volume24h, r.pct24h, r.spot24h, r.deriv24h])


def _write_csv_market_history(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "market_cap_usd", "volume_24h_usd", "btc_dominance_pct"])
        for r in rows:
            w.writerow([r.get("date"), r.get("market_cap"), r.get("volume_24h"), r.get("btc_dom")])


def _write_csv_series(path: Path, rows: List[Dict[str, Any]], value_name: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", value_name])
        for r in rows:
            w.writerow([r.get("date"), r.get("value")])


def _write_csv_breadth(path: Path, breadth: Dict[str, Any]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k in ["btc_share", "top2_to_10_share", "outside_top10_share", "top10_share"]:
            w.writerow([k, breadth.get(k)])
        for k in ["definition", "risk_breadth_definition", "risk_asset_count"]:
            w.writerow([k, breadth.get(k)])
        w.writerow(["risk_asset_symbols", ",".join(breadth.get("risk_asset_symbols") or [])])
        w.writerow(["excluded_symbols", ",".join(breadth.get("excluded_symbols") or [])])


def _write_csv_top2_trend(path: Path, top2: Dict[str, Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset", "symbol", "price_usd", "open_usd", "high_usd", "low_usd", "change_24h_pct", "range_pos_pct", "trend", "source"])
        for asset in ["BTC", "ETH"]:
            row = top2.get(asset) or {}
            w.writerow(
                [
                    asset,
                    row.get("symbol"),
                    row.get("price"),
                    row.get("open"),
                    row.get("high"),
                    row.get("low"),
                    row.get("change_pct"),
                    row.get("range_pos_pct"),
                    row.get("trend"),
                    row.get("source"),
                ]
            )


def _write_csv_top2_intraday(path: Path, series: Dict[str, List[Dict[str, Any]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset", "symbol", "timestamp_utc", "open_usd", "high_usd", "low_usd", "close_usd", "source"])
        for asset in ["BTC", "ETH"]:
            rows = series.get(asset) or []
            symbol = f"{asset}USDT"
            for r in rows:
                ts = r.get("ts")
                ts_txt = ts.isoformat() if isinstance(ts, datetime) else ""
                w.writerow([asset, symbol, ts_txt, r.get("open"), r.get("high"), r.get("low"), r.get("close"), r.get("source")])


def _write_csv_stablecoin_yields(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "protocol",
                "chain",
                "asset",
                "supply_apy_pct",
                "rewards_apy_pct",
                "total_apy_pct",
                "total_apy_method",
                "borrow_apy_pct",
                "tvl_usd",
                "total_supply_usd",
                "total_borrow_usd",
                "utilization_pct",
                "supply_cap_usd",
                "borrow_cap_usd",
                "available_liquidity_usd",
                "can_be_collateral",
                "is_paused",
                "is_frozen",
                "data_completeness",
                "risk_note",
                "safety_rank",
                "pool_id",
                "source_primary",
                "source_tags",
                "updated_at_utc",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r.get("protocol"),
                    r.get("chain"),
                    r.get("asset"),
                    r.get("supply_apy"),
                    r.get("rewards_apy"),
                    r.get("total_apy"),
                    r.get("total_apy_method"),
                    r.get("borrow_apy"),
                    r.get("tvl_usd"),
                    r.get("total_supply_usd"),
                    r.get("total_borrow_usd"),
                    r.get("utilization_pct"),
                    r.get("supply_cap_usd"),
                    r.get("borrow_cap_usd"),
                    r.get("available_liquidity_usd"),
                    r.get("can_be_collateral"),
                    r.get("is_paused"),
                    r.get("is_frozen"),
                    r.get("data_completeness"),
                    r.get("risk_note"),
                    r.get("safety_rank"),
                    r.get("pool_id"),
                    r.get("source_primary"),
                    ",".join(r.get("source_tags")) if isinstance(r.get("source_tags"), list) else r.get("source_tags"),
                    r.get("updated_at"),
                ]
            )


def _write_csv_stablecoin_yields_extended(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset", "protocol", "chain", "total_apy_pct", "base_apy_pct", "rewards_apy_pct", "tvl_usd", "source"])
        for r in rows:
            w.writerow(
                [
                    r.get("asset"),
                    r.get("protocol"),
                    r.get("chain"),
                    r.get("total_apy_pct"),
                    r.get("base_apy_pct"),
                    r.get("rewards_apy_pct"),
                    r.get("tvl_usd"),
                    r.get("source"),
                ]
            )


def _write_csv_stablecoin_cefi_rates(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset", "provider", "apy_pct", "source", "source_url", "retrieved_at", "verification_status", "is_extreme_apy"])
        for r in rows:
            w.writerow(
                [
                    r.get("asset"),
                    r.get("provider"),
                    r.get("apy_pct"),
                    r.get("source"),
                    r.get("source_url"),
                    r.get("retrieved_at"),
                    r.get("verification_status"),
                    r.get("is_extreme_apy"),
                ]
            )


def _write_csv_rwa_asset_classes(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset_class", "value_usd", "change_7d_pct", "as_of", "retrieved_at", "freshness_status", "source", "source_type"])
        for r in rows:
            w.writerow(
                [
                    r.get("asset_class"),
                    r.get("value_usd"),
                    r.get("change_7d_pct"),
                    r.get("as_of"),
                    r.get("retrieved_at"),
                    r.get("freshness_status"),
                    r.get("source"),
                    r.get("source_type"),
                ]
            )


def _write_csv_rwa_token_movers(path: Path, rows: List[Dict[str, Any]]) -> None:
    fields = [
        "ticker", "symbol", "chain_id", "contract_address", "price_usd", "change_24h_pct",
        "rsi14", "sma6", "sma24", "range_24h_pct", "onchain_volume_24h_raw", "buy_volume_24h_raw", "sell_volume_24h_raw",
        "flow_unit_status", "flow_anomaly_reason", "onchain_volume_24h_usd",
        "buy_volume_24h_usd", "sell_volume_24h_usd", "net_buy_24h_usd", "liquidity_usd",
        "holders", "top10_holders_pct", "smart_money_holders", "smart_money_holding_pct",
        "smart_signal_source", "smart_signal_coverage", "smart_signal_direction", "smart_signal_count", "smart_signal_value_usd", "smart_signal_time_ms", "smart_signal_status",
        "stock_price_usd", "shares_multiplier", "shares_multiplier_source", "reference_price_usd", "premium_pct", "premium_status", "market_status", "reason_code", "reason_msg",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _write_csv_nondefi_carry(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "exchange",
                "asset",
                "spot_price_usd",
                "mark_price_usd",
                "index_price_usd",
                "basis_pct",
                "funding_rate_pct",
                "funding_interval_hours",
                "annual_funding_pct",
                "open_interest_contracts",
                "quote_ccy",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r.get("exchange"),
                    r.get("asset"),
                    r.get("spot_price"),
                    r.get("mark_price"),
                    r.get("index_price"),
                    r.get("basis_pct"),
                    r.get("funding_rate_pct"),
                    r.get("funding_interval_hours"),
                    r.get("annual_funding_pct"),
                    r.get("open_interest_contracts"),
                    r.get("quote_ccy"),
                ]
            )


def _write_csv_borrow_rates(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "asset", "daily_rate_pct", "annual_rate_pct", "borrow_limit", "tier", "rate_basis", "updated_at_utc"])
        for r in rows:
            w.writerow(
                [
                    r.get("source"),
                    r.get("asset"),
                    r.get("daily_rate_pct"),
                    r.get("annual_rate_pct"),
                    r.get("borrow_limit"),
                    r.get("tier"),
                    r.get("rate_basis"),
                    r.get("updated_at"),
                ]
            )


def _write_csv_taoli_binance_margin_rates(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["asset", "daily_rate_pct", "annual_rate_pct", "borrow_limit", "source", "updated_at_utc"])
        for r in rows:
            w.writerow(
                [
                    r.get("asset"),
                    r.get("daily_rate_pct"),
                    r.get("annual_rate_pct"),
                    r.get("borrow_limit"),
                    r.get("source"),
                    r.get("updated_at"),
                ]
            )


def _style_axes(ax: Any, grid_axis: str = "y") -> None:
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, linewidth=0.8, alpha=0.95)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(THEME["axis"])
    ax.spines["bottom"].set_color(THEME["axis"])
    ax.tick_params(labelsize=9)


def _label_offset(max_abs: float, ratio: float = 0.04, floor: float = 0.2) -> float:
    return max(max_abs * ratio, floor)


def _save_fig(fig: Any, out: Path) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        fig.tight_layout()
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor=THEME["bg"])
    plt.close(fig)


def _plot_market_snapshot_levels(market_cap: Optional[float], volume_24h: Optional[float], btc_dom: Optional[float], out: Path) -> None:
    vals = [market_cap, volume_24h, btc_dom]
    if all(v is None for v in vals):
        return
    items = [
        ("总市值", (f"{float(market_cap)/1e12:.2f}T" if market_cap is not None else "N/A"), THEME["primary"]),
        ("24h成交", (f"{float(volume_24h)/1e9:.2f}B" if volume_24h is not None else "N/A"), THEME["secondary"]),
        ("BTC.D", (f"{float(btc_dom):.2f}%" if btc_dom is not None else "N/A"), THEME["accent"]),
    ]

    fig, ax = plt.subplots(figsize=(10.8, 3.6))
    ax.set_title("全市场当日水平", loc="left")
    ax.axis("off")

    card_w = 0.29
    card_h = 0.68
    x0 = [0.02, 0.355, 0.69]
    y = 0.16
    for i, (label, value, color) in enumerate(items):
        box = FancyBboxPatch(
            (x0[i], y),
            card_w,
            card_h,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=1.0,
            edgecolor=THEME["axis"],
            facecolor=THEME["panel"],
            transform=ax.transAxes,
        )
        ax.add_patch(box)
        ax.plot([x0[i] + 0.02, x0[i] + card_w - 0.02], [y + card_h - 0.01, y + card_h - 0.01], color=color, linewidth=3.0, transform=ax.transAxes)
        ax.text(x0[i] + 0.03, y + card_h - 0.12, label, fontsize=11, color=THEME["muted"], transform=ax.transAxes)
        ax.text(x0[i] + 0.03, y + 0.24, value, fontsize=25, fontweight="bold", color=THEME["text"], transform=ax.transAxes)

    _save_fig(fig, out)


def _plot_market_daily_change(mc_chg: Optional[float], vol_chg: Optional[float], dom_chg: Optional[float], out: Path) -> None:
    vals = [mc_chg, vol_chg, dom_chg]
    if all(v is None for v in vals):
        return
    labels = ["市值 24h%", "成交 24h%", "BTC.D 变化(pct)"]
    nums = [float(mc_chg or 0.0), float(vol_chg or 0.0), float(dom_chg or 0.0)]
    colors = [THEME["positive"] if x >= 0 else THEME["negative"] for x in nums]

    fig, ax = plt.subplots(figsize=(10.8, 4.3))
    x = [0, 1, 2]
    for i, v in enumerate(nums):
        ax.vlines(x[i], 0, v, color=colors[i], linewidth=2.4, alpha=0.95)
    ax.scatter(x, nums, color=colors, s=84, edgecolors=THEME["bg"], linewidths=1.2, zorder=3)
    ax.axhline(0, color=THEME["muted"], linewidth=1.1)
    ax.set_title("全市场当日变化（相对前日）", loc="left")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    _style_axes(ax, "y")

    max_abs = max(abs(x) for x in nums) if nums else 0.0
    lim = max(max_abs * 1.25, 0.8)
    ax.set_ylim(-lim, lim)
    offset = _label_offset(max_abs, ratio=0.06, floor=0.18)
    for i, v in enumerate(nums):
        v = nums[i]
        txt = "N/A" if vals[i] is None else f"{v:+.2f}"
        y = v + offset if v >= 0 else v - offset
        va = "bottom" if v >= 0 else "top"
        ax.text(i, y, txt, ha="center", va=va, fontsize=9)
    _save_fig(fig, out)


def _plot_breadth_snapshot(breadth: Dict[str, Any], out: Path) -> None:
    btc = breadth.get("btc_share")
    top2_10 = breadth.get("top2_to_10_share")
    outside = breadth.get("outside_top10_share")
    if btc is None or top2_10 is None or outside is None:
        return

    fig, ax = plt.subplots(figsize=(10.8, 2.8))
    segs = [
        ("BTC", float(btc), THEME["btc"]),
        ("Top10其余", float(top2_10), THEME["primary"]),
        ("Top10外", float(outside), "#84CC16"),
    ]
    left = 0.0
    for name, val, color in segs:
        ax.barh([0], [val], left=left, color=color, height=0.46, edgecolor=THEME["bg"], linewidth=0.8)
        txt = f"{name} {val:.1f}%"
        if val >= 9:
            ax.text(left + val / 2.0, 0, txt, ha="center", va="center", fontsize=9, color=THEME["bg"], fontweight="bold")
        else:
            ax.text(left + val + 0.8, 0, txt, ha="left", va="center", fontsize=9, color=THEME["text"])
        left += val

    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([])
    ax.set_xlabel("市值占比 (%)")
    ax.set_title("市值集中度结构（含稳定币与质押映射）", loc="left")
    _style_axes(ax, "x")
    _save_fig(fig, out)


def _plot_exchange_24h(rows: List[ExchangeRow], out: Path) -> None:
    if not rows:
        return
    ordered = sorted(rows, key=lambda r: (r.pct24h or 0.0), reverse=True)
    names = [r.name for r in ordered]
    pct = [r.pct24h or 0.0 for r in ordered]
    colors = [THEME["positive"] if x >= 0 else THEME["negative"] for x in pct]

    fig, ax = plt.subplots(figsize=(10.8, 5.4))
    y = list(range(len(names)))
    for i, v in enumerate(pct):
        ax.hlines(y=i, xmin=0, xmax=v, color=colors[i], linewidth=2.6, alpha=0.95)
    ax.scatter(pct, y, color=colors, s=85, zorder=3, edgecolors=THEME["bg"], linewidths=1.2)
    ax.axvline(0, color=THEME["muted"], linewidth=1.1)
    ax.set_xlabel("24h 成交额变化 (%)")
    ax.set_title("前排交易所 24h 成交额变化（棒棒糖图）", loc="left")
    _style_axes(ax, "x")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.invert_yaxis()

    max_abs = max(abs(x) for x in pct) if pct else 0.0
    lim = max(max_abs * 1.22, 3.0)
    ax.set_xlim(-lim, lim)
    offset = _label_offset(max_abs, ratio=0.03, floor=0.25)
    for i, v in enumerate(pct):
        v = pct[i]
        x = v + offset if v >= 0 else v - offset
        ha = "left" if v >= 0 else "right"
        ax.text(x, i, f"{v:+.1f}%", va="center", ha=ha, fontsize=8.8)
    _save_fig(fig, out)


def _plot_exchange_structure(rows: List[ExchangeRow], out: Path) -> None:
    rows = [r for r in rows if (r.spot24h or 0.0) > 0.0 or (r.deriv24h or 0.0) > 0.0]
    if not rows:
        return
    rows.sort(key=lambda r: (r.spot24h or 0.0) + (r.deriv24h or 0.0), reverse=True)
    rows = rows[:8]
    labels: List[str] = []
    spot_share: List[float] = []
    deriv_share: List[float] = []
    totals: List[float] = []
    for r in rows:
        spot = float(r.spot24h or 0.0) / 1e9
        deriv = float(r.deriv24h or 0.0) / 1e9
        total = spot + deriv
        if total <= 0:
            continue
        labels.append(r.name)
        spot_share.append(spot / total * 100.0)
        deriv_share.append(deriv / total * 100.0)
        totals.append(total)
    if not labels:
        return

    fig, ax = plt.subplots(figsize=(10.8, 5.4))
    y = list(range(len(labels)))
    ax.barh(y, spot_share, color=THEME["secondary"], edgecolor=THEME["bg"], height=0.62, label="Spot 占比")
    ax.barh(y, deriv_share, left=spot_share, color=THEME["primary"], edgecolor=THEME["bg"], height=0.62, label="Derivatives 占比")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("成交占比 (%)")
    ax.set_title("前排交易所现货/衍生品结构", loc="left")
    _style_axes(ax, "x")
    ax.legend(frameon=False, loc="lower right")

    for i in range(len(labels)):
        ax.text(101.0, i, f"{totals[i]:.1f}B", va="center", ha="left", fontsize=8.5, color=THEME["muted"])
    ax.text(1.02, -0.07, "右侧标注为总成交额(B USD)", transform=ax.transAxes, fontsize=8.3, color=THEME["muted"])
    _save_fig(fig, out)


def _plot_top_assets(rows: List[Dict[str, Any]], out: Path) -> None:
    if not rows:
        return
    rows = [r for r in rows if r.get("chg24") is not None]
    if not rows:
        return
    rows.sort(key=lambda x: x.get("chg24") or 0.0, reverse=True)
    names = [r.get("symbol") for r in rows]
    pct = [float(r.get("chg24") or 0.0) for r in rows]

    fig, ax = plt.subplots(figsize=(10.8, 3.1))
    max_abs = max(abs(x) for x in pct)
    max_abs = max(max_abs, 1.0)
    data = [pct]
    img = ax.imshow(data, cmap="RdYlGn", vmin=-max_abs, vmax=max_abs, aspect="auto")
    ax.set_title("Top10 资产 24h 热力格", loc="left")
    ax.set_yticks([])
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, fontsize=8.8)
    for i, v in enumerate(pct):
        txt_color = THEME["text"] if abs(v) < max_abs * 0.45 else THEME["bg"]
        ax.text(i, 0, f"{v:+.2f}%", ha="center", va="center", fontsize=8.7, color=txt_color, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(img, ax=ax, orientation="horizontal", fraction=0.12, pad=0.22)
    cbar.set_label("24h 涨跌幅 (%)")
    cbar.outline.set_visible(False)
    _save_fig(fig, out)


def _plot_stablecoin_yield_snapshot(rows: List[Dict[str, Any]], out: Path) -> None:
    if not rows:
        return
    ordered = sorted(
        rows,
        key=lambda r: (
            int(r.get("safety_rank") or 99),
            -(float(r.get("tvl_usd") or 0.0)),
            -(float(r.get("total_apy") or 0.0)),
        ),
    )[:10]
    if not ordered:
        return

    labels: List[str] = []
    native_part: List[float] = []
    rewards_part: List[float] = []
    totals: List[float] = []
    tvls: List[float] = []
    for r in ordered:
        protocol = str(r.get("protocol") or "")
        asset = str(r.get("asset") or "")
        chain = str(r.get("chain") or "")
        labels.append(f"{protocol}-{asset} ({chain})")
        native = _safe_float(r.get("supply_apy"))
        rewards = _safe_float(r.get("rewards_apy"))
        total = _safe_float(r.get("total_apy"))
        if total is None:
            total = float(native or 0.0) + float(rewards or 0.0)
        base = float(native or 0.0)
        reward = float(rewards or 0.0)
        if reward <= 0 and total is not None and total > base:
            reward = float(total - base)
        native_part.append(max(0.0, base))
        rewards_part.append(max(0.0, reward))
        totals.append(float(total or 0.0))
        tvls.append(float(r.get("tvl_usd") or 0.0) / 1e9)

    fig, ax = plt.subplots(figsize=(12.0, 5.6))
    y = list(range(len(labels)))
    ax.barh(y, native_part, color=THEME["primary"], edgecolor=THEME["bg"], height=0.58, label="Native APY")
    ax.barh(y, rewards_part, left=native_part, color=THEME["accent"], edgecolor=THEME["bg"], height=0.58, label="Rewards APY")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.invert_yaxis()
    ax.set_xlabel("收益率（%）")
    ax.set_title("稳定币收益快照（安全优先筛选）", loc="left")
    _style_axes(ax, "x")
    ax.legend(frameon=False, loc="lower right")

    xmax = max((x + yv) for x, yv in zip(native_part, rewards_part)) if native_part else 1.0
    ax.set_xlim(0, max(1.0, xmax * 1.32))
    for i in range(len(labels)):
        ax.text(
            native_part[i] + rewards_part[i] + 0.05,
            i,
            f"{totals[i]:.2f}% | TVL {tvls[i]:.2f}B",
            va="center",
            ha="left",
            fontsize=8.1,
            color=THEME["muted"],
        )

    _save_fig(fig, out)


def _plot_stablecoin_aave_vs_peers(rows: List[Dict[str, Any]], out: Path) -> None:
    if not rows:
        return
    assets = ["USDC", "USDT", "DAI", "USDS", "PYUSD", "SUSDS"]
    pairs: List[Tuple[str, float, float]] = []

    for asset in assets:
        aave_candidates = [
            r
            for r in rows
            if str(r.get("asset") or "").upper() == asset and str(r.get("protocol_key") or "") == "aave-v3" and _safe_float(r.get("total_apy")) is not None
        ]
        peer_candidates = [
            r
            for r in rows
            if str(r.get("asset") or "").upper() == asset and str(r.get("protocol_key") or "") != "aave-v3" and _safe_float(r.get("total_apy")) is not None
        ]
        if not aave_candidates or not peer_candidates:
            continue

        aave_best = max(aave_candidates, key=lambda x: float(x.get("tvl_usd") or 0.0))
        peer_best = max(peer_candidates, key=lambda x: float(x.get("total_apy") or 0.0))
        aave_apy = float(aave_best.get("total_apy") or 0.0)
        peer_apy = float(peer_best.get("total_apy") or 0.0)
        pairs.append((asset, aave_apy, peer_apy))

    if not pairs:
        return

    # Sort by absolute gap, larger gaps first for readability.
    pairs.sort(key=lambda x: abs(x[2] - x[1]), reverse=True)
    labels = [x[0] for x in pairs]
    aave_vals = [x[1] for x in pairs]
    peer_vals = [x[2] for x in pairs]

    fig, ax = plt.subplots(figsize=(10.8, 4.8))
    y = list(range(len(labels)))
    for i in range(len(labels)):
        lo = min(aave_vals[i], peer_vals[i])
        hi = max(aave_vals[i], peer_vals[i])
        ax.hlines(i, lo, hi, color=THEME["axis"], linewidth=2.0, zorder=1)
        ax.scatter([aave_vals[i]], [i], color=THEME["primary"], s=90, edgecolors=THEME["bg"], linewidths=1.0, zorder=3)
        ax.scatter([peer_vals[i]], [i], color=THEME["accent"], s=90, edgecolors=THEME["bg"], linewidths=1.0, zorder=3)
        gap = peer_vals[i] - aave_vals[i]
        ax.text(hi + 0.06, i, f"Δ {gap:+.2f}%", va="center", ha="left", fontsize=8.5, color=THEME["muted"])

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Total APY (%)")
    ax.set_title("Aave 与主流协议稳定币收益对比", loc="left")
    _style_axes(ax, "x")

    max_v = max(max(aave_vals), max(peer_vals), 1.0)
    ax.set_xlim(0, max_v * 1.35)
    handles = [
        Patch(facecolor=THEME["primary"], edgecolor=THEME["bg"], label="Aave"),
        Patch(facecolor=THEME["accent"], edgecolor=THEME["bg"], label="Best Peer"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower right")
    _save_fig(fig, out)


def _plot_rwa_asset_class_snapshot(rows: List[Dict[str, Any]], out: Path) -> None:
    pts = [r for r in rows if _safe_float(r.get("value_usd")) is not None]
    if not pts:
        return
    pts = sorted(pts, key=lambda r: float(r.get("value_usd") or 0.0), reverse=True)
    labels = [str(r.get("asset_class") or "") for r in pts]
    values = [float(r.get("value_usd") or 0.0) / 1e9 for r in pts]
    changes = [_safe_float(r.get("change_7d_pct")) for r in pts]
    colors = [THEME["positive"] if (c or 0.0) >= 0 else THEME["negative"] for c in changes]

    fig, ax = plt.subplots(figsize=(11.2, 5.2))
    y = list(range(len(labels)))
    ax.barh(y, values, color=colors, edgecolor=THEME["bg"], height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Distributed / represented value (USD, B)")
    ax.set_title("RWA资产类别快照（RWA.xyz）", loc="left")
    _style_axes(ax, "x")

    xmax = max(values) if values else 1.0
    ax.set_xlim(0, max(1.0, xmax * 1.35))
    for i, v in enumerate(values):
        c = changes[i]
        change_txt = "N/A" if c is None else f"7D {c:+.2f}%"
        ax.text(v + max(xmax * 0.025, 0.08), i, f"${v:.2f}B | {change_txt}", va="center", ha="left", fontsize=8.5, color=THEME["muted"])

    handles = [
        Patch(facecolor=THEME["positive"], edgecolor=THEME["bg"], label="7D up"),
        Patch(facecolor=THEME["negative"], edgecolor=THEME["bg"], label="7D down"),
    ]
    ax.legend(handles=handles, frameon=False, loc="lower right")
    _save_fig(fig, out)


def _plot_nondefi_carry_snapshot(rows: List[Dict[str, Any]], out: Path) -> None:
    pts = [r for r in rows if _safe_float(r.get("annual_funding_pct")) is not None]
    if not pts:
        return

    pts = sorted(pts, key=lambda r: float(r.get("annual_funding_pct") or 0.0), reverse=True)
    labels = [f"{r.get('exchange')}-{r.get('asset')}" for r in pts]
    funding_vals = [float(r.get("annual_funding_pct") or 0.0) for r in pts]
    basis_vals: List[Optional[float]] = [_safe_float(r.get("basis_pct")) for r in pts]
    colors = [THEME["primary"] if "Binance" in lb else THEME["accent"] for lb in labels]

    fig, ax = plt.subplots(figsize=(11.4, 5.4))
    y = list(range(len(labels)))
    ax.barh(y, funding_vals, color=colors, edgecolor=THEME["bg"], height=0.58)
    ax.axvline(0, color=THEME["muted"], linewidth=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.2)
    ax.invert_yaxis()
    ax.set_xlabel("Annualized Funding (%)")
    ax.set_title("非DeFi期现快照（资金费率主图）", loc="left")
    _style_axes(ax, "x")

    max_abs = max([abs(v) for v in funding_vals] + [1.0])
    ax.set_xlim(-max_abs * 1.35, max_abs * 1.35)
    offset = _label_offset(max_abs, ratio=0.03, floor=0.15)
    for i, v in enumerate(funding_vals):
        x = v + offset if v >= 0 else v - offset
        ha = "left" if v >= 0 else "right"
        basis = basis_vals[i]
        btxt = "N/A" if basis is None else f"{basis:+.2f}%"
        ax.text(x, i, f"{v:+.2f}%  |  basis {btxt}", va="center", ha=ha, fontsize=8.7)

    handles = [Patch(facecolor=THEME["primary"], edgecolor=THEME["bg"], label="Binance"), Patch(facecolor=THEME["accent"], edgecolor=THEME["bg"], label="OKX")]
    ax.legend(handles=handles, frameon=False, loc="lower right")
    _save_fig(fig, out)


def _plot_top2_intraday(series: Dict[str, List[Dict[str, Any]]], out: Path) -> None:
    btc_rows = series.get("BTC") or []
    eth_rows = series.get("ETH") or []
    if len(btc_rows) < 2 and len(eth_rows) < 2:
        fig, ax = plt.subplots(figsize=(10.8, 4.2))
        ax.axis("off")
        ax.text(0.02, 0.66, "BTC/ETH 近24h（1h）价格路径", fontsize=14, fontweight="bold", transform=ax.transAxes)
        ax.text(0.02, 0.42, "Binance 1h 数据暂不可用", fontsize=12, color=THEME["negative"], transform=ax.transAxes)
        ax.text(0.02, 0.26, "已降级为文本说明，避免正文图片引用失效。", fontsize=10.5, color=THEME["muted"], transform=ax.transAxes)
        _save_fig(fig, out)
        return

    fig, ax = plt.subplots(figsize=(10.8, 4.2))
    plotted = 0

    for asset, rows, color in [("BTC", btc_rows, THEME["btc"]), ("ETH", eth_rows, THEME["eth"])]:
        closes = [float(r.get("close") or 0.0) for r in rows if r.get("close") is not None]
        if len(closes) < 2:
            continue
        base = closes[0]
        if base <= 0:
            continue
        norm = [x / base * 100.0 for x in closes]
        x = list(range(len(norm)))
        chg = (closes[-1] / closes[0] - 1.0) * 100.0
        ax.plot(x, norm, color=color, linewidth=2.2, label=f"{asset} ({chg:+.2f}%)")
        ax.scatter([x[-1]], [norm[-1]], color=color, s=38, zorder=3, edgecolors=THEME["bg"], linewidths=1.0)
        plotted += 1

    if plotted == 0:
        plt.close(fig)
        return

    # Use BTC timestamps for x labels when available; otherwise fallback to ETH.
    x_rows = btc_rows if len(btc_rows) >= 2 else eth_rows
    x_labels = []
    for r in x_rows:
        ts = r.get("ts")
        if isinstance(ts, datetime):
            x_labels.append(ts.strftime("%m-%d %H:%M"))
        else:
            x_labels.append("")

    x_len = len(x_labels)
    if x_len > 1:
        step = max(1, x_len // 6)
        ticks = list(range(0, x_len, step))
        if ticks[-1] != x_len - 1:
            ticks.append(x_len - 1)
        ax.set_xticks(ticks)
        ax.set_xticklabels([x_labels[i] for i in ticks], rotation=20, ha="right", fontsize=8.4)

    ax.set_title("BTC/ETH 近24h（1h）价格路径", loc="left")
    ax.set_ylabel("归一化价格（起点=100）")
    _style_axes(ax, "y")
    ax.legend(frameon=False, ncol=2, loc="upper left")
    _save_fig(fig, out)


def _plot_derivatives(deribit: Dict[str, Optional[float]], dvol: Dict[str, Optional[float]], out: Path) -> None:
    f_btc = (deribit.get("btc_funding_8h") or 0.0) * 10000.0
    f_eth = (deribit.get("eth_funding_8h") or 0.0) * 10000.0
    oi_btc = (deribit.get("btc_open_interest") or 0.0) / 1e6
    oi_eth = (deribit.get("eth_open_interest") or 0.0) / 1e6
    d_btc = dvol.get("btc_dvol_close") or 0.0
    d_eth = dvol.get("eth_dvol_close") or 0.0

    fig = plt.figure(figsize=(12.8, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.2)
    ax_radar = fig.add_subplot(gs[0, 0], projection="polar")
    ax_tbl = fig.add_subplot(gs[0, 1])

    metrics = ["Funding强度", "OI强度", "DVOL强度"]
    max_f = max(abs(f_btc), abs(f_eth), 0.1)
    max_oi = max(oi_btc, oi_eth, 0.1)
    max_d = max(d_btc, d_eth, 1.0)
    btc_norm = [abs(f_btc) / max_f, oi_btc / max_oi, d_btc / max_d]
    eth_norm = [abs(f_eth) / max_f, oi_eth / max_oi, d_eth / max_d]

    angles = [n / float(len(metrics)) * 2 * math.pi for n in range(len(metrics))]
    angles += angles[:1]
    btc_plot = btc_norm + btc_norm[:1]
    eth_plot = eth_norm + eth_norm[:1]

    ax_radar.set_theta_offset(math.pi / 2)
    ax_radar.set_theta_direction(-1)
    ax_radar.plot(angles, btc_plot, color=THEME["btc"], linewidth=2.2, label="BTC")
    ax_radar.fill(angles, btc_plot, color=THEME["btc"], alpha=0.2)
    ax_radar.plot(angles, eth_plot, color=THEME["eth"], linewidth=2.2, label="ETH")
    ax_radar.fill(angles, eth_plot, color=THEME["eth"], alpha=0.18)
    ax_radar.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], metrics)
    ax_radar.set_ylim(0, 1.0)
    ax_radar.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax_radar.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=8)
    ax_radar.grid(color=THEME["grid"], linewidth=0.85)
    ax_radar.set_title("BTC vs ETH 衍生品强度雷达", y=1.1, loc="left")
    ax_radar.legend(loc="upper right", bbox_to_anchor=(1.2, 1.12), frameon=False)

    ax_tbl.axis("off")
    table_rows = [
        ["Funding 8h (bps)", f"{f_btc:+.2f}", f"{f_eth:+.2f}"],
        ["Perp OI (M)", f"{oi_btc:.1f}", f"{oi_eth:.1f}"],
        ["DVOL 收盘", f"{d_btc:.1f}", f"{d_eth:.1f}"],
    ]
    table = ax_tbl.table(
        cellText=table_rows,
        colLabels=["指标", "BTC", "ETH"],
        loc="center",
        cellLoc="center",
        colLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.65)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(THEME["bg"])
        if r == 0:
            cell.set_facecolor(THEME["axis"])
            cell.set_text_props(weight="bold")
        else:
            cell.set_facecolor(THEME["panel"])
    ax_tbl.text(0.03, 0.16, "雷达图为归一化强度，方向以原始数值为准。", fontsize=8.5, color=THEME["muted"], transform=ax_tbl.transAxes)

    fig.suptitle("衍生品快照", x=0.07, ha="left", fontweight="bold")
    _save_fig(fig, out)


def _plot_sentiment_snapshot(fng_val: Optional[float], fng_delta: Optional[float], btc_dvol: Optional[float], eth_dvol: Optional[float], out: Path) -> None:
    if all(v is None for v in [fng_val, fng_delta, btc_dvol, eth_dvol]):
        return
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))

    # Left: semicircle gauge for F&G
    ax_g = axes[0]
    ax_g.set_title("情绪温度计（F&G）", loc="left")
    ax_g.set_aspect("equal")
    ax_g.axis("off")
    bands = [
        (180, 120, "#FCA5A5"),
        (120, 60, "#FCD34D"),
        (60, 0, "#86EFAC"),
    ]
    for start, end, color in bands:
        ax_g.add_patch(Wedge((0, 0), 1.0, end, start, width=0.22, facecolor=color, edgecolor=THEME["bg"]))

    val = float(fng_val or 0.0)
    val = max(0.0, min(100.0, val))
    angle = math.radians(180 - val * 1.8)
    ax_g.plot([0, 0.72 * math.cos(angle)], [0, 0.72 * math.sin(angle)], color=THEME["text"], linewidth=2.4)
    ax_g.scatter([0], [0], s=34, color=THEME["text"], zorder=3)
    ax_g.text(-1.0, -0.08, "0", fontsize=8.5, color=THEME["muted"])
    ax_g.text(-0.04, 1.02, "50", fontsize=8.5, color=THEME["muted"])
    ax_g.text(0.95, -0.08, "100", fontsize=8.5, color=THEME["muted"])
    if fng_val is None:
        ax_g.text(0, -0.2, "N/A", ha="center", va="center", fontsize=18, fontweight="bold")
    else:
        delta_txt = "N/A" if fng_delta is None else f"{float(fng_delta):+,.0f}"
        delta_color = THEME["muted"] if fng_delta is None else (THEME["positive"] if float(fng_delta) >= 0 else THEME["negative"])
        ax_g.text(0, -0.12, f"{val:.0f}", ha="center", va="center", fontsize=20, fontweight="bold")
        ax_g.text(0, -0.32, f"Δ {delta_txt}", ha="center", va="center", fontsize=10, color=delta_color)
    ax_g.set_xlim(-1.2, 1.2)
    ax_g.set_ylim(-0.45, 1.15)

    # Right: DVOL regime dot plot
    ax_d = axes[1]
    ax_d.set_title("隐含波动定位（DVOL）", loc="left")
    ax_d.axhspan(0, 45, color="#DCFCE7", alpha=0.75)
    ax_d.axhspan(45, 60, color="#FEF3C7", alpha=0.75)
    ax_d.axhspan(60, 100, color="#FEE2E2", alpha=0.75)
    ax_d.axhline(45, color=THEME["muted"], linestyle="--", linewidth=1)
    ax_d.axhline(60, color=THEME["muted"], linestyle="--", linewidth=1)
    x = [0, 1]
    vals = [float(btc_dvol or 0.0), float(eth_dvol or 0.0)]
    colors = [THEME["btc"], THEME["eth"]]
    ax_d.plot(x, vals, color=THEME["axis"], linewidth=1.4, zorder=1)
    ax_d.scatter(x, vals, s=[145, 145], color=colors, edgecolors=THEME["bg"], linewidths=1.4, zorder=3)
    ax_d.set_xticks(x)
    ax_d.set_xticklabels(["BTC DVOL", "ETH DVOL"])
    ax_d.set_ylim(0, 100)
    ax_d.set_ylabel("指数")
    _style_axes(ax_d, "y")
    for i, v in enumerate(vals):
        txt = "N/A" if [btc_dvol, eth_dvol][i] is None else f"{v:.1f}"
        ax_d.text(x[i], v + 2.2, txt, ha="center", va="bottom", fontsize=8.7, fontweight="bold")
    ax_d.text(1.02, 0.16, "0-45: Complacency", fontsize=8, color=THEME["muted"], transform=ax_d.transAxes)
    ax_d.text(1.02, 0.31, "45-60: Neutral", fontsize=8, color=THEME["muted"], transform=ax_d.transAxes)
    ax_d.text(1.02, 0.58, "60+: Panic", fontsize=8, color=THEME["muted"], transform=ax_d.transAxes)

    fig.suptitle("情绪与波动当日快照", x=0.07, ha="left", fontweight="bold")
    _save_fig(fig, out)


def _build_context(target_date: date) -> DailyContext:
    from cex_daily_modules.pipeline import build_context

    return build_context(sys.modules[__name__], target_date)


def _write_manifest(path: Path, ctx: DailyContext) -> None:
    from cex_daily_modules.registry import MODULE_SOURCES

    core_modules = {
        "market_history": all(
            value is not None
            for value in (ctx.market_cap, ctx.prev_market_cap, ctx.volume_24h, ctx.prev_volume_24h, ctx.btc_dom, ctx.prev_btc_dom)
        ),
        "top_assets": len(ctx.top_assets) >= 5,
        "btc_eth_24h": all((ctx.top2_trend.get(asset) or {}).get("price") is not None for asset in ("BTC", "ETH")),
        "derivatives": all(ctx.deribit.get(key) is not None for key in ("btc_funding_8h", "eth_funding_8h")),
        "rwa_asset_classes": bool(ctx.rwa_asset_classes),
        "rwa_token_movers": bool(ctx.rwa_token_movers),
    }
    if not all(core_modules.values()):
        coverage_status = "degraded"
    elif ctx.data_gaps or ctx.source_warnings:
        coverage_status = "partial"
    else:
        coverage_status = "complete"
    obj = {
        "date": ctx.target_date.isoformat(),
        "generated_at_shanghai": ctx.generated_at_shanghai,
        "data_gaps": ctx.data_gaps,
        "source_warnings": ctx.source_warnings,
        "coverage_status": coverage_status,
        "coverage": {
            "status": coverage_status,
            "core_modules": core_modules,
            "data_gap_count": len(ctx.data_gaps),
            "source_warning_count": len(ctx.source_warnings),
            "modules": ctx.module_status,
        },
        "module_sources": MODULE_SOURCES,
        "market": {
            "as_of": ctx.market_as_of,
            "lag_days": ctx.market_lag_days,
            "market_cap": ctx.market_cap,
            "prev_market_cap": ctx.prev_market_cap,
            "volume_24h": ctx.volume_24h,
            "prev_volume_24h": ctx.prev_volume_24h,
            "btc_dom": ctx.btc_dom,
            "prev_btc_dom": ctx.prev_btc_dom,
        },
        "counts": {
            "top_assets": len(ctx.top_assets),
            "exchanges": len(ctx.exchanges),
            "nondefi_carry": len(ctx.nondefi_carry),
            "borrow_rates": len(ctx.borrow_rates),
            "stablecoin_yields": len(ctx.stablecoin_yields),
            "stablecoin_yields_extended": len(ctx.stablecoin_yields_extended),
            "stablecoin_cefi_rates": len(ctx.stablecoin_cefi_rates),
            "rwa_asset_classes": len(ctx.rwa_asset_classes),
            "rwa_token_movers": len(ctx.rwa_token_movers),
            "rwa_smartmoney_covered_assets": int((ctx.rwa_smartmoney or {}).get("covered_assets") or 0),
            "rwa_smartmoney_active_signals": int((ctx.rwa_smartmoney or {}).get("active_signals") or 0),
            "taoli_binance_margin_rates": len(ctx.taoli_binance_margin_rates),
            "smartmoney_traders": len(ctx.smartmoney_traders),
            "smartmoney_signals": len(ctx.smartmoney_signals),
            "smartmoney_position_rows": len((ctx.smartmoney_positions or {}).get("rows") or []),
            "okx_news_sentiment_rows": len((ctx.okx_news_sentiment or {}).get("rows") or []),
        },
        "top2_trend": ctx.top2_trend,
        "top2_intraday_points": {
            "BTC": len(ctx.top2_intraday.get("BTC") or []),
            "ETH": len(ctx.top2_intraday.get("ETH") or []),
        },
        "nondefi_carry": ctx.nondefi_carry,
        "borrow_rates": ctx.borrow_rates,
        "coingecko": ctx.coingecko_capability,
        "derivatives": ctx.deribit,
        "dvol": ctx.dvol,
        "sentiment": ctx.fng,
        "breadth_snapshot": ctx.breadth_snapshot,
        "source_registry": {
            "market_cap_volume_btc_dominance": "CoinMarketCap global metrics historical",
            "top_assets": ctx.coingecko_capability.get("used"),
            "btc_24h": (ctx.top2_trend.get("BTC") or {}).get("source"),
            "eth_24h": (ctx.top2_trend.get("ETH") or {}).get("source"),
            "btc_intraday": ((ctx.top2_intraday.get("BTC") or [{}])[-1]).get("source"),
            "eth_intraday": ((ctx.top2_intraday.get("ETH") or [{}])[-1]).get("source"),
            "btc_perpetual": ctx.deribit.get("btc_source"),
            "eth_perpetual": ctx.deribit.get("eth_source"),
            "btc_dvol": ctx.dvol.get("btc_source"),
            "eth_dvol": ctx.dvol.get("eth_source"),
            "fear_greed": ctx.fng.get("source"),
            "stablecoin_yields": "DefiLlama + protocol official APIs",
            "stablecoin_platform_apy": "Bitcompare (CeFi/DeFi/Hybrid)",
            "rwa_smart_money": (ctx.rwa_smartmoney or {}).get("source"),
        },
        "stablecoin_yields": ctx.stablecoin_yields,
        "stablecoin_yields_extended": ctx.stablecoin_yields_extended,
        "stablecoin_cefi_rates": ctx.stablecoin_cefi_rates,
        "rwa_asset_classes": ctx.rwa_asset_classes,
        "rwa_token_movers": ctx.rwa_token_movers,
        "rwa_smartmoney": ctx.rwa_smartmoney,
        "taoli_binance_margin_rates": ctx.taoli_binance_margin_rates,
        "smartmoney_traders": ctx.smartmoney_traders,
        "smartmoney_signals": ctx.smartmoney_signals,
        "smartmoney_positions": ctx.smartmoney_positions,
        "okx_news_sentiment": ctx.okx_news_sentiment,
    }
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_report(path: Path, ctx: DailyContext) -> None:
    mc_chg = (ctx.market_cap / ctx.prev_market_cap - 1.0) * 100.0 if ctx.market_cap and ctx.prev_market_cap else None
    vol_chg = (ctx.volume_24h / ctx.prev_volume_24h - 1.0) * 100.0 if ctx.volume_24h and ctx.prev_volume_24h else None
    dom_chg = (ctx.btc_dom - ctx.prev_btc_dom) if (ctx.btc_dom is not None and ctx.prev_btc_dom is not None) else None
    market_complete = all(v is not None for v in (ctx.market_cap, ctx.prev_market_cap, ctx.volume_24h, ctx.prev_volume_24h, ctx.btc_dom, ctx.prev_btc_dom))
    market_as_of = ctx.market_as_of or ctx.target_date.isoformat()
    market_time_label = "当日" if market_as_of == ctx.target_date.isoformat() else f"最新可得（截至 {market_as_of}）"

    asset_rows = [x for x in ctx.top_assets if x.get("chg24") is not None and _is_risk_breadth_asset(x)]
    asset_up = sum(1 for x in asset_rows if (x.get("chg24") or 0.0) > 0)
    asset_dn = sum(1 for x in asset_rows if (x.get("chg24") or 0.0) < 0)
    asset_flat = sum(1 for x in asset_rows if float(x.get("chg24") or 0.0) == 0.0)
    asset_sorted = sorted(asset_rows, key=lambda x: x.get("chg24") or 0.0, reverse=True)
    asset_top = asset_sorted[0] if asset_sorted else None
    asset_tail = asset_sorted[-1] if asset_sorted else None
    asset_avg = (sum(float(x.get("chg24") or 0.0) for x in asset_rows) / len(asset_rows)) if asset_rows else None
    asset_spread = (
        (float(asset_top.get("chg24") or 0.0) - float(asset_tail.get("chg24") or 0.0))
        if asset_top and asset_tail
        else None
    )

    exch_sorted = [x for x in ctx.exchanges if x.pct24h is not None]
    exch_sorted.sort(key=lambda x: x.pct24h or 0.0, reverse=True)
    exch_top = exch_sorted[0] if exch_sorted else None
    exch_tail = exch_sorted[-1] if exch_sorted else None
    exch_up = sum(1 for x in exch_sorted if (x.pct24h or 0.0) > 0)
    exch_dn = sum(1 for x in exch_sorted if (x.pct24h or 0.0) < 0)
    exch_mid = (sum(float(x.pct24h or 0.0) for x in exch_sorted) / len(exch_sorted)) if exch_sorted else None

    total_spot = sum(float(x.spot24h or 0.0) for x in ctx.exchanges)
    total_deriv = sum(float(x.deriv24h or 0.0) for x in ctx.exchanges)
    deriv_share = (total_deriv / (total_spot + total_deriv) * 100.0) if (total_spot + total_deriv) > 0 else None

    outside_share = ctx.breadth_snapshot.get("outside_top10_share")
    btc_share = ctx.breadth_snapshot.get("btc_share")
    top2_10_share = ctx.breadth_snapshot.get("top2_to_10_share")
    risk_asset_symbols = ctx.breadth_snapshot.get("risk_asset_symbols") or []
    excluded_symbols = ctx.breadth_snapshot.get("excluded_symbols") or []

    fng_val = ctx.fng.get("value")
    fng_delta = ctx.fng.get("delta")
    fng_as_of = str(ctx.fng.get("as_of") or ctx.target_date.isoformat())
    fng_time_label = "当日" if fng_as_of == ctx.target_date.isoformat() else f"最新可得值（截至 {fng_as_of}）"
    btc_funding = ctx.deribit.get("btc_funding_8h")
    eth_funding = ctx.deribit.get("eth_funding_8h")
    btc_oi = ctx.deribit.get("btc_open_interest")
    eth_oi = ctx.deribit.get("eth_open_interest")
    btc_dvol = ctx.dvol.get("btc_dvol_close")
    eth_dvol = ctx.dvol.get("eth_dvol_close")
    btc_funding_bps = btc_funding * 10000.0 if btc_funding is not None else None
    eth_funding_bps = eth_funding * 10000.0 if eth_funding is not None else None
    dvol_pair = f"{btc_dvol:.2f}/{eth_dvol:.2f}" if btc_dvol is not None and eth_dvol is not None else "N/A"
    btc_t = ctx.top2_trend.get("BTC") if isinstance(ctx.top2_trend, dict) else None
    eth_t = ctx.top2_trend.get("ETH") if isinstance(ctx.top2_trend, dict) else None
    intraday_change: Dict[str, Optional[float]] = {}
    for asset in ("BTC", "ETH"):
        series = ctx.top2_intraday.get(asset) or []
        first = _safe_float(series[0].get("close")) if series else None
        last = _safe_float(series[-1].get("close")) if series else None
        intraday_change[asset] = ((last / first - 1.0) * 100.0) if first and last else None
    nondefi_rows = ctx.nondefi_carry or []
    nondefi_venues = sorted({str(r.get("exchange") or "") for r in nondefi_rows if r.get("exchange")})
    borrow_rate_rows = ctx.borrow_rates or []
    nondefi_with_funding = [r for r in nondefi_rows if r.get("annual_funding_pct") is not None]
    nondefi_with_basis = [r for r in nondefi_rows if r.get("basis_pct") is not None]
    nondefi_best = (
        max(nondefi_with_funding, key=lambda r: float(r.get("annual_funding_pct") or -10**9))
        if nondefi_with_funding
        else None
    )
    nondefi_most_negative = (
        min(nondefi_with_funding, key=lambda r: float(r.get("annual_funding_pct") or 10**9))
        if nondefi_with_funding
        else None
    )
    nondefi_basis_abs_max = (
        max(nondefi_with_basis, key=lambda r: abs(float(r.get("basis_pct") or 0.0)))
        if nondefi_with_basis
        else None
    )
    stable_rows = ctx.stablecoin_yields or []
    stable_rows_extended_all = ctx.stablecoin_yields_extended or []
    stable_rows_extended_top = stable_rows_extended_all[:10]
    stable_cefi_rows = ctx.stablecoin_cefi_rates or []
    rwa_rows = ctx.rwa_asset_classes or []
    rwa_movers = ctx.rwa_token_movers or []
    rwa_top = max(rwa_rows, key=lambda r: float(r.get("value_usd") or 0.0)) if rwa_rows else None
    rwa_rising = [r for r in rwa_rows if (_safe_float(r.get("change_7d_pct")) or 0.0) > 0]
    rwa_falling = [r for r in rwa_rows if (_safe_float(r.get("change_7d_pct")) or 0.0) < 0]
    rwa_trade_like = [
        r
        for r in rwa_rows
        if str(r.get("asset_class") or "") in {"Tokenized Stocks", "Active Strategies", "Non-U.S. Government Debt"}
    ]
    taoli_rows = ctx.taoli_binance_margin_rates or []
    stable_top: List[Dict[str, Any]] = []
    stable_asset_order = {"USDC": 1, "USDT": 2, "DAI": 3, "USDS": 4, "SUSDS": 5, "PYUSD": 6}
    stable_chain_order = {"Ethereum": 1, "Arbitrum": 2, "Base": 3}
    stable_extended = sorted(
        [
            r
            for r in stable_rows
            if (_safe_float(r.get("tvl_usd")) is not None and float(_safe_float(r.get("tvl_usd")) or 0.0) >= 1_000_000.0)
        ],
        key=lambda r: (
            stable_asset_order.get(str(r.get("asset") or "").upper(), 99),
            int(STABLE_YIELD_PROJECT_PRIORITY.get(str(r.get("protocol_key") or ""), 99)),
            stable_chain_order.get(str(r.get("chain") or ""), 99),
            -float(r.get("tvl_usd") or 0.0),
        ),
    )
    if stable_rows:
        # Keep cross-protocol comparability first, then fill with highest-ranked pools.
        seen_protocols: set[str] = set()
        for r in stable_rows:
            p = str(r.get("protocol") or "")
            if p and p not in seen_protocols:
                stable_top.append(r)
                seen_protocols.add(p)
        for r in stable_rows:
            if len(stable_top) >= 10:
                break
            if r not in stable_top:
                stable_top.append(r)
    stable_with_rewards = sum(1 for r in stable_top if (r.get("rewards_apy") or 0.0) > 0)
    stable_with_caps = sum(1 for r in stable_top if (r.get("supply_cap_usd") is not None or r.get("borrow_cap_usd") is not None))
    stable_with_state = sum(1 for r in stable_top if (r.get("is_paused") is not None or r.get("is_frozen") is not None))
    stable_supply_cov = (
        sum(1 for r in stable_top if r.get("supply_apy") is not None) / len(stable_top) * 100.0 if stable_top else None
    )
    stable_borrow_cov = (
        sum(1 for r in stable_top if r.get("borrow_apy") is not None) / len(stable_top) * 100.0 if stable_top else None
    )
    stable_util_cov = (
        sum(1 for r in stable_top if r.get("utilization_pct") is not None) / len(stable_top) * 100.0 if stable_top else None
    )
    stable_native_avg = (
        sum(float(r.get("supply_apy") or 0.0) for r in stable_top if r.get("supply_apy") is not None) / max(1, sum(1 for r in stable_top if r.get("supply_apy") is not None))
        if stable_top
        else None
    )

    # Regime + narrative layer: prioritize interpretation over raw numbers.
    if mc_chg is None or vol_chg is None:
        regime_label = "核心数据覆盖不足"
        regime_text = "全市场市值或成交数据不完整，不能判断量价关系、广度扩散或风险预算变化。"
    elif mc_chg >= 1.0 and vol_chg >= 0:
        regime_label = "交易性修复"
        regime_text = "价格与成交共振上行；现有样本只覆盖头部风险资产，尚不足以证明长尾市场已扩散。"
    elif mc_chg < 0 and vol_chg >= 0:
        regime_label = "压力重定价"
        regime_text = "价格回撤但换手抬升，说明市场在高分歧下重估风险，波动脉冲概率偏高。"
    elif mc_chg < 0 and vol_chg < 0:
        regime_label = "防守下移"
        regime_text = "价格与成交同步走弱，属于防守型下移结构，短线以控制回撤为主。"
    elif mc_chg >= 0 and vol_chg < 0:
        regime_label = "缩量修复"
        regime_text = "市值上升但成交下降，价格修复尚未得到交易活跃度确认。"
    else:
        regime_label = "区间交易"
        regime_text = "价格与成交未形成同向趋势，市场仍在区间内进行结构轮动。"

    breadth_call = "头部风险资产样本不足，暂不判断参与度。"
    observed_risk_assets = asset_up + asset_dn + asset_flat
    if observed_risk_assets:
        if asset_up / observed_risk_assets >= 0.7:
            breadth_call = "头部风险资产上涨覆盖率较高，但该样本不能外推为长尾扩散。"
        elif asset_dn / observed_risk_assets >= 0.7:
            breadth_call = "头部风险资产下跌覆盖率较高，风险参与度偏弱。"
        else:
            breadth_call = "头部风险资产涨跌分化，方向一致性有限。"

    venue_call = "平台流量呈分化状态，头部与非头部恢复节奏不一致。"
    if exch_up is not None and exch_dn is not None:
        if exch_up > exch_dn:
            venue_call = "多数平台成交回暖，短线流动性环境较前一日改善。"
        elif exch_up < exch_dn:
            venue_call = "多数平台成交走弱，样本只支持成交收缩及降幅分化，不支持资金回流判断。"

    leverage_call = "杠杆拥挤度整体可控。"
    if btc_funding_bps is not None and eth_funding_bps is not None:
        if btc_funding_bps > 1.0 or eth_funding_bps > 1.0:
            leverage_call = "多头付费抬升，杠杆侧开始拥挤，需警惕回撤时的资金费率反转。"
        elif btc_funding_bps < -1.0 or eth_funding_bps < -1.0:
            leverage_call = "空头付费偏深，短线挤空风险上升，但趋势确认仍需成交配合。"

    vol_call = "期权端对尾部波动的定价仍偏谨慎。"
    if btc_dvol is not None and eth_dvol is not None:
        if btc_dvol < 45 and eth_dvol < 60:
            vol_call = "隐含波动率处于相对低位，期权保护成本当前不高。"
        elif btc_dvol > 65 or eth_dvol > 85:
            vol_call = "隐含波动率处于高位区，市场对尾部风险仍给出较高保险价格。"

    sentiment_call = "情绪与价格修复节奏尚未完全同步。"
    if fng_val is not None:
        if fng_val < 25:
            sentiment_call = "情绪仍在恐惧区，反弹更容易受到外部事件扰动。"
        elif fng_val > 60:
            sentiment_call = "情绪回到偏乐观区，若成交不跟随，需防止短线追高回撤。"

    desk_note_1 = "仓位管理优先级高于方向押注，建议保持核心仓位稳定、战术仓位滚动。"
    desk_note_2 = "若交易所衍生品占比继续上升，建议同步收紧杠杆和止损参数。"
    desk_note_3 = "关注情绪改善与广度扩散是否同步发生，二者背离时避免追逐单边。"

    pulse_detail = "核心数据不足，当前不能判断价格、成交与主导率之间的关系。"
    if mc_chg is not None and vol_chg is not None:
        if mc_chg > 0 and vol_chg > 0:
            pulse_detail = "价格与成交同步上行，属于健康修复结构；若次日成交不掉队，修复延续概率更高。"
        elif mc_chg > 0 and vol_chg < 0:
            pulse_detail = "价格上涨但成交回落，反弹质量偏弱，需警惕高位回吐。"
        elif mc_chg < 0 and vol_chg > 0:
            pulse_detail = "价格下行但换手放大，反映分歧加剧，通常伴随更高的日内波动。"
        else:
            pulse_detail = "价格与成交同步走弱，风险偏好仍在收缩，盘面更偏防守。"

    breadth_detail = (
        f"方向样本为 {len(risk_asset_symbols)} 个头部风险资产，已排除 {', '.join(excluded_symbols) or '无'}；"
        "Top10 外占比仅是市值集中度，不作为风险扩散代理。"
    )

    asset_detail = "头部资产分化仍在，当前更像结构行情。"
    if asset_up + asset_dn > 0:
        if asset_up >= 7:
            asset_detail = "上涨家数明显占优，但首尾分化仍大，表明反弹并非无差别普涨。"
        elif asset_up <= 3:
            asset_detail = "下跌家数占优，风险偏好修复仍较脆弱，短线追高性价比一般。"
        else:
            asset_detail = "涨跌家数接近均衡，市场处于结构轮动阶段，方向一致性较弱。"

    exchange_detail = "平台流量分层明显，交易恢复并不均匀。"
    if exch_top and exch_tail:
        gap = (exch_top.pct24h or 0.0) - (exch_tail.pct24h or 0.0)
        if exch_up == 0 and exch_dn > 0:
            exchange_detail = f"样本平台成交普遍收缩，最小与最大降幅相差 {gap:.2f}pct；这只说明收缩幅度不同，不构成流动性回流或价格发现能力增强的证据。"
        else:
            exchange_detail = f"最强与最弱平台的 24h 变化差达到 {gap:.2f}pct，说明平台间成交变化分化，但不能据此推断资金因果流向。"

    structure_detail = "衍生品在样本成交中占比较高，短线波动通常会被杠杆交易放大。"
    if deriv_share is not None:
        if deriv_share >= 85:
            structure_detail = "衍生品占比处于高位；是否放大波动仍需结合盘口、强平与 DVOL 数据验证。"
        elif deriv_share >= 70:
            structure_detail = "衍生品仍是主导成交形态，但该占比不能单独证明价格由杠杆情绪驱动。"
        else:
            structure_detail = "现货占比回升，有助于降低短线噪音，趋势延续性相对更好。"

    deriv_detail = "Funding 与 DVOL 的组合显示，方向拥挤暂未极端，但尾部风险定价仍未完全回落。"
    if btc_funding_bps is not None and eth_funding_bps is not None and btc_dvol is not None and eth_dvol is not None:
        if abs(btc_funding_bps) < 0.5 and abs(eth_funding_bps) < 0.5 and (btc_dvol > 50 or eth_dvol > 70):
            deriv_detail = "资金费率接近中性，说明方向拥挤度有限；但 DVOL 仍偏高，市场对突发波动仍保留保险溢价。"
        elif btc_funding_bps > 1.0 or eth_funding_bps > 1.0:
            deriv_detail = "多头付费抬升且波动仍高，组合信号偏向拥挤，需防范回撤时杠杆反身性。"
        elif btc_funding_bps < -1.0 or eth_funding_bps < -1.0:
            deriv_detail = "空头付费偏深，若成交继续回暖，短线有挤空触发条件。"

    sentiment_detail = "情绪仍在低位区，价格修复尚未转化为广泛风险偏好回升。"
    if fng_val is not None:
        if fng_val < 25 and fng_delta is not None and fng_delta > 0:
            sentiment_detail = "恐惧区内出现边际改善，说明市场开始试探修复，但尚不足以支持激进风险暴露。"
        elif fng_val < 25:
            sentiment_detail = "情绪维持在恐惧区，反弹通常更依赖事件驱动，持续性需要成交确认。"
        elif fng_val < 45:
            sentiment_detail = "情绪仍在恐惧区但已脱离极端恐惧，是否修复仍需成交和广度确认。"
        elif fng_val < 56:
            sentiment_detail = "情绪处于中性区，后续需要成交和广度同步改善才能确认趋势。"
        else:
            sentiment_detail = "情绪进入偏乐观区，需关注是否出现过热信号与波动回摆。"

    lines: List[str] = []
    lines.append(f"# 二级市场日报（{ctx.target_date.isoformat()}）")
    lines.append("")
    lines.append("## 今日亮点")
    if exch_mid is not None:
        lines.append(f"- 前排交易所样本成交普遍收缩：上涨 {exch_up} 家、下跌 {exch_dn} 家，24h 变化均值 {_fmt_pct(exch_mid)}。")
    tokenized_stocks = next((r for r in rwa_rows if str(r.get("asset_class")) == "Tokenized Stocks"), None)
    if tokenized_stocks:
        lines.append(
            f"- Tokenized Stocks 类别规模 {_fmt_usd(_safe_float(tokenized_stocks.get('value_usd')))}，"
            f"7D {_fmt_pct(_safe_float(tokenized_stocks.get('change_7d_pct')))}（截至 {tokenized_stocks.get('as_of') or 'N/A'}）。"
        )
    if rwa_movers:
        movers_text = "、".join(f"{r.get('ticker')} {_fmt_pct(_safe_float(r.get('change_24h_pct')))}" for r in rwa_movers[:3])
        lines.append(f"- RWA 映射异动居前：{movers_text}；底层市场休市时仅作为链上价格变化观察，不作溢折价结论。")
    lines.append("")
    lines.append("## 数据时点与口径")
    lines.append(
        f"- 采集完成时间：{ctx.generated_at_shanghai}（Asia/Shanghai）；全市场指标：{market_time_label}；"
        f"F&G：截至 {fng_as_of}；RWA 类别：截至 "
        f"{max((str(r.get('as_of')) for r in rwa_rows if r.get('as_of')), default='N/A')}。"
    )
    lines.append(
        f"- Top10 来源：{ctx.coingecko_capability.get('used') or '不可用'}；"
        f"BTC/ETH rolling 24h：{(btc_t or {}).get('source') or '不可用'}；"
        f"永续与 DVOL：{ctx.deribit.get('btc_source') or '不可用'} / {ctx.dvol.get('btc_source') or '不可用'}。"
    )
    lines.append("- fallback 只替换等价指标并保留真实来源和截止时间；来源失败详情仅记录在 manifest 后台字段。")
    lines.append("")
    lines.append("## 关键结论")
    if market_complete:
        lines.append(
            f"- 全市场指标{market_time_label}：市值 {_fmt_usd(ctx.market_cap)}（24h {_fmt_pct(mc_chg)}），"
            f"成交额 {_fmt_usd(ctx.volume_24h)}（24h {_fmt_pct(vol_chg)}）。"
        )
        lines.append(
            f"- BTC 主导率 {_fmt_pct(ctx.btc_dom, signed=False)}（{dom_chg:+.2f}pct），Top10 外市值占比（集中度口径）{outside_share:.2f}%。"
            if dom_chg is not None and outside_share is not None
            else f"- BTC 主导率 {_fmt_pct(ctx.btc_dom, signed=False)}。"
        )
    else:
        lines.append("- 全市场市值、成交额或 BTC 主导率数据不完整，本期不判断量价关系和市场广度。")
    lines.append(
        f"- 头部风险资产（排除稳定币、质押及信用映射）上涨 {asset_up} / 下跌 {asset_dn} / 平盘 {asset_flat}，平均涨跌幅 {_fmt_pct(asset_avg)}，首尾分化 {asset_spread:.2f}pct。"
        if asset_avg is not None and asset_spread is not None
        else "- 头部风险资产参与度统计不完整。"
    )
    lines.append(
        f"- 衍生品：BTC/ETH 资金费率分别为 {btc_funding_bps:+.2f}bps / {eth_funding_bps:+.2f}bps，DVOL 收盘 {btc_dvol:.2f} / {eth_dvol:.2f}。"
        if btc_funding_bps is not None and eth_funding_bps is not None and btc_dvol is not None and eth_dvol is not None
        else "- 衍生品：部分数据缺失。"
    )
    lines.append("")

    lines.append("## 今日盘面判断")
    if market_complete:
        lines.append(f"今日市场状态为“{regime_label}”。{regime_text}{breadth_call}当前证据尚不足以确认新一轮趋势启动。")
    else:
        lines.append(f"今日市场状态为“{regime_label}”。{regime_text}本期仅保留可独立验证的 Top10、交易所、衍生品和 RWA 结构信号。")
    lines.append("")

    lines.append("## 核心驱动因素")
    lines.append(
        f"从交易所成交看，{_trim_cn_sentence(venue_call)}；"
        f"从杠杆维度看，{_trim_cn_sentence(leverage_call)}；"
        f"从期权定价看，{_trim_cn_sentence(vol_call)}；"
        f"情绪方面，{_trim_cn_sentence(sentiment_call)}。以上是并列观察，不把同步变化直接解释为事件因果。"
    )
    lines.append("")

    lines.append("## BTC/ETH 24h 趋势判断")
    _append_md_image(lines, "BTC/ETH 24h价格路径", "charts/chart_btc_eth_24h_trend.png")
    lines.append(
        f"口径：文字涨跌来自交易所 rolling 24h ticker；图内路径为当前可得 {len(ctx.top2_intraday.get('BTC') or [])} 个小时点，"
        f"首尾变化 BTC {_fmt_pct(intraday_change.get('BTC'))}、ETH {_fmt_pct(intraday_change.get('ETH'))}，两者窗口不可混用。"
    )
    if btc_t and eth_t:
        btc_pos = btc_t.get("range_pos_pct")
        eth_pos = eth_t.get("range_pos_pct")
        lines.append(
            f"- BTC：{_fmt_price_usd(_safe_float(btc_t.get('price')))}（24h {_fmt_pct(_safe_float(btc_t.get('change_pct')))}，"
            f"区间 {_fmt_price_usd(_safe_float(btc_t.get('low')))} - {_fmt_price_usd(_safe_float(btc_t.get('high')))}，"
            f"当前位于区间 {btc_pos:.0f}%）=> {btc_t.get('trend')}。"
            if btc_pos is not None
            else f"- BTC：{_fmt_price_usd(_safe_float(btc_t.get('price')))}（24h {_fmt_pct(_safe_float(btc_t.get('change_pct')))}) => {btc_t.get('trend')}。"
        )
        lines.append(
            f"- ETH：{_fmt_price_usd(_safe_float(eth_t.get('price')))}（24h {_fmt_pct(_safe_float(eth_t.get('change_pct')))}，"
            f"区间 {_fmt_price_usd(_safe_float(eth_t.get('low')))} - {_fmt_price_usd(_safe_float(eth_t.get('high')))}，"
            f"当前位于区间 {eth_pos:.0f}%）=> {eth_t.get('trend')}。"
            if eth_pos is not None
            else f"- ETH：{_fmt_price_usd(_safe_float(eth_t.get('price')))}（24h {_fmt_pct(_safe_float(eth_t.get('change_pct')))}) => {eth_t.get('trend')}。"
        )
        btc_chg = _safe_float(btc_t.get("change_pct"))
        eth_chg = _safe_float(eth_t.get("change_pct"))
        if btc_chg is not None and eth_chg is not None:
            if btc_chg <= -1.0 and eth_chg <= -1.0:
                if eth_chg < btc_chg - 0.5:
                    lines.append("- 简评：BTC 偏弱震荡下行，ETH 相对更弱。")
                elif btc_chg < eth_chg - 0.5:
                    lines.append("- 简评：ETH 偏弱震荡下行，BTC 相对更弱。")
                else:
                    lines.append("- 简评：BTC 与 ETH 同步走弱，短线仍以防守为主。")
            elif btc_chg >= 1.0 and eth_chg >= 1.0:
                lines.append("- 简评：BTC 与 ETH 同步偏强，短线仍有上行动能。")
            elif btc_chg > 0 and eth_chg > 0:
                stronger = "ETH" if eth_chg > btc_chg else "BTC"
                lines.append(f"- 简评：BTC 与 ETH 均温和上涨，{stronger} 相对更强，但幅度尚未达到强趋势阈值。")
            else:
                lines.append("- 简评：BTC 与 ETH 出现分化，短线以结构性机会为主。")
    else:
        lines.append("- BTC/ETH 24h 趋势数据暂不可用。")
    lines.append("")

    lines.append("## 稳定币收益情况（链上协议）")
    if stable_top:
        stable_sorted_by_total = sorted(
            [r for r in stable_top if r.get("total_apy") is not None],
            key=lambda r: float(r.get("total_apy") or 0.0),
            reverse=True,
        )
        stable_sorted_by_tvl = sorted(
            [r for r in stable_top if r.get("tvl_usd") is not None],
            key=lambda r: float(r.get("tvl_usd") or 0.0),
            reverse=True,
        )
        stable_sorted_by_util = sorted(
            [r for r in stable_top if r.get("utilization_pct") is not None],
            key=lambda r: float(r.get("utilization_pct") or 0.0),
            reverse=True,
        )
        featured = stable_sorted_by_total[:4]
        util_hot = sum(1 for r in stable_top if (r.get("utilization_pct") or 0.0) >= 70.0)
        total_vals = [float(r.get("total_apy") or 0.0) for r in stable_top if r.get("total_apy") is not None]
        total_min = min(total_vals) if total_vals else None
        total_max = max(total_vals) if total_vals else None

        lines.append(
            f"按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 {len(stable_top)} 个主流池；原生供给利率均值约 {_fmt_pct(stable_native_avg)}。"
            if stable_native_avg is not None
            else f"按安全优先（协议成熟度、链层风险、是否依赖激励）筛选了 {len(stable_top)} 个主流池。"
        )
        lines.append(
            f"其中包含奖励补贴的池有 {stable_with_rewards} 个，补贴收益已单列，不与原生利率混合。"
        )
        lines.append("")
        lines.append("核心观察")
        if total_min is not None and total_max is not None:
            lines.append(f"- 利率结构：Total APY 位于 {_fmt_pct(total_min, signed=False)} 至 {_fmt_pct(total_max, signed=False)} 区间。")
        if stable_sorted_by_tvl:
            tvl_head = stable_sorted_by_tvl[:2]
            tvl_text = "、".join(
                [
                    f"{x.get('protocol')}-{x.get('asset')}（{x.get('chain')}，TVL {_fmt_usd(_safe_float(x.get('tvl_usd')))}）"
                    for x in tvl_head
                ]
            )
            lines.append(f"- 资金集中：TVL 主要集中在 {tvl_text}。")
        if featured:
            yield_text = "、".join(
                [
                    f"{x.get('protocol')}-{x.get('asset')}（{x.get('chain')}，Total {_fmt_pct(_safe_float(x.get('total_apy')), signed=False)}）"
                    for x in featured[:2]
                ]
            )
            lines.append(f"- 收益领先：当前收益靠前样本包括 {yield_text}。")
        lines.append("")
        lines.append("风险提示")
        lines.append(f"- 利用率达到 70% 以上的池有 {util_hot} 个，杠杆需求主要集中在头部池。")
        if stable_sorted_by_util:
            u0 = stable_sorted_by_util[0]
            lines.append(
                f"- 利用率最高样本：{u0.get('protocol')}-{u0.get('asset')}（{u0.get('chain')}）"
                f" {_fmt_pct(_safe_float(u0.get('utilization_pct')), signed=False)}，"
                f"Borrow APY {_fmt_pct(_safe_float(u0.get('borrow_apy')), signed=False)}。"
            )
        lines.append(f"- 奖励收益池数量：{stable_with_rewards} 个。当前收益主体仍以原生利率为主。")
        lines.append("")
        if stable_top:
            source_counts: Dict[str, int] = {}
            source_scope = stable_extended if stable_extended else stable_top
            for r in source_scope:
                tags = r.get("source_tags") if isinstance(r.get("source_tags"), list) else []
                for t in tags:
                    source_counts[str(t)] = source_counts.get(str(t), 0) + 1
            source_text = "，".join([f"{k}({v})" for k, v in sorted(source_counts.items(), key=lambda x: x[0])]) if source_counts else "DefiLlama"
            lines.append(f"数据覆盖：{source_text}。")
            lines.append("")
            lines.append("稳定币收益对照表（安全优先）")
            lines.append("| 协议 | 链 | 币种 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |")
            lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|")
            for r in stable_top:
                tags = r.get("source_tags") if isinstance(r.get("source_tags"), list) else []
                source = "+".join(tags) if tags else str(r.get("source_primary") or "DefiLlama")
                lines.append(
                    f"| {r.get('protocol')} | {r.get('chain')} | {r.get('asset')} | "
                    f"{_fmt_pct(_safe_float(r.get('supply_apy')), signed=False)} | "
                    f"{_fmt_pct(_safe_float(r.get('borrow_apy')), signed=False)} | "
                    f"{_fmt_pct(_safe_float(r.get('rewards_apy')), signed=False)} | "
                    f"{_fmt_pct(_safe_float(r.get('total_apy')), signed=False)} | "
                    f"{_fmt_pct(_safe_float(r.get('utilization_pct')), signed=False)} | "
                    f"{_fmt_usd(_safe_float(r.get('tvl_usd')))} | "
                    f"{source} |"
                )
            if stable_extended:
                lines.append("")
                lines.append(f"稳定币收益对比（扩展样本共 {len(stable_extended)} 条，展示 Top10）")
                lines.append("| 币种 | 协议 | 链 | Supply | Borrow | Rewards | Total | Utilization | TVL | 数据源 |")
                lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|")
                for r in stable_extended[:10]:
                    tags = r.get("source_tags") if isinstance(r.get("source_tags"), list) else []
                    source = "+".join(tags) if tags else str(r.get("source_primary") or "DefiLlama")
                    lines.append(
                        f"| {r.get('asset')} | {r.get('protocol')} | {r.get('chain')} | "
                        f"{_fmt_pct(_safe_float(r.get('supply_apy')), signed=False)} | "
                        f"{_fmt_pct(_safe_float(r.get('borrow_apy')), signed=False)} | "
                        f"{_fmt_pct(_safe_float(r.get('rewards_apy')), signed=False)} | "
                        f"{_fmt_pct(_safe_float(r.get('total_apy')), signed=False)} | "
                        f"{_fmt_pct(_safe_float(r.get('utilization_pct')), signed=False)} | "
                        f"{_fmt_usd(_safe_float(r.get('tvl_usd')))} | "
                        f"{source} |"
                    )
            if stable_rows_extended_all or stable_cefi_rows:
                lines.append("")
                lines.append("跨源补充（比 taoli 更全）")
                protocol_cnt = len({str(r.get("protocol") or "") for r in stable_rows_extended_all if r.get("protocol")})
                chain_cnt = len({str(r.get("chain") or "") for r in stable_rows_extended_all if r.get("chain")})
                asset_cnt = len({str(r.get("asset") or "") for r in stable_rows_extended_all if r.get("asset")})
                lines.append(
                    f"- 新增对比源：DefiLlama 全量稳定币池（筛选口径）+ Bitcompare 平台 APY（CeFi/DeFi/Hybrid），并与现有链上主流池快照交叉核对。"
                )
                lines.append(
                    f"- 覆盖规模：原链上精表 {len(stable_extended)} 条；DefiLlama 扩展样本 {len(stable_rows_extended_all)} 条（展示 Top{len(stable_rows_extended_top)}）；Bitcompare 稳定币利率样本 {len(stable_cefi_rows)} 条。"
                )
                lines.append(f"- 覆盖维度：扩展样本覆盖 {protocol_cnt} 个协议、{chain_cnt} 条链、{asset_cnt} 类稳定币。")
                lines.append("- 口径说明：Bitcompare 混合 CeFi、DeFi 与 Hybrid 平台展示 APY；taoli 为 Binance 借币年化。两者用于横向参考，不等价于无风险套利收益。")
                if stable_rows_extended_top:
                    lines.append("")
                    lines.append(
                        f"稳定币收益补充表（DefiLlama 扩展，TVL≥${int(STABLE_EXTENDED_MIN_TVL_USD/1_000_000)}M，展示 Top{len(stable_rows_extended_top)}）"
                    )
                    lines.append("| 币种 | 协议 | 链 | Base | Rewards | Total | TVL | 数据源 |")
                    lines.append("|---|---|---|---:|---:|---:|---:|---|")
                    for r in stable_rows_extended_top:
                        lines.append(
                            f"| {r.get('asset')} | {r.get('protocol')} | {r.get('chain')} | "
                            f"{_fmt_pct(_safe_float(r.get('base_apy_pct')), signed=False)} | "
                            f"{_fmt_pct(_safe_float(r.get('rewards_apy_pct')), signed=False)} | "
                            f"{_fmt_pct(_safe_float(r.get('total_apy_pct')), signed=False)} | "
                            f"{_fmt_usd(_safe_float(r.get('tvl_usd')))} | "
                            f"{r.get('source') or 'DefiLlama API'} |"
                        )
                if stable_cefi_rows:
                    taoli_by_asset: Dict[str, Dict[str, Any]] = {
                        str(r.get("asset") or "").upper(): r for r in taoli_rows if r.get("asset")
                    }
                    lines.append("")
                    lines.append("稳定币平台聚合报价与借币成本（不可直接计算套利利差）")
                    lines.append("| 币种 | Bitcompare 平台最高APY | 对应平台 | taoli(Binance借币年化) | 可执行性 |")
                    lines.append("|---|---:|---|---:|---|")
                    for row in stable_cefi_rows:
                        asset = str(row.get("asset") or "").upper()
                        apy = _safe_float(row.get("apy_pct"))
                        taoli_annual = _safe_float((taoli_by_asset.get(asset) or {}).get("annual_rate_pct"))
                        execution_note = "未验证期限、额度、锁仓、奖励构成与地区准入"
                        if apy is not None and apy >= 20.0:
                            execution_note = "高收益聚合报价；未验证期限、容量、奖励构成与地区准入"
                        lines.append(
                            f"| {asset} | "
                            f"{_fmt_pct(apy, signed=False)} | "
                            f"{row.get('provider') or 'N/A'} | "
                            f"{_fmt_pct(taoli_annual, signed=False)} | "
                            f"{execution_note} |"
                        )
                    lines.append("说明：平台 APY 与保证金借币成本的产品期限、风险、准入和容量不同，不计算或宣称可执行套利利差。")
        lines.append("")
        lines.append("交易含义：当前稳定币收益更偏“头部池中等收益 + 局部高利用率”结构，策略上优先流动性与透明度，再考虑收益增强。")
        lines.append("部分池的 Borrow 与 Utilization 暂未返回，表内仅展示已获取字段。")
    else:
        lines.append("稳定币收益数据暂不可用，本期不作收益比较。")
    lines.append("")

    lines.append("## RWA 结构观察")
    lines.append("### 今日 tokenized stocks 异动雷达")
    if rwa_movers:
        def _rwa_flow_text(row: Dict[str, Any]) -> str:
            buy = _safe_float(row.get("buy_volume_24h_usd"))
            sell = _safe_float(row.get("sell_volume_24h_usd"))
            net = _safe_float(row.get("net_buy_24h_usd"))
            if buy is None or sell is None or net is None:
                return "链上买卖流不可用"
            if buy == 0 and sell == 0:
                return "未观测到可用买卖流"
            if net > 0:
                return f"链上主动买入占优（净额 {_fmt_usd(net)}）"
            if net < 0:
                return f"链上主动卖出占优（净额 {_fmt_usd(net)}）"
            return "链上买卖流大致平衡"

        def _rwa_premium_text(row: Dict[str, Any]) -> str:
            premium = _safe_float(row.get("premium_pct"))
            premium_status = str(row.get("premium_status") or "")
            if premium_status == "unavailable_multiplier":
                return "不可计算（份额倍率缺失）"
            if premium_status != "live" or premium is None:
                return "不可计算（参考价冻结）"
            return _fmt_pct(premium)

        def _rwa_smart_text(row: Dict[str, Any]) -> str:
            smart_direction = row.get("smart_signal_direction")
            if smart_direction:
                count = _safe_int(row.get("smart_signal_count"))
                return (
                    f"聪明钱信号为 {smart_direction}（"
                    f"{count if count is not None else '数量不可用'}，{_fmt_usd(_safe_float(row.get('smart_signal_value_usd'))) }）"
                )
            holders = _safe_int(row.get("smart_money_holders"))
            if holders is None:
                return "聪明钱持有地址与活跃信号不可用"
            if holders == 0:
                return "未观测到聪明钱持有地址或活跃信号"
            return f"未匹配到活跃交易信号，聪明钱持有地址 {holders} 个"

        lines.append("筛选口径：核心美股/ETF 映射观察池按链上代币 24h 绝对涨跌选出前 5，再结合 1h K 线、技术指标、链上买卖流、持仓集中度和底层美股交易状态解释。")
        lines.append("| 标的 | 24h | RSI14 | SMA6/24 | 链上净买入 | 映射溢折价 | 状态/事件 |")
        lines.append("|---|---:|---:|---|---:|---:|---|")
        for r in rwa_movers:
            sma6 = _safe_float(r.get("sma6"))
            sma24 = _safe_float(r.get("sma24"))
            trend = "多头" if sma6 is not None and sma24 is not None and sma6 > sma24 else ("空头" if sma6 is not None and sma24 is not None else "N/A")
            event = r.get("reason_msg") or r.get("reason_code") or r.get("market_status") or "normal"
            lines.append(
                f"| {r.get('ticker')} | {_fmt_pct(_safe_float(r.get('change_24h_pct')))} | "
                f"{_fmt_num(_safe_float(r.get('rsi14')), 1)} | {trend} | "
                f"{_fmt_usd(_safe_float(r.get('net_buy_24h_usd')))} | "
                f"{_rwa_premium_text(r)} | {event} |"
            )
        lines.append("")
        for r in rwa_movers[:3]:
            sma6 = _safe_float(r.get("sma6"))
            sma24 = _safe_float(r.get("sma24"))
            technical = "短周期均线位于长周期上方" if sma6 is not None and sma24 is not None and sma6 > sma24 else "短周期均线未站上长周期均线"
            reason = r.get("reason_msg") or r.get("reason_code")
            lines.append(
                f"- **{r.get('ticker')}**：24h {_fmt_pct(_safe_float(r.get('change_24h_pct')))}，RSI14 {_fmt_num(_safe_float(r.get('rsi14')), 1)}，"
                f"{technical}；{_rwa_flow_text(r)}；{_rwa_smart_text(r)}。映射溢折价 {_rwa_premium_text(r)}。"
                + (f"资产状态显示 `{reason}`，这是可验证的事件线索。" if reason else "当前未发现资产级停牌、财报限制或公司行动状态。")
            )
        lines.append("")
        lines.append("24×7 交易含义：美股休市期间，tokenized stock 的变化更像对新闻、指数期货和加密风险偏好的提前定价；但底层现货缺少连续套利锚、链上流动性通常更薄，溢折价可能放大。美股开盘后若底层价格不确认，夜间涨跌可能快速回归。")
        lines.append("归因纪律：公司行动/财报限制、K 线和链上流向属于事实；只有事件时间、价格方向和资金方向一致时才写成高置信归因，其余仅标记为相关性或待验证假设。")
    else:
        lines.append("今日 tokenized stocks 异动数据暂不可用，本期不作异动判断。")
    lines.append("")
    lines.append("### RWA 资产类别背景")
    if rwa_rows:
        _append_md_image(lines, "RWA资产类别快照", "charts/chart_rwa_asset_class_snapshot.png")
        as_ofs = sorted({str(r.get("as_of") or "") for r in rwa_rows if r.get("as_of")})
        as_of_txt = as_ofs[-1] if as_ofs else "来源页未披露"
        total_value = sum(float(r.get("value_usd") or 0.0) for r in rwa_rows)
        trade_like_value = sum(float(r.get("value_usd") or 0.0) for r in rwa_trade_like)
        trade_like_share = trade_like_value / total_value * 100.0 if total_value > 0 else None
        top_txt = (
            f"{rwa_top.get('asset_class')}（{_fmt_usd(_safe_float(rwa_top.get('value_usd')))}，"
            f"7D {_fmt_pct(_safe_float(rwa_top.get('change_7d_pct'))) }）"
            if rwa_top
            else "N/A"
        )
        lines.append(
            f"RWA.xyz 公开页快照显示，样本资产类别合计约 {_fmt_usd(total_value)}；最大类别为 {top_txt}。"
            f"7D 上升类别 {len(rwa_rising)} 个、下降类别 {len(rwa_falling)} 个，说明 RWA 当前更适合当作结构变量，而不是日内方向信号。"
        )
        if trade_like_share is not None:
            lines.append(
                f"其中股票、主动策略和非美债这类交易属性更强的类别合计约 {_fmt_usd(trade_like_value)}，占样本 {_fmt_pct(trade_like_share, signed=False)}。"
                "这部分更接近 CEX 新品类、Perps 和跨资产成交额的观察入口。"
            )
        lines.append("")
        lines.append("RWA 资产类别对照表")
        lines.append("| 类别 | 规模 | 7D变化 | as of |")
        lines.append("|---|---:|---:|---|")
        for r in rwa_rows:
            lines.append(
                f"| {r.get('asset_class')} | "
                f"{_fmt_usd(_safe_float(r.get('value_usd')))} | "
                f"{_fmt_pct(_safe_float(r.get('change_7d_pct')))} | "
                f"{r.get('as_of') or '来源页未披露'} |"
            )
        lines.append("")
        lines.append(
            "交易含义：RWA 放在日报里可以，但应定位为二级市场的产品线与风险偏好背景；"
            "只有 tokenized stocks、RWA perps、可交易收益资产扩容时，才更直接影响交易所成交结构。"
        )
        lines.append("数据源：RWA.xyz 公开资产类别页；正式 API 可在设置 RWA_API_KEY 后替换为更稳定口径。")
    else:
        lines.append("RWA 资产类别快照暂不可用，本期不作类别规模比较。")
    lines.append("")

    lines.append("## 非 DeFi（交易所期现）")
    if nondefi_rows:
        _append_md_image(lines, "非DeFi期现快照", "charts/chart_nondefi_carry_snapshot.png")
        lines.append(
            f"本期可用样本仅覆盖 {'、'.join(nondefi_venues)} 的 BTC/ETH 现货与永续。"
            + ("Funding 与 basis 均有可用记录。" if nondefi_with_basis else "Funding 可用，但 basis 缺少有效记录，不作基差策略判断。")
        )
        if nondefi_best:
            lines.append(
                f"- Funding 最高样本：{nondefi_best.get('exchange')}-{nondefi_best.get('asset')}，"
                f"年化约 {_fmt_pct(_safe_float(nondefi_best.get('annual_funding_pct')), signed=False)}。"
            )
        if nondefi_most_negative:
            lines.append(
                f"- Funding 最低样本：{nondefi_most_negative.get('exchange')}-{nondefi_most_negative.get('asset')}，"
                f"年化约 {_fmt_pct(_safe_float(nondefi_most_negative.get('annual_funding_pct')), signed=False)}。"
            )
        if nondefi_basis_abs_max:
            lines.append(
                f"- Basis 偏离最大：{nondefi_basis_abs_max.get('exchange')}-{nondefi_basis_abs_max.get('asset')}，"
                f"相对指数约 {_fmt_pct(_safe_float(nondefi_basis_abs_max.get('basis_pct')), signed=False)}。"
            )
        if borrow_rate_rows:
            lines.append("")
            lines.append("借币成本多源对比表")
            lines.append("| 资产 | Binance(日/年) | OKX(日/年) | Bybit(日/年) | Backpack(日/年) | KuCoin(日/年) | 最低日利率 |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|")
            source_order = ["Binance", "OKX", "Bybit", "Backpack", "KuCoin"]
            preferred_assets = ["USDT", "USDC", "DAI", "USDE", "BTC", "ETH"]
            by_asset_source: Dict[Tuple[str, str], Dict[str, Any]] = {}
            for r in borrow_rate_rows:
                asset = str(r.get("asset") or "").upper()
                source = str(r.get("source") or "")
                if not asset or not source:
                    continue
                key = (asset, source)
                cur = by_asset_source.get(key)
                if cur is None or float(r.get("daily_rate_pct") or 9999.0) < float(cur.get("daily_rate_pct") or 9999.0):
                    by_asset_source[key] = r
            all_assets = sorted({str(r.get("asset") or "").upper() for r in borrow_rate_rows if r.get("asset")})
            assets = [a for a in preferred_assets if a in all_assets] + [a for a in all_assets if a not in preferred_assets]

            def _fmt_limit_short(v: Optional[float]) -> str:
                if v is None:
                    return "N/A"
                if v >= 1_000_000:
                    return f"{v / 1_000_000:.1f}M"
                if v >= 1_000:
                    return f"{v / 1_000:.0f}k"
                if v >= 1:
                    return f"{v:,.0f}"
                return f"{v:.4f}".rstrip("0").rstrip(".")

            def _fmt_rate_cell(row: Optional[Dict[str, Any]]) -> str:
                if not row:
                    return "N/A"
                daily = _safe_float(row.get("daily_rate_pct"))
                annual = _safe_float(row.get("annual_rate_pct"))
                if daily is None or annual is None:
                    return "N/A"
                lim_txt = _fmt_limit_short(_safe_float(row.get("borrow_limit")))
                return f"{_fmt_pct(daily, signed=False)}/{_fmt_pct(annual, signed=False)} · {lim_txt}"

            for asset in assets:
                rows = [by_asset_source.get((asset, s)) for s in source_order]
                daily_candidates = [(r, _safe_float(r.get("daily_rate_pct"))) for r in rows if r and _safe_float(r.get("daily_rate_pct")) is not None]
                best_txt = "N/A"
                if daily_candidates:
                    best_row, best_daily = min(daily_candidates, key=lambda x: float(x[1] or 9999.0))
                    best_txt = f"{best_row.get('source')} {_fmt_pct(best_daily, signed=False)}"
                lines.append(
                    f"| {asset} | "
                    f"{_fmt_rate_cell(rows[0])} | "
                    f"{_fmt_rate_cell(rows[1])} | "
                    f"{_fmt_rate_cell(rows[2])} | "
                    f"{_fmt_rate_cell(rows[3])} | "
                    f"{_fmt_rate_cell(rows[4])} | "
                    f"{best_txt} |"
                )
            lines.append("说明：统一按日利率/年化展示，单元格尾部为可借额度。")
        if nondefi_with_basis:
            lines.append("- 交易含义：Funding 与 basis 同时可用时才能评估 carry；当前数值只代表快照，不代表可持续收益。")
        else:
            lines.append("- 交易含义：当前只能观察 funding，缺少 basis 时不评估 carry 利差或套利空间。")
        lines.append("该部分与链上收益分开统计，便于比较两类策略的收益与风险结构。")
    else:
        lines.append("非 DeFi 期现样本暂不可用，本期不作 carry 判断。")
    lines.append("")

    lines.append("## 市场脉冲")
    if market_complete:
        _append_md_image(lines, "全市场当日水平", "charts/chart_market_snapshot_levels.png")
        lines.append(
            f"{market_time_label}，全市场市值 {_fmt_usd(ctx.market_cap)}，24h 成交额 {_fmt_usd(ctx.volume_24h)}，"
            f"BTC 主导率 {_fmt_pct(ctx.btc_dom, signed=False)}。"
        )
        lines.append(pulse_detail)
        lines.append("")
        _append_md_image(lines, "全市场当日变化", "charts/chart_market_daily_change.png")
        lines.append(f"相对前一观测日，市值 {_fmt_pct(mc_chg)}、成交 {_fmt_pct(vol_chg)}、BTC.D {dom_chg:+.2f}pct。")
        lines.append("该段仅描述同步变化；没有事件时间与资金路径证据时，不将量价共振写成事件因果。")
    else:
        lines.append("全市场市值、成交额或 BTC 主导率缺少完整的连续两期数据，本期不生成水平图、变化图，也不判断量价关系。")
    lines.append("")

    lines.append("## 主导率与市值集中度")
    if outside_share is not None and btc_share is not None and top2_10_share is not None:
        _append_md_image(lines, "市值集中度快照", "charts/chart_market_breadth_snapshot.png")
        lines.append(
            f"当前市值结构为 BTC {btc_share:.2f}% / Top10 其余 {top2_10_share:.2f}% / Top10 外 {outside_share:.2f}%。"
            "该图含稳定币与质押映射，只描述集中度，不证明风险偏好扩散。"
        )
        lines.append(breadth_detail)
    else:
        lines.append("市值集中度快照不完整，本期不生成结构图，也不推断资金向核心或长尾资产扩散。")
    lines.append("")

    lines.append("## 资产表现与交易所成交")
    _append_md_image(lines, "Top10资产24h表现", "charts/chart_top10_assets_24h.png")
    if asset_top and asset_tail and asset_avg is not None and asset_spread is not None:
        lines.append(
            f"Top10 中领涨 {asset_top.get('symbol')}（{asset_top.get('chg24'):+.2f}%），尾部 {asset_tail.get('symbol')}（{asset_tail.get('chg24'):+.2f}%），均值 {_fmt_pct(asset_avg)}。分化 {asset_spread:.2f}pct，结构性交易仍是主导。"
        )
    else:
        lines.append("Top10 涨跌数据不完整。")
    lines.append(
        f"{asset_detail}对交易而言，这通常意味着“选币”比“全市场方向”更重要，错配带来的收益差会明显放大。"
    )
    lines.append("")

    _append_md_image(lines, "前排交易所24h变化", "charts/chart_exchange_24h_change.png")
    if exch_top and exch_tail and exch_mid is not None:
        lines.append(
            f"前排样本上涨 {exch_up} 家、下跌 {exch_dn} 家，均值 {_fmt_pct(exch_mid)}。{exch_top.name} 最强（{exch_top.pct24h:+.2f}%），{exch_tail.name} 最弱（{exch_tail.pct24h:+.2f}%）。"
        )
    else:
        lines.append("交易所 24h 成交变化数据不完整。")
    lines.append(
        f"{exchange_detail}报价连续性和滑点是否同步变化仍需盘口数据验证，执行层面应继续监控成交质量。"
    )
    lines.append("")
    _append_md_image(lines, "交易所现货衍生品结构", "charts/chart_exchange_spot_deriv_structure.png")
    if deriv_share is not None:
        lines.append(
            f"样本内衍生品成交占比 {deriv_share:.2f}%。该比例描述成交结构，不单独用于判断后续波动方向或幅度。"
        )
    else:
        lines.append("交易所结构占比数据不完整。")
    lines.append(
        f"{structure_detail}后续需用盘口深度、强平和事件窗口数据验证具体传导机制。"
    )
    lines.append("")

    lines.append("## 衍生品与情绪")
    if btc_funding_bps is not None and eth_funding_bps is not None and btc_dvol is not None and eth_dvol is not None:
        lines.append(
            f"资金费率（Funding）仍在中性附近，BTC/ETH 分别 {btc_funding_bps:+.2f}bps / {eth_funding_bps:+.2f}bps；未平仓合约（OI）为 {_fmt_usd(btc_oi)} / {_fmt_usd(eth_oi)}；隐含波动率指数（DVOL）位于 {_dvol_regime(btc_dvol)} / {_dvol_regime(eth_dvol)}。"
        )
    else:
        lines.append("衍生品关键指标有缺口，当前解读以可得数据为准。")
    lines.append(
        f"{deriv_detail}因此更合适的做法不是激进追单边，而是围绕波动管理仓位和节奏。"
    )
    lines.append("")
    _append_md_image(lines, "情绪与波动当日快照", "charts/chart_sentiment_snapshot.png")
    if fng_val is not None:
        lines.append(
            f"恐惧与贪婪指数（F&G）{fng_time_label} {fng_val:.0f}（较前一观测日 {fng_delta:+.0f}）；"
            f"BTC/ETH DVOL 为 {dvol_pair}，对应 {_dvol_regime(btc_dvol)} / {_dvol_regime(eth_dvol)}。"
            if fng_delta is not None
            else f"恐惧与贪婪指数（F&G）{fng_time_label} {fng_val:.0f}。"
        )
    else:
        lines.append("F&G 数据不可用，情绪判断需结合成交与 funding 变化。")
    lines.append(
        f"{sentiment_detail}只有当情绪、广度和成交三者同时改善，市场才更可能从“反弹交易”切换到“趋势交易”。"
    )
    lines.append("")

    lines.append("## Binance Web3 RWA 聪明钱信号")
    rwa_signal_rows = (ctx.rwa_smartmoney or {}).get("rows") or []
    active_rwa_signals = [row for row in rwa_signal_rows if row.get("coverage_status") == "active_signal"]
    covered_rwa_assets = [row for row in rwa_signal_rows if row.get("coverage_status") in {"active_signal", "no_matching_signal"}]
    lines.append(
        f"公开接口覆盖 Top5 中 {len(covered_rwa_assets)} 个标的，当前命中 {len(active_rwa_signals)} 个活跃信号。"
        "未命中表示本次公开信号页没有对应记录，不等于聪明钱地址数为零。"
    )
    lines.append("| 标的 | 覆盖状态 | 方向 | 聪明钱地址 | 信号金额 | 状态 |")
    lines.append("|---|---|---|---:|---:|---|")
    coverage_labels = {
        "active_signal": "有信号",
        "no_matching_signal": "已覆盖/未命中",
        "source_unavailable": "数据源不可用",
        "unsupported_chain": "链未支持",
    }
    for row in rwa_signal_rows:
        lines.append(
            f"| {row.get('ticker') or 'N/A'} | {coverage_labels.get(str(row.get('coverage_status')), '未知')} | "
            f"{row.get('direction') or 'N/A'} | "
            f"{_safe_int(row.get('smart_money_count')) if _safe_int(row.get('smart_money_count')) is not None else 'N/A'} | "
            f"{_fmt_usd(_safe_float(row.get('total_value_usd')))} | {row.get('signal_status') or 'N/A'} |"
        )
    lines.append("")
    lines.append("交易含义：该数据是代币级链上信号，用于验证资金参与方向，不代表全市场交易员排行榜，也不应单独作为开仓触发。")
    lines.append("")

    lines.append("## 可选交易员仓位增强")
    sm_traders = ctx.smartmoney_traders or []
    sm_signals = ctx.smartmoney_signals or {}
    sm_positions = (ctx.smartmoney_positions or {}).get("rows") or []
    sm_trader_count = _safe_int((ctx.smartmoney_positions or {}).get("trader_count")) or 0
    if sm_traders:
        lines.append(f"当日抓取到 OKX 聪明钱榜单 Top{len(sm_traders)}（30d 按 PnL 排序，仅作补充）。")
        lines.append("| # | 昵称 | Author ID | 30d PnL | 收益率 | 胜率 | 最大回撤 | 资产 |")
        lines.append("|---|---|---|---:|---:|---:|---:|---:|")
        for i, row in enumerate(sm_traders, start=1):
            pnl_ratio = _safe_float(row.get("pnlRatio"))
            win_rate = _safe_float(row.get("winRate"))
            max_drawdown = _safe_float(row.get("maxDrawdown"))
            lines.append(
                f"| {i} | {row.get('nickName') or 'N/A'} | {row.get('authorId') or 'N/A'} | "
                f"{_fmt_usd(_safe_float(row.get('pnl')))} | "
                f"{_fmt_pct((pnl_ratio * 100.0) if pnl_ratio is not None else None)} | "
                f"{_fmt_pct((win_rate * 100.0) if win_rate is not None else None, signed=False)} | "
                f"{_fmt_pct((max_drawdown * 100.0) if max_drawdown is not None else None)} | "
                f"{_fmt_usd(_safe_float(row.get('asset')))} |"
            )
    else:
        lines.append("未启用或未取得公开交易员榜单；不影响 Binance Web3 代币级信号覆盖。")
    lines.append("")
    if sm_positions:
        lines.append(f"基于可用交易员详情成功解析 {sm_trader_count} 位交易员仓位，按净名义仓位（USDT）排序：")
        lines.append("| 合约 | 多头名义 | 空头名义 | 净敞口 | 多头人数 | 空头人数 |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in sm_positions[:8]:
            lines.append(
                f"| {row.get('inst_id') or 'N/A'} | {_fmt_usd(_safe_float(row.get('long_usd')))} | "
                f"{_fmt_usd(_safe_float(row.get('short_usd')))} | {_fmt_usd(_safe_float(row.get('net_usd')))} | "
                f"{_safe_int(row.get('long_traders')) if _safe_int(row.get('long_traders')) is not None else 'N/A'} | "
                f"{_safe_int(row.get('short_traders')) if _safe_int(row.get('short_traders')) is not None else 'N/A'} |"
            )
        top1 = sm_positions[0]
        top2 = sm_positions[1] if len(sm_positions) > 1 else None
        lines.append("")
        lines.append(
            f"动向：仓位主要集中在 {top1.get('inst_id')}（净敞口 {_fmt_usd(_safe_float(top1.get('net_usd')))})"
            + (f" 与 {top2.get('inst_id')}（净敞口 {_fmt_usd(_safe_float(top2.get('net_usd')))})。" if top2 else "。")
        )
        lines.append("含义：若净多持续集中于 BTC/ETH 主合约，通常代表风险偏好偏向核心资产，而非全面扩散。")
        lines.append("观察点：重点跟踪净敞口是否由单边转向对冲，以及空头人数是否开始抬升。")
    else:
        lines.append("仓位结构暂不可用，本期不作仓位方向判断。")
    lines.append("")
    if sm_signals:
        lines.append("附：BTC/ETH 聚合信号快照（OKX Smart Money）")
        lines.append("| 资产 | 多头占比 | 加权多头占比 | 多头人数 | 空头人数 | 净名义仓位(USDT) | 1h 变化 | 多头均价 | 空头均价 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for symbol in ["BTC", "ETH"]:
            s = sm_signals.get(symbol) or {}
            long_ratio = _safe_float(s.get("longRatio"))
            weighted_long_ratio = _safe_float(s.get("weightedLongRatio"))
            lines.append(
                f"| {symbol} | "
                f"{_fmt_pct((long_ratio * 100.0) if long_ratio is not None else None, signed=False)} | "
                f"{_fmt_pct((weighted_long_ratio * 100.0) if weighted_long_ratio is not None else None, signed=False)} | "
                f"{_safe_int(s.get('longTraders')) if _safe_int(s.get('longTraders')) is not None else 'N/A'} | "
                f"{_safe_int(s.get('shortTraders')) if _safe_int(s.get('shortTraders')) is not None else 'N/A'} | "
                f"{_fmt_usd(_safe_float(s.get('netNotionalUsdt')))} | "
                f"{_fmt_pct((_safe_float(s.get('vs1h')) or 0.0) * 100.0 if _safe_float(s.get('vs1h')) is not None else None)} | "
                f"{_fmt_price_usd(_safe_float(s.get('smartMoneyLongAvgEntry')))} | "
                f"{_fmt_price_usd(_safe_float(s.get('smartMoneyShortAvgEntry')))} |"
            )
    elif ctx.smartmoney_signal_attempted:
        lines.append("BTC/ETH 聪明钱聚合信号暂不可用，本期不作信号判断。")
    else:
        lines.append("BTC/ETH 聪明钱聚合信号未启用（设置 `OKX_SMARTMONEY_FETCH_SIGNAL=1` 可尝试拉取）。")
    lines.append("")
    lines.append("交易含义：交易员仓位只用于方向与拥挤度补充观察。")
    lines.append("")

    sentiment_rows = (ctx.okx_news_sentiment or {}).get("rows") or []
    if sentiment_rows:
        lines.append("## 补充：OKX 新闻情绪快照")
        lines.append("| 资产 | 情绪标签 | 看多占比 | 看空占比 | 提及量 | 情绪分数 |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for row in sentiment_rows[:6]:
            lines.append(
                f"| {row.get('coin') or 'N/A'} | {row.get('label') or 'N/A'} | "
                f"{_fmt_pct((_safe_float(row.get('bullish_ratio')) or 0.0) * 100.0 if _safe_float(row.get('bullish_ratio')) is not None else None, signed=False)} | "
                f"{_fmt_pct((_safe_float(row.get('bearish_ratio')) or 0.0) * 100.0 if _safe_float(row.get('bearish_ratio')) is not None else None, signed=False)} | "
                f"{_safe_int(row.get('mention_count')) if _safe_int(row.get('mention_count')) is not None else 'N/A'} | "
                f"{_safe_float(row.get('score')):.3f}" + " |"
            )
        lines.append("")
        lines.append("观察点：若“提及量上升 + 看多占比抬升”与聪明钱净多共振，短期趋势延续概率通常更高。")
        lines.append("")

    lines.append("## 未来24小时观察")
    if risk_asset_symbols and ctx.btc_dom is not None:
        lines.append("1. 若头部风险资产上涨覆盖率连续改善且 BTC.D 回落，再结合更广币种样本验证风险偏好是否扩散。")
    else:
        lines.append("1. 等待全市场市值与 BTC.D 连续数据恢复后，再验证风险偏好是否扩散。")
    lines.append("2. 若衍生品占比继续上升而 funding 仍中性，只能确认交易向杠杆侧集中；是否放大波动仍需结合 DVOL 与成交验证。")
    lines.append("3. 若 F&G 反弹但 DVOL 不降，代表情绪与风险定价背离，追涨胜率会明显下降。")
    lines.append("")

    lines.append("## 交易与风控含义")
    lines.append(f"- {desk_note_1}")
    lines.append(f"- {desk_note_2}")
    lines.append(f"- {desk_note_3}")
    lines.append("")

    def _drop_empty_section(heading: str, next_heading: str) -> None:
        try:
            start = lines.index(heading)
            end = lines.index(next_heading, start + 1)
        except ValueError:
            return
        del lines[start:end]

    if not (sm_traders or sm_positions or sm_signals):
        _drop_empty_section("## OKX 聪明钱仓位结构（Top10交易员）", "## OKX 新闻情绪快照")
    if not sentiment_rows:
        _drop_empty_section("## OKX 新闻情绪快照", "## 未来24小时观察")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _prepare_notion_import_bundle(outdir: Path, report_path: Path, charts_dir: Path) -> Path:
    """
    Build a Notion-importable local bundle:
    - notion_import/daily_secondary_report_import.md
    - notion_import/charts/*.png
    - notion_import/README_IMPORT.md
    - notion_import_bundle.zip
    """
    bundle_dir = outdir / "notion_import"
    bundle_charts = bundle_dir / "charts"
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_charts.mkdir(parents=True, exist_ok=True)

    for chart in sorted(charts_dir.glob("chart_*.png")):
        if chart.is_file():
            shutil.copy2(chart, bundle_charts / chart.name)

    src = report_path.read_text(encoding="utf-8")
    # Notion import recognizes local relative links better with explicit "./" prefix.
    src = src.replace("](charts/", "](./charts/")
    import_md = bundle_dir / "daily_secondary_report_import.md"
    import_md.write_text(src, encoding="utf-8")

    readme = bundle_dir / "README_IMPORT.md"
    readme.write_text(
        "\n".join(
            [
                "# Notion 导入说明",
                "",
                "1. 打开 Notion，进入目标父页面。",
                "2. 选择 Import -> Markdown & CSV。",
                "3. 选择本目录下的 daily_secondary_report_import.md。",
                "4. 如图片未自动挂载，手动将 notion_import/charts 目录中的图片拖入对应位置即可。",
                "",
                "提示：notion_import_bundle.zip 已包含 md 与 charts，可直接解压后导入。",
                "",
            ]
        ),
        encoding="utf-8",
    )

    zip_path = outdir / "notion_import_bundle.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(import_md, arcname="daily_secondary_report_import.md")
        zf.write(readme, arcname="README_IMPORT.md")
        for chart in sorted(bundle_charts.glob("*.png")):
            zf.write(chart, arcname=f"charts/{chart.name}")
    return import_md


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 CEX 二级市场日报包")
    parser.add_argument("--date", dest="day", required=True, help="目标日期 YYYY-MM-DD（必填；由调用方按 Asia/Shanghai 显式传入）")
    parser.add_argument("--outdir", help="输出目录；不传则自动按日期建目录")
    parser.add_argument("--base-dir", default="./reports", help="自动输出时的根目录，默认 ./reports")
    parser.add_argument("--subdir", default="secondary_daily_cn", help="自动输出时的子目录名，默认 secondary_daily_cn")
    args = parser.parse_args()

    target = datetime.strptime(args.day, "%Y-%m-%d").date()

    if args.outdir:
        outdir = Path(args.outdir)
    else:
        outdir = Path(args.base_dir) / target.isoformat() / args.subdir
    charts_dir, data_dir = _ensure_dirs(outdir)
    _cleanup_legacy_outputs(charts_dir, data_dir)

    ctx = _build_context(target)
    mc_chg = (ctx.market_cap / ctx.prev_market_cap - 1.0) * 100.0 if ctx.market_cap and ctx.prev_market_cap else None
    vol_chg = (ctx.volume_24h / ctx.prev_volume_24h - 1.0) * 100.0 if ctx.volume_24h and ctx.prev_volume_24h else None
    dom_chg = (ctx.btc_dom - ctx.prev_btc_dom) if (ctx.btc_dom is not None and ctx.prev_btc_dom is not None) else None

    _write_csv_top_assets(data_dir / "top10_assets_24h.csv", ctx.top_assets)
    _write_csv_exchanges(data_dir / "front_exchanges_24h.csv", ctx.exchanges)
    _write_csv_breadth(data_dir / "market_breadth_snapshot.csv", ctx.breadth_snapshot)
    _write_csv_top2_trend(data_dir / "btc_eth_24h_trend.csv", ctx.top2_trend)
    _write_csv_top2_intraday(data_dir / "btc_eth_24h_1h_series.csv", ctx.top2_intraday)
    _write_csv_nondefi_carry(data_dir / "nondefi_carry_snapshot.csv", ctx.nondefi_carry)
    _write_csv_borrow_rates(data_dir / "borrow_rates_snapshot.csv", ctx.borrow_rates)
    _write_csv_stablecoin_yields(data_dir / "stablecoin_yields_snapshot.csv", ctx.stablecoin_yields)
    _write_csv_stablecoin_yields_extended(data_dir / "stablecoin_yields_extended_defillama.csv", ctx.stablecoin_yields_extended)
    _write_csv_stablecoin_cefi_rates(data_dir / "stablecoin_cefi_rates_bitcompare.csv", ctx.stablecoin_cefi_rates)
    _write_csv_rwa_asset_classes(data_dir / "rwa_asset_class_snapshot.csv", ctx.rwa_asset_classes)
    _write_csv_rwa_token_movers(data_dir / "rwa_token_movers.csv", ctx.rwa_token_movers)
    _write_csv_taoli_binance_margin_rates(data_dir / "taoli_binance_margin_rates.csv", ctx.taoli_binance_margin_rates)
    _write_manifest(outdir / "daily_manifest.json", ctx)

    market_complete = all(v is not None for v in (ctx.market_cap, ctx.prev_market_cap, ctx.volume_24h, ctx.prev_volume_24h, ctx.btc_dom, ctx.prev_btc_dom))
    if market_complete:
        _plot_market_snapshot_levels(ctx.market_cap, ctx.volume_24h, ctx.btc_dom, charts_dir / "chart_market_snapshot_levels.png")
        _plot_market_daily_change(mc_chg, vol_chg, dom_chg, charts_dir / "chart_market_daily_change.png")
    breadth_complete = all(ctx.breadth_snapshot.get(key) is not None for key in ("outside_top10_share", "btc_share", "top2_to_10_share"))
    if breadth_complete:
        _plot_breadth_snapshot(ctx.breadth_snapshot, charts_dir / "chart_market_breadth_snapshot.png")
    _plot_exchange_24h(ctx.exchanges, charts_dir / "chart_exchange_24h_change.png")
    _plot_top_assets(ctx.top_assets, charts_dir / "chart_top10_assets_24h.png")
    _plot_nondefi_carry_snapshot(ctx.nondefi_carry, charts_dir / "chart_nondefi_carry_snapshot.png")
    _plot_rwa_asset_class_snapshot(ctx.rwa_asset_classes, charts_dir / "chart_rwa_asset_class_snapshot.png")
    _plot_top2_intraday(ctx.top2_intraday, charts_dir / "chart_btc_eth_24h_trend.png")
    _plot_exchange_structure(ctx.exchanges, charts_dir / "chart_exchange_spot_deriv_structure.png")
    _plot_sentiment_snapshot(ctx.fng.get("value"), ctx.fng.get("delta"), ctx.dvol.get("btc_dvol_close"), ctx.dvol.get("eth_dvol_close"), charts_dir / "chart_sentiment_snapshot.png")

    report_path = outdir / "daily_secondary_report.md"
    _write_report(report_path, ctx)
    notion_import_md = _prepare_notion_import_bundle(outdir, report_path, charts_dir)

    print(f"[ok] 日报输出目录: {outdir}")
    print(f"[ok] Notion 导入文件: {notion_import_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
