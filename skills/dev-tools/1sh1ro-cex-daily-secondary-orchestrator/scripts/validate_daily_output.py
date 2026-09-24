#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_FILES = [
    "daily_secondary_report.md",
    "daily_manifest.json",
    "data/top10_assets_24h.csv",
    "data/btc_eth_24h_1h_series.csv",
    "data/stablecoin_cefi_rates_bitcompare.csv",
    "data/rwa_token_movers.csv",
    "data/rwa_asset_class_snapshot.csv",
]

REQUIRED_SOURCES = [
    "market_cap_volume_btc_dominance",
    "top_assets",
    "btc_24h",
    "eth_24h",
    "btc_intraday",
    "eth_intraday",
    "btc_perpetual",
    "eth_perpetual",
    "btc_dvol",
    "eth_dvol",
    "fear_greed",
    "stablecoin_yields",
    "stablecoin_platform_apy",
    "rwa_smart_money",
]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one explicitly dated daily-report output directory.")
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--date", required=True)
    return parser.parse_args()


def _usable_rwa_movers(rows: Any) -> int:
    if not isinstance(rows, list):
        return 0
    return sum(
        1
        for row in rows
        if isinstance(row, dict) and row.get("ticker") and row.get("change_24h_pct") is not None
    )


def _parseable_rwa_classes(rows: Any) -> int:
    if not isinstance(rows, list):
        return 0
    return sum(
        1
        for row in rows
        if isinstance(row, dict) and row.get("asset_class") and row.get("value_usd") is not None
    )


def main() -> int:
    args = _parse_args()
    root = args.dir.resolve()
    errors: List[str] = []
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        errors.append(f"missing files: {', '.join(missing)}")

    manifest_path = root / "daily_manifest.json"
    report_path = root / "daily_secondary_report.md"
    manifest: Dict[str, Any] = {}
    report = ""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"manifest parse failed: {exc}")
    try:
        report = report_path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"report read failed: {exc}")

    if manifest.get("date") != args.date:
        errors.append(f"manifest date={manifest.get('date')!r}, expected={args.date!r}")
    expected_title = f"# 二级市场日报（{args.date}）"
    if not report.startswith(expected_title):
        errors.append(f"report title does not start with {expected_title!r}")

    gaps = manifest.get("data_gaps")
    if not isinstance(gaps, list):
        errors.append("data_gaps must be a list")
    if not isinstance(manifest.get("source_warnings"), list):
        errors.append("source_warnings must be a list")
    coverage_status = manifest.get("coverage_status")
    coverage = manifest.get("coverage") if isinstance(manifest.get("coverage"), dict) else {}
    if coverage_status not in {"complete", "partial", "degraded"}:
        errors.append("coverage_status must be complete, partial, or degraded")
    if coverage.get("status") != coverage_status:
        errors.append("coverage.status must match coverage_status")
    if (gaps or manifest.get("source_warnings")) and coverage_status == "complete":
        errors.append("coverage_status cannot be complete when gaps or source warnings exist")
    if not isinstance(coverage.get("core_modules"), dict):
        errors.append("coverage.core_modules must be an object")
    module_status = coverage.get("modules") if isinstance(coverage.get("modules"), dict) else {}
    required_modules = {"market", "derivatives", "yields", "rwa", "sentiment"}
    if set(module_status) != required_modules:
        errors.append("coverage.modules must contain market, derivatives, yields, rwa, and sentiment")
    if any(value not in {"complete", "partial", "degraded"} for value in module_status.values()):
        errors.append("coverage.modules contains an invalid status")
    module_sources = manifest.get("module_sources") if isinstance(manifest.get("module_sources"), dict) else {}
    if set(module_sources) != required_modules:
        errors.append("module_sources must contain market, derivatives, yields, rwa, and sentiment")
    generated_at = manifest.get("generated_at_shanghai")
    if not isinstance(generated_at, str) or "T" not in generated_at or "+08:00" not in generated_at:
        errors.append("generated_at_shanghai must be an ISO timestamp with +08:00 offset")

    source_registry = manifest.get("source_registry")
    if not isinstance(source_registry, dict):
        errors.append("source_registry must be an object")
        missing_sources = REQUIRED_SOURCES
    else:
        missing_sources = [key for key in REQUIRED_SOURCES if not source_registry.get(key)]
    if missing_sources:
        errors.append(f"missing source registry entries: {', '.join(missing_sources)}")

    counts = manifest.get("counts") if isinstance(manifest.get("counts"), dict) else {}
    if int(counts.get("rwa_smartmoney_covered_assets") or 0) == 0:
        coverage_rows = ((manifest.get("rwa_smartmoney") or {}).get("rows") or [])
        structured_unavailable = bool(coverage_rows) and all(
            isinstance(row, dict) and row.get("coverage_status") in {"source_unavailable", "unsupported_chain"}
            for row in coverage_rows
        )
        if not structured_unavailable and not any("Binance Web3" in str(gap) and "聪明钱" in str(gap) for gap in (gaps or [])):
            errors.append("Binance Web3 RWA smart-money coverage is empty but no structured data_gap is recorded")

    movers = _usable_rwa_movers(manifest.get("rwa_token_movers"))
    classes = _parseable_rwa_classes(manifest.get("rwa_asset_classes"))
    if movers < 1:
        errors.append("rwa_token_movers has no usable records")
    if classes < 1:
        errors.append("rwa_asset_classes has no parseable records")

    leaked_markers = [
        marker
        for marker in ("DATA COVERAGE", "source_warnings", "Session expired", "CoinGecko 数据获取失败")
        if marker in report
    ]
    if leaked_markers:
        errors.append(f"backend diagnostics leaked into report: {', '.join(leaked_markers)}")

    image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", report)
    missing_images = [ref for ref in image_refs if not ref.startswith(("http://", "https://")) and not (root / ref).is_file()]
    if missing_images:
        errors.append(f"report references missing images: {', '.join(missing_images)}")

    market = manifest.get("market") if isinstance(manifest.get("market"), dict) else {}
    market_complete = all(
        market.get(key) is not None
        for key in ("market_cap", "prev_market_cap", "volume_24h", "prev_volume_24h", "btc_dom", "prev_btc_dom")
    )
    if not market_complete:
        invalid_market_claims = [
            phrase
            for phrase in ("价格与成交同向上行", "风险预算有边际回补", "流动性仍在选择性回流")
            if phrase in report
        ]
        if invalid_market_claims:
            errors.append(f"directional claims present while core market data is incomplete: {', '.join(invalid_market_claims)}")
        for ref in ("charts/chart_market_snapshot_levels.png", "charts/chart_market_daily_change.png", "charts/chart_market_breadth_snapshot.png"):
            if ref in report:
                errors.append(f"conditional market chart referenced without complete data: {ref}")

    for index, row in enumerate(manifest.get("rwa_token_movers") or []):
        if not isinstance(row, dict):
            continue
        status = str(row.get("market_status") or "").lower()
        if status not in {"open", "trading"} and row.get("premium_pct") is not None:
            errors.append(f"rwa_token_movers[{index}].premium_pct must be null when reference market is closed")
        if row.get("shares_multiplier") is None and any(
            row.get(key) is not None for key in ("reference_price_usd", "premium_pct")
        ):
            errors.append(f"rwa_token_movers[{index}] cannot calculate reference/premium without shares_multiplier")
        if row.get("flow_unit_status") in {"raw_unit_unverified", "anomalous_scale"} and any(
            row.get(key) is not None
            for key in ("onchain_volume_24h_usd", "buy_volume_24h_usd", "sell_volume_24h_usd", "net_buy_24h_usd")
        ):
            errors.append(f"rwa_token_movers[{index}] exposes USD flow fields without validated units")
        coverage = row.get("smart_signal_coverage")
        if coverage not in {"active_signal", "no_matching_signal", "source_unavailable", "unsupported_chain"}:
            errors.append(f"rwa_token_movers[{index}].smart_signal_coverage is invalid")
        if coverage != "active_signal" and any(
            row.get(key) is not None for key in ("smart_signal_direction", "smart_signal_count", "smart_signal_value_usd")
        ):
            errors.append(f"rwa_token_movers[{index}] has signal values without an active signal")

    for index, row in enumerate(manifest.get("rwa_asset_classes") or []):
        if not isinstance(row, dict):
            continue
        freshness = row.get("freshness_status")
        if freshness == "source_date_unavailable" and row.get("as_of") is not None:
            errors.append(f"rwa_asset_classes[{index}].as_of must be null when source date is unavailable")
        if freshness not in {"source_dated", "source_date_unavailable"}:
            errors.append(f"rwa_asset_classes[{index}].freshness_status is invalid")

    for index, row in enumerate(manifest.get("stablecoin_yields") or []):
        if not isinstance(row, dict):
            continue
        supply = row.get("supply_apy")
        rewards = row.get("rewards_apy")
        total = row.get("total_apy")
        if total is None or (supply is None and rewards is None):
            continue
        expected_total = float(supply or 0.0) + float(rewards or 0.0)
        if abs(float(total) - expected_total) > 0.02:
            errors.append(
                f"stablecoin_yields[{index}].total_apy is inconsistent with supply_apy + rewards_apy"
            )

    forbidden_report_phrases = [
        phrase
        for phrase in (
            "利差(APY-借币)",
            "流动性仍在选择性回流",
            "情绪回到中性区",
            "报价连续性和滑点表现会同步分化",
            "价格连续性更多由杠杆侧情绪决定",
        )
        if phrase in report
    ]
    if forbidden_report_phrases:
        errors.append(f"forbidden misleading report phrases: {', '.join(forbidden_report_phrases)}")
    if "两者窗口不可混用" not in report:
        errors.append("BTC/ETH ticker and intraday chart window distinction is missing")
    if "charts/chart_derivatives_snapshot.png" in report:
        errors.append("mixed-unit derivatives radar chart must not be referenced")

    top_rows = []
    try:
        with (root / "data/top10_assets_24h.csv").open(encoding="utf-8") as handle:
            top_rows = list(csv.DictReader(handle))
    except Exception as exc:
        errors.append(f"top10 CSV parse failed: {exc}")
    breadth = manifest.get("breadth_snapshot") if isinstance(manifest.get("breadth_snapshot"), dict) else {}
    if breadth.get("risk_breadth_definition") != "top_market_cap_directional_assets_excluding_stablecoins_staked_and_credit_mappings":
        errors.append("risk breadth definition is missing or invalid")
    excluded = {str(value).upper() for value in (breadth.get("excluded_symbols") or [])}
    top_symbols = {str(row.get("symbol") or "").upper() for row in top_rows}
    required_exclusions = top_symbols & {"USDT", "USDC", "DAI", "USDS", "FDUSD", "STETH", "WSTETH", "RETH", "CBETH", "WEETH", "FIGR_HELOC"}
    if not required_exclusions.issubset(excluded):
        errors.append("stablecoin or staked-asset constituents are missing from risk-breadth exclusions")
    risk_symbols = {str(value).upper() for value in (breadth.get("risk_asset_symbols") or [])}
    flat_count = sum(
        1 for row in top_rows
        if str(row.get("symbol") or "").upper() in risk_symbols
        and abs(float(row.get("change_24h_pct") or 0.0)) < 1e-12
    )
    if f"平盘 {flat_count}" not in report:
        errors.append(f"risk-asset flat count is missing or inconsistent; expected 平盘 {flat_count}")

    result = {
        "status": "failed" if errors else "ok",
        "date": manifest.get("date"),
        "directory": str(root),
        "usable_rwa_movers": movers,
        "parseable_rwa_asset_classes": classes,
        "data_gaps": gaps if isinstance(gaps, list) else None,
        "source_warning_count": len(manifest.get("source_warnings") or []),
        "source_registry": source_registry,
        "referenced_image_count": len(image_refs),
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
