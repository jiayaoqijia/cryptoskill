"""Broker interface and order validation shared by every adapter."""

from __future__ import annotations

from typing import Dict, List, Optional

ORDER_TYPES = ("market", "limit", "stop", "stop_limit")
SIDES = ("buy", "sell")


class BrokerError(RuntimeError):
    pass


def normalize_order(order: Dict) -> Dict:
    """Validate and normalize an order dict. Raises BrokerError with a clear message."""
    o = dict(order)
    o["symbol"] = str(o.get("symbol") or "").strip()
    if not o["symbol"]:
        raise BrokerError("order needs a symbol")
    o["side"] = str(o.get("side") or "").lower()
    if o["side"] in ("long", "b"):
        o["side"] = "buy"
    if o["side"] in ("short", "s"):
        o["side"] = "sell"
    if o["side"] not in SIDES:
        raise BrokerError("side must be buy or sell")
    try:
        o["qty"] = float(o.get("qty"))
    except (TypeError, ValueError):
        raise BrokerError("qty must be a number") from None
    if o["qty"] <= 0:
        raise BrokerError("qty must be > 0")
    if o["qty"].is_integer():
        o["qty"] = int(o["qty"])
    o["type"] = str(o.get("type") or "limit").lower().replace("-", "_")
    if o["type"] in ("mkt",):
        o["type"] = "market"
    if o["type"] in ("lmt",):
        o["type"] = "limit"
    if o["type"] not in ORDER_TYPES:
        raise BrokerError(f"type must be one of {', '.join(ORDER_TYPES)}")
    for k in ("limit_price", "stop_price", "stop_loss", "take_profit"):
        if o.get(k) in ("", None):
            o[k] = None
        else:
            try:
                o[k] = float(o[k])
            except (TypeError, ValueError):
                raise BrokerError(f"{k} must be a number") from None
            if o[k] <= 0:
                raise BrokerError(f"{k} must be > 0")
    if o["type"] in ("limit", "stop_limit") and o["limit_price"] is None:
        raise BrokerError(f"{o['type']} order needs limit_price")
    if o["type"] in ("stop", "stop_limit") and o["stop_price"] is None:
        raise BrokerError(f"{o['type']} order needs stop_price")
    ref = o["limit_price"] or o["stop_price"]
    if ref and o.get("stop_loss"):
        if o["side"] == "buy" and o["stop_loss"] >= ref:
            raise BrokerError("stop_loss must be below the entry price for a buy")
        if o["side"] == "sell" and o["stop_loss"] <= ref:
            raise BrokerError("stop_loss must be above the entry price for a sell")
    if ref and o.get("take_profit"):
        if o["side"] == "buy" and o["take_profit"] <= ref:
            raise BrokerError("take_profit must be above the entry price for a buy")
        if o["side"] == "sell" and o["take_profit"] >= ref:
            raise BrokerError("take_profit must be below the entry price for a sell")
    return o


class Broker:
    name = "base"
    live = False

    def account(self) -> Dict:
        """{'equity', 'cash', 'currency', 'broker', 'live'}"""
        raise NotImplementedError

    def positions(self) -> List[Dict]:
        """[{'symbol', 'qty' (signed), 'avg_price', 'last_price', 'market_value', 'unrealized_pnl'}]"""
        raise NotImplementedError

    def orders(self, open_only: bool = False) -> List[Dict]:
        raise NotImplementedError

    def place(self, order: Dict) -> Dict:
        """Returns {'order_id', 'status', ...}"""
        raise NotImplementedError

    def cancel(self, order_id: str) -> Dict:
        raise NotImplementedError

    def get_order(self, order_id: str) -> Optional[Dict]:
        return next((o for o in self.orders() if str(o.get("order_id")) == str(order_id)), None)
