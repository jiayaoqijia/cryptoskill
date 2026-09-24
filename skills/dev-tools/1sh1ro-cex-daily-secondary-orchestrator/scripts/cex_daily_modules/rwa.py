from __future__ import annotations

from datetime import date
from typing import Any

from .base import ModuleResult, build_result


SOURCES = {
    "asset_classes": "RWA.xyz public pages (undocumented page payload)",
    "tokenized_stocks": "Binance Web3 public RWA stock, dynamic, kline and token endpoints",
    "smart_money": "Binance Web3 public Smart Money Signal",
}


def collect(engine: Any, target: date) -> ModuleResult:
    gaps: list[str] = []
    warnings: list[str] = []
    classes = engine._fetch_rwa_asset_classes(gaps)
    movers, smartmoney = engine._fetch_rwa_token_movers(target, gaps)
    return build_result(
        "rwa",
        target,
        {"rwa_asset_classes": classes, "rwa_token_movers": movers, "rwa_smartmoney": smartmoney},
        gaps,
        warnings,
        SOURCES,
    )
