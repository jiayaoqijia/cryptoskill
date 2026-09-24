from __future__ import annotations

from datetime import date
from typing import Any, Callable, Dict

from . import derivatives, market, rwa, sentiment, yields
from .base import ModuleResult


MODULES: Dict[str, Callable[[Any, date], ModuleResult]] = {
    "market": market.collect,
    "derivatives": derivatives.collect,
    "yields": yields.collect,
    "rwa": rwa.collect,
    "sentiment": sentiment.collect,
}

MODULE_SOURCES = {
    "market": market.SOURCES,
    "derivatives": derivatives.SOURCES,
    "yields": yields.SOURCES,
    "rwa": rwa.SOURCES,
    "sentiment": sentiment.SOURCES,
}


def collect_module(name: str, engine: Any, target: date) -> ModuleResult:
    try:
        collector = MODULES[name]
    except KeyError as exc:
        raise ValueError(f"unknown daily module: {name}") from exc
    return collector(engine, target)
