#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import hashlib
import shutil
import statistics
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from monthly_module_registry import MODULE_ORDER, MODULE_SOURCES, build_module_commands

VALIDATOR = "~/.claude/skills/cex-monthly-secondary-orchestrator/scripts/validate_monthly_output.py"

CMC_GLOBAL_HIST = "https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical"

COINBASE_REF = "https://www.coinbase.com/institutional/research-insights/research/trading-insights/crypto-market-positioning-february-2026"
BINANCE_REF = "https://www.binance.com/en/research/analysis/monthly-market-insights-2026-02/"
KUCOIN_REF = "https://www.kucoin.com/news/articles/crypto-daily-market-report-february-25-2026"


@dataclass
class TaskResult:
    name: str
    status: str
    package_dir: Path
    notes: str


def _latest_completed_month(today: Optional[date] = None) -> str:
    t = today or date.today()
    if t.month == 1:
        return f"{t.year - 1}-12"
    return f"{t.year}-{t.month - 1:02d}"


def _month_minus(month: str, n: int) -> str:
    dt = datetime.strptime(month, "%Y-%m")
    y = dt.year
    m = dt.month - n
    while m <= 0:
        y -= 1
        m += 12
    return f"{y}-{m:02d}"


def _month_bounds(month: str) -> Tuple[date, date]:
    dt = datetime.strptime(month, "%Y-%m")
    start = date(dt.year, dt.month, 1)
    if dt.month == 12:
        nxt = date(dt.year + 1, 1, 1)
    else:
        nxt = date(dt.year, dt.month + 1, 1)
    return start, nxt - timedelta(days=1)


def _fmt_usd(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    x = abs(v)
    if x >= 1e12:
        s = f"${x/1e12:.2f}T"
    elif x >= 1e9:
        s = f"${x/1e9:.2f}B"
    elif x >= 1e6:
        s = f"${x/1e6:.2f}M"
    else:
        s = f"${x:,.0f}"
    return f"-{s}" if v < 0 else s


def _fmt_pct(v: Optional[float], signed: bool = True) -> str:
    if v is None:
        return "N/A"
    return f"{v:+.2f}%" if signed else f"{v:.2f}%"


def _fmt_bps(v: Optional[float]) -> str:
    if v is None:
        return "N/A"
    return f"{v * 10000:+.2f}bps"


def _safe_float(v: Any) -> Optional[float]:
    try:
        return float(v)
    except Exception:
        return None


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def _run(name: str, cmd: List[str], package_dir: Path) -> TaskResult:
    package_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    log = package_dir / "run.log"
    log.write_text((proc.stdout or "") + "\n--- STDERR ---\n" + (proc.stderr or ""), encoding="utf-8")
    if proc.returncode == 0:
        return TaskResult(name, "ok", package_dir, "")
    note = f"exit={proc.returncode}; see {log}"
    return TaskResult(name, "failed", package_dir, note)


def _copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def _prepare_output(charts_dir: Path, packages_dir: Path) -> None:
    charts_dir.mkdir(parents=True, exist_ok=True)
    packages_dir.mkdir(parents=True, exist_ok=True)

    # Remove stale chart artifacts from previous runs (for example old annual figures).
    for p in charts_dir.glob("*.png"):
        try:
            p.unlink()
        except Exception:
            pass

    for stale in (charts_dir.parent / "orchestrated_secondary_report.md", charts_dir.parent / "monthly_manifest.json"):
        if stale.exists():
            stale.unlink()

    for name in ("fig1", "fig2", "fig3", "fig4", "fig6", "deribit", "core_report"):
        d = packages_dir / name
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)


def _get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    full = url if not params else f"{url}?{urlencode(params)}"
    req = Request(full, headers={"User-Agent": "cex-monthly-secondary-orchestrator/1.0", "Accept": "application/json"})
    with urlopen(req, timeout=40) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_cmc_month_stats(month: str) -> Dict[str, Any]:
    start, end = _month_bounds(month)
    end_excl = end + timedelta(days=1)
    payload = _get_json(
        CMC_GLOBAL_HIST,
        {
            "interval": "1d",
            "convertId": "2781",
            "timeStart": f"{start.isoformat()}T00:00:00.000Z",
            "timeEnd": f"{end_excl.isoformat()}T00:00:00.000Z",
        },
    )
    quotes = ((payload.get("data") or {}).get("quotes") or []) if isinstance(payload, dict) else []

    rows: List[Tuple[date, Optional[float], Optional[float], Optional[float]]] = []
    for q in quotes:
        if not isinstance(q, dict):
            continue
        ts = q.get("timestamp")
        if not isinstance(ts, str):
            continue
        try:
            d = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
        except Exception:
            continue
        if d < start or d > end:
            continue
        qq = q.get("quote")
        qq0 = qq[0] if isinstance(qq, list) and qq and isinstance(qq[0], dict) else {}
        mc = qq0.get("totalMarketCap")
        vol = qq0.get("totalVolume24H")
        dom = q.get("btcDominance")
        rows.append(
            (
                d,
                float(mc) if isinstance(mc, (int, float)) else None,
                float(vol) if isinstance(vol, (int, float)) else None,
                float(dom) if isinstance(dom, (int, float)) else None,
            )
        )
    rows.sort(key=lambda x: x[0])

    cap_rows = [r for r in rows if r[1] is not None]
    vol_rows = [r for r in rows if r[2] is not None]
    dom_rows = [r for r in rows if r[3] is not None]

    cap_start = cap_rows[0][1] if cap_rows else None
    cap_end = cap_rows[-1][1] if cap_rows else None
    cap_chg = ((cap_end / cap_start - 1.0) * 100.0) if cap_start and cap_end else None
    cap_min = min((r[1] for r in cap_rows if r[1] is not None), default=None)
    cap_max = max((r[1] for r in cap_rows if r[1] is not None), default=None)
    cap_drawdown = ((cap_min / cap_max - 1.0) * 100.0) if cap_min and cap_max else None

    vol_avg = (sum(r[2] for r in vol_rows if r[2] is not None) / len(vol_rows)) if vol_rows else None
    vol_max = max((r[2] for r in vol_rows if r[2] is not None), default=None)

    dom_start = dom_rows[0][3] if dom_rows else None
    dom_end = dom_rows[-1][3] if dom_rows else None
    dom_chg = (dom_end - dom_start) if dom_start is not None and dom_end is not None else None
    dom_min = min((r[3] for r in dom_rows if r[3] is not None), default=None)
    dom_max = max((r[3] for r in dom_rows if r[3] is not None), default=None)

    return {
        "requested_start": start.isoformat(),
        "requested_end": end.isoformat(),
        "actual_start": rows[0][0].isoformat() if rows else None,
        "actual_end": rows[-1][0].isoformat() if rows else None,
        "observation_count": len({r[0] for r in rows}),
        "cap_start": cap_start,
        "cap_end": cap_end,
        "cap_chg_pct": cap_chg,
        "cap_min": cap_min,
        "cap_max": cap_max,
        "cap_drawdown_pct": cap_drawdown,
        "vol_avg": vol_avg,
        "vol_max": vol_max,
        "dom_start": dom_start,
        "dom_end": dom_end,
        "dom_chg": dom_chg,
        "dom_min": dom_min,
        "dom_max": dom_max,
    }


def _read_fig2_summary(csv_path: Path) -> Tuple[Optional[Tuple[str, float]], Optional[Tuple[str, float]]]:
    if not csv_path.exists():
        return None, None
    rows: List[Tuple[str, float]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            sym = (row.get("symbol") or "").upper()
            pct_raw = row.get("monthly_change_pct")
            try:
                pct = float(pct_raw) if pct_raw not in (None, "") else None
            except Exception:
                pct = None
            if sym and pct is not None:
                rows.append((sym, pct))
    if not rows:
        return None, None
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows[0], rows[-1]


def _read_fig2_rows(csv_path: Path) -> List[Tuple[str, float]]:
    out: List[Tuple[str, float]] = []
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            sym = (row.get("symbol") or "").upper()
            pct = _safe_float(row.get("monthly_change_pct"))
            if sym and pct is not None:
                out.append((sym, pct))
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def _read_fig6_last(csv_path: Path) -> Optional[float]:
    if not csv_path.exists():
        return None
    last: Optional[float] = None
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            v = row.get("outside_share_pct")
            try:
                last = float(v) if v not in (None, "") else last
            except Exception:
                pass
    return last


def _read_deribit_snapshot(csv_path: Path) -> Dict[str, Optional[float]]:
    out = {"btc_funding_8h": None, "eth_funding_8h": None}
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ccy = row.get("currency")
            try:
                f8h = float(row.get("funding_8h") or "")
            except Exception:
                f8h = None
            if ccy == "BTC":
                out["btc_funding_8h"] = f8h
            elif ccy == "ETH":
                out["eth_funding_8h"] = f8h
    return out


def _read_deribit_monthly(csv_path: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {"btc_funding_8h": None, "eth_funding_8h": None, "rows": []}
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ccy = str(row.get("currency") or "").upper()
            avg = _safe_float(row.get("average_funding_8h"))
            record = dict(row)
            record["observation_count"] = _safe_int(row.get("observation_count"))
            record["average_funding_8h"] = avg
            out["rows"].append(record)
            if ccy == "BTC":
                out["btc_funding_8h"] = avg
            elif ccy == "ETH":
                out["eth_funding_8h"] = avg
    return out


def _append_image(lines: List[str], outdir: Path, rel: str) -> bool:
    if not (outdir / rel).is_file():
        return False
    lines.extend([f"![{Path(rel).name}]({rel})", ""])
    return True


def _read_deribit_dvol_stats(csv_path: Path) -> Dict[str, Any]:
    out = {
        "btc_min": None,
        "btc_max": None,
        "btc_end": None,
        "btc_peak_date": None,
        "eth_min": None,
        "eth_max": None,
        "eth_end": None,
        "eth_peak_date": None,
    }
    if not csv_path.exists():
        return out
    btc_vals: List[Tuple[date, float]] = []
    eth_vals: List[Tuple[date, float]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            d: Optional[date] = None
            ds = row.get("date")
            if isinstance(ds, str):
                try:
                    d = datetime.strptime(ds, "%Y-%m-%d").date()
                except Exception:
                    d = None
            try:
                b = float(row.get("btc_dvol_close") or "")
                if d is not None:
                    btc_vals.append((d, b))
            except Exception:
                pass
            try:
                e = float(row.get("eth_dvol_close") or "")
                if d is not None:
                    eth_vals.append((d, e))
            except Exception:
                pass
    if btc_vals:
        out["btc_min"] = min(v for _, v in btc_vals)
        out["btc_max"] = max(v for _, v in btc_vals)
        out["btc_end"] = btc_vals[-1][1]
        btc_peak = max(btc_vals, key=lambda x: x[1])
        out["btc_peak_date"] = btc_peak[0].isoformat()
    if eth_vals:
        out["eth_min"] = min(v for _, v in eth_vals)
        out["eth_max"] = max(v for _, v in eth_vals)
        out["eth_end"] = eth_vals[-1][1]
        eth_peak = max(eth_vals, key=lambda x: x[1])
        out["eth_peak_date"] = eth_peak[0].isoformat()
    return out


def _read_fig3_snapshot(csv_path: Path) -> Dict[str, Optional[float]]:
    out = {
        "total_tvl_usd": None,
        "ethereum_share_pct": None,
        "solana_share_pct": None,
        "bsc_share_pct": None,
        "others_share_pct": None,
    }
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            out["total_tvl_usd"] = _safe_float(row.get("total_tvl_usd"))
            out["ethereum_share_pct"] = _safe_float(row.get("ethereum_share_pct"))
            out["solana_share_pct"] = _safe_float(row.get("solana_share_pct"))
            out["bsc_share_pct"] = _safe_float(row.get("bsc_share_pct"))
            out["others_share_pct"] = _safe_float(row.get("others_share_pct"))
    return out


def _read_fig4_volume(csv_path: Path) -> Optional[float]:
    if not csv_path.exists():
        return None
    last: Optional[float] = None
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            v = _safe_float(row.get("volume_usd"))
            if v is not None:
                last = v
    return last


def _read_deribit_oi(csv_path: Path) -> Dict[str, Dict[str, Optional[float]]]:
    out: Dict[str, Dict[str, Optional[float]]] = {
        "BTC": {"future_oi": None, "option_oi": None},
        "ETH": {"future_oi": None, "option_oi": None},
    }
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ccy = str(row.get("currency") or "").upper()
            kind = str(row.get("kind") or "").lower()
            oi = _safe_float(row.get("open_interest_sum"))
            if ccy not in out or oi is None:
                continue
            if kind == "future":
                out[ccy]["future_oi"] = oi
            elif kind == "option":
                out[ccy]["option_oi"] = oi
    return out


def _read_exchange_rows(csv_path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not csv_path.exists():
        return rows
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(
                {
                    "rank": _safe_int(row.get("rank")),
                    "name": row.get("name") or "",
                    "volume30d_usd": _safe_float(row.get("volume30d_usd")),
                    "pct30d": _safe_float(row.get("pct30d")),
                    "pct7d": _safe_float(row.get("pct7d")),
                    "spot24h_usd": _safe_float(row.get("spot24h_usd")),
                    "deriv24h_usd": _safe_float(row.get("deriv24h_usd")),
                }
            )
    rows.sort(key=lambda x: (x["rank"] is None, x["rank"] if x["rank"] is not None else 10_000, x["name"]))
    return rows


def _fng_label(v: int) -> str:
    if v < 25:
        return "Extreme Fear"
    if v < 45:
        return "Fear"
    if v < 55:
        return "Neutral"
    if v < 75:
        return "Greed"
    return "Extreme Greed"


def _fng_label_cn(v: int) -> str:
    if v < 25:
        return "极度恐惧"
    if v < 45:
        return "恐惧"
    if v < 55:
        return "中性"
    if v < 75:
        return "贪婪"
    return "极度贪婪"


def _fetch_fng_month_stats(month: str) -> Dict[str, Optional[float]]:
    out: Dict[str, Optional[float]] = {
        "start": None,
        "end": None,
        "min": None,
        "max": None,
        "avg": None,
        "below_20_days": None,
    }
    start, end = _month_bounds(month)
    payload = _get_json("https://api.alternative.me/fng/", {"limit": "120"})
    raw = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(raw, list):
        return out
    vals: List[Tuple[date, int]] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        ts = row.get("timestamp")
        v = row.get("value")
        if not (isinstance(ts, str) and ts.isdigit() and isinstance(v, str) and v.isdigit()):
            continue
        d = datetime.utcfromtimestamp(int(ts)).date()
        if start <= d <= end:
            vals.append((d, int(v)))
    vals.sort(key=lambda x: x[0])
    if not vals:
        return out
    numbers = [v for _, v in vals]
    out["start"] = float(numbers[0])
    out["end"] = float(numbers[-1])
    out["min"] = float(min(numbers))
    out["max"] = float(max(numbers))
    out["avg"] = float(sum(numbers) / len(numbers))
    out["below_20_days"] = float(sum(1 for n in numbers if n < 20))
    return out


def _fetch_cg_daily_prices(coin_id: str, days: int) -> List[Tuple[date, float]]:
    payload = _get_json(
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart",
        {"vs_currency": "usd", "days": str(days)},
    )
    arr = payload.get("prices") if isinstance(payload, dict) else None
    if not isinstance(arr, list):
        return []
    by_day: Dict[date, float] = {}
    for row in arr:
        if not (isinstance(row, list) and len(row) >= 2):
            continue
        ts, px = row[0], row[1]
        if not isinstance(ts, (int, float)) or not isinstance(px, (int, float)):
            continue
        d = datetime.utcfromtimestamp(ts / 1000.0).date()
        by_day[d] = float(px)
    return sorted(by_day.items(), key=lambda x: x[0])


def _compute_rv7(prices: List[Tuple[date, float]]) -> Dict[date, float]:
    if len(prices) < 8:
        return {}
    rets: List[Tuple[date, float]] = []
    for i in range(1, len(prices)):
        prev = prices[i - 1][1]
        cur = prices[i][1]
        if prev <= 0 or cur <= 0:
            continue
        rets.append((prices[i][0], math.log(cur / prev)))
    out: Dict[date, float] = {}
    window = 7
    for i in range(window - 1, len(rets)):
        chunk = [x[1] for x in rets[i - window + 1 : i + 1]]
        if len(chunk) < 2:
            continue
        std = statistics.pstdev(chunk)
        out[rets[i][0]] = std * math.sqrt(365.0) * 100.0
    return out


def _fetch_rv_month_stats(month: str) -> Dict[str, Optional[float]]:
    out: Dict[str, Optional[float]] = {
        "btc_start": None,
        "btc_end": None,
        "btc_min": None,
        "btc_max": None,
        "eth_start": None,
        "eth_end": None,
        "eth_min": None,
        "eth_max": None,
    }
    start, end = _month_bounds(month)
    days_needed = max(45, min(365, (date.today() - start).days + 12))
    btc = _fetch_cg_daily_prices("bitcoin", days_needed)
    eth = _fetch_cg_daily_prices("ethereum", days_needed)
    btc_rv = _compute_rv7(btc)
    eth_rv = _compute_rv7(eth)
    btc_vals = [v for d, v in sorted(btc_rv.items()) if start <= d <= end]
    eth_vals = [v for d, v in sorted(eth_rv.items()) if start <= d <= end]
    if btc_vals:
        out["btc_start"] = btc_vals[0]
        out["btc_end"] = btc_vals[-1]
        out["btc_min"] = min(btc_vals)
        out["btc_max"] = max(btc_vals)
    if eth_vals:
        out["eth_start"] = eth_vals[0]
        out["eth_end"] = eth_vals[-1]
        out["eth_min"] = min(eth_vals)
        out["eth_max"] = max(eth_vals)
    return out


def build_report(month: str, outdir: Path, tasks: List[TaskResult]) -> Dict[str, Any]:
    charts_dir = outdir / "charts"
    packages = outdir / "packages"
    start, end = _month_bounds(month)

    month_stats = fetch_cmc_month_stats(month)
    fig2_top, fig2_tail = _read_fig2_summary(packages / "fig2" / "fig2_top10_monthly_performance.csv")
    fig2_rows = _read_fig2_rows(packages / "fig2" / "fig2_top10_monthly_performance.csv")
    outside_share = _read_fig6_last(packages / "fig6" / "fig6_altcoin_outside_top10_share.csv")
    deribit = _read_deribit_monthly(packages / "deribit" / "deribit_funding_monthly.csv")
    dvol = _read_deribit_dvol_stats(packages / "deribit" / "deribit_dvol_daily.csv")
    deribit_manifest: Dict[str, Any] = {}
    try:
        deribit_manifest = json.loads((packages / "deribit" / "deribit_manifest.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    oi_snapshot_usable = bool((deribit_manifest.get("oi_snapshot") or {}).get("usable_as_target_month_end"))
    deribit_oi = _read_deribit_oi(packages / "deribit" / "deribit_oi_volume_snapshot.csv") if oi_snapshot_usable else {}
    fig3 = _read_fig3_snapshot(packages / "fig3" / "fig3_defi_tvl_share.csv")
    nft_volume = _read_fig4_volume(packages / "fig4" / "fig4_monthly_nft_volume.csv")
    # The core package exposes a rolling/current CMC exchange snapshot, not an
    # auditable historical calendar-month series. Never relabel it as target month.
    exchange_rows: List[Dict[str, Any]] = []
    try:
        fng_stats = _fetch_fng_month_stats(month)
    except Exception:
        fng_stats = {"start": None, "end": None, "min": None, "max": None, "avg": None, "below_20_days": None}
    try:
        rv_stats = _fetch_rv_month_stats(month)
    except Exception:
        rv_stats = {
            "btc_start": None,
            "btc_end": None,
            "btc_min": None,
            "btc_max": None,
            "eth_start": None,
            "eth_end": None,
            "eth_min": None,
            "eth_max": None,
        }

    cap_chg = month_stats.get("cap_chg_pct")
    dom_chg = month_stats.get("dom_chg")
    if cap_chg is not None and cap_chg > 0:
        lead = (
            f"{start.month} 月市场更像一次修复，而不是一轮全面风险偏好回归。"
            "总市值较月初回升，但是否扩散到长尾仍需更广的收益率样本验证。"
        )
    elif cap_chg is not None and cap_chg < 0:
        lead = (
            f"{start.month} 月市场延续防守格局，资金更多回流核心资产，长尾板块承接偏弱。"
        )
    else:
        lead = f"{start.month} 月市场整体仍以结构分化为主，交易主线集中在核心资产。"

    fig2_losses = [p for _, p in fig2_rows if p < 0]
    fig2_gains = [p for _, p in fig2_rows if p > 0]
    fig2_mid = statistics.median([p for _, p in fig2_rows]) if fig2_rows else None
    fig2_spread = (fig2_top[1] - fig2_tail[1]) if fig2_top and fig2_tail else None
    fng_end = _safe_int(fng_stats.get("end"))
    fng_avg = _safe_float(fng_stats.get("avg"))
    nft_volume_b = (nft_volume / 1e9) if nft_volume is not None else None
    cap_chg_text = _fmt_pct(cap_chg)
    dom_chg_text = f"{dom_chg:+.2f}pct" if dom_chg is not None else "N/A"

    lines: List[str] = []
    lines.append(f"# {start.year} 年 {start.month} 月二级市场月报")
    lines.append("")
    lines.append(
        f"{lead}本月更值得关注的不是单一价格涨跌，而是资金集中度、杠杆温度与情绪确认之间的错位。"
    )
    lines.append("")

    lines.append("## Key Takeaways")
    lines.append(
        f"- 市场从防守转向修复：总市值由 {_fmt_usd(month_stats.get('cap_start'))} 升至 {_fmt_usd(month_stats.get('cap_end'))}，月内变化 {cap_chg_text}，但 BTC 主导率同步上行 {dom_chg_text}。"
    )
    if fig2_top and fig2_tail:
        gain_claim = "全部上涨" if not fig2_losses else f"上涨 {len(fig2_gains)} 个、下跌 {len(fig2_losses)} 个"
        lines.append(
            f"- 头部资产样本{gain_claim}：中位数收益 {_fmt_pct(fig2_mid)}，最强 {fig2_top[0]} {_fmt_pct(fig2_top[1])}，最弱 {fig2_tail[0]} {_fmt_pct(fig2_tail[1])}。"
        )
    if outside_share is not None:
        lines.append(
            f"- 月末市值集中度：Top10 外市值占比为 {outside_share:.2f}%；该指标描述市值结构，不单独证明长尾风险偏好。"
        )
    bfd = deribit.get("btc_funding_8h")
    efd = deribit.get("eth_funding_8h")
    lines.append(
        f"- Deribit BTC/ETH 月内平均 8h 资金费率为 {_fmt_bps(bfd)} / {_fmt_bps(efd)}；是否拥挤还需结合分布与 OI 历史。"
    )
    if fng_end is not None:
        lines.append(
            f"- 情绪仍落后于价格：月末恐惧与贪婪指数为 {fng_end}（{_fng_label_cn(fng_end)}），更像仓位修补后的谨慎修复。"
        )
    lines.append("")

    lines.append("## 宏观代理与市场状态")
    if cap_chg is not None and cap_chg > 0 and dom_chg is not None and dom_chg >= 0:
        lines.append(
            f"总市值月内上行 {cap_chg:+.2f}%，BTC 主导率提高 {dom_chg:+.2f}pct。这个组合通常对应“核心资产修复”而不是“全市场进攻”：资金愿意重新承担风险，但优先选择流动性最好、共识最强的资产。"
        )
    elif cap_chg is not None and cap_chg > 0:
        lines.append(
            f"总市值月内上行 {cap_chg:+.2f}%，但 BTC 主导率没有同步走强，说明修复并非单一龙头驱动，内部轮动和板块分化更重要。"
        )
    elif cap_chg is not None and cap_chg < 0:
        lines.append(
            f"总市值月内下行 {cap_chg:+.2f}%，风险偏好仍偏谨慎，市场更多体现为去杠杆和防守性交易。"
        )
    else:
        lines.append("市值与主导率没有给出单边信号，市场仍处在结构分化阶段。")
    lines.append("")
    _append_image(lines, outdir, "charts/core_chart_1_marketcap.png")
    _append_image(lines, outdir, "charts/core_chart_2_btc_dom.png")
    lines.append("接下来需要确认的是成交额能否继续放大。如果市值上行但成交没有跟随，修复容易停留在估值回补；若成交同步回升，才更接近趋势延续。")
    lines.append("")

    lines.append("## 交易所流量与资金活跃度")
    if exchange_rows:
        vol30_sum = sum((x.get("volume30d_usd") or 0.0) for x in exchange_rows)
        prev_sum = 0.0
        for x in exchange_rows:
            v = x.get("volume30d_usd")
            p = x.get("pct30d")
            if v is None or p is None or p <= -99.0:
                continue
            prev_sum += v / (1.0 + p / 100.0)
        sum_chg = (vol30_sum / prev_sum - 1.0) * 100.0 if prev_sum > 0 else None

        ranked = [x for x in exchange_rows if x.get("pct30d") is not None]
        ranked.sort(key=lambda x: x.get("pct30d") or -9999, reverse=True)
        top_up = ranked[0] if ranked else None
        top_down = ranked[-1] if ranked else None

        lines.append(
            f"前排样本 30d 成交额合计约 {_fmt_usd(vol30_sum)}，估算环比 {_fmt_pct(sum_chg)}。"
        )
        if top_up and top_down:
            lines.append(
                f"增幅靠前为 {top_up['name']}（{_fmt_pct(top_up.get('pct30d'))}），回落靠前为 {top_down['name']}（{_fmt_pct(top_down.get('pct30d'))}）。"
            )
        lines.append("")
        lines.append("![core_chart_3_exchange_30d_change.png](charts/core_chart_3_exchange_30d_change.png)")
        lines.append("")
    else:
        lines.append(
            f"前排交易所历史自然月明细暂无可验证数据，因此本节不使用当前/滚动 30d 快照冒充目标月。全市场口径显示，{start.month} 月日均成交额约 {_fmt_usd(month_stats.get('vol_avg'))}，成交峰值约 {_fmt_usd(month_stats.get('vol_max'))}。"
        )
        lines.append("这意味着本月价格修复并不是在完全低流动性环境中完成，但平台间流量迁移和执行质量仍需要在补齐交易所明细后再判断。")
        lines.append("")

    lines.append("## 主流资产表现与市场广度")
    if fig2_rows:
        lines.append("口径说明：Top10 样本按报告生成时的当前市值排名选取，再回溯目标月收益；该方法存在幸存者偏差，不代表目标月初的历史 Top10 成分。")
        lines.append(
            f"头部资产中，表现最强的是 {fig2_top[0]}（{fig2_top[1]:+.2f}%），最弱的是 {fig2_tail[0]}（{fig2_tail[1]:+.2f}%），收益差约 {fig2_spread:.2f}pct。"
        )
        lines.append(
            f"上涨资产 {len(fig2_gains)} 个、下跌资产 {len(fig2_losses)} 个，头部样本中位数收益为 {_fmt_pct(fig2_mid)}。这说明本月不是单一资产行情，但也还不是长尾全面补涨。"
        )
        if outside_share is not None:
            lines.append(f"Top10 外市值占比月末为 {outside_share:.2f}%；它是集中度指标，不能代替更广资产收益率广度。")
        lines.append("")
    _append_image(lines, outdir, "charts/fig2_top10_monthly_performance.png")
    _append_image(lines, outdir, "charts/fig6_altcoin_outside_top10_share.png")

    lines.append("## 链上风险偏好：DeFi 稳定，NFT 仍弱")
    if fig3.get("total_tvl_usd") is not None:
        lines.append(
            f"DeFi TVL 月末约 {_fmt_usd(fig3.get('total_tvl_usd'))}，Ethereum 占比 {fig3.get('ethereum_share_pct'):.2f}%，Solana 与 BSC 分别为 {fig3.get('solana_share_pct'):.2f}% / {fig3.get('bsc_share_pct'):.2f}%。"
        )
        lines.append(
            f"结构上，链上资金仍高度集中在 Ethereum 生态，Others 占比 {fig3.get('others_share_pct'):.2f}%。这更像稳态配置，而不是高风险链上 beta 的快速扩张。"
        )
    else:
        lines.append("DeFi TVL 数据暂不可用，链上风险偏好以 NFT 与二级市场广度作为替代观察。")
    if nft_volume is not None:
        lines.append(
            f"NFT 月成交额约 {_fmt_usd(nft_volume)}（约 {nft_volume_b:.2f}B 美元）。该体量相对主流币修复仍偏弱，说明非同质化资产尚未成为本轮风险偏好的主线。"
        )
    else:
        lines.append("NFT 成交数据本次未稳定返回，因此不将 NFT 作为本月风险偏好判断的核心依据。")
    lines.append("")
    _append_image(lines, outdir, "charts/fig3_defi_tvl_share.png")
    _append_image(lines, outdir, "charts/fig4_monthly_nft_volume.png")

    lines.append("## 衍生品仓位温度")
    if bfd is not None and efd is not None:
        if abs(bfd) < 0.00001 and abs(efd) < 0.00001:
            lines.append(
                f"BTC 与 ETH 的资金费率都接近零轴（{_fmt_bps(bfd)} / {_fmt_bps(efd)}），说明杠杆并不拥挤，仓位更偏中性博弈。"
            )
        elif bfd > 0 and efd > 0:
            lines.append(
                f"资金费率整体为正（BTC {_fmt_bps(bfd)}，ETH {_fmt_bps(efd)}），市场仍有一定多头偏好，但尚未到极端拥挤的阶段。"
            )
        elif bfd < 0 and efd < 0:
            lines.append(
                f"资金费率整体偏负（BTC {_fmt_bps(bfd)}，ETH {_fmt_bps(efd)}），说明杠杆端仍带有防守或对冲意味。"
            )
        else:
            lines.append(
                f"BTC 与 ETH 的资金费率并不一致（{_fmt_bps(bfd)} / {_fmt_bps(efd)}），说明衍生品仓位更多体现结构分化而不是单边共识。"
            )
        if dvol.get("btc_end") is not None and dvol.get("eth_end") is not None:
            lines.append(
                f"DVOL 月末降至 BTC {dvol['btc_end']:.2f} / ETH {dvol['eth_end']:.2f}，较月内高点 BTC {dvol['btc_max']:.2f} / ETH {dvol['eth_max']:.2f} 明显回落。波动率回落与资金费率中性共存，意味着市场短期更像“修复后的再定价”，而不是高杠杆趋势行情。"
            )
        lines.append("")
    _append_image(lines, outdir, "charts/chart_deribit_funding.png")
    if not _append_image(lines, outdir, "charts/chart_deribit_oi.png"):
        lines.append("OI 仅有运行时快照，距离目标月末超过 48 小时，已从本月报告剔除。")
        lines.append("")
    _append_image(lines, outdir, "charts/chart_deribit_dvol.png")

    lines.append("## 情绪与波动定价")
    if fng_stats.get("end") is not None:
        end_fng = int(fng_stats["end"] or 0)
        lines.append(
            f"恐惧与贪婪指数月末为 {end_fng}，处于{_fng_label_cn(end_fng)}区间；月均约 {fng_avg:.1f}。价格若已修复而情绪仍偏弱，往往意味着这轮上行更像仓位修补，而不是新一轮全面风险偏好扩张。"
        )
    else:
        lines.append("情绪修复仍需结合后续成交与广度确认，短线更容易出现事件驱动下的波动放大。")
    lines.append("")
    _append_image(lines, outdir, "charts/core_chart_4_fng.png")
    _append_image(lines, outdir, "charts/core_chart_5_realized_vol.png")

    inside_share = (100.0 - outside_share) if outside_share is not None else None
    btc_fut = (deribit_oi.get("BTC") or {}).get("future_oi")
    btc_opt = (deribit_oi.get("BTC") or {}).get("option_oi")
    eth_fut = (deribit_oi.get("ETH") or {}).get("future_oi")
    eth_opt = (deribit_oi.get("ETH") or {}).get("option_oi")
    btc_opt_ratio = (btc_opt / btc_fut * 100.0) if isinstance(btc_opt, float) and isinstance(btc_fut, float) and btc_fut > 0 else None
    eth_opt_ratio = (eth_opt / eth_fut * 100.0) if isinstance(eth_opt, float) and isinstance(eth_fut, float) and eth_fut > 0 else None

    lines.append("## 下月交易框架（基准情景）")
    lines.append("1. 基准情景：维持核心资产优先，BTC/ETH/SOL 等高流动性资产仍是主要风险预算承载。只要 Funding 保持中性、DVOL 不重新上冲，回撤更适合看作仓位再平衡窗口。")
    lines.append("2. 上行情景：若 Top10 外占比连续抬升、成交额放大且 F&G 回到中性区间以上，可以逐步提高 beta 暴露，重点选择流动性充足且相对强势的头部 alt。")
    lines.append("3. 风险情景：若价格继续上行但情绪和成交不确认，或 DVOL 重新抬升而 Funding 转正过快，应降低追涨仓位，优先执行止盈和保证金缓冲。")
    lines.append("")

    (outdir / "orchestrated_secondary_report.md").write_text("\n".join(lines), encoding="utf-8")
    return {
        "market": month_stats,
        "deribit": deribit_manifest,
        "fig2_row_count": len(fig2_rows),
        "nft_volume_usd": nft_volume,
        "exchange_history_status": "unavailable_current_snapshot_rejected",
        "oi_snapshot_used": oi_snapshot_usable,
    }


def write_manifest(path: Path, tasks: List[TaskResult]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["task", "status", "package_dir", "notes"])
        for t in tasks:
            w.writerow([t.name, t.status, str(t.package_dir), t.notes])


def write_json_manifest(path: Path, month: str, tasks: List[TaskResult], report_meta: Dict[str, Any], outdir: Path) -> Dict[str, Any]:
    required_tasks = {"fig2", "fig3", "fig6", "deribit", "core_report"}
    task_map = {t.name: {"status": t.status, "notes": t.notes, "package_dir": str(t.package_dir)} for t in tasks}
    failed_required = sorted(name for name in required_tasks if (task_map.get(name) or {}).get("status") != "ok")
    gaps: List[str] = []
    if failed_required:
        gaps.append("required tasks failed: " + ", ".join(failed_required))
    if (task_map.get("fig4") or {}).get("status") != "ok":
        gaps.append("NFT monthly source unavailable; NFT chart and conclusion omitted")
    if report_meta.get("exchange_history_status") != "ok":
        gaps.append("historical calendar-month exchange volume unavailable; current rolling snapshot rejected")
    if not report_meta.get("oi_snapshot_used"):
        gaps.append("Deribit OI current snapshot is not within 48h of target month end; omitted")

    files: Dict[str, Dict[str, Any]] = {}
    for file_path in sorted(p for p in outdir.rglob("*") if p.is_file() and p.name not in {path.name}):
        rel = str(file_path.relative_to(outdir))
        files[rel] = {"size": file_path.stat().st_size, "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest()}
    market = report_meta.get("market") or {}
    market_exact = market.get("actual_start") == market.get("requested_start") and market.get("actual_end") == market.get("requested_end")
    status = "failed" if failed_required or not market_exact or not (outdir / "orchestrated_secondary_report.md").is_file() else ("partial" if gaps else "complete")
    obj = {
        "month": month,
        "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "status": status,
        "tasks": task_map,
        "module_sources": MODULE_SOURCES,
        "coverage": {
            "requested_start": market.get("requested_start"),
            "requested_end": market.get("requested_end"),
            "market_actual_start": market.get("actual_start"),
            "market_actual_end": market.get("actual_end"),
            "market_observation_count": market.get("observation_count"),
            "market_exact_calendar_month": market_exact,
            "fig2_return_method": "exact_market_chart_range",
            "fig2_universe_method": "current_market_cap_snapshot_survivorship_bias_disclosed",
            "deribit_funding_source": "public/get_funding_rate_history",
            "oi_snapshot_used": bool(report_meta.get("oi_snapshot_used")),
        },
        "data_gaps": gaps,
        "report_meta": report_meta,
        "files": files,
    }
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return obj


def main() -> int:
    parser = argparse.ArgumentParser(description="Run orchestrated CEX monthly secondary report pipeline")
    parser.add_argument("--month", default=_latest_completed_month(), help="YYYY-MM")
    parser.add_argument("--outdir", default=None, help="Output directory")
    parser.add_argument(
        "--context-months",
        type=int,
        default=1,
        help="Comparison window size for monthly charts (default: 1 => strict current month only)",
    )
    parser.add_argument("--fig6-top-alt", type=int, default=10)
    args = parser.parse_args()

    outdir = Path(args.outdir) if args.outdir else Path(f"./reports/{args.month}/secondary_orchestrated")
    charts_dir = outdir / "charts"
    packages = outdir / "packages"
    outdir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)
    packages.mkdir(parents=True, exist_ok=True)

    _prepare_output(charts_dir, packages)

    context_months = max(1, int(args.context_months))
    context_start = _month_minus(args.month, context_months - 1) if context_months > 1 else args.month

    commands = build_module_commands(args.month, packages, context_start, args.fig6_top_alt)
    tasks = [_run(name, commands[name], packages / name) for name in MODULE_ORDER]

    copies = {
        packages / "fig2" / "fig2_top10_monthly_performance.png": charts_dir / "fig2_top10_monthly_performance.png",
        packages / "fig3" / "fig3_defi_tvl_share.png": charts_dir / "fig3_defi_tvl_share.png",
        packages / "fig4" / "fig4_monthly_nft_volume.png": charts_dir / "fig4_monthly_nft_volume.png",
        packages / "fig6" / "fig6_altcoin_outside_top10_share.png": charts_dir / "fig6_altcoin_outside_top10_share.png",
        packages / "deribit" / "chart_deribit_dvol.png": charts_dir / "chart_deribit_dvol.png",
        packages / "deribit" / "chart_deribit_funding.png": charts_dir / "chart_deribit_funding.png",
        packages / "deribit" / "chart_deribit_oi.png": charts_dir / "chart_deribit_oi.png",
        packages / "core_report" / "charts" / "chart_1_marketcap.png": charts_dir / "core_chart_1_marketcap.png",
        packages / "core_report" / "charts" / "chart_2_btc_dom.png": charts_dir / "core_chart_2_btc_dom.png",
        packages / "core_report" / "charts" / "chart_4_fng.png": charts_dir / "core_chart_4_fng.png",
        packages / "core_report" / "charts" / "chart_5_realized_vol.png": charts_dir / "core_chart_5_realized_vol.png",
    }
    for src, dst in copies.items():
        _copy_if_exists(src, dst)

    write_manifest(outdir / "orchestrator_manifest.csv", tasks)

    required_failed = [t.name for t in tasks if t.name in {"fig2", "fig3", "fig6", "deribit", "core_report"} and t.status != "ok"]
    report_meta: Dict[str, Any] = {}
    if not required_failed:
        try:
            report_meta = build_report(args.month, outdir, tasks)
        except Exception as exc:
            report_meta = {"build_error": str(exc)}
    manifest = write_json_manifest(outdir / "monthly_manifest.json", args.month, tasks, report_meta, outdir)

    validation = subprocess.run(
        ["python3", VALIDATOR, "--dir", str(outdir), "--month", args.month],
        capture_output=True,
        text=True,
    )
    (outdir / "validation.json").write_text(validation.stdout or json.dumps({"status": "failed", "errors": [validation.stderr]}), encoding="utf-8")

    print(f"[{manifest['status']}] report: {outdir / 'orchestrated_secondary_report.md'}")
    print(f"[{manifest['status']}] manifest: {outdir / 'monthly_manifest.json'}")
    print(f"[{manifest['status']}] charts: {charts_dir}")
    return 1 if manifest["status"] == "failed" or validation.returncode != 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
