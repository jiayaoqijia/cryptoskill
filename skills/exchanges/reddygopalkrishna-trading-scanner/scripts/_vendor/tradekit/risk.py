"""Position sizing and risk math. Pure functions, no I/O."""

from __future__ import annotations

import math
from typing import Dict, List, Optional


def _round_lot(units: float, lot: float, fractional: bool) -> float:
    if lot and lot > 0:
        return math.floor(units / lot + 1e-9) * lot
    return units if fractional else math.floor(units + 1e-9)


def position_size(equity: float, entry: float, stop: float, risk_pct: float = 1.0,
                  lot_size: float = 1, multiplier: float = 1.0, max_position_pct: Optional[float] = None,
                  cash: Optional[float] = None, fractional: bool = False, fee_per_unit: float = 0.0,
                  margin_pct: float = 100.0) -> Dict:
    """Fixed-fractional sizing: risk `risk_pct`% of equity between entry and stop.

    multiplier  contract multiplier (futures/options point value); 1 for stocks/crypto
    lot_size    tradable increment (e.g. 1 share, 0.001 BTC, a futures lot of 50)
    margin_pct  capital required as % of notional (100 = cash equity, <100 for leveraged products)
    """
    if equity <= 0:
        raise ValueError("equity must be > 0")
    if entry <= 0 or stop <= 0:
        raise ValueError("entry and stop must be > 0")
    per_unit = abs(entry - stop) * multiplier + fee_per_unit
    if per_unit <= 0:
        raise ValueError("entry and stop must differ")
    side = "long" if stop < entry else "short"
    budget = equity * risk_pct / 100.0
    units = budget / per_unit
    limits = {"risk": units}
    capital_per_unit = entry * multiplier * margin_pct / 100.0
    if max_position_pct:
        limits["max_position"] = equity * max_position_pct / 100.0 / capital_per_unit
    if cash is not None:
        limits["cash"] = max(cash, 0) / capital_per_unit
    binding = min(limits, key=limits.get)
    units = _round_lot(limits[binding], lot_size, fractional)
    notional = units * entry * multiplier
    actual_risk = units * per_unit
    return {
        "side": side, "qty": units, "lots": (units / lot_size) if lot_size and lot_size > 1 else None,
        "entry": entry, "stop": stop, "risk_per_unit": round(per_unit, 6),
        "risk_budget": round(budget, 2), "actual_risk": round(actual_risk, 2),
        "actual_risk_pct": round(actual_risk / equity * 100, 4),
        "notional": round(notional, 2), "capital_required": round(units * capital_per_unit, 2),
        "position_pct": round(notional / equity * 100, 2), "binding_constraint": binding,
        "note": None if units > 0 else "size rounds to zero - stop too wide, lot too large, or risk too small",
    }


def atr_stop(entry: float, atr_value: float, mult: float = 2.0, side: str = "long") -> float:
    return entry - mult * atr_value if side == "long" else entry + mult * atr_value


def reward_risk(entry: float, stop: float, target: float) -> Optional[float]:
    risk = abs(entry - stop)
    if risk == 0:
        return None
    return round(abs(target - entry) / risk, 3)


def r_targets(entry: float, stop: float, rs=(1, 2, 3)) -> List[Dict]:
    risk = entry - stop
    return [{"r": r, "price": round(entry + r * risk, 6)} for r in rs]


def kelly(win_rate: float, payoff: float) -> float:
    """Kelly fraction f* = W - (1-W)/R. Returns 0 when there is no edge."""
    if payoff <= 0:
        return 0.0
    f = win_rate - (1 - win_rate) / payoff
    return max(0.0, f)


def volatility_size(equity: float, price: float, annual_vol_pct: float, target_vol_pct: float = 10.0,
                    lot_size: float = 1, fractional: bool = False) -> Dict:
    """Size so the position contributes target_vol_pct annualized volatility to the account."""
    if annual_vol_pct <= 0:
        raise ValueError("annual volatility must be > 0")
    weight = target_vol_pct / annual_vol_pct
    units = _round_lot(equity * weight / price, lot_size, fractional)
    return {"qty": units, "weight_pct": round(weight * 100, 2), "notional": round(units * price, 2)}


def risk_of_ruin(win_rate: float, payoff: float, risk_pct: float, ruin_pct: float = 50.0) -> float:
    """Classic approximation for fixed-fractional betting (probability of losing ruin_pct of equity)."""
    edge = win_rate * payoff - (1 - win_rate)
    if edge <= 0:
        return 1.0
    a = (1 - edge / (payoff + 1)) / (1 + edge / (payoff + 1))
    units = ruin_pct / risk_pct
    return round(min(1.0, a ** units), 6)


def open_risk(positions: List[Dict]) -> float:
    """Sum of (entry - stop) * qty across positions that carry a stop."""
    total = 0.0
    for p in positions:
        stop = p.get("stop")
        if stop is None:
            continue
        price = p.get("last_price") or p.get("avg_price") or p.get("entry")
        qty = p.get("qty", 0)
        total += max(0.0, (price - stop) * qty) if qty > 0 else max(0.0, (stop - price) * -qty)
    return total
