#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List


def _args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate an explicitly dated monthly report package")
    p.add_argument("--dir", required=True, type=Path)
    p.add_argument("--month", required=True)
    return p.parse_args()


def _read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    args = _args()
    root = args.dir.resolve()
    errors: List[str] = []
    manifest_path = root / "monthly_manifest.json"
    report_path = root / "orchestrated_secondary_report.md"
    try:
        manifest: Dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        manifest = {}
        errors.append(f"manifest parse failed: {exc}")
    try:
        report = report_path.read_text(encoding="utf-8")
    except Exception as exc:
        report = ""
        errors.append(f"report read failed: {exc}")

    if manifest.get("month") != args.month:
        errors.append(f"manifest month mismatch: {manifest.get('month')!r}")
    if manifest.get("status") not in {"complete", "partial"}:
        errors.append(f"manifest status is not publishable: {manifest.get('status')!r}")
    coverage = manifest.get("coverage") if isinstance(manifest.get("coverage"), dict) else {}
    module_sources = manifest.get("module_sources") if isinstance(manifest.get("module_sources"), dict) else {}
    if set(module_sources) != {"fig2", "fig3", "fig4", "fig6", "deribit", "core_report"}:
        errors.append("module_sources registry is incomplete")
    if not coverage.get("market_exact_calendar_month"):
        errors.append("CMC market series does not cover the exact requested calendar month")
    if coverage.get("fig2_return_method") != "exact_market_chart_range":
        errors.append("Top10 return method is not exact market_chart/range")
    if coverage.get("fig2_universe_method") != "current_market_cap_snapshot_survivorship_bias_disclosed":
        errors.append("Top10 universe method or survivorship-bias disclosure is missing")

    start = datetime.strptime(args.month + "-01", "%Y-%m-%d").date()
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)
    end = next_month - timedelta(days=1)

    fig2_path = root / "packages/fig2/fig2_top10_monthly_performance.csv"
    try:
        fig2 = _read_rows(fig2_path)
    except Exception as exc:
        fig2 = []
        errors.append(f"fig2 CSV parse failed: {exc}")
    if len(fig2) < 5:
        errors.append("fig2 has fewer than five usable rows")
    for idx, row in enumerate(fig2):
        if row.get("return_method") != "exact_market_chart_range":
            errors.append(f"fig2[{idx}] uses a rolling proxy")
        if row.get("actual_start_date") != start.isoformat() or row.get("actual_end_date") != end.isoformat():
            errors.append(f"fig2[{idx}] does not use exact month boundary dates")

    for rel in (
        "packages/fig3/fig3_defi_tvl_share.csv",
        "packages/fig4/fig4_monthly_nft_volume.csv",
        "packages/fig6/fig6_altcoin_outside_top10_share.csv",
    ):
        try:
            rows = _read_rows(root / rel)
            if args.month not in {row.get("month") for row in rows}:
                errors.append(f"{rel} does not contain target month")
        except Exception as exc:
            errors.append(f"{rel} parse failed: {exc}")

    funding_path = root / "packages/deribit/deribit_funding_monthly.csv"
    try:
        funding = _read_rows(funding_path)
    except Exception as exc:
        funding = []
        errors.append(f"monthly funding CSV parse failed: {exc}")
    if {r.get("currency") for r in funding} != {"BTC", "ETH"}:
        errors.append("monthly funding must contain BTC and ETH")
    for row in funding:
        try:
            if int(row.get("observation_count") or 0) < 24:
                errors.append(f"{row.get('currency')} monthly funding observation count is too small")
        except Exception:
            errors.append(f"{row.get('currency')} monthly funding observation count is invalid")

    deribit_manifest = ((manifest.get("report_meta") or {}).get("deribit") or {})
    dvol = deribit_manifest.get("dvol") if isinstance(deribit_manifest.get("dvol"), dict) else {}
    for ccy in ("btc", "eth"):
        if dvol.get(f"{ccy}_start") != start.isoformat() or dvol.get(f"{ccy}_end") != end.isoformat():
            errors.append(f"{ccy.upper()} DVOL does not cover exact target month")

    image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", report)
    missing = [ref for ref in image_refs if not (root / ref).is_file()]
    if missing:
        errors.append("report references missing images: " + ", ".join(missing))
    expected_title = f"# {start.year} 年 {start.month} 月二级市场月报"
    if not report.startswith(expected_title):
        errors.append("report title month mismatch")
    if start.month != 4 and "4 月日均成交额" in report:
        errors.append("hard-coded April fallback text leaked into report")
    if "幸存者偏差" not in report:
        errors.append("Top10 current-universe survivorship-bias disclosure is missing from report")

    losses = 0
    for row in fig2:
        try:
            losses += float(row.get("monthly_change_pct") or 0) < 0
        except Exception:
            pass
    if losses and "Top10 样本全部上涨" in report:
        errors.append("report claims all Top10 rose despite negative rows")

    result = {"status": "failed" if errors else "ok", "month": args.month, "directory": str(root), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
