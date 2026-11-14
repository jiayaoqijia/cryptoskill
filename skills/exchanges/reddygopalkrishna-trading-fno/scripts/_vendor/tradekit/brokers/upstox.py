"""Upstox API adapter (REST, standard library only).

Credentials (environment variables win over secrets.json):
    UPSTOX_API_KEY / upstox_api_key
    UPSTOX_API_SECRET / upstox_api_secret         (only needed to create a session)
    UPSTOX_REDIRECT_URI / upstox_redirect_uri     must match the app's registered redirect URL
    UPSTOX_ACCESS_TOKEN / upstox_access_token     valid until 03:30 the next day; re-login daily

Symbols are Upstox instrument keys: SEGMENT|ISIN, e.g. NSE_EQ|INE669E01016. Find them in Upstox's
daily instrument file https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz.
Products: D (delivery, alias CNC), I (intraday, alias MIS), MTF.
Rules (Upstox notice, in force since 1 Apr 2026): MARKET orders are not allowed - use limit orders; order
calls can require a registered static IP. Pricing of the API is not stated in the developer docs.
Not implemented: holdings (endpoint not verified), so only the day's positions are listed.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from urllib.parse import urlencode

from .. import config
from . import _rest
from .base import Broker, BrokerError, normalize_order

API = "https://api.upstox.com/v2"
HFT = "https://api-hft.upstox.com"
_TYPE = {"market": "MARKET", "limit": "LIMIT", "stop": "SL-M", "stop_limit": "SL"}
_PRODUCT = {"CNC": "D", "D": "D", "MIS": "I", "I": "I", "MTF": "MTF"}
_OPEN = ("validation pending", "modify pending", "trigger pending", "put order req received",
         "modify after market order req received", "after market order req received", "open", "modify validation pending",
         "cancel pending", "open pending", "modified")


class UpstoxClient:
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        self.api_key = api_key or config.secret("upstox_api_key", "UPSTOX_API_KEY")
        self.access_token = access_token or config.secret("upstox_access_token", "UPSTOX_ACCESS_TOKEN")

    def _h(self, json_body: bool = False) -> Dict[str, str]:
        _rest.need("Upstox", access_token=self.access_token)
        h = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}
        if json_body:
            h["Content-Type"] = "application/json"
        return h

    def _req(self, method, url, params=None, body=None):
        j = _rest.call("Upstox", method, url, self._h(body is not None), params=params, body=body)
        if isinstance(j, dict) and j.get("status") == "error":
            errs = j.get("errors") or [{}]
            raise BrokerError(f"Upstox {method} {url.split('.com', 1)[-1]}: {errs[0].get('message', j)} ({errs[0].get('errorCode')})")
        return j.get("data", j) if isinstance(j, dict) else j

    # session ----------------------------------------------------------
    def login_url(self, redirect_uri: str) -> str:
        q = urlencode({"response_type": "code", "client_id": self.api_key, "redirect_uri": redirect_uri, "state": "tskills"})
        return f"{API}/login/authorization/dialog?{q}"

    def generate_session(self, code: str, api_secret: str, redirect_uri: str) -> Dict:
        _rest.need("Upstox", api_key=self.api_key)
        j = _rest.call("Upstox", "POST", API + "/login/authorization/token", {"Accept": "application/json"},
                       form={"code": code, "client_id": self.api_key, "client_secret": api_secret,
                             "redirect_uri": redirect_uri, "grant_type": "authorization_code"})
        if not j.get("access_token"):
            raise BrokerError("Upstox login failed: no access token returned (auth codes are single use)")
        self.access_token = j["access_token"]
        return j

    # api ------------------------------------------------------------------
    def funds(self):
        return self._req("GET", API + "/user/get-funds-and-margin", params={"segment": "SEC"})

    def positions(self):
        return self._req("GET", API + "/portfolio/short-term-positions")

    def orders(self):
        return self._req("GET", API + "/order/retrieve-all")

    def place_order(self, body):
        return self._req("POST", HFT + "/v3/order/place", body=body)

    def cancel_order(self, order_id):
        return self._req("DELETE", HFT + "/v2/order/cancel", params={"order_id": order_id})


class UpstoxBroker(Broker):
    name = "upstox"
    live = True

    def __init__(self, client: Optional[UpstoxClient] = None):
        self.client = client or UpstoxClient()
        self.cfg = config.load()

    def account(self) -> Dict:
        eq = (self.client.funds() or {}).get("equity", {})
        avail = _rest.f(eq.get("available_margin"))
        used = _rest.f(eq.get("used_margin"))
        return {"broker": "upstox", "live": True, "currency": self.cfg["account"].get("currency"),
                "cash": round(avail, 2), "equity": round(avail + used, 2), "margin_used": used}

    def positions(self) -> List[Dict]:
        out = []
        for p in self.client.positions() or []:
            q = _rest.f(p.get("quantity"))
            if q == 0:
                continue
            last, avg = _rest.f(p.get("last_price")), _rest.f(p.get("average_price"))
            out.append({"symbol": p.get("instrument_token"), "qty": q, "avg_price": avg, "last_price": last,
                        "market_value": round(q * last, 2),
                        "unrealized_pnl": round(_rest.f(p.get("unrealised"), (last - avg) * q), 2),
                        "product": p.get("product"), "name": p.get("trading_symbol")})
        return out

    def orders(self, open_only: bool = False) -> List[Dict]:
        out = []
        for o in self.client.orders() or []:
            st = str(o.get("status", "")).lower()
            if open_only and st not in _OPEN:
                continue
            out.append({"order_id": o.get("order_id"), "symbol": o.get("instrument_token"),
                        "side": str(o.get("transaction_type", "")).lower(), "qty": o.get("quantity"),
                        "type": o.get("order_type"), "limit_price": o.get("price"), "stop_price": o.get("trigger_price"),
                        "status": "filled" if st == "complete" else st, "filled_qty": o.get("filled_quantity"),
                        "avg_fill_price": o.get("average_price"), "product": o.get("product"),
                        "created": o.get("order_timestamp"), "message": o.get("status_message")})
        return out

    def to_params(self, order: Dict) -> Dict:
        o = normalize_order(order)
        if o["type"] == "market":
            raise BrokerError("Upstox no longer accepts MARKET orders via the API (since 1 Apr 2026) - use a limit order")
        key = o["symbol"]
        if "|" not in key:
            raise BrokerError("Upstox symbols are instrument keys like NSE_EQ|INE669E01016 (from the instrument file)")
        tag = "".join(c for c in str(order.get("tag") or "tskills") if c.isalnum())[:40]
        return {"quantity": _rest.whole_qty(o, "Upstox"), "product": _rest.product_for(order, _PRODUCT, "Upstox"),
                "validity": "DAY", "price": o["limit_price"] or 0, "tag": tag, "instrument_token": key,
                "order_type": _TYPE[o["type"]], "transaction_type": o["side"].upper(), "disclosed_quantity": 0,
                "trigger_price": o["stop_price"] or 0, "is_amo": False}

    def place(self, order: Dict) -> Dict:
        params = self.to_params(order)
        j = self.client.place_order(params) or {}
        ids = j.get("order_ids") or ([j["order_id"]] if j.get("order_id") else [])
        if not ids:
            raise BrokerError(f"Upstox did not return an order id: {str(j)[:200]}")
        return {"order_id": ids[0], "status": "submitted", "broker": "upstox", "params": params}

    def cancel(self, order_id: str) -> Dict:
        j = self.client.cancel_order(order_id) or {}
        return {"order_id": j.get("order_id", order_id), "status": "cancel_requested"}
