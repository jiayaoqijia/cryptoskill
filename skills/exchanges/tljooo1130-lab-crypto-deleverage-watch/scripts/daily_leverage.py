#!/usr/bin/env python3
"""Daily BTC leverage collector and chart.

Usage (Asia/Bangkok daily job, e.g. 09:30):
    python3 scripts/daily_leverage.py --data-dir ./data/leverage

Optional:
    --elr 0.249 --elr-asof 2026-11-09
    --no-backfill
    --plot-only
    --days 30

One row per Asia/Bangkok calendar date in history.csv.
OKX 1D bars are stamped 00:00 UTC+8 and assigned to that UTC+8 date, so a
09:30 Bangkok run already sees "today" for long/short and historical OI.
Live OKX OI / funding always overwrite today's row.
Do not fabricate missing series. CoinGlass / Hyperliquid / liquidations /
ELR have no free multi-day history here and start from the first live run.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.ticker import AutoMinorLocator

def _default_data_dir() -> Path:
    env = __import__("os").environ.get("LEVERAGE_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent / "data" / "leverage"

DIR = _default_data_dir()
CSV_PATH = DIR / "history.csv"
ELR_PATH = DIR / "elr_manual.json"
BKK = ZoneInfo("Asia/Bangkok")
CST = ZoneInfo("Asia/Shanghai")
UTC = timezone.utc

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TIMEOUT = 25

# Seed for 2026-11-12 only, used when a live fetch fails on the first run.
# Values gathered 2026-11-12 22:14–22:25 Asia/Bangkok.
SEED_2026_11_12 = {
    "btc_price_usd": 71371.0,
    "btc_mcap_usd": 1435348215099.0,
    "total_oi_usd": 51020000000.0,
    "oi_mcap_pct": 3.56,
    "okx_oi_usd": 2641272051.36,
    "okx_oi_btc": 36920.8841,
    "okx_funding_8h": 0.0000690592722751,
    "okx_ls_account": 3.09,
    "hl_oi_usd": 2776075857.62,
    "hl_funding_raw": 0.0000088091,
    "hl_funding_period": "1h",
    "hl_funding_8h_equiv": 0.0000704728,
    "liq_24h_usd": 304560000.0,
    "liq_long_usd": 265730000.0,
    "liq_long_share_pct": 87.0,
    "elr": 0.249,
    "elr_asof": "2026-11-09",
}
SEED_NOTES = (
    "seed 2026-11-12: CoinGecko/OKX/HL live around 22:20 BKK; "
    "CoinGlass page 22:14–22:31 BKK (OI $51.02B, 3.56%, liq $304.56M, longs 87%); "
    "ELR 0.249 as-of 2026-11-09 from CryptoQuant XWIN insight"
)

COLS = [
    "date",
    "row_type",
    "btc_price_usd",
    "btc_mcap_usd",
    "total_oi_usd",
    "oi_mcap_pct",
    "okx_oi_usd",
    "okx_oi_btc",
    "okx_funding_8h",
    "okx_funding_8h_avg",
    "okx_ls_account",
    "hl_oi_usd",
    "hl_funding_raw",
    "hl_funding_period",
    "hl_funding_8h_equiv",
    "liq_24h_usd",
    "liq_long_usd",
    "liq_long_share_pct",
    "elr",
    "elr_asof",
    "fetched_at",
    "notes",
]

NUMERIC = [c for c in COLS if c not in ("date", "row_type", "hl_funding_period", "elr_asof", "fetched_at", "notes")]


def now_bkk() -> datetime:
    return datetime.now(BKK)


def today_bkk() -> str:
    return now_bkk().strftime("%Y-%m-%d")


def parse_ts(ts) -> datetime:
    t = int(float(ts))
    if t > 1e12:
        t = t / 1000
    return datetime.fromtimestamp(t, tz=UTC)


def okx_daily_date(ts) -> str:
    """Assign OKX 1D bars stamped 00:00 UTC+8 to that UTC+8 calendar date."""
    return parse_ts(ts).astimezone(CST).strftime("%Y-%m-%d")


def bkk_date(ts) -> str:
    return parse_ts(ts).astimezone(BKK).strftime("%Y-%m-%d")


def http_get(url: str, headers: dict | None = None) -> bytes:
    h = {"User-Agent": UA, "Accept": "application/json,text/html;q=0.9"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def http_post_json(url: str, payload: dict) -> bytes:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def try_json(fn, retries=2, pause=1.2):
    last = None
    for i in range(retries):
        try:
            return fn(), None
        except Exception as e:
            last = e
            if i + 1 < retries:
                time.sleep(pause)
    return None, last


def fmt(v, kind="generic"):
    if v is None or v == "":
        return ""
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    if not np.isfinite(x):
        return ""
    if kind == "funding":
        return f"{x:.12f}".rstrip("0").rstrip(".")
    if kind == "pct":
        return f"{x:.6g}"
    if kind == "price":
        return f"{x:.4f}"
    if kind == "intish":
        return f"{x:.4f}"
    return f"{x:.10g}"


def to_float(v):
    if v is None or v == "":
        return None
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None


# ---------- fetchers ----------

def fetch_coingecko_live():
    raw = http_get(
        "https://api.coingecko.com/api/v3/coins/bitcoin"
        "?localization=false&tickers=false&community_data=false&developer_data=false"
    )
    m = json.loads(raw)["market_data"]
    return {
        "btc_price_usd": float(m["current_price"]["usd"]),
        "btc_mcap_usd": float(m["market_cap"]["usd"]),
    }


def fetch_coingecko_history(days: int):
    raw = http_get(
        f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        f"?vs_currency=usd&days={days}&interval=daily"
    )
    data = json.loads(raw)
    by_date = {}
    for ts, px in data.get("prices") or []:
        dt = parse_ts(ts)
        if dt.hour != 0 or dt.minute != 0:
            continue  # skip incomplete "now" point
        d = dt.astimezone(UTC).strftime("%Y-%m-%d")
        by_date.setdefault(d, {})["btc_price_usd"] = float(px)
    for ts, cap in data.get("market_caps") or []:
        dt = parse_ts(ts)
        if dt.hour != 0 or dt.minute != 0:
            continue
        d = dt.astimezone(UTC).strftime("%Y-%m-%d")
        by_date.setdefault(d, {})["btc_mcap_usd"] = float(cap)
    return by_date


def fetch_okx_live():
    out = {}
    oi = json.loads(http_get("https://www.okx.com/api/v5/public/open-interest?instId=BTC-USDT-SWAP"))
    row = (oi.get("data") or [None])[0]
    if not row:
        raise RuntimeError(f"OKX OI empty: {oi}")
    out["okx_oi_usd"] = float(row["oiUsd"])
    out["okx_oi_btc"] = float(row["oiCcy"])
    fr = json.loads(http_get("https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP"))
    frow = (fr.get("data") or [None])[0]
    if not frow:
        raise RuntimeError(f"OKX funding empty: {fr}")
    out["okx_funding_8h"] = float(frow["fundingRate"])
    return out


def fetch_okx_oi_history():
    raw = http_get(
        "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history"
        "?instId=BTC-USDT-SWAP&period=1D"
    )
    data = json.loads(raw).get("data") or []
    by_date = {}
    for x in data:
        # [ts, oi_contracts, oi_btc, oi_usd]
        d = okx_daily_date(x[0])
        by_date[d] = {"okx_oi_btc": float(x[2]), "okx_oi_usd": float(x[3])}
    return by_date


def fetch_okx_ls_history():
    raw = http_get(
        "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-account-ratio"
        "?ccy=BTC&period=1D"
    )
    data = json.loads(raw).get("data") or []
    by_date = {}
    for x in data:
        d = okx_daily_date(x[0])
        by_date[d] = {"okx_ls_account": float(x[1])}
    return by_date


def fetch_okx_funding_history():
    raw = http_get(
        "https://www.okx.com/api/v5/public/funding-rate-history?instId=BTC-USDT-SWAP&limit=100"
    )
    data = json.loads(raw).get("data") or []
    buckets = {}
    for x in data:
        d = bkk_date(x["fundingTime"])
        buckets.setdefault(d, []).append(float(x["fundingRate"]))
    by_date = {}
    for d, vals in buckets.items():
        # API returns newest first; after grouping, last settled that day is vals[0]
        # Use chronological last = first appended if we reverse... we appended newest first,
        # so vals[0] is the latest settlement that Bangkok date.
        by_date[d] = {
            "okx_funding_8h": vals[0],
            "okx_funding_8h_avg": sum(vals) / len(vals),
        }
    return by_date


def fetch_hyperliquid():
    raw = http_post_json("https://api.hyperliquid.xyz/info", {"type": "metaAndAssetCtxs"})
    meta, ctxs = json.loads(raw)
    for i, u in enumerate(meta.get("universe") or []):
        if u.get("name") == "BTC":
            c = ctxs[i]
            oi = float(c["openInterest"])
            px = float(c.get("markPx") or c.get("midPx") or 0)
            fund = float(c["funding"])
            # HL funding is 1-hour; convert to an 8h equivalent for comparison.
            return {
                "hl_oi_usd": oi * px,
                "hl_funding_raw": fund,
                "hl_funding_period": "1h",
                "hl_funding_8h_equiv": fund * 8.0,
            }
    raise RuntimeError("Hyperliquid BTC not found")


def fetch_coinglass():
    """Parse the public CoinGlass BTC page snap. Fragile; may break if the page changes."""
    html = http_get("https://www.coinglass.com/currencies/BTC").decode("utf-8", "ignore")
    start = html.find('id="__NEXT_DATA__"')
    if start < 0:
        raise RuntimeError("CoinGlass page missing __NEXT_DATA__")
    j = html.find(">", start) + 1
    end = html.find("</script>", j)
    snap = json.loads(html[j:end])["props"]["pageProps"]["snap"]
    oi = float(snap["openInterest"])
    mcap = float(snap["marketCap"])
    liq = snap.get("liquidation24h") or {}
    long_usd = float(liq.get("long") or 0)
    short_usd = float(liq.get("short") or 0)
    total_liq = long_usd + short_usd
    share = (long_usd / total_liq * 100.0) if total_liq else None
    # fundingRate on the page is already in percent (e.g. 0.0077 meaning 0.0077%/8h)
    return {
        "total_oi_usd": oi,
        "coinglass_mcap_usd": mcap,
        "oi_mcap_pct": (oi / mcap * 100.0) if mcap else None,
        "liq_24h_usd": total_liq if total_liq else None,
        "liq_long_usd": long_usd if total_liq else None,
        "liq_long_share_pct": share,
        "coinglass_update": snap.get("updateTime"),
    }


# ---------- csv ----------

def empty_row(date: str) -> dict:
    r = {c: "" for c in COLS}
    r["date"] = date
    return r


def load_csv(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("date"):
                # keep only known columns, preserve extras in notes if needed
                r = empty_row(row["date"])
                for c in COLS:
                    if c in row and row[c] is not None:
                        r[c] = row[c]
                out[row["date"]] = r
    return out


def save_csv(path: Path, rows: dict[str, dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = [rows[d] for d in sorted(rows)]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        for r in ordered:
            w.writerow({c: r.get(c, "") for c in COLS})


def merge_notes(*parts: str) -> str:
    seen = []
    for p in parts:
        p = (p or "").strip()
        if p and p not in seen:
            seen.append(p)
    return " | ".join(seen)


def upsert(store: dict, date: str, fields: dict, row_type: str, notes: str, fetched_at: str = ""):
    old = store.get(date) or empty_row(date)
    new = dict(old)
    for k, v in fields.items():
        if k not in COLS or k in ("date", "row_type", "notes", "fetched_at"):
            continue
        kind = "funding" if "funding" in k or k == "elr" else "pct" if "pct" in k or k == "okx_ls_account" else "price" if "price" in k else "generic"
        s = fmt(v, kind)
        if s != "":
            new[k] = s
    if old.get("row_type") == "live" and row_type == "backfill":
        new["row_type"] = "live"
    else:
        new["row_type"] = row_type
    new["date"] = date
    new["notes"] = merge_notes(old.get("notes", ""), notes)
    if row_type == "live" and fetched_at:
        new["fetched_at"] = fetched_at
    elif not new.get("fetched_at") and fetched_at:
        new["fetched_at"] = fetched_at
    store[date] = new


def recompute_oi_mcap(row: dict):
    oi = to_float(row.get("total_oi_usd"))
    cap = to_float(row.get("btc_mcap_usd"))
    if oi and cap:
        row["oi_mcap_pct"] = fmt(oi / cap * 100.0, "pct")


# ---------- ELR sidecar ----------

def load_elr() -> dict:
    if ELR_PATH.exists():
        return json.loads(ELR_PATH.read_text())
    return {}


def save_elr(elr, asof, source=""):
    payload = {
        "elr": float(elr),
        "elr_asof": asof,
        "source": source
        or "CryptoQuant (manual). Update this file or pass --elr / --elr-asof.",
        "updated_at": now_bkk().strftime("%Y-%m-%d %H:%M Asia/Bangkok"),
    }
    ELR_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    return payload


# ---------- plot ----------

def setup_font():
    path = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    if path.exists():
        font_manager.fontManager.addfont(str(path))
        # The TTC contains several CJK families; pick SC if registered.
        names = {f.name for f in font_manager.fontManager.ttflist}
        for name in ("Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans CJK TC"):
            if name in names:
                plt.rcParams["font.family"] = name
                break
        else:
            plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.25
    plt.rcParams["grid.linestyle"] = "--"


def series(rows, col):
    xs, ys = [], []
    for d in sorted(rows):
        v = to_float(rows[d].get(col))
        if v is None:
            continue
        xs.append(datetime.strptime(d, "%Y-%m-%d"))
        ys.append(v)
    return xs, ys


def style_axis(ax, ylabel):
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_minor_locator(AutoMinorLocator(3))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot(rows: dict, out_path: Path, fetch_str: str):
    setup_font()
    fig, axes = plt.subplots(6, 1, figsize=(11.2, 15.2), sharex=False)
    fig.suptitle("BTC 杠杆与踩踏观察指标（日线）", fontsize=15, fontweight="bold", y=0.995)
    fig.text(
        0.5,
        0.972,
        f"获取于 {fetch_str}（曼谷时间，UTC+7）  ·  虚线是历史粗略参考，不是规则或阈值",
        ha="center",
        fontsize=9,
        color="#444",
    )

    # 1. OI / mcap
    ax = axes[0]
    x, y = series(rows, "oi_mcap_pct")
    if x:
        ax.plot(x, y, "o-", color="#1f4e79", lw=1.6, ms=5, label="全市场 OI / BTC 市值")
        ax.annotate(f"{y[-1]:.2f}%", (x[-1], y[-1]), textcoords="offset points", xytext=(6, 6), fontsize=8, color="#1f4e79")
    ax.axhline(4.0, color="#c0392b", ls="--", lw=1.1, label="4% 粗略参考")
    ax.set_ylim(0, max(5.0, (max(y) * 1.25 if y else 5)))
    style_axis(ax, "OI / 市值（%）")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    if len(x) <= 1:
        ax.text(0.01, 0.08, "全市场 OI 从今天起记（CoinGlass 无免费历史接口，未回填）",
                transform=ax.transAxes, ha="left", va="bottom", fontsize=7.5, color="#666")

    # 2. funding
    ax = axes[1]
    x, y = series(rows, "okx_funding_8h")
    ypct = [v * 100 for v in y]
    if x:
        ax.plot(x, ypct, "o-", color="#0b6e4f", lw=1.6, ms=4, label="OKX 资金费率（每8小时）")
    xh, yh = series(rows, "hl_funding_8h_equiv")
    if xh:
        ax.plot(xh, [v * 100 for v in yh], "s--", color="#2a9d8f", lw=1.1, ms=4, label="Hyperliquid 折合8小时（1小时费率×8）")
    style_axis(ax, "资金费率（%/8h）")
    data_max = max(ypct + [v * 100 for v in yh], default=0.01)
    data_min = min(ypct + [v * 100 for v in yh], default=0)
    # If values sit far below 0.05%/8h, zoom to the series so daily moves are visible
    # and state that the 0.05% rough reference is above the frame.
    if data_max < 0.025:
        lo = min(-0.005, data_min * 1.4 if data_min < 0 else -0.002)
        hi = max(0.02, data_max * 1.8)
        ax.set_ylim(lo, hi)
        ax.axhline(0.05, color="#c0392b", ls="--", lw=1.1, label="0.05%/8h 粗略参考（在本图上方）")
        ax.text(
            0.99, 0.95,
            f"0.05%/8h 粗略参考在刻度上方（当前约 {ypct[-1]:.3f}%，距离较远）" if ypct else "0.05%/8h 粗略参考在刻度上方",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color="#c0392b",
        )
    else:
        ax.axhline(0.05, color="#c0392b", ls="--", lw=1.1, label="0.05%/8h 粗略参考")
        ax.set_ylim(min(-0.01, data_min * 1.4 if data_min < 0 else -0.005), max(0.06, data_max * 1.15))
    ax.legend(loc="upper left", fontsize=8, frameon=False)

    # 3. long/short
    ax = axes[2]
    x, y = series(rows, "okx_ls_account")
    if x:
        ax.plot(x, y, "o-", color="#6a4c93", lw=1.6, ms=4, label="OKX BTC 账户多空比")
        ax.annotate(f"{y[-1]:.2f}", (x[-1], y[-1]), textcoords="offset points", xytext=(6, 6), fontsize=8, color="#6a4c93")
    ax.axhline(1.0, color="#888", ls=":", lw=1.0, label="1.0（多空账户一样多）")
    style_axis(ax, "账户多空比")
    ax.legend(loc="upper left", fontsize=8, frameon=False)

    # 4. OKX OI BTC vs price
    ax = axes[3]
    xo, yo = series(rows, "okx_oi_btc")
    if xo:
        ax.plot(xo, yo, "o-", color="#1f4e79", lw=1.6, ms=4, label="OKX BTC 永续持仓（币）")
    ax.set_ylabel("OKX 持仓（BTC）", fontsize=9)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax2 = ax.twinx()
    xp, yp = series(rows, "btc_price_usd")
    if xp:
        ax2.plot(xp, yp, "-", color="#e07a3d", lw=1.4, alpha=0.9, label="BTC 价格")
    ax2.set_ylabel("BTC 价格（美元）", fontsize=9, color="#e07a3d")
    ax2.tick_params(labelsize=8, colors="#e07a3d")
    ax2.spines["top"].set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8, frameon=False)
    ax.grid(True, alpha=0.25, linestyle="--")

    # 5. liquidations
    ax = axes[4]
    x, y = series(rows, "liq_24h_usd")
    xl, yl = series(rows, "liq_long_usd")
    if x:
        millions = [v / 1e6 for v in y]
        ax.bar(x, millions, width=0.6, color="#7b2d26", alpha=0.8, label="24h 清算总额")
        if xl:
            # align long bars on same dates
            long_map = {a: b for a, b in zip(xl, yl)}
            longs = [long_map.get(a, 0) / 1e6 for a in x]
            ax.bar(x, longs, width=0.6, color="#c0392b", alpha=0.95, label="其中多头")
        last_share = None
        last_date = max(x)
        last_key = last_date.strftime("%Y-%m-%d")
        if last_key in rows:
            last_share = to_float(rows[last_key].get("liq_long_share_pct"))
        last_val = millions[x.index(last_date)]
        share_txt = f"{last_share:.0f}% 多头" if last_share is not None else ""
        ax.annotate(
            f"${last_val:.0f}M\n{share_txt}",
            (last_date, last_val),
            textcoords="offset points",
            xytext=(-52, 6),
            fontsize=8,
            ha="right",
            va="bottom",
        )
        # room for the label above the bar
        ax.set_ylim(0, max(millions) * 1.25)
    style_axis(ax, "24h 清算（百万美元）")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    if len(x) <= 1:
        ax.text(0.50, 0.95, "清算从今天起记，历史未回填", transform=ax.transAxes,
                ha="center", va="top", fontsize=7.5, color="#666")

    # 6. ELR (manual, sparse)
    ax = axes[5]
    x, y = series(rows, "elr")
    if x:
        ax.plot(x, y, "D", color="#1b4965", ms=8, label="ELR 手工值（有更新日期才记）")
        for a, b in zip(x, y):
            ax.annotate(f"{b:.3f}", (a, b), textcoords="offset points", xytext=(6, 8), fontsize=8)
    ax.axhline(0.28, color="#c0392b", ls="--", lw=1.1, label="0.28 粗略参考（约 2025-10-06）")
    style_axis(ax, "估算杠杆率 ELR")
    ax.set_ylim(0, max(0.35, (max(y) * 1.3 if y else 0.35)))
    ax.set_xlabel("日期（亚洲/曼谷）", fontsize=9)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.set_title("CryptoQuant ELR 需手工更新（--elr / elr_manual.json），不是每日自动接口", fontsize=8, loc="right", color="#666", pad=2)

    # Align x range across panels
    all_dates = []
    for r in rows.values():
        all_dates.append(datetime.strptime(r["date"], "%Y-%m-%d"))
    if all_dates:
        xmin = min(all_dates) - timedelta(days=1)
        xmax = max(all_dates) + timedelta(days=1)
        for a in axes:
            a.set_xlim(xmin, xmax)

    footer = (
        "来源：CoinGecko，OKX 公开接口，Hyperliquid 公开接口，CoinGlass 公开页面（若抓取成功），"
        "CryptoQuant ELR 为手工录入。  以上只是信息整理，不构成投资建议。"
    )
    fig.text(0.5, 0.006, footer, ha="center", va="bottom", fontsize=7.5, color="#333", wrap=True)
    fig.tight_layout(rect=(0.03, 0.025, 0.98, 0.965))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


# ---------- main ----------

def main(argv=None):
    p = argparse.ArgumentParser(description="Collect daily BTC leverage metrics and chart them")
    p.add_argument("--days", type=int, default=30, help="backfill window in days")
    p.add_argument("--no-backfill", action="store_true")
    p.add_argument("--plot-only", action="store_true")
    p.add_argument("--elr", type=float, default=None)
    p.add_argument("--elr-asof", default=None, help="YYYY-MM-DD")
    p.add_argument("--elr-source", default="")
    p.add_argument(
        "--data-dir",
        default=None,
        help="Directory for history.csv, charts, and elr_manual.json (or set LEVERAGE_DATA_DIR)",
    )
    args = p.parse_args(argv)

    global DIR, CSV_PATH, ELR_PATH
    if args.data_dir:
        DIR = Path(args.data_dir).expanduser().resolve()
        CSV_PATH = DIR / "history.csv"
        ELR_PATH = DIR / "elr_manual.json"

    DIR.mkdir(parents=True, exist_ok=True)
    today = today_bkk()
    fetched_at = now_bkk().strftime("%Y-%m-%d %H:%M Asia/Bangkok")
    store = load_csv(CSV_PATH)
    errors = []

    if not args.plot_only:
        # manual ELR
        if args.elr is not None:
            asof = args.elr_asof or today
            save_elr(args.elr, asof, args.elr_source)
        elr_info = load_elr()
        if not elr_info and today == "2026-11-12":
            elr_info = save_elr(
                SEED_2026_11_12["elr"],
                SEED_2026_11_12["elr_asof"],
                "CryptoQuant insight by XWIN dated 2026-11-09 (not a live API print)",
            )

        if not args.no_backfill:
            # CoinGecko history
            hist, err = try_json(lambda: fetch_coingecko_history(args.days + 2))
            if err:
                errors.append(f"coingecko_history: {err}")
            else:
                start = (now_bkk().date() - timedelta(days=args.days)).strftime("%Y-%m-%d")
                for d, fields in hist.items():
                    if d < start or d >= today:
                        continue
                    # CoinGecko interval=daily points are 00:00 UTC (morning in Bangkok),
                    # not a Bangkok close. Do not overwrite a live same-day snapshot.
                    existing = store.get(d) or {}
                    if existing.get("row_type") == "live":
                        continue
                    upsert(store, d, fields, "backfill", "backfill: CoinGecko daily")

            # OKX histories
            for name, fn, tag in (
                ("okx_oi_history", fetch_okx_oi_history, "backfill: OKX OI 1D"),
                ("okx_ls_history", fetch_okx_ls_history, "backfill: OKX account long/short 1D"),
                ("okx_funding_history", fetch_okx_funding_history, "backfill: OKX funding history"),
            ):
                data, err = try_json(fn)
                if err:
                    errors.append(f"{name}: {err}")
                    continue
                start = (now_bkk().date() - timedelta(days=args.days)).strftime("%Y-%m-%d")
                for d, fields in data.items():
                    if d < start or d > today:
                        continue
                    # For today, only fill LS / funding avg if live later overwrites OI/funding.
                    upsert(store, d, fields, "backfill" if d < today else "live" if d == today else "backfill", tag)

        # live fetches
        live = {}
        src_ok = []
        src_fail = []

        cg, err = try_json(fetch_coingecko_live)
        if err:
            src_fail.append(f"CoinGecko live ({err})")
        else:
            live.update(cg)
            src_ok.append("CoinGecko")

        okx, err = try_json(fetch_okx_live)
        if err:
            src_fail.append(f"OKX live ({err})")
        else:
            live.update(okx)
            src_ok.append("OKX")

        # latest LS for today if the daily bar exists (already upserted) or from a fresh pull
        ls, err = try_json(fetch_okx_ls_history)
        if not err and today in ls:
            live["okx_ls_account"] = ls[today]["okx_ls_account"]
        elif not err:
            # no bar mapped to today yet; do not invent. Leave previous/empty.
            src_fail.append("OKX LS today bar not published yet")

        hl, err = try_json(fetch_hyperliquid)
        if err:
            src_fail.append(f"Hyperliquid ({err})")
        else:
            live.update(hl)
            src_ok.append("Hyperliquid")

        glass, err = try_json(fetch_coinglass)
        if err:
            src_fail.append(f"CoinGlass ({err})")
        else:
            live["total_oi_usd"] = glass["total_oi_usd"]
            live["liq_24h_usd"] = glass["liq_24h_usd"]
            live["liq_long_usd"] = glass["liq_long_usd"]
            live["liq_long_share_pct"] = glass["liq_long_share_pct"]
            # Prefer CoinGecko mcap for oi/mcap if we have it; else CoinGlass mcap.
            cap = live.get("btc_mcap_usd") or glass.get("coinglass_mcap_usd")
            if cap and glass["total_oi_usd"]:
                live["oi_mcap_pct"] = glass["total_oi_usd"] / cap * 100.0
            src_ok.append("CoinGlass page")

        # Seed fallbacks only for today's first run if a fetch failed
        seeded = []
        if today == "2026-11-12":
            for k, v in SEED_2026_11_12.items():
                if k in ("elr", "elr_asof"):
                    continue
                if live.get(k) is None:
                    live[k] = v
                    seeded.append(k)
        if seeded:
            src_fail.append("seeded: " + ",".join(seeded))

        if elr_info.get("elr") is not None:
            live["elr"] = float(elr_info["elr"])
            live["elr_asof"] = elr_info.get("elr_asof", "")

        notes = "live: " + (", ".join(src_ok) if src_ok else "no live source")
        if src_fail:
            notes += " | missing/failed: " + "; ".join(src_fail)
        if seeded:
            notes += " | " + SEED_NOTES
        if elr_info:
            notes += f" | ELR {elr_info.get('elr')} as-of {elr_info.get('elr_asof')} ({elr_info.get('source','')})"

        upsert(store, today, live, "live", notes, fetched_at)
        if store[today].get("total_oi_usd") and store[today].get("btc_mcap_usd"):
            recompute_oi_mcap(store[today])

        # Also recompute oi/mcap on any row that has both
        for r in store.values():
            if r.get("total_oi_usd") and r.get("btc_mcap_usd") and not r.get("oi_mcap_pct"):
                recompute_oi_mcap(r)

        save_csv(CSV_PATH, store)

        # write a small run log
        meta = {
            "fetched_at": fetched_at,
            "today": today,
            "sources_ok": src_ok,
            "sources_fail": src_fail,
            "errors": [str(e) for e in errors],
            "rows": len(store),
            "csv": str(CSV_PATH),
        }
        (DIR / "last_run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

    if not store:
        store = load_csv(CSV_PATH)
    png = DIR / f"leverage_{today}.png"
    plot(store, png, fetched_at if not args.plot_only else now_bkk().strftime("%Y-%m-%d %H:%M Asia/Bangkok"))

    # stdout summary for the routine / parent
    row = store.get(today, {})
    print(f"csv={CSV_PATH}")
    print(f"png={png}")
    print(f"today={today} row_type={row.get('row_type')} fetched_at={row.get('fetched_at')}")
    for c in (
        "btc_price_usd",
        "btc_mcap_usd",
        "total_oi_usd",
        "oi_mcap_pct",
        "okx_oi_usd",
        "okx_oi_btc",
        "okx_funding_8h",
        "okx_ls_account",
        "hl_oi_usd",
        "hl_funding_8h_equiv",
        "liq_24h_usd",
        "liq_long_share_pct",
        "elr",
        "elr_asof",
    ):
        print(f"  {c}={row.get(c,'')}")
    print(f"notes={row.get('notes','')}")
    if errors:
        print("backfill_errors:", errors, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
