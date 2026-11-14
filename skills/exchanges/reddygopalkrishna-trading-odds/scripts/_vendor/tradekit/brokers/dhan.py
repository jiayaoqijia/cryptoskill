"""DhanHQ v2 adapter (REST, standard library only).

Credentials (environment variables win over secrets.json):
    DHAN_CLIENT_ID / dhan_client_id
    DHAN_ACCESS_TOKEN / dhan_access_token     valid 24 hours; create it in web.dhan.co > Access DhanHQ APIs

Symbols are EXCHANGESEGMENT:SECURITYID, e.g. NSE_EQ:11536 (Dhan identifies instruments by numeric
securityId; look it up in Dhan's scrip master CSV, https://images.dhan.co/api-data/api-scrip-master.csv).
Products: CNC, INTRADAY (alias MIS), MARGIN (alias NRML), MTF.
Cost: Trading APIs are free for all Dhan users (Data APIs are paid and are not used here).
Rules: a registered static IP is mandatory for placing, modifying and cancelling orders.
Dhan's published example responses are not fully consistent (e.g. fund field spelled "availabelBalance");
this adapter accepts both spellings.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .. import config
from . import _rest
from .base import Broker, BrokerError, normalize_order

BASE = "https://api.dhan.co/v2"
_TYPE = {"market": "MARKET", "limit": "LIMIT", "stop": "STOP_LOSS_MARKET", "stop_limit": "STOP_LOSS"}
_PRODUCT = {"CNC": "CNC", "MIS": "INTRADAY", "INTRADAY": "INTRADAY", "NRML": "MARGIN", "MARGIN": "MARGIN", "MTF": "MTF"}
_OPEN = ("TRANSIT", "PENDING", "PART_TRADED")


def split_symbol(symbol: str):
    seg, _, sid = symbol.strip().partition(":")
    if not sid or not sid.isdigit():
        raise BrokerError("Dhan symbols look like NSE_EQ:11536 (EXCHANGESEGMENT:securityId from the scrip master)")
    return seg.upper(), sid


class DhanClient:
    def __init__(self, client_id: Optional[str] = None, access_token: Optional[str] = None):
        self.client_id = client_id or config.secret("dhan_client_id", "DHAN_CLIENT_ID")
        self.access_token = access_token or config.secret("dhan_access_token", "DHAN_ACCESS_TOKEN")

    def _req(self, method, path, body=None):
        _rest.need("Dhan", client_id=self.client_id, access_token=self.access_token)
        return _rest.call("Dhan", method, BASE + path, {"access-token": self.access_token, "Content-Type": "application/json",
                                                         "Accept": "application/json"}, body=body)

    def profile(self):
        return self._req("GET", "/profile")

    def fundlimit(self):
        return self._req("GET", "/fundlimit")

    def positions(self):
        return self._req("GET", "/positions")

    def holdings(self):
        return self._req("GET", "/holdings")

    def orders(self):
        return self._req("GET", "/orders")

    def place_order(self, body):
        return self._req("POST", "/orders", body=body)

    def cancel_order(self, order_id):
        return self._req("DELETE", f"/orders/{order_id}")


class DhanBroker(Broker):
    name = "dhan"
    live = True

    def __init__(self, client: Optional[DhanClient] = None):
        self.client = client or DhanClient()
        self.cfg = config.load()

    def account(self) -> Dict:
        f = self.client.fundlimit()
        cash = _rest.f(_rest.first(f, ("availabelBalance", "availableBalance"), 0))
        return {"broker": "dhan", "live": True, "currency": self.cfg["account"].get("currency"),
                "cash": round(cash, 2), "equity": round(cash + _rest.f(f.get("utilizedAmount")), 2)}

    def positions(self) -> List[Dict]:
        out = []
        try:
            held = self.client.holdings()
            for h in held if isinstance(held, list) else []:
                q = _rest.f(h.get("totalQty"))
                if q:
                    avg = _rest.f(h.get("avgCostPrice"))
                    out.append({"symbol": f"{h.get('exchange', 'NSE')}_EQ:{h.get('securityId')}", "qty": q, "avg_price": avg,
                                "last_price": avg, "market_value": round(q * avg, 2), "unrealized_pnl": 0.0,
                                "product": "CNC", "name": h.get("tradingSymbol")})
        except BrokerError:
            pass  # a fresh account with no holdings can answer with an error body
        pos = self.client.positions()
        for p in pos if isinstance(pos, list) else []:
            q = _rest.f(p.get("netQty"))
            if q == 0:
                continue
            avg = _rest.f(p.get("costPrice"))
            out.append({"symbol": f"{p.get('exchangeSegment')}:{p.get('securityId')}", "qty": q, "avg_price": avg,
                        "last_price": avg, "market_value": round(q * avg, 2),
                        "unrealized_pnl": round(_rest.f(p.get("unrealizedProfit")), 2),
                        "product": p.get("productType"), "name": p.get("tradingSymbol")})
        return out  # Dhan returns no last price; value is at cost

    def orders(self, open_only: bool = False) -> List[Dict]:
        out = []
        book = self.client.orders()
        for o in book if isinstance(book, list) else []:
            st = str(o.get("orderStatus", "")).upper()
            if open_only and st not in _OPEN:
                continue
            out.append({"order_id": o.get("orderId"), "symbol": f"{o.get('exchangeSegment')}:{o.get('securityId')}",
                        "side": str(o.get("transactionType", "")).lower(), "qty": o.get("quantity"),
                        "type": o.get("orderType"), "limit_price": o.get("price"), "stop_price": o.get("triggerPrice"),
                        "status": st.lower(), "filled_qty": o.get("filledQty"), "avg_fill_price": o.get("averageTradedPrice"),
                        "product": o.get("productType"), "created": o.get("createTime"), "message": o.get("omsErrorDescription")})
        return out

    def to_params(self, order: Dict) -> Dict:
        o = normalize_order(order)
        seg, sid = split_symbol(o["symbol"])
        _rest.need("Dhan", client_id=self.client.client_id)
        tag = "".join(c for c in str(order.get("tag") or "tskills") if c.isalnum() or c in "_- ")[:30]
        return {"dhanClientId": self.client.client_id, "correlationId": tag, "transactionType": o["side"].upper(),
                "exchangeSegment": seg, "productType": _rest.product_for(order, _PRODUCT, "Dhan"),
                "orderType": _TYPE[o["type"]], "validity": "DAY", "securityId": sid,
                "quantity": _rest.whole_qty(o, "Dhan"), "price": o["limit_price"] or 0,
                "triggerPrice": o["stop_price"] or 0}

    def place(self, order: Dict) -> Dict:
        params = self.to_params(order)
        j = self.client.place_order(params)
        if not j.get("orderId"):
            raise BrokerError(f"Dhan did not return an orderId: {str(j)[:200]}")
        return {"order_id": j["orderId"], "status": "submitted", "broker_status": j.get("orderStatus"),
                "broker": "dhan", "params": params}

    def cancel(self, order_id: str) -> Dict:
        j = self.client.cancel_order(order_id) or {}
        return {"order_id": j.get("orderId", order_id), "status": "cancel_requested"}
