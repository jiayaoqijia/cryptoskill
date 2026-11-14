"""Broker adapters. All share the Broker interface in base.py."""

from __future__ import annotations

from typing import Optional

from .. import config
from .base import Broker, BrokerError  # noqa: F401


BROKERS = ("paper", "kite", "fyers", "upstox", "dhan", "groww")


def get_broker(name: Optional[str] = None) -> Broker:
    name = (name or config.load()["broker"]["name"] or "paper").lower()
    if name == "paper":
        from .paper import PaperBroker
        return PaperBroker()
    if name == "kite":
        from .kite import KiteBroker
        return KiteBroker()
    if name == "fyers":
        from .fyers import FyersBroker
        return FyersBroker()
    if name == "upstox":
        from .upstox import UpstoxBroker
        return UpstoxBroker()
    if name == "dhan":
        from .dhan import DhanBroker
        return DhanBroker()
    if name == "groww":
        from .groww import GrowwBroker
        return GrowwBroker()
    raise BrokerError(f"unknown broker {name!r} ({' | '.join(BROKERS)})")
