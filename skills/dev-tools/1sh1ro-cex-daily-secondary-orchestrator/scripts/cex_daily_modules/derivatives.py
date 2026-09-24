from __future__ import annotations

from datetime import date
from typing import Any

from .base import ModuleResult, build_result, fetch_recoverable


SOURCES = {
    "perpetual_snapshot": "Deribit public/ticker; OKX public fallback",
    "dvol": "Deribit public/get_volatility_index_data",
    "nondefi_carry": "Binance Futures and OKX public market endpoints",
}


def collect(engine: Any, target: date) -> ModuleResult:
    gaps: list[str] = []
    warnings: list[str] = []
    deribit = engine._fetch_deribit(gaps)
    dvol, dvol_history = engine._fetch_dvol(target, gaps, lookback_days=2)
    carry = fetch_recoverable(engine._fetch_nondefi_carry, gaps, warnings)
    return build_result(
        "derivatives",
        target,
        {"deribit": deribit, "dvol": dvol, "dvol_history": dvol_history, "nondefi_carry": carry},
        gaps,
        warnings,
        SOURCES,
    )
