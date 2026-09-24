from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict

from .registry import MODULES, collect_module


def collect_all(engine: Any, target: date) -> Dict[str, Any]:
    results = {name: collect_module(name, engine, target) for name in MODULES}
    data: Dict[str, Any] = {}
    gaps: list[str] = []
    warnings: list[str] = []
    for result in results.values():
        data.update(result.data)
        gaps.extend(result.data_gaps)
        warnings.extend(result.source_warnings)
    data["data_gaps"] = gaps
    data["source_warnings"] = warnings
    data["module_status"] = {name: result.status for name, result in results.items()}
    return data


def build_context(engine: Any, target: date) -> Any:
    data = collect_all(engine, target)
    market = data["market"]
    return engine.DailyContext(
        target_date=target,
        generated_at_shanghai=datetime.now(tz=timezone(timedelta(hours=8))).isoformat(),
        market_as_of=market.get("as_of"),
        market_lag_days=market.get("lag_days"),
        market_cap=market.get("market_cap"),
        prev_market_cap=market.get("prev_market_cap"),
        volume_24h=market.get("volume_24h"),
        prev_volume_24h=market.get("prev_volume_24h"),
        btc_dom=market.get("btc_dom"),
        prev_btc_dom=market.get("prev_btc_dom"),
        market_history=market.get("history") or [],
        breadth_snapshot=data["breadth_snapshot"],
        top_assets=data["top_assets"],
        exchanges=data["exchanges"],
        deribit=data["deribit"],
        dvol=data["dvol"],
        dvol_history=data["dvol_history"],
        fng=data["fng"],
        fng_series=data["fng_series"],
        top2_trend=data["top2_trend"],
        top2_intraday=data["top2_intraday"],
        nondefi_carry=data["nondefi_carry"],
        borrow_rates=data["borrow_rates"],
        coingecko_capability=data["coingecko_capability"],
        stablecoin_yields=data["stablecoin_yields"],
        stablecoin_yields_extended=data["stablecoin_yields_extended"],
        stablecoin_cefi_rates=data["stablecoin_cefi_rates"],
        rwa_asset_classes=data["rwa_asset_classes"],
        rwa_token_movers=data["rwa_token_movers"],
        rwa_smartmoney=data["rwa_smartmoney"],
        taoli_binance_margin_rates=data["taoli_binance_margin_rates"],
        smartmoney_traders=data["smartmoney_traders"],
        smartmoney_signals=data["smartmoney_signals"],
        smartmoney_signal_attempted=data["smartmoney_signal_attempted"],
        smartmoney_positions=data["smartmoney_positions"],
        okx_news_sentiment=data["okx_news_sentiment"],
        module_status=data["module_status"],
        data_gaps=data["data_gaps"],
        source_warnings=data["source_warnings"],
    )
