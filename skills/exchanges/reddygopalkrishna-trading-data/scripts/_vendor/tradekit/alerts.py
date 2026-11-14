"""Price, move and clock alerts for any market. Each alert rings once (until reset or re-armed).

Rule types
    above / below   price at or above / at or below `price`
    stop / target   the same, labelled for a trade (long: stop rings below, target above; short flips)
    pct             moved `pct` percent from the previous close (`direction` up | down | any)
    time            the exchange's local clock passed `at` (HH:MM) on a trading day
    open / close    the symbol's exchange opened, or is `minutes` from its close

Rules live in TRADING_SKILLS_HOME/alerts.json; what rang lives in state/alerts.json.
An alert is information, never an order.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from typing import Dict, List, Optional

from . import config, session

TYPES = ("above", "below", "stop", "target", "pct", "time", "open", "close")


def _rules_file():
    return config.path("alerts.json")


def _state_file():
    return config.path("state", "alerts.json")


def load_rules() -> List[Dict]:
    f = _rules_file()
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text()).get("rules", [])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"{f} is not valid JSON: {e}") from None


def save_rules(rules: List[Dict]) -> None:
    _rules_file().write_text(json.dumps({"rules": rules}, indent=2) + "\n")


def load_state() -> Dict:
    f = _state_file()
    if not f.exists():
        return {"rang": {}}
    try:
        return json.loads(f.read_text())
    except json.JSONDecodeError:
        return {"rang": {}}


def save_state(st: Dict) -> None:
    _state_file().write_text(json.dumps(st, indent=2) + "\n")


def make_id(rule: Dict, existing: List[Dict]) -> str:
    base = "-".join(str(x) for x in (rule.get("symbol") or "clock", rule["type"],
                                     rule.get("price") or rule.get("pct") or rule.get("at") or rule.get("minutes") or ""))
    base = re.sub(r"[^a-z0-9.-]+", "-", base.lower()).strip("-")
    ids = {r["id"] for r in existing}
    rid, n = base, 2
    while rid in ids:
        rid, n = f"{base}-{n}", n + 1
    return rid


def add(rule: Dict) -> Dict:
    if rule.get("type") not in TYPES:
        raise ValueError(f"alert type must be one of {', '.join(TYPES)}")
    if rule["type"] in ("above", "below", "stop", "target") and rule.get("price") is None:
        raise ValueError(f"a {rule['type']} alert needs a price")
    if rule["type"] in ("above", "below", "stop", "target", "pct", "open", "close") and not rule.get("symbol"):
        raise ValueError(f"a {rule['type']} alert needs a symbol")
    if rule["type"] == "pct" and not rule.get("pct"):
        raise ValueError("a pct alert needs --pct N")
    if rule["type"] == "time" and not re.match(r"^\d{1,2}:\d{2}$", str(rule.get("at") or "")):
        raise ValueError("a time alert needs --at HH:MM (the exchange's local time)")
    rules = load_rules()
    rule = {k: v for k, v in rule.items() if v is not None}
    rule.setdefault("created", dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
    rule["id"] = rule.get("id") or make_id(rule, rules)
    rules.append(rule)
    save_rules(rules)
    return rule


def remove(rule_id: str) -> bool:
    rules = load_rules()
    keep = [r for r in rules if r["id"] != rule_id]
    save_rules(keep)
    st = load_state()
    st["rang"].pop(rule_id, None)
    save_state(st)
    return len(keep) != len(rules)


def reset(rule_id: Optional[str] = None) -> int:
    st = load_state()
    n = len(st["rang"]) if rule_id is None else int(rule_id in st["rang"])
    if rule_id is None:
        st["rang"] = {}
    else:
        st["rang"].pop(rule_id, None)
    save_state(st)
    return n


def from_trades(trades: List[Dict], existing: List[Dict]) -> List[Dict]:
    """Stop and target alerts for open trades in the journal (skips ones already set)."""
    have = {(r.get("symbol"), r["type"], r.get("price")) for r in existing}
    out = []
    for t in trades:
        side = "short" if str(t.get("side", "long")).lower() in ("short", "sell") else "long"
        for kind, price in (("stop", t.get("stop")), ("target", t.get("target"))):
            if price is None or (t["symbol"], kind, float(price)) in have:
                continue
            out.append({"symbol": t["symbol"], "type": kind, "price": float(price), "side": side,
                        "note": f"journal trade #{t.get('id')} {kind}", "trade_id": t.get("id")})
    return out


def _crossed(rule: Dict, price: float) -> bool:
    kind, lvl = rule["type"], float(rule["price"])
    short = rule.get("side") == "short"
    if kind == "above" or (kind == "target" and not short) or (kind == "stop" and short):
        return price >= lvl
    return price <= lvl


def rearm(rule: Dict, quote: Optional[Dict], rang: Dict) -> bool:
    """A price rule with "rearm": true rings again once the price has gone back across its level."""
    if not rule.get("rearm") or rule["id"] not in rang or rule["type"] not in ("above", "below", "stop", "target"):
        return False
    if quote and quote.get("price") is not None and not _crossed(rule, quote["price"]):
        rang.pop(rule["id"], None)
        return True
    return False


def evaluate(rule: Dict, quote: Optional[Dict], now_local: str, rang: Dict) -> Optional[str]:
    """Message if the rule rings now, else None. `quote` = {price, previous_close, session, status}."""
    rid, today = rule["id"], now_local[:10]
    last = rang.get(rid)
    daily = rule["type"] in ("pct", "time", "open", "close")
    if last and (not daily or last[:10] == today):
        return None
    if rule.get("date") and rule["date"] != today:
        return None
    kind = rule["type"]
    sym = rule.get("symbol", "")
    if kind in ("above", "below", "stop", "target"):
        if not quote or quote.get("price") is None:
            return None
        p = quote["price"]
        if not _crossed(rule, p):
            return None
        words = {"above": "is at or above", "below": "is at or below", "stop": "hit the stop", "target": "hit the target"}
        return f"{sym} {p:,.2f} {words[kind]} {float(rule['price']):,.2f}" + (f" ({rule['note']})" if rule.get("note") else "")
    if kind == "pct":
        if not quote or quote.get("price") is None or not quote.get("previous_close"):
            return None
        move = (quote["price"] / quote["previous_close"] - 1) * 100
        d = rule.get("direction", "any")
        if abs(move) < float(rule["pct"]) or (d == "up" and move < 0) or (d == "down" and move > 0):
            return None
        return f"{sym} {quote['price']:,.2f} is {move:+.2f}% from the previous close {quote['previous_close']:,.2f}"
    sess = (quote or {}).get("session")
    status = (quote or {}).get("status")
    if kind == "time":
        if quote is not None and not sess:
            return None  # no session today on that exchange: not a trading day
        if now_local[11:16] < rule["at"].zfill(5):
            return None
        return f"It is {now_local[11:16]} ({rule['at']} alert{': ' + rule['label'] if rule.get('label') else ''})"
    if kind == "open":
        if status != "open":
            return None
        return f"{sym}'s exchange is open (session {sess['open']}-{sess['close']} local time)"
    if kind == "close":
        if status != "open" or not sess or not sess.get("close"):
            return None
        left = session.hm(sess["close"]) - session.hm(now_local[11:16])
        if left > int(rule.get("minutes", 5)):
            return None
        return f"{sym}'s exchange closes in {left} min ({sess['close']} local): flat-by-close time"
    return None
