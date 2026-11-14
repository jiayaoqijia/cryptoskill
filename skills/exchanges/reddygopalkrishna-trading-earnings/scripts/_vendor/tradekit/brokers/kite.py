"""Zerodha Kite Connect v3 adapter (REST, standard library only).

Credentials (environment variables win over secrets.json):
    KITE_API_KEY / kite_api_key
    KITE_API_SECRET / kite_api_secret        (only needed to create a session)
    KITE_ACCESS_TOKEN / kite_access_token    (valid until the next morning; re-login daily)

Plans: the free "Personal" plan supports orders, GTT, portfolio and margins.
Historical candles and live quotes need the paid "Connect" plan.
Order APIs may be subject to your broker's and regulator's API rules
(e.g. registered static IP, algo identifiers). Check them before going live.

Symbols are EXCHANGE:TRADINGSYMBOL (e.g. NSE:INFY). A bare symbol uses broker.default_exchange.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import time
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Dict, List, Optional, Sequence

from .. import config, http
from .base import Broker, BrokerError, normalize_order

BASE = "https://api.kite.trade"
LOGIN = "https://kite.zerodha.com/connect/login"


class KiteClient:
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        self.api_key = api_key or config.secret("kite_api_key", "KITE_API_KEY")
        self.access_token = access_token or config.secret("kite_access_token", "KITE_ACCESS_TOKEN")
        if not self.api_key:
            raise BrokerError("Kite API key missing. Run: setup.py kite-login --api-key YOUR_KEY")

    # ------------------------------------------------------------ plumbing
    def _headers(self, auth: bool = True) -> Dict[str, str]:
        h = {"X-Kite-Version": "3"}
        if auth:
            if not self.access_token:
                raise BrokerError("Kite access token missing or expired. Run setup.py kite-login and kite-session.")
            h["Authorization"] = f"token {self.api_key}:{self.access_token}"
        return h

    def _req(self, method: str, path: str, params=None, data=None, auth=True, raw=False):
        try:
            body = http.request(method, BASE + path, params=params, data=data, headers=self._headers(auth))
        except http.HTTPError as e:
            msg = e.body
            try:
                j = json.loads(e.body)
                msg = f"{j.get('error_type', '')}: {j.get('message', e.body)}"
            except (json.JSONDecodeError, TypeError):
                pass
            if e.status == 403:
                msg += " (token expired or plan lacks this API - re-login, or data needs the Connect plan)"
            raise BrokerError(f"Kite {method} {path} failed [{e.status}] {msg}") from None
        if raw:
            return body.decode("utf-8")
        j = json.loads(body.decode("utf-8"))
        if j.get("status") != "success":
            raise BrokerError(f"Kite error: {j.get('message', j)}")
        return j.get("data")

    # ------------------------------------------------------------ session
    def login_url(self) -> str:
        return f"{LOGIN}?v=3&api_key={self.api_key}"

    def generate_session(self, request_token: str, api_secret: str) -> Dict:
        checksum = hashlib.sha256((self.api_key + request_token + api_secret).encode()).hexdigest()
        data = self._req("POST", "/session/token", data={"api_key": self.api_key, "request_token": request_token,
                                                          "checksum": checksum}, auth=False)
        self.access_token = data["access_token"]
        return data

    # ------------------------------------------------------------ account
    def profile(self) -> Dict:
        return self._req("GET", "/user/profile")

    def margins(self) -> Dict:
        return self._req("GET", "/user/margins")

    def positions(self) -> Dict:
        return self._req("GET", "/portfolio/positions")

    def holdings(self) -> List[Dict]:
        return self._req("GET", "/portfolio/holdings")

    def orders(self) -> List[Dict]:
        return self._req("GET", "/orders")

    def order_history(self, order_id: str) -> List[Dict]:
        return self._req("GET", f"/orders/{order_id}")

    # ------------------------------------------------------------ orders
    def place_order(self, variety: str = "regular", **params) -> Dict:
        return self._req("POST", f"/orders/{variety}", data=params)

    def modify_order(self, order_id: str, variety: str = "regular", **params) -> Dict:
        return self._req("PUT", f"/orders/{variety}/{order_id}", data=params)

    def cancel_order(self, order_id: str, variety: str = "regular") -> Dict:
        return self._req("DELETE", f"/orders/{variety}/{order_id}")

    def place_gtt_single(self, exchange: str, tradingsymbol: str, trigger: float, last_price: float,
                         transaction_type: str, quantity: int, product: str, limit_price: float) -> Dict:
        condition = {"exchange": exchange, "tradingsymbol": tradingsymbol, "trigger_values": [trigger],
                     "last_price": last_price}
        orders = [{"exchange": exchange, "tradingsymbol": tradingsymbol, "transaction_type": transaction_type,
                   "quantity": quantity, "order_type": "LIMIT", "product": product, "price": limit_price}]
        return self._req("POST", "/gtt/triggers", data={"type": "single", "condition": json.dumps(condition),
                                                          "orders": json.dumps(orders)})

    # ------------------------------------------------------------ market data (Connect plan)
    def ltp(self, instruments: Sequence[str]) -> Dict:
        return self._req("GET", "/quote/ltp", params={"i": list(instruments)})

    def quote(self, instruments: Sequence[str]) -> Dict:
        return self._req("GET", "/quote", params={"i": list(instruments)})

    def historical(self, token: int, interval: str, frm: str, to: str) -> List[List]:
        data = self._req("GET", f"/instruments/historical/{token}/{interval}", params={"from": frm, "to": to})
        return data.get("candles", [])

    def instruments(self, exchange: Optional[str] = None) -> List[Dict]:
        cache = config.path("cache", "kite", f"instruments_{exchange or 'all'}.csv")
        if cache.exists() and time.time() - cache.stat().st_mtime < 20 * 3600:
            text = cache.read_text()
        else:
            text = self._req("GET", f"/instruments/{exchange}" if exchange else "/instruments", raw=True)
            cache.write_text(text)
        return list(csv.DictReader(io.StringIO(text)))

    def instrument_token(self, symbol: str) -> int:
        exch, ts = split_symbol(symbol)
        for row in self.instruments(exch):
            if row.get("tradingsymbol") == ts:
                return int(row["instrument_token"])
        raise BrokerError(f"instrument {exch}:{ts} not found")


def split_symbol(symbol: str):
    if ":" in symbol:
        e, t = symbol.split(":", 1)
        return e.upper(), t.upper()
    default = config.load()["broker"].get("default_exchange")
    if not default:
        raise BrokerError(f"use EXCHANGE:SYMBOL (e.g. NSE:{symbol.upper()}) or set broker.default_exchange")
    return default.upper(), symbol.upper()


_TYPE_MAP = {"market": "MARKET", "limit": "LIMIT", "stop": "SL-M", "stop_limit": "SL"}

# Used when the instrument list (which carries each symbol's tick_size) is unavailable.
# 0.05 is a multiple of the common 0.01 tick, so prices on it are valid for both.
DEFAULT_TICK = Decimal("0.05")


def _dec(x) -> Decimal:
    return Decimal(str(x))


def on_tick(price: float, tick: Decimal) -> bool:
    return (_dec(price) % tick) == 0


def round_to_tick(price: float, tick: Decimal, mode: str = "nearest") -> float:
    """Round a price to the tick grid. mode: nearest | down | up."""
    rounding = {"nearest": ROUND_HALF_UP, "down": ROUND_FLOOR, "up": ROUND_CEILING}[mode]
    steps = (_dec(price) / tick).quantize(Decimal(1), rounding=rounding)
    return float(steps * tick)


class KiteBroker(Broker):
    name = "kite"
    live = True

    def __init__(self, client: Optional[KiteClient] = None):
        self.client = client or KiteClient()
        self.cfg = config.load()

    def account(self) -> Dict:
        m = self.client.margins()
        eq = m.get("equity", {})
        net = float(eq.get("net", 0))
        hold_val = 0.0
        try:
            for h in self.client.holdings():
                hold_val += float(h.get("last_price", 0)) * float(h.get("quantity", 0) + h.get("t1_quantity", 0))
        except BrokerError:
            pass
        return {"broker": "kite", "live": True, "currency": self.cfg["account"].get("currency"),
                "cash": round(float(eq.get("available", {}).get("live_balance", net)), 2),
                "equity": round(net + hold_val, 2), "margin_net": net, "holdings_value": round(hold_val, 2)}

    def positions(self) -> List[Dict]:
        out = []
        for h in self.client.holdings():
            q = float(h.get("quantity", 0)) + float(h.get("t1_quantity", 0))
            if q == 0:
                continue
            last = float(h.get("last_price", 0))
            avg = float(h.get("average_price", 0))
            out.append({"symbol": f"{h['exchange']}:{h['tradingsymbol']}", "qty": q, "avg_price": avg,
                        "last_price": last, "market_value": round(q * last, 2),
                        "unrealized_pnl": round((last - avg) * q, 2), "product": "CNC"})
        for p in (self.client.positions() or {}).get("net", []):
            q = float(p.get("quantity", 0))
            if q == 0:
                continue
            last = float(p.get("last_price", 0))
            avg = float(p.get("average_price", 0))
            out.append({"symbol": f"{p['exchange']}:{p['tradingsymbol']}", "qty": q, "avg_price": avg,
                        "last_price": last, "market_value": round(q * last, 2),
                        "unrealized_pnl": round(float(p.get("pnl", (last - avg) * q)), 2),
                        "product": p.get("product")})
        return out

    def orders(self, open_only: bool = False) -> List[Dict]:
        out = []
        for o in self.client.orders() or []:
            st = str(o.get("status", "")).lower()
            if open_only and st not in ("open", "trigger pending", "validation pending", "put order req received"):
                continue
            out.append({"order_id": o.get("order_id"), "symbol": f"{o.get('exchange')}:{o.get('tradingsymbol')}",
                        "side": str(o.get("transaction_type", "")).lower(), "qty": o.get("quantity"),
                        "type": o.get("order_type"), "limit_price": o.get("price"),
                        "stop_price": o.get("trigger_price"), "status": st, "filled_qty": o.get("filled_quantity"),
                        "avg_fill_price": o.get("average_price"), "product": o.get("product"),
                        "created": o.get("order_timestamp"), "message": o.get("status_message")})
        return out

    def tick_size(self, exch: str, ts: str) -> Decimal:
        """The instrument's tick size from Kite's instrument list, else DEFAULT_TICK."""
        try:
            for row in self.client.instruments(exch):
                if row.get("tradingsymbol") == ts:
                    tick = _dec(row.get("tick_size") or "0")
                    if tick > 0:
                        return tick
                    break
        except (BrokerError, AttributeError, RuntimeError, OSError, InvalidOperation, ValueError):
            pass
        return DEFAULT_TICK

    def _check_tick(self, label: str, price: float, tick: Decimal) -> None:
        if not on_tick(price, tick):
            lo, hi = round_to_tick(price, tick, "down"), round_to_tick(price, tick, "up")
            raise BrokerError(f"{label} {price:g} is not a multiple of the tick size {tick} - "
                              f"use {lo:g} or {hi:g}")

    def to_kite_params(self, order: Dict) -> Dict:
        o = normalize_order(order)
        exch, ts = split_symbol(o["symbol"])
        if not float(o["qty"]).is_integer():
            raise BrokerError("Kite quantities must be whole numbers")
        if o["type"] != "market":
            tick = self.tick_size(exch, ts)
            if o["type"] in ("limit", "stop_limit"):
                self._check_tick("limit price", o["limit_price"], tick)
            if o["type"] in ("stop", "stop_limit"):
                self._check_tick("stop price", o["stop_price"], tick)
        product = (order.get("product") or self.cfg["broker"].get("default_product") or "CNC").upper()
        params = {"exchange": exch, "tradingsymbol": ts, "transaction_type": o["side"].upper(),
                  "quantity": int(o["qty"]), "order_type": _TYPE_MAP[o["type"]], "product": product,
                  "validity": "DAY", "tag": str(order.get("tag") or "tskills")[:20]}
        if o["type"] in ("limit", "stop_limit"):
            params["price"] = o["limit_price"]
        if o["type"] in ("stop", "stop_limit"):
            params["trigger_price"] = o["stop_price"]
        return params

    def place(self, order: Dict) -> Dict:
        params = self.to_kite_params(order)
        data = self.client.place_order("regular", **params)
        return {"order_id": data.get("order_id"), "status": "submitted", "broker": "kite", "params": params}

    def cancel(self, order_id: str) -> Dict:
        data = self.client.cancel_order(order_id)
        return {"order_id": data.get("order_id", order_id), "status": "cancel_requested"}

    def protect_plan(self, symbol: str, stop: float, buffer_pct: float = 0.5) -> Dict:
        """Validate a GTT stop and compute its limit price (no network call except the cached instrument list)."""
        exch, ts = split_symbol(symbol)
        tick = self.tick_size(exch, ts)
        self._check_tick("stop price", stop, tick)
        # sell limit below the trigger, rounded down onto the tick grid so Kite accepts it
        limit = round_to_tick(stop * (1 - buffer_pct / 100), tick, "down")
        return {"exchange": exch, "tradingsymbol": ts, "trigger": stop, "limit": limit, "tick": str(tick)}

    def protect(self, symbol: str, qty: int, stop: float, product: str = "CNC", buffer_pct: float = 0.5) -> Dict:
        """Place a GTT stop-loss for an existing long holding."""
        plan = self.protect_plan(symbol, stop, buffer_pct)
        exch, ts, limit = plan["exchange"], plan["tradingsymbol"], plan["limit"]
        try:
            last = float(self.client.ltp([f"{exch}:{ts}"])[f"{exch}:{ts}"]["last_price"])
        except (BrokerError, KeyError):
            last = stop * 1.05
        data = self.client.place_gtt_single(exch, ts, stop, last, "SELL", int(qty), product, limit)
        return {"gtt_id": data.get("trigger_id"), "status": "gtt_active", "trigger": stop, "limit": limit}
