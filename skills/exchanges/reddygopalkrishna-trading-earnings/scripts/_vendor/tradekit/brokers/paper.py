"""Paper broker: a local simulated account. Default broker - no keys, no real money.

State lives in TRADING_SKILLS_HOME/paper/account.json. Prices come from the
configured data provider (or an injected price function in tests).

Fill model
    market      fills immediately at last price +/- slippage
    limit       fills immediately if marketable, else rests; fills when a later bar trades through
    stop        triggers when a bar trades through the stop, fills at stop (or the open on a gap) +/- slippage
    stop_loss / take_profit on an entry create an OCO pair of exit orders once the entry fills
Commission and slippage come from config "costs".
"""

from __future__ import annotations

import datetime as dt
import json
import uuid
from typing import Callable, Dict, List, Optional

from .. import config
from .base import Broker, BrokerError, normalize_order

PriceFn = Callable[[str], float]
BarFn = Callable[[str], Optional[Dict]]  # latest bar {open, high, low, close, date}


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


class PaperBroker(Broker):
    name = "paper"
    live = False

    def __init__(self, price_fn: Optional[PriceFn] = None, bar_fn: Optional[BarFn] = None,
                 starting_cash: Optional[float] = None):
        self.file = config.path("paper", "account.json")
        cfg = config.load()
        self.costs = cfg["costs"]
        self._price_fn = price_fn
        self._bar_fn = bar_fn
        if self.file.exists():
            self.state = json.loads(self.file.read_text())
        else:
            cash = float(starting_cash if starting_cash is not None else cfg["account"]["equity"])
            self.state = self._fresh(cash, cfg["account"].get("currency", "USD"))
            self._save()

    # ------------------------------------------------------------ state
    @staticmethod
    def _fresh(cash: float, currency: str) -> Dict:
        return {"cash": cash, "starting_cash": cash, "currency": currency, "positions": {},
                "orders": [], "fills": [], "realized_pnl": 0.0, "created": _now()}

    def _save(self) -> None:
        tmp = self.file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2))
        tmp.replace(self.file)

    def reset(self, cash: Optional[float] = None) -> Dict:
        cfg = config.load()
        c = float(cash if cash is not None else cfg["account"]["equity"])
        self.state = self._fresh(c, cfg["account"].get("currency", "USD"))
        self._save()
        return self.account()

    # ------------------------------------------------------------ prices
    def _price(self, symbol: str) -> float:
        if self._price_fn:
            return float(self._price_fn(symbol))
        from ..data import get_provider
        return float(get_provider().quote(symbol)["price"])

    def _bar(self, symbol: str) -> Optional[Dict]:
        if self._bar_fn:
            return self._bar_fn(symbol)
        from ..data import get_bars
        b = get_bars(symbol, "1d", "5d", use_cache=False)
        return b.last() if len(b) else None

    # ------------------------------------------------------------ interface
    def account(self) -> Dict:
        mv = 0.0
        upnl = 0.0
        for sym, p in self.state["positions"].items():
            try:
                last = self._price(sym)
            except Exception:  # noqa: BLE001
                last = p["avg_price"]
            mv += p["qty"] * last
            upnl += (last - p["avg_price"]) * p["qty"]
        equity = self.state["cash"] + mv
        return {"broker": "paper", "live": False, "currency": self.state["currency"],
                "cash": round(self.state["cash"], 2), "equity": round(equity, 2),
                "market_value": round(mv, 2), "unrealized_pnl": round(upnl, 2),
                "realized_pnl": round(self.state["realized_pnl"], 2),
                "starting_cash": self.state["starting_cash"],
                "return_pct": round((equity / self.state["starting_cash"] - 1) * 100, 3)
                if self.state["starting_cash"] else None}

    def positions(self) -> List[Dict]:
        out = []
        for sym, p in self.state["positions"].items():
            try:
                last = self._price(sym)
            except Exception:  # noqa: BLE001
                last = p["avg_price"]
            out.append({"symbol": sym, "qty": p["qty"], "avg_price": round(p["avg_price"], 6),
                        "last_price": last, "market_value": round(p["qty"] * last, 2),
                        "unrealized_pnl": round((last - p["avg_price"]) * p["qty"], 2),
                        "opened": p.get("opened")})
        return out

    def orders(self, open_only: bool = False) -> List[Dict]:
        return [o for o in self.state["orders"] if not open_only or o["status"] in ("open", "pending_parent")]

    def place(self, order: Dict) -> Dict:
        o = normalize_order(order)
        o.update({"order_id": "P" + uuid.uuid4().hex[:10], "status": "open", "created": _now(),
                  "filled_qty": 0, "avg_fill_price": None, "parent_id": order.get("parent_id"),
                  "oco_group": order.get("oco_group")})
        self.state["orders"].append(o)
        if o["type"] in ("market", "limit"):
            price = self._price(o["symbol"])
            if o["type"] == "market":
                self._fill(o, price, slip=True)
            elif (o["side"] == "buy" and price <= o["limit_price"]) or (o["side"] == "sell" and price >= o["limit_price"]):
                self._fill(o, min(price, o["limit_price"]) if o["side"] == "buy" else max(price, o["limit_price"]), slip=False)
        self._save()
        return self._public(o)

    def cancel(self, order_id: str) -> Dict:
        for o in self.state["orders"]:
            if o["order_id"] == order_id:
                if o["status"] not in ("open", "pending_parent"):
                    raise BrokerError(f"order {order_id} is {o['status']}, cannot cancel")
                o["status"] = "cancelled"
                o["updated"] = _now()
                # cancelling an entry cancels its attached exits
                for c in self.state["orders"]:
                    if c.get("parent_id") == order_id and c["status"] in ("open", "pending_parent"):
                        c["status"] = "cancelled"
                self._save()
                return self._public(o)
        raise BrokerError(f"order {order_id} not found")

    def close_all(self) -> List[Dict]:
        """Cancel open orders and flatten every position at market."""
        for o in self.state["orders"]:
            if o["status"] in ("open", "pending_parent"):
                o["status"] = "cancelled"
        results = []
        for sym, p in list(self.state["positions"].items()):
            side = "sell" if p["qty"] > 0 else "buy"
            results.append(self.place({"symbol": sym, "side": side, "qty": abs(p["qty"]), "type": "market",
                                       "tag": "flatten"}))
        self._save()
        return results

    def process(self) -> List[Dict]:
        """Check resting orders against each symbol's latest bar. Returns fills made."""
        made = []
        open_orders = [o for o in self.state["orders"] if o["status"] == "open" and o["type"] != "market"]
        bars: Dict[str, Optional[Dict]] = {}
        for o in open_orders:
            if o["status"] != "open":  # may have been cancelled by an OCO sibling this pass
                continue
            if o["symbol"] not in bars:
                try:
                    bars[o["symbol"]] = self._bar(o["symbol"])
                except Exception:  # noqa: BLE001
                    bars[o["symbol"]] = None
            bar = bars[o["symbol"]]
            if not bar:
                continue
            px = self._trigger_price(o, bar)
            if px is not None:
                self._fill(o, px, slip=o["type"] in ("stop",))
                made.append(self._public(o))
        self._save()
        return made

    # ------------------------------------------------------------ internals
    @staticmethod
    def _trigger_price(o: Dict, bar: Dict) -> Optional[float]:
        hi, lo, op = bar["high"], bar["low"], bar["open"]
        side, t = o["side"], o["type"]
        if t == "limit":
            lp = o["limit_price"]
            if side == "buy" and lo <= lp:
                return min(op, lp)
            if side == "sell" and hi >= lp:
                return max(op, lp)
        elif t in ("stop", "stop_limit"):
            sp = o["stop_price"]
            if side == "buy" and hi >= sp:
                fill = max(op, sp)
                if t == "stop_limit" and fill > o["limit_price"]:
                    return None
                return fill
            if side == "sell" and lo <= sp:
                fill = min(op, sp)
                if t == "stop_limit" and fill < o["limit_price"]:
                    return None
                return fill
        return None

    def _commission(self, notional: float) -> float:
        return abs(notional) * float(self.costs.get("commission_pct", 0)) / 100 + float(self.costs.get("commission_fixed", 0))

    def _fill(self, o: Dict, price: float, slip: bool) -> None:
        s = float(self.costs.get("slippage_pct", 0)) / 100 if slip else 0.0
        px = price * (1 + s) if o["side"] == "buy" else price * (1 - s)
        qty = o["qty"]
        signed = qty if o["side"] == "buy" else -qty
        notional = px * qty
        fee = self._commission(notional)
        pos = self.state["positions"].get(o["symbol"])
        realized = 0.0
        if pos is None:
            self.state["positions"][o["symbol"]] = {"qty": signed, "avg_price": px, "opened": _now()}
        else:
            old = pos["qty"]
            new = old + signed
            if old * signed > 0:  # adding
                pos["avg_price"] = (pos["avg_price"] * abs(old) + px * qty) / abs(new)
                pos["qty"] = new
            else:  # reducing / flipping
                closed = min(abs(old), qty)
                realized = (px - pos["avg_price"]) * closed * (1 if old > 0 else -1)
                if abs(new) < 1e-12:
                    del self.state["positions"][o["symbol"]]
                    # flat: attached exit orders for this symbol are no longer needed
                    for c in self.state["orders"]:
                        if c is not o and c["symbol"] == o["symbol"] and c.get("parent_id") and c["status"] == "open":
                            c["status"] = "cancelled"
                elif new * old > 0:
                    pos["qty"] = new
                else:
                    self.state["positions"][o["symbol"]] = {"qty": new, "avg_price": px, "opened": _now()}
        self.state["cash"] -= signed * px + fee
        self.state["realized_pnl"] += realized - fee
        o.update({"status": "filled", "filled_qty": qty, "avg_fill_price": round(px, 6), "fee": round(fee, 4),
                  "filled_at": _now(), "realized_pnl": round(realized - fee, 4)})
        self.state["fills"].append({"order_id": o["order_id"], "symbol": o["symbol"], "side": o["side"],
                                    "qty": qty, "price": px, "fee": fee, "time": o["filled_at"],
                                    "realized_pnl": realized - fee, "tag": o.get("tag")})
        # OCO: a filled exit cancels its siblings
        if o.get("oco_group"):
            for c in self.state["orders"]:
                if c is not o and c.get("oco_group") == o["oco_group"] and c["status"] == "open":
                    c["status"] = "cancelled"
        # attached exits become live after an entry fills
        if o.get("stop_loss") or o.get("take_profit"):
            exit_side = "sell" if o["side"] == "buy" else "buy"
            group = "G" + uuid.uuid4().hex[:8]
            if o.get("stop_loss"):
                self._child(o, {"symbol": o["symbol"], "side": exit_side, "qty": qty, "type": "stop",
                                "stop_price": o["stop_loss"], "tag": "stop_loss"}, group)
            if o.get("take_profit"):
                self._child(o, {"symbol": o["symbol"], "side": exit_side, "qty": qty, "type": "limit",
                                "limit_price": o["take_profit"], "tag": "take_profit"}, group)

    def _child(self, parent: Dict, spec: Dict, group: str) -> None:
        c = normalize_order(spec)
        c.update({"order_id": "P" + uuid.uuid4().hex[:10], "status": "open", "created": _now(),
                  "filled_qty": 0, "avg_fill_price": None, "parent_id": parent["order_id"], "oco_group": group})
        self.state["orders"].append(c)

    @staticmethod
    def _public(o: Dict) -> Dict:
        keys = ("order_id", "symbol", "side", "qty", "type", "limit_price", "stop_price", "stop_loss",
                "take_profit", "status", "filled_qty", "avg_fill_price", "fee", "created", "filled_at",
                "parent_id", "tag")
        return {k: o.get(k) for k in keys if o.get(k) is not None}
