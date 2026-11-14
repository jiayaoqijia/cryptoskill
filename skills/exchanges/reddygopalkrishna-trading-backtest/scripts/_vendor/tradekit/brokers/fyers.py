"""Fyers API v3 adapter (REST, standard library only).

Credentials (environment variables win over secrets.json):
    FYERS_APP_ID / fyers_app_id               e.g. ABCD1234-100
    FYERS_SECRET / fyers_secret               (only needed to create a session)
    FYERS_REDIRECT_URI / fyers_redirect_uri   must match the app's registered redirect URL
    FYERS_ACCESS_TOKEN / fyers_access_token   expires daily (about 06:30 IST); re-login each day

Symbols are EXCHANGE:SYMBOL-SERIES (e.g. NSE:SBIN-EQ). A bare symbol uses broker.default_exchange and "-EQ".
Products: CNC, INTRADAY (alias MIS), MARGIN (alias NRML), MTF.
Plans: the Standard API plan is free. Order APIs need an app with the Order Placement permission.
Since the 2026 SEBI retail-algo rules, order calls can require a registered static IP on the app.
Verified against the v3 docs: login, place (sync), cancel, order book fields. The positions and funds
paths follow Fyers' SDK (GET /positions, GET /funds) and are not spelled out in the docs pages we read.
"""

from __future__ import annotations

import hashlib
from typing import Dict, List, Optional
from urllib.parse import urlencode

from .. import config
from . import _rest
from .base import Broker, BrokerError, normalize_order

BASE = "https://api-t1.fyers.in/api/v3"
_TYPE = {"market": 2, "limit": 1, "stop": 3, "stop_limit": 4}
_PRODUCT = {"CNC": "CNC", "MIS": "INTRADAY", "INTRADAY": "INTRADAY", "NRML": "MARGIN", "MARGIN": "MARGIN", "MTF": "MTF"}
_STATUS = {1: "cancelled", 2: "filled", 4: "transit", 5: "rejected", 6: "open", 7: "expired"}
_OPEN = (4, 6)


class FyersClient:
    def __init__(self, app_id: Optional[str] = None, access_token: Optional[str] = None):
        self.app_id = app_id or config.secret("fyers_app_id", "FYERS_APP_ID")
        self.access_token = access_token or config.secret("fyers_access_token", "FYERS_ACCESS_TOKEN")

    def _h(self) -> Dict[str, str]:
        _rest.need("Fyers", app_id=self.app_id, access_token=self.access_token)
        return {"Authorization": f"{self.app_id}:{self.access_token}", "Content-Type": "application/json"}

    def _req(self, method, path, params=None, body=None):
        j = _rest.call("Fyers", method, BASE + path, self._h(), params=params, body=body)
        if isinstance(j, dict) and j.get("s") == "error":
            raise BrokerError(f"Fyers {method} {path}: {j.get('message', j)} (code {j.get('code')})")
        return j

    # session ----------------------------------------------------------
    def login_url(self, redirect_uri: str) -> str:
        q = urlencode({"client_id": self.app_id, "redirect_uri": redirect_uri, "response_type": "code", "state": "tskills"})
        return f"{BASE}/generate-authcode?{q}"

    def generate_session(self, auth_code: str, secret: str) -> Dict:
        h = hashlib.sha256(f"{self.app_id}:{secret}".encode()).hexdigest()
        j = _rest.call("Fyers", "POST", BASE + "/validate-authcode", {"Content-Type": "application/json"},
                       body={"grant_type": "authorization_code", "appIdHash": h, "code": auth_code})
        if j.get("s") != "ok" or not j.get("access_token"):
            raise BrokerError(f"Fyers login failed: {j.get('message', 'no access token returned')}")
        self.access_token = j["access_token"]
        return j

    # api ------------------------------------------------------------------
    def funds(self):
        return self._req("GET", "/funds")

    def positions(self):
        return self._req("GET", "/positions")

    def orderbook(self):
        return self._req("GET", "/orders")

    def place_order(self, body):
        return self._req("POST", "/orders/sync", body=body)

    def cancel_order(self, order_id):
        return self._req("DELETE", "/orders/sync", body={"id": order_id})


def fyers_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if ":" in s:
        return s
    exch = config.load()["broker"].get("default_exchange")
    if not exch:
        raise BrokerError(f"use EXCHANGE:SYMBOL-EQ (e.g. NSE:{s}-EQ) or set broker.default_exchange")
    return f"{exch.upper()}:{s}-EQ"


class FyersBroker(Broker):
    name = "fyers"
    live = True

    def __init__(self, client: Optional[FyersClient] = None):
        self.client = client or FyersClient()
        self.cfg = config.load()

    def account(self) -> Dict:
        rows = {str(r.get("title", "")).lower(): _rest.f(r.get("equityAmount")) for r in self.client.funds().get("fund_limit", [])}
        total, avail = rows.get("total balance", 0.0), rows.get("available balance", 0.0)
        return {"broker": "fyers", "live": True, "currency": self.cfg["account"].get("currency"),
                "cash": round(avail, 2), "equity": round(total or avail, 2)}

    def positions(self) -> List[Dict]:
        out = []
        for p in self.client.positions().get("netPositions", []):
            q = _rest.f(p.get("netQty"))
            if q == 0:
                continue
            last, avg = _rest.f(p.get("ltp")), _rest.f(p.get("netAvg"))
            out.append({"symbol": p.get("symbol"), "qty": q, "avg_price": avg, "last_price": last,
                        "market_value": round(q * last, 2),
                        "unrealized_pnl": round(_rest.f(p.get("unrealized_profit"), (last - avg) * q), 2),
                        "product": p.get("productType")})
        return out

    def orders(self, open_only: bool = False) -> List[Dict]:
        out = []
        for o in self.client.orderbook().get("orderBook", []):
            code = o.get("status")
            if open_only and code not in _OPEN:
                continue
            out.append({"order_id": o.get("id"), "symbol": o.get("symbol"), "side": "buy" if o.get("side") == 1 else "sell",
                        "qty": o.get("qty"), "type": {v: k for k, v in _TYPE.items()}.get(o.get("type"), o.get("type")),
                        "limit_price": o.get("limitPrice"), "stop_price": o.get("stopPrice"),
                        "status": _STATUS.get(code, str(code)), "filled_qty": o.get("filledQty"),
                        "avg_fill_price": o.get("tradedPrice"), "product": o.get("productType"),
                        "created": o.get("orderDateTime"), "message": o.get("message")})
        return out

    def to_params(self, order: Dict) -> Dict:
        o = normalize_order(order)
        tag = "".join(c for c in str(order.get("tag") or "tskills") if c.isalnum())[:30] or "tskills"
        return {"symbol": fyers_symbol(o["symbol"]), "qty": _rest.whole_qty(o, "Fyers"), "type": _TYPE[o["type"]],
                "side": 1 if o["side"] == "buy" else -1, "productType": _rest.product_for(order, _PRODUCT, "Fyers"),
                "limitPrice": o["limit_price"] or 0, "stopPrice": o["stop_price"] or 0, "validity": "DAY",
                "disclosedQty": 0, "offlineOrder": False, "stopLoss": 0, "takeProfit": 0, "orderTag": tag}

    def place(self, order: Dict) -> Dict:
        params = self.to_params(order)
        j = self.client.place_order(params)
        return {"order_id": j.get("id"), "status": "submitted", "broker": "fyers", "params": params}

    def cancel(self, order_id: str) -> Dict:
        j = self.client.cancel_order(order_id)
        return {"order_id": j.get("id", order_id), "status": "cancel_requested"}
