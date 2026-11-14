"""Pre-trade risk gate and approval tokens.

The gate turns the risk limits in config["risk"] into hard PASS/FAIL checks.
A PASS writes a short-lived approval that the trading-broker requires before it
will submit an order. This makes "no plan, no trade" mechanical, not optional.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from typing import Dict, List, Optional

from . import config
from .journal import Journal


def _check(name: str, ok: Optional[bool], detail: str, warn_only: bool = False) -> Dict:
    if ok is None:
        status = "warn"
    elif ok:
        status = "pass"
    else:
        status = "warn" if warn_only else "fail"
    return {"check": name, "status": status, "detail": detail}


def evaluate(trade: Dict, equity: float, journal: Optional[Journal] = None, cfg: Optional[Dict] = None,
             open_positions: Optional[List[Dict]] = None) -> Dict:
    """trade: symbol, side(long/short), entry, stop, target?, qty, setup?, thesis?"""
    cfg = cfg or config.load()
    lim = cfg["risk"]
    j = journal or Journal()
    side = "long" if str(trade.get("side", "long")).lower() in ("long", "buy") else "short"
    entry = float(trade["entry"])
    stop = float(trade["stop"]) if trade.get("stop") not in (None, "") else None
    target = float(trade["target"]) if trade.get("target") not in (None, "") else None
    qty = float(trade.get("qty") or 0)
    checks: List[Dict] = []

    checks.append(_check("kill_switch_off", not config.kill_switch_on(),
                         "kill switch is OFF" if not config.kill_switch_on() else "KILL SWITCH IS ON - trading halted"))
    has_stop = stop is not None and ((side == "long" and stop < entry) or (side == "short" and stop > entry))
    checks.append(_check("stop_defined", has_stop,
                         f"stop {stop} on the correct side of entry {entry}" if has_stop
                         else "a valid stop is required (below entry for long, above for short)"))
    checks.append(_check("plan_documented", bool(trade.get("setup") or trade.get("thesis")),
                         "setup/thesis recorded" if (trade.get("setup") or trade.get("thesis"))
                         else "add --setup or --thesis: why this trade, what invalidates it", warn_only=True))
    checks.append(_check("qty_positive", qty > 0, f"qty {qty:g}" if qty > 0 else "qty must be > 0"))

    risk_amt = abs(entry - stop) * qty if has_stop else None
    if risk_amt is not None:
        rp = risk_amt / equity * 100
        checks.append(_check("risk_per_trade", rp <= lim["risk_per_trade_pct"] + 1e-9,
                             f"risk {rp:.2f}% of equity (limit {lim['risk_per_trade_pct']}%)"))
    if target is not None and has_stop:
        rr = abs(target - entry) / abs(entry - stop)
        checks.append(_check("reward_risk", rr >= lim["min_reward_risk"],
                             f"reward:risk {rr:.2f} (minimum {lim['min_reward_risk']})"))
    else:
        checks.append(_check("reward_risk", None, "no target given - reward:risk not checked"))

    notional = entry * qty
    pp = notional / equity * 100 if equity else 100
    checks.append(_check("position_size", pp <= lim["max_position_pct"] + 1e-9,
                         f"position {pp:.1f}% of equity (limit {lim['max_position_pct']}%)"))

    open_trades = j.list(status="open")
    heat = 0.0
    for t in open_trades:
        if t["stop"] is not None and t["entry_price"] is not None and t["qty"]:
            heat += abs(t["entry_price"] - t["stop"]) * float(t["qty"])
    total_heat = (heat + (risk_amt or 0)) / equity * 100
    checks.append(_check("portfolio_heat", total_heat <= lim["max_open_risk_pct"] + 1e-9,
                         f"open risk incl. this trade {total_heat:.2f}% (limit {lim['max_open_risk_pct']}%)"))

    n_open = len(open_trades)
    if open_positions is not None:
        n_open = max(n_open, len(open_positions))
    checks.append(_check("max_positions", n_open < lim["max_open_positions"],
                         f"{n_open} open positions (limit {lim['max_open_positions']})"))

    dup = any(t["symbol"] == trade["symbol"] for t in open_trades) or any(
        p.get("symbol") == trade["symbol"] for p in (open_positions or []))
    checks.append(_check("no_duplicate", not dup, "no existing position in this symbol" if not dup
                         else "already holding this symbol - adding is a new decision; size it as such",
                         warn_only=True))

    today_pnl = sum(t["pnl"] or 0 for t in j.closed_today())
    dl = -today_pnl / equity * 100 if today_pnl < 0 else 0.0
    checks.append(_check("daily_loss_limit", dl < lim["max_daily_loss_pct"],
                         f"today's realized loss {dl:.2f}% (limit {lim['max_daily_loss_pct']}%)"))

    streak = j.consecutive_losses()
    checks.append(_check("loss_streak", streak < lim["max_consecutive_losses"],
                         f"{streak} consecutive losses (pause at {lim['max_consecutive_losses']})"))

    dd = drawdown_from_peak(j, equity)
    if dd is not None:
        checks.append(_check("max_drawdown", dd < lim["max_drawdown_pct"],
                             f"account {dd:.2f}% below its journal peak (limit {lim['max_drawdown_pct']}%)"))

    fails = [c for c in checks if c["status"] == "fail"]
    warns = [c for c in checks if c["status"] == "warn"]
    verdict = "FAIL" if fails else ("PASS_WITH_WARNINGS" if warns else "PASS")
    return {"verdict": verdict, "symbol": trade["symbol"], "side": side, "entry": entry, "stop": stop,
            "setup": trade.get("setup") or "", "thesis": trade.get("thesis") or "",
            "target": target, "qty": qty, "risk_amount": round(risk_amt, 2) if risk_amt is not None else None,
            "equity_used": equity, "checks": checks,
            "blocking": [c["check"] for c in fails], "warnings": [c["check"] for c in warns]}


def drawdown_from_peak(j: Journal, equity: float) -> Optional[float]:
    closed = j.list(status="closed")
    if not closed:
        return None
    realized = sum(t["pnl"] or 0 for t in closed)
    start = equity - realized
    eq = start
    peak = start
    for t in closed:
        eq += t["pnl"] or 0
        peak = max(peak, eq)
    return max(0.0, (1 - equity / peak) * 100) if peak > 0 else None


# ------------------------------------------------------------------ approvals

def _hash(symbol: str, side: str, qty: float, stop: Optional[float]) -> str:
    raw = f"{symbol}|{side}|{float(qty):g}|{'' if stop is None else round(float(stop), 6)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def write_approval(result: Dict, trade_id: Optional[int] = None) -> Dict:
    cfg = config.load()
    now = dt.datetime.now()
    ttl = int(cfg["risk"].get("approval_ttl_minutes", 30))
    h = _hash(result["symbol"], result["side"], result["qty"], result["stop"])
    appr = {"approval_id": "A" + h, "symbol": result["symbol"], "side": result["side"], "qty": result["qty"],
            "entry": result["entry"], "stop": result["stop"], "target": result["target"],
            "verdict": result["verdict"], "trade_id": trade_id, "setup": result.get("setup", ""),
            "thesis": result.get("thesis", ""),
            "created": now.isoformat(timespec="seconds"),
            "expires": (now + dt.timedelta(minutes=ttl)).isoformat(timespec="seconds")}
    config.path("approvals", appr["approval_id"] + ".json").write_text(json.dumps(appr, indent=2))
    return appr


def find_approval(symbol: str, side: str, qty: float, stop: Optional[float]) -> Optional[Dict]:
    side = "long" if side in ("buy", "long") else "short"
    f = config.path("approvals", "A" + _hash(symbol, side, qty, stop) + ".json")
    if not f.exists():
        return None
    a = json.loads(f.read_text())
    if dt.datetime.fromisoformat(a["expires"]) < dt.datetime.now():
        return None
    return a


def consume_approval(approval_id: str) -> None:
    f = config.path("approvals", approval_id + ".json")
    if f.exists():
        f.unlink()


def audit(event: str, **data) -> None:
    rec = {"time": dt.datetime.now().isoformat(timespec="seconds"), "event": event, **data}
    with open(config.path("audit.log"), "a") as fh:
        fh.write(json.dumps(rec, default=str) + "\n")
