from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contracts import AdapterType


class AdapterScope(str, Enum):
    CORE = "core"
    OPTIONAL = "optional"


@dataclass(frozen=True)
class AdapterSpec:
    provider: str
    adapter_type: AdapterType
    scope: AdapterScope
    description: str
    skill_aliases: tuple[str, ...] = ()


ADAPTER_SPECS: tuple[AdapterSpec, ...] = (
    AdapterSpec(
        provider="alpaca",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.CORE,
        description="Primary equities/crypto broker adapter.",
        skill_aliases=("alpaca", "alpaca-trading", "alpaca-mcp"),
    ),
    AdapterSpec(
        provider="binance",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.CORE,
        description="Primary crypto exchange adapter.",
        skill_aliases=("binance", "binance-api"),
    ),
    AdapterSpec(
        provider="coinbase-advanced",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.CORE,
        description="US-focused crypto execution adapter.",
        skill_aliases=("coinbase", "coinbase-advanced", "coinbase-trade"),
    ),
    AdapterSpec(
        provider="kalshi",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.CORE,
        description="Prediction/event market execution adapter.",
        skill_aliases=("kalshi",),
    ),
    AdapterSpec(
        provider="polymarket",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.CORE,
        description="Prediction market adapter.",
        skill_aliases=("polymarket",),
    ),
    AdapterSpec(
        provider="polygon",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.CORE,
        description="Primary market data adapter for multi-asset coverage.",
        skill_aliases=("polygon", "polygon-io"),
    ),
    AdapterSpec(
        provider="taapi",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.CORE,
        description="Technical indicator API adapter.",
        skill_aliases=("taapi", "taapi-io"),
    ),
    AdapterSpec(
        provider="x-sentiment",
        adapter_type=AdapterType.NEWS,
        scope=AdapterScope.OPTIONAL,
        description="X/Twitter sentiment adapter.",
        skill_aliases=("x", "twitter", "x-api"),
    ),
    AdapterSpec(
        provider="weibo-sentiment",
        adapter_type=AdapterType.NEWS,
        scope=AdapterScope.OPTIONAL,
        description="Weibo sentiment adapter for Asia coverage.",
        skill_aliases=("weibo", "weibo-api"),
    ),
    AdapterSpec(
        provider="brave-search",
        adapter_type=AdapterType.NEWS,
        scope=AdapterScope.OPTIONAL,
        description="Web/news research adapter via Brave Search.",
        skill_aliases=("brave", "brave-search"),
    ),
    AdapterSpec(
        provider="kraken",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.OPTIONAL,
        description="Optional crypto exchange adapter.",
        skill_aliases=("kraken",),
    ),
    AdapterSpec(
        provider="ibkr",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.OPTIONAL,
        description="Optional Interactive Brokers adapter.",
        skill_aliases=("ibkr", "interactive-brokers"),
    ),
    AdapterSpec(
        provider="alpha-vantage",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.OPTIONAL,
        description="Optional market data adapter.",
        skill_aliases=("alpha-vantage",),
    ),
    AdapterSpec(
        provider="iex-cloud",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.OPTIONAL,
        description="Optional equities market data adapter.",
        skill_aliases=("iex", "iex-cloud"),
    ),
    AdapterSpec(
        provider="nasdaq-public",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.OPTIONAL,
        description="Optional Nasdaq public feed adapter.",
        skill_aliases=("nasdaq", "nasdaq-public"),
    ),
    AdapterSpec(
        provider="opend-futu",
        adapter_type=AdapterType.EXECUTION,
        scope=AdapterScope.OPTIONAL,
        description="Optional OpenD (MooMoo/Futu) adapter.",
        skill_aliases=("opend", "futu", "moomoo"),
    ),
    AdapterSpec(
        provider="yahoo-finance",
        adapter_type=AdapterType.MARKET_DATA,
        scope=AdapterScope.OPTIONAL,
        description="Optional Yahoo Finance market data adapter.",
        skill_aliases=("yahoo", "yahoo-finance"),
    ),
)

