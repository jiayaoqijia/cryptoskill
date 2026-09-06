try:
    from .binance_market import get_market_snapshot
except ImportError:
    from binance_market import get_market_snapshot
from score_trade import TradeInput, analyze_trade
import json


def analyze_live_trade(symbol, side, entry, stop_loss, take_profit, leverage=1.0, position_size=None):
    trade = TradeInput(
        symbol=symbol,
        side=side,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        leverage=leverage,
        position_size=position_size,
    )

    market_data = get_market_snapshot(symbol)
    structural_analysis = analyze_trade(trade)

    spot = market_data.get("spot", {})
    futures = market_data.get("futures", {})

    spot_price = spot.get("last_price")
    mark_price = futures.get("mark_price")
    funding_rate = futures.get("last_funding_rate")
    spread_pct = spot.get("spread_pct")
    open_interest = futures.get("open_interest")

    live_findings = []
    live_score_adjustment = 0

    if spot_price:
        deviation_pct = ((trade.entry - spot_price) / spot_price) * 100
        structural_analysis["entry_vs_live_pct"] = round(deviation_pct, 3)

        if abs(deviation_pct) > 5:
            live_score_adjustment -= 20
            live_findings.append("Entry is far from current market price.")
        elif abs(deviation_pct) > 2:
            live_score_adjustment -= 10
            live_findings.append("Entry has notable deviation from live price.")

    if funding_rate is not None:
        if trade.side.lower() == "long" and funding_rate > 0.0005:
            live_score_adjustment -= 5
            live_findings.append("Elevated positive funding adds LONG crowding risk.")
        elif trade.side.lower() == "short" and funding_rate < -0.0005:
            live_score_adjustment -= 5
            live_findings.append("Elevated negative funding adds SHORT crowding risk.")

    if spread_pct is not None and spread_pct > 0.1:
        live_score_adjustment -= 10
        live_findings.append("Live spread is unusually wide.")

    if spot_price and mark_price:
        basis_pct = ((mark_price - spot_price) / spot_price) * 100
        structural_analysis["futures_spot_basis_pct"] = round(basis_pct, 4)

        if abs(basis_pct) > 0.5:
            live_score_adjustment -= 5
            live_findings.append("Futures/spot basis is elevated.")

    structural_analysis["live_score_adjustment"] = live_score_adjustment
    structural_analysis["live_findings"] = live_findings
    structural_analysis["live_context"] = {
        "spot_price": spot_price,
        "mark_price": mark_price,
        "funding_rate": funding_rate,
        "spread_pct": spread_pct,
        "open_interest": open_interest,
    }

    base_score = structural_analysis.get("trade_integrity_score", 0)
    final_score = max(0, min(100, base_score + live_score_adjustment))
    structural_analysis["final_live_adjusted_score"] = final_score

    return {
        "trade_analysis": structural_analysis,
        "live_market_data": market_data,
    }


if __name__ == "__main__":
    result = analyze_live_trade(
        symbol="BTCUSDT",
        side="long",
        entry=79200,
        stop_loss=78000,
        take_profit=82000,
        leverage=5,
        position_size=200,
    )

    print(json.dumps(result, indent=2))
