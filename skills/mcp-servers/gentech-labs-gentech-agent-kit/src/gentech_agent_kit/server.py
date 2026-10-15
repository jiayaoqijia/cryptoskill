"""
GenTech Agent Kit — MCP Server
One install. Full stack. Your agent, running.

Integrates CoinMarketCap data, DeFi intelligence, agent identity,
and x402 payment rails into a single MCP server.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

import httpx
from fastmcp import FastMCP

from . import plugins as _plugins

# ── Version ─────────────────────────────────────────────────────────────────

VERSION = "0.3.0"

# ── Config (all from env, zero hardcoded secrets) ──────────────────────────

CMC_API_KEY = os.environ.get("CMC_API_KEY", "")
CMC_BASE = "https://pro-api.coinmarketcap.com"

_LOG = logging.getLogger("gentech-kit")

# Validate required config at import time
if not CMC_API_KEY:
    raise RuntimeError(
        "CMC_API_KEY environment variable is required. "
        "Get a free key at https://coinmarketcap.com/api/"
    )

# ── Shared HTTP Client ──────────────────────────────────────────────────────

_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=15.0)
    return _client


def _cleanup_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


class CMCError(Exception):
    """Wraps upstream CMC API errors with safe messages."""


def _cmc_headers() -> dict[str, str]:
    return {"Accept": "application/json", "X-CMC_PRO_API_KEY": CMC_API_KEY}


def _cmc_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    client = _get_client()
    try:
        resp = client.get(f"{CMC_BASE}{path}", params=params, headers=_cmc_headers())
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as exc:
        _LOG.error("CMC API error %s: %s", exc.response.status_code, exc.response.text[:200])
        raise CMCError("CoinMarketCap API request failed") from exc
    except httpx.RequestError as exc:
        _LOG.error("CMC request failed: %s", exc)
        raise CMCError("Could not reach CoinMarketCap API") from exc


# ── Input Validation ────────────────────────────────────────────────────────

_SYMBOL_RE = re.compile(r"^[A-Za-z0-9,\s]{1,100}$")


def _validate_symbol(symbol: str) -> str:
    s = symbol.strip()
    if not _SYMBOL_RE.match(s):
        raise ValueError("Invalid symbol. Use letters, numbers, and commas only (e.g. 'BTC' or 'BTC,ETH,SOL').")
    return s.upper()


def _validate_start(start: int) -> int:
    return max(1, start)


def _validate_limit(limit: int) -> int:
    return max(1, min(100, limit))


# ── Helpers ─────────────────────────────────────────────────────────────────


def _extract_coin(info_list: Any) -> dict[str, Any]:
    """CMC v2 returns arrays per symbol; extract first element."""
    if isinstance(info_list, list) and info_list:
        return info_list[0]
    if isinstance(info_list, dict):
        return info_list
    return {}


def _safe_result(data: dict[str, Any], error_prefix: str = "Request failed") -> str:
    """Catch any exception and return a sanitized JSON error."""
    try:
        return json.dumps(data, indent=2)
    except Exception as exc:
        _LOG.error("%s — serialization error: %s", error_prefix, exc)
        return json.dumps({"error": error_prefix})


# ── MCP Server ──────────────────────────────────────────────────────────────

mcp = FastMCP("GenTech Agent Kit")

# Auto-discover and register plugins
_plugins.register_plugins(mcp)

# ──────────────────────────────────────────────────────────────────────────
#  TOOLS — CoinMarketCap Data
# ──────────────────────────────────────────────────────────────────────────


@mcp.tool()
def get_quote(symbol: str) -> str:
    """Get current price quote for crypto symbols. Supports single or multiple comma-separated symbols (e.g. 'BTC' or 'BTC,ETH,SOL'). Cost: $0.001 USDC/query."""
    try:
        sym = _validate_symbol(symbol)
        data = _cmc_get("/v2/cryptocurrency/quotes/latest", {"symbol": sym})
        result: dict[str, Any] = {
            "symbol": sym,
            "timestamp": data.get("status", {}).get("timestamp"),
        }
        for s, raw in data.get("data", {}).items():
            info = _extract_coin(raw)
            q = info.get("quote", {}).get("USD", {})
            result[s] = {
                "price": q.get("price"),
                "24h_change_pct": q.get("percent_change_24h"),
                "market_cap": q.get("market_cap"),
                "volume_24h": q.get("volume_24h"),
            }
        return _safe_result(result)
    except (ValueError, CMCError) as exc:
        return json.dumps({"error": str(exc)})


@mcp.tool()
def get_listings(start: int = 1, limit: int = 20) -> str:
    """Get top token listings by market cap. Returns up to 100 tokens ranked by market cap. Cost: $0.001 USDC/query."""
    try:
        s = _validate_start(start)
        l = _validate_limit(limit)
        data = _cmc_get("/v1/cryptocurrency/listings/latest", {
            "start": s, "limit": l, "sort": "market_cap", "sort_dir": "desc",
        })
        tokens = []
        for item in data.get("data", []):
            q = item.get("quote", {}).get("USD", {})
            tokens.append({
                "rank": item.get("cmc_rank"),
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "price": q.get("price"),
                "24h_change_pct": q.get("percent_change_24h"),
                "market_cap": q.get("market_cap"),
            })
        return _safe_result({"count": len(tokens), "tokens": tokens})
    except CMCError as exc:
        return json.dumps({"error": str(exc)})


@mcp.tool()
def search_token(symbol: str) -> str:
    """Search for crypto token information by symbol. Returns metadata, description, tags, logo URL. Cost: $0.001 USDC/query."""
    try:
        sym = _validate_symbol(symbol)
        data = _cmc_get("/v1/cryptocurrency/info", {"symbol": sym})
        result: dict[str, Any] = {}
        for s, info in data.get("data", {}).items():
            result[s] = {
                "name": info.get("name"),
                "symbol": info.get("symbol"),
                "category": info.get("category"),
                "description": info.get("description"),
                "logo": info.get("logo"),
                "date_added": info.get("date_added"),
                "platform": info.get("platform"),
                "tags": info.get("tags", []),
            }
        return _safe_result(result)
    except (ValueError, CMCError) as exc:
        return json.dumps({"error": str(exc)})


@mcp.tool()
def get_trending(kind: str = "latest") -> str:
    """Get trending crypto data. Options: gainers, losers, most_visited, latest. Cost: $0.001 USDC/query."""
    try:
        valid_kinds = {"gainers", "losers", "most_visited", "latest"}
        k = kind.lower().strip()
        if k not in valid_kinds:
            return json.dumps({"error": f"Invalid kind '{kind}'. Options: {', '.join(sorted(valid_kinds))}"})
        endpoints = {
            "gainers": "/v1/cryptocurrency/trending/gainers-losers",
            "losers": "/v1/cryptocurrency/trending/gainers-losers",
            "most_visited": "/v1/cryptocurrency/trending/most-visited",
            "latest": "/v1/cryptocurrency/trending/latest",
        }
        params: dict[str, Any] = {}
        if k in ("gainers", "losers"):
            params = {"sort_dir": "asc" if k == "gainers" else "desc", "limit": "20"}
        data = _cmc_get(endpoints[k], params)
        items = []
        for item in data.get("data", []):
            q = item.get("quote", {}).get("USD", {}) if "quote" in item else {}
            items.append({
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "price": q.get("price"),
                "change_24h_pct": q.get("percent_change_24h"),
            })
        return _safe_result({"kind": k, "count": len(items), "results": items})
    except CMCError as exc:
        return json.dumps({"error": str(exc)})


@mcp.tool()
def get_dex_pairs(symbol: str) -> str:
    """Get DEX pair data for a token across exchanges. Returns price, volume, liquidity. Cost: $0.001 USDC/query."""
    try:
        sym = _validate_symbol(symbol)
        data = _cmc_get("/v4/dex/pairs", {"symbol": sym})
        pairs = []
        for pair in data.get("data", {}).get("pairs", [])[:20]:
            base = pair.get("base_currency", {}).get("symbol", "?")
            quote = pair.get("quote_currency", {}).get("symbol", "?")
            pairs.append({
                "exchange": pair.get("exchange", {}).get("name"),
                "pair": f"{base}/{quote}",
                "price": pair.get("quote", {}).get("price"),
                "volume_24h_usd": pair.get("volume_24h_usd"),
                "liquidity_usd": pair.get("liquidity_usd"),
                "price_change_24h_pct": pair.get("price_change_24h"),
            })
        return _safe_result({"symbol": sym, "count": len(pairs), "pairs": pairs})
    except (ValueError, CMCError) as exc:
        return json.dumps({"error": str(exc)})


# ──────────────────────────────────────────────────────────────────────────
#  TOOLS — Kit Meta
# ──────────────────────────────────────────────────────────────────────────


@mcp.tool()
def kit_info() -> str:
    """Get GenTech Agent Kit version, available tools, and update status."""
    tools_list = [
        "get_quote(symbol) — Real-time crypto prices",
        "get_listings(start, limit) — Top tokens by market cap",
        "search_token(symbol) — Token metadata and details",
        "get_trending(kind) — Gainers, losers, most visited",
        "get_dex_pairs(symbol) — DEX liquidity pair data",
    ]
    plugins = _plugins.get_plugin_list()
    return json.dumps({
        "name": "GenTech Agent Kit",
        "version": VERSION,
        "description": "One install. Full stack. Your agent, running.",
        "tools": tools_list,
        "plugins": len(plugins),
        "plugins_list": [p.get("name") for p in plugins],
        "updates": "Always receiving updates — run `uv tool install --reinstall` to get the latest",
        "docs": "https://github.com/Gentech-Labs/genTech-agent-kit",
    }, indent=2)


# ── Entry Point ──────────────────────────────────────────────────────────────


def main() -> None:
    try:
        mcp.run()
    finally:
        _cleanup_client()


if __name__ == "__main__":
    main()