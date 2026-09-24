from __future__ import annotations

from datetime import date
from typing import Any

from .base import ModuleResult, build_result, fetch_recoverable


SOURCES = {
    "borrow_rates": "Binance, OKX, KuCoin and Backpack public endpoints; Bybit public endpoint via optional Mihomo JP route",
    "stablecoin_primary": "DefiLlama plus Aave, Compound and Morpho official APIs",
    "stablecoin_extended": "DefiLlama yields API",
    "platform_apy": "Bitcompare aggregator, unverified quote",
}


def collect(engine: Any, target: date) -> ModuleResult:
    gaps: list[str] = []
    warnings: list[str] = []
    borrow = fetch_recoverable(engine._fetch_borrow_rates, gaps, warnings)
    primary = fetch_recoverable(engine._fetch_stablecoin_yields, gaps, warnings)
    extended = fetch_recoverable(engine._fetch_stablecoin_yields_extended, gaps, warnings)
    platform = fetch_recoverable(engine._fetch_stablecoin_cefi_rates, gaps, warnings)
    return build_result(
        "yields",
        target,
        {
            "borrow_rates": borrow,
            "stablecoin_yields": primary,
            "stablecoin_yields_extended": extended,
            "stablecoin_cefi_rates": platform,
            "taoli_binance_margin_rates": engine._build_taoli_binance_margin_rates(borrow),
        },
        gaps,
        warnings,
        SOURCES,
    )
