#!/usr/bin/env python3
"""Monitor whether a crypto perpetual-futures leverage flush looks complete.

Fetches public OKX and Binance data, scores four conditions (account long/short
ratio, open-interest drawdown from the running high, OKX top-trader position
ratio, OKX short-vs-long liquidations), updates a state file, and prints one
JSON object. Notify only when a condition upgrades or falls from "met".

No API keys. Not investment advice.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests

# ---------- endpoints ----------
OKX_TICKERS = "https://www.okx.com/api/v5/market/tickers"
OKX_ACCOUNT_RATIO = "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-account-ratio"
OKX_OI_HISTORY = "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history"
# Current OKX docs require instId (not ccy) on the top-trader position-ratio endpoint.
OKX_TOP_POS = "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-position-ratio-contract-top-trader"
OKX_LIQ = "https://www.okx.com/api/v5/public/liquidation-orders"
OKX_FUNDING = "https://www.okx.com/api/v5/public/funding-rate"

# fapi.binance.com often returns HTTP 451 (geo block). www.binance.com serves
# the same public futures data paths and is the fallback.
BN_ACCOUNT_RATIO = "/futures/data/globalLongShortAccountRatio"
BN_OI_HIST = "/futures/data/openInterestHist"
BN_TOP_POS = "/futures/data/topLongShortPositionRatio"
BN_TICKER = "/fapi/v1/ticker/price"
BN_PREMIUM = "/fapi/v1/premiumIndex"

# Contract value (sz multiplier) for OKX USDT-margined swaps.
CTVAL = {"BTC": 0.01, "ETH": 0.1}

# Default thresholds from the live 30-minute watch.
THRESH = {
    "account_near": 2.3,
    "account_met": 2.0,
    "oi_near": 0.15,
    "oi_met": 0.20,
    "okx_top_near": 0.95,
    "okx_top_met": 1.0,
    "bn_top_flag": 1.5,
    "liq_near": 0.50,
    "liq_met": 1.00,
}

RANK = {"none": 0, "near": 1, "met": 2}
STATUS_NAMES = ("none", "near", "met")
CONDITIONS = ("account_ratio", "oi_drop", "top_trader_position", "short_liquidations")
DISCLAIMER = "以上只是信息整理，不构成投资建议"

UA = "crypto-deleverage-watch/1.0"


# ---------- HTTP ----------
def http_get(session: requests.Session, url: str, params=None, timeout=25, retries=3):
    last = None
    for i in range(retries):
        try:
            r = session.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last = e
            time.sleep(0.4 * (i + 1))
    raise last


def get_binance(session: requests.Session, path: str, params=None, timeout=25):
    """Try fapi.binance.com first, then www.binance.com (451 geo-block fallback)."""
    urls = [f"https://fapi.binance.com{path}", f"https://www.binance.com{path}"]
    last = None
    used = None
    for url in urls:
        try:
            data = http_get(session, url, params=params, timeout=timeout)
            return data, url
        except Exception as e:
            last = e
            continue
    raise last


# ---------- helpers ----------
def iso(ms: int, tz: dt.tzinfo) -> str:
    return dt.datetime.fromtimestamp(int(ms) / 1000, tz).isoformat(timespec="seconds")


def parse_window_start(raw: str | None, now: dt.datetime, tz: dt.tzinfo) -> dt.datetime:
    if not raw:
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    raw = raw.strip()
    if len(raw) == 10:
        return dt.datetime.fromisoformat(raw).replace(tzinfo=tz)
    start = dt.datetime.fromisoformat(raw)
    if start.tzinfo is None:
        start = start.replace(tzinfo=tz)
    return start


def worse_status(*statuses: str) -> str:
    """Return the most flushed of the given statuses (met > near > none)."""
    best = "none"
    for s in statuses:
        if s in RANK and RANK[s] > RANK[best]:
            best = s
    return best


def account_status(ratio: float | None, near: float, met: float) -> str:
    if ratio is None:
        return "unknown"
    # Lower account long/short ratio = more flushed longs.
    if ratio < met:
        return "met"
    if ratio < near:
        return "near"
    return "none"


def oi_status(drop: float | None, near: float, met: float) -> str:
    if drop is None:
        return "unknown"
    if drop >= met:
        return "met"
    if drop >= near:
        return "near"
    return "none"


def okx_top_status(ratio: float | None, near: float, met: float) -> str:
    """OKX top-trader notional long/short. Default: near >= 0.95, met >= 1.0.

    The live routine used this upward threshold because OKX top traders were
    already net short (< 1). It is a neutralization / cover signal, not a
    'crowded long' signal. Binance is scored separately.
    """
    if ratio is None:
        return "unknown"
    if ratio >= met:
        return "met"
    if ratio >= near:
        return "near"
    return "none"


def side_of(row: dict) -> str:
    ps = row.get("posSide", "")
    if ps == "long":
        return "long"
    if ps == "short":
        return "short"
    if ps == "net" and row.get("side") == "sell":
        return "long"
    return "short"


def should_notify(old: str, new: str) -> bool:
    if new not in RANK or old not in RANK:
        return new != old and new != "unknown"
    if RANK[new] > RANK[old]:
        return True
    if old == "met" and new != "met":
        return True
    return False


def empty_status(coins: list[str]) -> dict:
    return {name: {c: "none" for c in coins} for name in CONDITIONS}


# ---------- fetchers ----------
def fetch_all(session: requests.Session, coins: list[str], start_ms: int, now_ms: int, tz: dt.tzinfo, errors: list[str]) -> dict:
    prices: dict[str, float] = {}
    funding: dict[str, Any] = {}
    okx_ratio, okx_ratio_ts = {}, {}
    bn_ratio, bn_ratio_ts = {}, {}
    okx_oi, okx_oi_ts, okx_oi_high, okx_oi_high_ts = {}, {}, {}, {}
    bn_oi, bn_oi_ts, bn_oi_high, bn_oi_high_ts = {}, {}, {}, {}
    okx_top, okx_top_ts = {}, {}
    bn_top, bn_top_ts = {}, {}
    liq: dict[str, Any] = {}
    bn_host_note = None

    inst = {c: f"{c}-USDT-SWAP" for c in coins}
    bn_sym = {c: f"{c}USDT" for c in coins}

    try:
        payload = http_get(session, OKX_TICKERS, {"instType": "SWAP"})
        data = {x["instId"]: x for x in payload.get("data", [])}
        for c in coins:
            row = data.get(inst[c])
            if row:
                prices[f"OKX_{c}"] = float(row["last"])
    except Exception as e:
        errors.append(f"OKX tickers failed: {e}")

    for c in coins:
        try:
            data, url = get_binance(session, BN_TICKER, {"symbol": bn_sym[c]})
            prices[f"BN_{c}"] = float(data["price"])
            if "www.binance.com" in url:
                bn_host_note = "fapi.binance.com returned an error or 451 geo-block; used www.binance.com public futures data endpoints"
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"Binance ticker {c} failed: {e}")

    for c in coins:
        try:
            payload = http_get(session, OKX_ACCOUNT_RATIO, {"ccy": c, "period": "5m"})
            if payload.get("code") != "0" or not payload.get("data"):
                errors.append(f"OKX account ratio {c} failed: code={payload.get('code')} msg={payload.get('msg')}")
                continue
            row = payload["data"][0]
            if isinstance(row, list):
                okx_ratio_ts[c] = int(row[0])
                okx_ratio[c] = float(row[1])
            else:
                okx_ratio_ts[c] = int(row.get("ts") or row.get("timestamp"))
                okx_ratio[c] = float(row.get("ratio") or row.get("longShortRatio"))
            time.sleep(0.15)
        except Exception as e:
            errors.append(f"OKX account ratio {c} failed: {e}")

    for c in coins:
        try:
            data, url = get_binance(session, BN_ACCOUNT_RATIO, {"symbol": bn_sym[c], "period": "5m", "limit": 30})
            if "www.binance.com" in url:
                bn_host_note = "fapi.binance.com returned an error or 451 geo-block; used www.binance.com public futures data endpoints"
            if not data:
                errors.append(f"Binance account ratio {c} empty")
                continue
            row = data[-1] if isinstance(data, list) else data
            bn_ratio[c] = float(row["longShortRatio"])
            bn_ratio_ts[c] = int(row["timestamp"])
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"Binance account ratio {c} failed: {e}")

    for c in coins:
        try:
            rows = []
            end = None
            pages = 0
            while pages < 20:
                params = {"instId": inst[c], "period": "5m", "limit": "100"}
                if end:
                    params["end"] = str(end)
                payload = http_get(session, OKX_OI_HISTORY, params)
                if payload.get("code") != "0" or not payload.get("data"):
                    if pages == 0:
                        errors.append(f"OKX OI {c} failed: code={payload.get('code')} msg={payload.get('msg')}")
                    break
                batch = payload["data"]
                rows.extend(batch)
                last = batch[-1]
                last_ts = int(last[0] if isinstance(last, list) else last["ts"])
                pages += 1
                if last_ts <= start_ms:
                    break
                end = last_ts - 1
                time.sleep(0.15)
            parsed = []
            for row in rows:
                if isinstance(row, list):
                    ts, _oi, oi_ccy = int(row[0]), float(row[1]), float(row[2])
                else:
                    ts = int(row["ts"])
                    oi_ccy = float(row.get("oiCcy") or row.get("oi"))
                if ts >= start_ms:
                    parsed.append((ts, oi_ccy))
            if not parsed:
                errors.append(f"OKX OI {c} has no bars since window start")
                continue
            by_ts = {ts: v for ts, v in parsed}
            parsed = sorted(by_ts.items())
            cur_ts, cur = max(parsed, key=lambda x: x[0])
            hi_ts, hi = max(parsed, key=lambda x: x[1])
            okx_oi[c] = cur
            okx_oi_ts[c] = cur_ts
            okx_oi_high[c] = hi
            okx_oi_high_ts[c] = hi_ts
        except Exception as e:
            errors.append(f"OKX OI {c} failed: {e}")

    for c in coins:
        try:
            data, url = get_binance(session, BN_OI_HIST, {"symbol": bn_sym[c], "period": "5m", "limit": 500})
            if "www.binance.com" in url:
                bn_host_note = "fapi.binance.com returned an error or 451 geo-block; used www.binance.com public futures data endpoints"
            if not data:
                errors.append(f"Binance OI {c} empty")
                continue
            parsed = []
            for row in data:
                ts = int(row["timestamp"])
                if ts >= start_ms:
                    # sumOpenInterest is coin-denominated on USDT-M futures.
                    parsed.append((ts, float(row["sumOpenInterest"])))
            if not parsed:
                errors.append(f"Binance OI {c} has no bars since window start")
                continue
            cur_ts, cur = max(parsed, key=lambda x: x[0])
            hi_ts, hi = max(parsed, key=lambda x: x[1])
            bn_oi[c] = cur
            bn_oi_ts[c] = cur_ts
            bn_oi_high[c] = hi
            bn_oi_high_ts[c] = hi_ts
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"Binance OI {c} failed: {e}")

    for c in coins:
        try:
            payload = http_get(session, OKX_TOP_POS, {"instId": inst[c], "period": "5m"})
            if payload.get("code") != "0" or not payload.get("data"):
                errors.append(f"OKX top-trader position ratio {c} failed: code={payload.get('code')} msg={payload.get('msg')}")
                continue
            row = payload["data"][0]
            if isinstance(row, list):
                okx_top_ts[c] = int(row[0])
                okx_top[c] = float(row[1])
            else:
                okx_top_ts[c] = int(row.get("ts"))
                okx_top[c] = float(row.get("ratio") or row.get("longShortRatio"))
            time.sleep(0.15)
        except Exception as e:
            errors.append(f"OKX top-trader position ratio {c} failed: {e}")

    for c in coins:
        try:
            data, url = get_binance(session, BN_TOP_POS, {"symbol": bn_sym[c], "period": "5m", "limit": 30})
            if "www.binance.com" in url:
                bn_host_note = "fapi.binance.com returned an error or 451 geo-block; used www.binance.com public futures data endpoints"
            if not data:
                errors.append(f"Binance top-trader position ratio {c} empty")
                continue
            row = data[-1]
            bn_top[c] = float(row["longShortRatio"])
            bn_top_ts[c] = int(row["timestamp"])
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"Binance top-trader position ratio {c} failed: {e}")

    # Optional context: funding (not a scored condition).
    for c in coins:
        try:
            payload = http_get(session, OKX_FUNDING, {"instId": inst[c]})
            row = (payload.get("data") or [None])[0]
            if row:
                funding[f"OKX_{c}"] = float(row.get("fundingRate"))
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"OKX funding {c} failed: {e}")
        try:
            data, url = get_binance(session, BN_PREMIUM, {"symbol": bn_sym[c]})
            if "www.binance.com" in url:
                bn_host_note = "fapi.binance.com returned an error or 451 geo-block; used www.binance.com public futures data endpoints"
            funding[f"BN_{c}"] = float(data["lastFundingRate"])
            time.sleep(0.1)
        except Exception as e:
            errors.append(f"Binance funding {c} failed: {e}")

    h1_ms = now_ms - 3_600_000
    h2_ms = now_ms - 7_200_000
    for c in coins:
        try:
            recs = []
            after = None
            pages = 0
            stop_reason = None
            while pages < 30:
                params = {"instType": "SWAP", "uly": f"{c}-USDT", "state": "filled", "limit": 100}
                if after:
                    params["after"] = after
                payload = http_get(session, OKX_LIQ, params)
                if payload.get("code") != "0":
                    stop_reason = f"code={payload.get('code')} msg={payload.get('msg')}"
                    if pages == 0:
                        errors.append(f"OKX liquidations {c} failed: {stop_reason}")
                    break
                data = payload.get("data") or []
                if not data or not data[0].get("details"):
                    stop_reason = "no more details"
                    break
                details = data[0]["details"]
                recs.extend(details)
                after = details[-1]["ts"]
                pages += 1
                if int(after) < h2_ms:
                    break
                time.sleep(0.15)
            if not recs:
                if not any(f"OKX liquidations {c} failed" in x for x in errors):
                    errors.append(f"OKX liquidations {c} empty pages={pages} {stop_reason}")
                continue

            ctval = CTVAL.get(c, 1.0)

            def usd_of(row, _ctval=ctval):
                return float(row["sz"]) * _ctval * float(row["bkPx"])

            def bucket(window_start):
                long_usd = short_usd = 0.0
                n_long = n_short = 0
                for row in recs:
                    ts = int(row["ts"])
                    if window_start <= ts <= now_ms:
                        usd = usd_of(row)
                        if side_of(row) == "long":
                            long_usd += usd
                            n_long += 1
                        else:
                            short_usd += usd
                            n_short += 1
                return {
                    "long_usd": round(long_usd, 2),
                    "short_usd": round(short_usd, 2),
                    "n_long": n_long,
                    "n_short": n_short,
                }

            h1 = bucket(h1_ms)
            h2 = bucket(h2_ms)
            prev = {
                "long_usd": round(h2["long_usd"] - h1["long_usd"], 2),
                "short_usd": round(h2["short_usd"] - h1["short_usd"], 2),
                "n_long": h2["n_long"] - h1["n_long"],
                "n_short": h2["n_short"] - h1["n_short"],
            }
            if h2["long_usd"] > 0:
                ratio = h2["short_usd"] / h2["long_usd"]
                inf = False
            else:
                ratio = None
                inf = h2["short_usd"] > 0
            short_rising = h1["short_usd"] > prev["short_usd"]
            if (inf or (ratio is not None and ratio >= THRESH["liq_met"])) and short_rising:
                status = "met"
            elif inf or (ratio is not None and ratio >= THRESH["liq_near"]):
                status = "near"
            else:
                status = "none"

            in_window = [x for x in recs if h2_ms <= int(x["ts"]) <= now_ms]
            latest_ts = max(int(x["ts"]) for x in recs) if recs else None
            oldest_ts = min(int(x["ts"]) for x in recs) if recs else None
            if oldest_ts is not None and oldest_ts > h2_ms:
                errors.append(f"OKX liquidations {c} paging did not cover the full 2 hours; earliest {iso(oldest_ts, tz)}")

            liq[c] = {
                "h1": h1,
                "h2": h2,
                "prev_h1": prev,
                "short_to_long": ratio,
                "short_to_long_inf": inf,
                "short_rising": short_rising,
                "status": status,
                "latest_ts": latest_ts,
                "latest_iso": iso(latest_ts, tz) if latest_ts else None,
                "n_fetched": len(recs),
                "n_in_window": len(in_window),
                "pages": pages,
                "oldest_fetched": iso(oldest_ts, tz) if oldest_ts else None,
            }
        except Exception as e:
            errors.append(f"OKX liquidations {c} failed: {e}")

    return {
        "prices": prices,
        "funding": funding,
        "okx_ratio": okx_ratio,
        "okx_ratio_ts": okx_ratio_ts,
        "bn_ratio": bn_ratio,
        "bn_ratio_ts": bn_ratio_ts,
        "okx_oi": okx_oi,
        "okx_oi_ts": okx_oi_ts,
        "okx_oi_high": okx_oi_high,
        "okx_oi_high_ts": okx_oi_high_ts,
        "bn_oi": bn_oi,
        "bn_oi_ts": bn_oi_ts,
        "bn_oi_high": bn_oi_high,
        "bn_oi_high_ts": bn_oi_high_ts,
        "okx_top": okx_top,
        "okx_top_ts": okx_top_ts,
        "bn_top": bn_top,
        "bn_top_ts": bn_top_ts,
        "liq": liq,
        "bn_host_note": bn_host_note,
    }


def merge_oi_high(state_high: float | None, series_high: float | None, series_ts: int | None, state_ts: str | None, tz: dt.tzinfo):
    """Keep the running high; update when the series makes a new high."""
    if series_high is None:
        return state_high, state_ts
    if state_high is None or series_high >= state_high:
        return series_high, iso(series_ts, tz) if series_ts else state_ts
    return state_high, state_ts


def evaluate(raw: dict, coins: list[str], state: dict, tz: dt.tzinfo) -> tuple[dict, dict]:
    """Return (conditions_detail, new_oi_high_state)."""
    oi_high = dict(state.get("oi_high") or {})
    oi_high_ts = dict(state.get("oi_high_ts") or {})
    detail: dict[str, Any] = {name: {} for name in CONDITIONS}

    for c in coins:
        # 1) account ratio — OKX is primary; Binance is also scored.
        okx_r = raw["okx_ratio"].get(c)
        bn_r = raw["bn_ratio"].get(c)
        okx_s = account_status(okx_r, THRESH["account_near"], THRESH["account_met"])
        bn_s = account_status(bn_r, THRESH["account_near"], THRESH["account_met"])
        # Conservative combined status: use the less-flushed (higher) ratio.
        if okx_r is not None and bn_r is not None:
            combined_ratio = max(okx_r, bn_r)
            combined = account_status(combined_ratio, THRESH["account_near"], THRESH["account_met"])
        elif okx_r is not None:
            combined_ratio, combined = okx_r, okx_s
        elif bn_r is not None:
            combined_ratio, combined = bn_r, bn_s
        else:
            combined_ratio, combined = None, "unknown"
        detail["account_ratio"][c] = {
            "status": combined,
            "okx": okx_r,
            "okx_status": okx_s,
            "okx_ts": iso(raw["okx_ratio_ts"][c], tz) if c in raw["okx_ratio_ts"] else None,
            "binance": bn_r,
            "binance_status": bn_s,
            "binance_ts": iso(raw["bn_ratio_ts"][c], tz) if c in raw["bn_ratio_ts"] else None,
            "combined_ratio": combined_ratio,
            "primary": "OKX, conservative max(OKX, Binance) for combined status",
        }

        # 2) OI drop vs running high (coin-denominated).
        drops = {}
        venue_status = {}
        for venue, cur_map, ts_map, series_high_map, series_high_ts_map, key in (
            ("OKX", raw["okx_oi"], raw["okx_oi_ts"], raw["okx_oi_high"], raw["okx_oi_high_ts"], f"OKX_{c}"),
            ("Binance", raw["bn_oi"], raw["bn_oi_ts"], raw["bn_oi_high"], raw["bn_oi_high_ts"], f"BN_{c}"),
        ):
            series_hi = series_high_map.get(c)
            series_hi_ts = series_high_ts_map.get(c)
            hi, hi_ts = merge_oi_high(oi_high.get(key), series_hi, series_hi_ts, oi_high_ts.get(key), tz)
            if hi is not None:
                oi_high[key] = hi
                oi_high_ts[key] = hi_ts
            cur = cur_map.get(c)
            drop = None
            if cur is not None and hi:
                drop = (hi - cur) / hi if hi else None
                # Guard against tiny negative drops from rounding if current is the high.
                if drop is not None and drop < 0:
                    drop = 0.0
            drops[venue] = {
                "current": cur,
                "current_ts": iso(ts_map[c], tz) if c in ts_map else None,
                "high": hi,
                "high_ts": hi_ts,
                "drop": drop,
                "status": oi_status(drop, THRESH["oi_near"], THRESH["oi_met"]),
            }
            venue_status[venue] = drops[venue]["status"]
        # Alert if either venue has flushed; still report both percentages.
        combined = worse_status(venue_status.get("OKX", "unknown"), venue_status.get("Binance", "unknown"))
        detail["oi_drop"][c] = {
            "status": combined,
            "okx": drops.get("OKX"),
            "binance": drops.get("Binance"),
            "combined_rule": "met/near if either venue hits the threshold (max drop)",
        }

        # 3) OKX top-trader notional ratio is official; Binance is reference.
        okx_t = raw["okx_top"].get(c)
        bn_t = raw["bn_top"].get(c)
        okx_ts = okx_top_status(okx_t, THRESH["okx_top_near"], THRESH["okx_top_met"])
        bn_flag = (bn_t is not None and bn_t < THRESH["bn_top_flag"])
        detail["top_trader_position"][c] = {
            "status": okx_ts,
            "okx": okx_t,
            "okx_ts": iso(raw["okx_top_ts"][c], tz) if c in raw["okx_top_ts"] else None,
            "binance": bn_t,
            "binance_ts": iso(raw["bn_top_ts"][c], tz) if c in raw["bn_top_ts"] else None,
            "binance_flag_below_1_5": bn_flag,
        }

        # 4) OKX short vs long liquidations (already status'd in fetch).
        row = raw["liq"].get(c) or {}
        detail["short_liquidations"][c] = {
            "status": row.get("status", "unknown") if row else "unknown",
            **row,
            "note": "Binance allForceOrders is not public; only OKX filled liquidation-orders are used",
        }

    return detail, {"oi_high": oi_high, "oi_high_ts": oi_high_ts}


def extract_status(detail: dict, coins: list[str]) -> dict:
    out = empty_status(coins)
    for name in CONDITIONS:
        for c in coins:
            st = (detail.get(name) or {}).get(c, {}).get("status", "unknown")
            out[name][c] = st
    return out


def detect_changes(prev: dict, curr: dict, coins: list[str]) -> list[dict]:
    changes = []
    for name in CONDITIONS:
        for c in coins:
            old = (prev.get(name) or {}).get(c, "none")
            new = (curr.get(name) or {}).get(c, "none")
            if old != new:
                changes.append({
                    "condition": name,
                    "asset": c,
                    "from": old,
                    "to": new,
                    "notify": should_notify(old, new),
                })
    return changes


def flushed_flag(status: dict, coins: list[str]) -> dict:
    counts = {}
    per = {}
    for c in coins:
        n = sum(1 for name in CONDITIONS if (status.get(name) or {}).get(c) == "met")
        counts[c] = n
        per[c] = n >= 3
    return {
        "per_asset": per,
        "met_counts": counts,
        "any": any(per.values()),
        "flag": "possibly mostly flushed" if any(per.values()) else None,
        "flag_zh": "可能已基本出清" if any(per.values()) else None,
        "rule": "flag when 3 or more of the 4 conditions are met for the same asset",
    }


def load_state(path: Path, coins: list[str]) -> dict:
    if not path.exists():
        return {
            "created": None,
            "window_start": None,
            "last_check": None,
            "oi_high": {},
            "oi_high_ts": {},
            "status": empty_status(coins),
        }
    return json.loads(path.read_text())


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2, default=str) + "\n")
    tmp.replace(path)


def run(args: argparse.Namespace) -> dict:
    tz = ZoneInfo(args.tz)
    now = dt.datetime.now(tz)
    now_ms = int(now.timestamp() * 1000)
    coins = [c.strip().upper() for c in args.coins.split(",") if c.strip()]
    state_path = Path(args.state).expanduser()
    state = load_state(state_path, coins)
    errors: list[str] = []

    keep = args.keep_window
    requested = parse_window_start(args.window_start, now, tz)
    prev_window = None
    if state.get("window_start"):
        try:
            prev_window = dt.datetime.fromisoformat(state["window_start"])
            if prev_window.tzinfo is None:
                prev_window = prev_window.replace(tzinfo=tz)
        except ValueError:
            prev_window = None

    if args.window_start:
        window_start = requested
    elif keep and prev_window is not None:
        window_start = prev_window
    elif prev_window is not None and prev_window.date() == now.date():
        window_start = prev_window
    else:
        window_start = requested  # today 00:00 in tz
        if prev_window is not None and prev_window.date() != now.date():
            # New calendar day: reset running highs unless --keep-window.
            state["oi_high"] = {}
            state["oi_high_ts"] = {}

    start_ms = int(window_start.timestamp() * 1000)

    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    raw = fetch_all(session, coins, start_ms, now_ms, tz, errors)
    detail, highs = evaluate(raw, coins, state, tz)
    status = extract_status(detail, coins)
    prev_status = state.get("status") or empty_status(coins)
    # Fill missing keys from older state files.
    for name in CONDITIONS:
        prev_status.setdefault(name, {})
        for c in coins:
            prev_status[name].setdefault(c, "none")
    changes = detect_changes(prev_status, status, coins)
    notify = [ch for ch in changes if ch["notify"]]
    flushed = flushed_flag(status, coins)

    out = {
        "fetched_at": now.isoformat(timespec="seconds"),
        "tz": args.tz,
        "window_start": window_start.isoformat(timespec="seconds"),
        "coins": coins,
        "prices": raw["prices"],
        "conditions": detail,
        "status": status,
        "prev_status": prev_status,
        "changes": changes,
        "notify": notify,
        "notify_rule": "notify only when a condition upgrades (none→near/met, near→met) or falls from met",
        "possibly_mostly_flushed": flushed,
        "context": {
            "funding": raw["funding"],
            "funding_note": "Funding is context only, not a scored condition. A common bottom reading is funding still negative while price stops making new lows.",
            "binance_host_note": raw["bn_host_note"],
            "binance_liquidations_note": "Binance allForceOrders is not public.",
            "oi_note": "Long OI always equals short OI. Judge positioning with account and top-trader ratios, not a 'long share of OI'. If top traders are flat or net short by notional while OI rises, the new longs are coming from retail.",
        },
        "thresholds": THRESH,
        "errors": errors,
        "disclaimer": DISCLAIMER,
    }

    new_state = {
        "created": state.get("created") or now.isoformat(timespec="seconds"),
        "window_start": window_start.isoformat(timespec="seconds"),
        "last_check": now.isoformat(timespec="seconds"),
        "oi_high": highs["oi_high"],
        "oi_high_ts": highs["oi_high_ts"],
        "status": status,
        "snapshot": {
            "prices": raw["prices"],
            "notify": notify,
            "changes": changes,
            "possibly_mostly_flushed": flushed,
            "errors": errors,
        },
    }
    if not args.no_write_state:
        save_state(state_path, new_state)
        out["state_path"] = str(state_path.resolve())
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Score four perp-deleveraging conditions from OKX/Binance public APIs and print JSON."
    )
    p.add_argument(
        "--state",
        default=os.environ.get("DELEVERAGE_STATE", "state.json"),
        help="State file path (default: ./state.json or $DELEVERAGE_STATE)",
    )
    p.add_argument("--tz", default=os.environ.get("DELEVERAGE_TZ", "Asia/Bangkok"))
    p.add_argument("--coins", default="BTC,ETH")
    p.add_argument(
        "--window-start",
        default=None,
        help="Window start, YYYY-MM-DD or ISO datetime in --tz. Default: today 00:00 in --tz.",
    )
    p.add_argument(
        "--keep-window",
        action="store_true",
        help="Do not reset the OI running high at midnight; keep the state's window_start.",
    )
    p.add_argument("--no-write-state", action="store_true")
    args = p.parse_args(argv)
    out = run(args)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
