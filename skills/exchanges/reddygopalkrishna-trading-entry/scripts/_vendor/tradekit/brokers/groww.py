"""Groww Trade API adapter (REST, standard library only).

Credentials (environment variables win over secrets.json):
    GROWW_ACCESS_TOKEN / groww_access_token   expires daily 06:00; create it under Groww > Trading APIs
    GROWW_API_KEY / groww_api_key             optional: lets `groww-login` mint the token with the approval flow
    GROWW_API_SECRET / groww_api_secret

Symbols are EXCHANGE:TRADINGSYMBOL (e.g. NSE:RELIANCE). Segment is CASH (equity) only here.
Products: CNC, MIS, NRML.
Cost: a "Trading API Subscription" is required (see groww.in/user/profile/trading-apis); the price is not
published in the API docs. Rate limits: orders 10/s and 250/min.
The docs do not state the response shape of every call; the field names used are the ones listed on
groww.in/trade-api/docs/curl (order list, holdings, positions, margins). No quotes are available, so
position values are at cost.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from typing import Dict, List, Optional

from .. import config
from . import _rest
from .base import Broker, BrokerError, normalize_order

BASE = "https://api.groww.in/v1"
_TYPE = {"market": "MARKET", "limit": "LIMIT", "stop": "SL_M", "stop_limit": "SL"}
_PRODUCT = {"CNC": "CNC", "MIS": "MIS", "NRML": "NRML"}
_OPEN = ("NEW", "ACKED", "TRIGGER_PENDING", "APPROVED", "MODIFICATION_REQUESTED", "CANCELLATION_REQUESTED")
_FILLED = ("EXECUTED", "COMPLETED")


class GrowwClient:
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or config.secret("groww_access_token", "GROWW_ACCESS_TOKEN")

    def _h(self) -> Dict[str, str]:
        _rest.need("Groww", access_token=self.access_token)
        return {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json", "X-API-VERSION": "1.0",
                "Content-Type": "application/json"}

    def _req(self, method, path, params=None, body=None):
        j = _rest.call("Groww", method, BASE + path, self._h(), params=params, body=body)
        if isinstance(j, dict) and j.get("status") == "FAILURE":
            e = j.get("error") or {}
            raise BrokerError(f"Groww {method} {path}: {e.get('message', j)} ({e.get('code')})")
        return j.get("payload", j) if isinstance(j, dict) else j

    def generate_token(self, api_key: str, api_secret: str) -> Dict:
        ts = str(int(time.time()))
        checksum = hashlib.sha256((api_secret + ts).encode()).hexdigest()
        j = _rest.call("Groww", "POST", BASE + "/token/api/access",
                       {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"},
                       body={"key_type": "approval", "checksum": checksum, "timestamp": ts})
        data = j.get("payload", j) if isinstance(j, dict) else {}
        if not data.get("token"):
            raise BrokerError("Groww did not return a token (approve the API key on the Groww Cloud API Keys page first)")
        self.access_token = data["token"]
        return data

    def margins(self):
        return self._req("GET", "/margins/detail/user")

    def holdings(self):
        return self._req("GET", "/holdings/user")

    def positions(self):
        return self._req("GET", "/positions/user", params={"segment": "CASH"})

    def orders(self):
        return self._req("GET", "/order/list", params={"segment": "CASH", "page": 0, "page_size": 100})

    def place_order(self, body):
        return self._req("POST", "/order/create", body=body)

    def cancel_order(self, order_id):
        return self._req("POST", "/order/cancel", body={"segment": "CASH", "groww_order_id": order_id})


def split_symbol(symbol: str):
    if ":" in symbol:
        e, t = symbol.split(":", 1)
    else:
        e, t = (config.load()["broker"].get("default_exchange") or ""), symbol
    if e.upper() not in ("NSE", "BSE") or not t:
        raise BrokerError("use EXCHANGE:SYMBOL with NSE or BSE (e.g. NSE:RELIANCE) or set broker.default_exchange")
    return e.upper(), t.upper()


class GrowwBroker(Broker):
    name = "groww"
    live = True

    def __init__(self, client: Optional[GrowwClient] = None):
        self.client = client or GrowwClient()
        self.cfg = config.load()

    def account(self) -> Dict:
        m = self.client.margins() or {}
        cash = _rest.f(m.get("clear_cash"))
        return {"broker": "groww", "live": True, "currency": self.cfg["account"].get("currency"),
                "cash": round(cash, 2), "equity": round(cash, 2), "margin_used": _rest.f(m.get("net_margin_used"))}

    def positions(self) -> List[Dict]:
        out = []
        for h in (self.client.holdings() or {}).get("holdings", []):
            q = _rest.f(h.get("quantity"))
            if q:
                avg = _rest.f(h.get("average_price"))
                out.append({"symbol": f"NSE:{h.get('trading_symbol')}", "qty": q, "avg_price": avg, "last_price": avg,
                            "market_value": round(q * avg, 2), "unrealized_pnl": 0.0, "product": "CNC"})
        for p in (self.client.positions() or {}).get("positions", []):
            q = _rest.f(p.get("quantity"))
            if q:
                avg = _rest.f(p.get("net_price"))
                out.append({"symbol": f"{p.get('exchange', 'NSE')}:{p.get('trading_symbol')}", "qty": q, "avg_price": avg,
                            "last_price": avg, "market_value": round(q * avg, 2),
                            "unrealized_pnl": 0.0, "realized_pnl": _rest.f(p.get("realised_pnl")), "product": p.get("product")})
        return out

    def orders(self, open_only: bool = False) -> List[Dict]:
        out = []
        for o in (self.client.orders() or {}).get("order_list", []):
            st = str(o.get("order_status", "")).upper()
            if open_only and st not in _OPEN:
                continue
            out.append({"order_id": o.get("groww_order_id"), "symbol": f"{o.get('exchange')}:{o.get('trading_symbol')}",
                        "side": str(o.get("transaction_type", "")).lower(), "qty": o.get("quantity"),
                        "type": o.get("order_type"), "limit_price": o.get("price"), "stop_price": o.get("trigger_price"),
                        "status": "filled" if st in _FILLED else st.lower(), "filled_qty": o.get("filled_quantity"),
                        "avg_fill_price": o.get("average_fill_price"), "product": o.get("product"),
                        "created": o.get("created_at"), "message": o.get("remark")})
        return out

    def to_params(self, order: Dict) -> Dict:
        o = normalize_order(order)
        exch, ts = split_symbol(o["symbol"])
        ref = "TS" + uuid.uuid4().hex[:12].upper()  # 14 chars, alphanumeric (docs: 8-20)
        p = {"trading_symbol": ts, "quantity": _rest.whole_qty(o, "Groww"), "validity": "DAY", "exchange": exch,
             "segment": "CASH", "product": _rest.product_for(order, _PRODUCT, "Groww"), "order_type": _TYPE[o["type"]],
             "transaction_type": o["side"].upper(), "order_reference_id": ref}
        if o["limit_price"] is not None:
            p["price"] = o["limit_price"]
        if o["stop_price"] is not None:
            p["trigger_price"] = o["stop_price"]
        return p

    def place(self, order: Dict) -> Dict:
        params = self.to_params(order)
        j = self.client.place_order(params) or {}
        if not j.get("groww_order_id"):
            raise BrokerError(f"Groww did not return an order id: {str(j)[:200]}")
        return {"order_id": j["groww_order_id"], "status": "submitted", "broker_status": j.get("order_status"),
                "broker": "groww", "params": params}

    def cancel(self, order_id: str) -> Dict:
        j = self.client.cancel_order(order_id) or {}
        return {"order_id": j.get("groww_order_id", order_id), "status": "cancel_requested"}
