from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class TradeInput:
    symbol: str
    side: str
    entry: float
    stop_loss: float
    take_profit: float
    leverage: float = 1.0
    position_size: Optional[float] = None


def analyze_trade(trade: TradeInput) -> dict:
    side = trade.side.lower().strip()

    if side not in ("long", "short"):
        raise ValueError("side must be 'long' or 'short'")

    if trade.entry <= 0:
        raise ValueError("entry must be greater than 0")

    if trade.stop_loss <= 0 or trade.take_profit <= 0:
        raise ValueError("stop_loss and take_profit must be greater than 0")

    if trade.leverage <= 0:
        raise ValueError("leverage must be greater than 0")

    if trade.position_size is not None and trade.position_size <= 0:
        raise ValueError("position_size must be greater than 0")

    if side == "long":
        if trade.stop_loss >= trade.entry:
            raise ValueError("LONG stop_loss must be below entry")
        if trade.take_profit <= trade.entry:
            raise ValueError("LONG take_profit must be above entry")

        risk_distance = trade.entry - trade.stop_loss
        reward_distance = trade.take_profit - trade.entry

    else:
        if trade.stop_loss <= trade.entry:
            raise ValueError("SHORT stop_loss must be above entry")
        if trade.take_profit >= trade.entry:
            raise ValueError("SHORT take_profit must be below entry")

        risk_distance = trade.stop_loss - trade.entry
        reward_distance = trade.entry - trade.take_profit

    stop_pct = (risk_distance / trade.entry) * 100
    target_pct = (reward_distance / trade.entry) * 100
    rr = reward_distance / risk_distance

    score = 100
    findings = []

    if rr < 1:
        score -= 35
        findings.append("Reward is smaller than risk.")
    elif rr < 1.5:
        score -= 20
        findings.append("Risk/reward is weak.")
    elif rr < 2:
        score -= 10
        findings.append("Risk/reward is acceptable.")
    else:
        findings.append("Risk/reward is strong.")

    if trade.leverage > 50:
        score -= 35
        findings.append("Leverage is extremely high.")
    elif trade.leverage > 20:
        score -= 25
        findings.append("Leverage is high.")
    elif trade.leverage > 10:
        score -= 15
        findings.append("Leverage is aggressive.")
    elif trade.leverage > 5:
        score -= 7
        findings.append("Leverage is moderate.")
    else:
        findings.append("Leverage is controlled.")

    exposure = stop_pct * trade.leverage

    if exposure >= 80:
        score -= 20
        findings.append("Leveraged stop exposure is very high.")
    elif exposure >= 40:
        score -= 10
        findings.append("Leveraged stop exposure is elevated.")

    score = max(0, min(100, score))

    if score >= 80:
        risk_level = "Strong"
    elif score >= 60:
        risk_level = "Acceptable"
    elif score >= 40:
        risk_level = "High Risk"
    else:
        risk_level = "Critical Risk"

    return {
        "symbol": trade.symbol.upper(),
        "side": side.upper(),
        "trade_integrity_score": score,
        "risk_level": risk_level,
        "risk_reward_ratio": round(rr, 2),
        "stop_distance_pct": round(stop_pct, 2),
        "target_distance_pct": round(target_pct, 2),
        "leveraged_stop_exposure": round(exposure, 2),
        "leverage": trade.leverage,
        "position_size": trade.position_size,
        "findings": findings,
        "data_scope": "Structural analysis only; no live market data used.",
    }


if __name__ == "__main__":
    example_trade = TradeInput(
        symbol="SOLUSDT",
        side="long",
        entry=140.0,
        stop_loss=136.0,
        take_profit=150.0,
        leverage=10.0,
        position_size=200.0,
    )

    result = analyze_trade(example_trade)
    print(json.dumps(result, indent=2))
