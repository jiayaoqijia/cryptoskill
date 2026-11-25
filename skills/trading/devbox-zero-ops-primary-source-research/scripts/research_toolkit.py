#!/usr/bin/env python3
"""
Primary-Source Research & Verification Toolkit

Zero-dependency Python 3.8+ standard-library CLI for querying 22 official,
zero-API-key primary data sources (macroeconomics, government/regulatory
filings, science/earth observation, software registries, Web3/markets, and
sports), parsing arbitrary Atom/RSS feeds, verifying plain-HTTP URL
fetchability, and validating research citation bundles.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

UA = "PrimarySourceResearch/1.0 (+https://github.com/devbox-zero-ops)"
SEC_UA = os.environ.get(
    "RESEARCH_SEC_USER_AGENT",
    "DevBoxZeroOps Research contact@xiaheai.com",
)
BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

STEERING_PATTERNS = [
    r"\byou must conclude\b",
    r"\bplease accept\b",
    r"\bmark this as\b",
    r"\bverdict should be\b",
    r"\bmove probability to\b",
]

SECONDARY_AGGREGATOR_DOMAINS = (
    "polymarket.com",
    "kalshi.com",
    "metaculus.com",
    "manifold.markets",
    "predictit.org",
    "betfair.com",
    "oddsportal.com",
)

ALLOWED_ATTACHMENT_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".txt",
    ".doc",
    ".docx",
    ".csv",
}

SOURCES_CATALOG = [
    {"id": 1, "name": "FRED", "subcommand": "fred", "category": "Macroeconomics", "host": "fred.stlouisfed.org"},
    {"id": 2, "name": "US Treasury Fiscal Data", "subcommand": "treasury", "category": "Macroeconomics", "host": "api.fiscaldata.treasury.gov"},
    {"id": 3, "name": "US Federal Register", "subcommand": "fedreg", "category": "Government & Regulatory", "host": "www.federalregister.gov"},
    {"id": 4, "name": "European Central Bank FX", "subcommand": "ecb-fx", "category": "Macroeconomics", "host": "data-api.ecb.europa.eu"},
    {"id": 5, "name": "World Bank Open Data", "subcommand": "worldbank", "category": "Macroeconomics", "host": "api.worldbank.org"},
    {"id": 6, "name": "SEC EDGAR", "subcommand": "sec", "category": "Government & Regulatory", "host": "data.sec.gov"},
    {"id": 7, "name": "US FDA Drugs@FDA (OpenFDA)", "subcommand": "openfda", "category": "Health & Regulatory", "host": "api.fda.gov"},
    {"id": 8, "name": "NIH ClinicalTrials.gov", "subcommand": "clinicaltrials", "category": "Health & Science", "host": "clinicaltrials.gov"},
    {"id": 9, "name": "USGS Earthquakes", "subcommand": "usgs-quake", "category": "Earth & Science", "host": "earthquake.usgs.gov"},
    {"id": 10, "name": "Open-Meteo (WMO/NOAA/DWD)", "subcommand": "weather", "category": "Earth & Science", "host": "api.open-meteo.com"},
    {"id": 11, "name": "CISA KEV Catalog", "subcommand": "kev", "category": "Cybersecurity", "host": "www.cisa.gov"},
    {"id": 12, "name": "arXiv Preprints", "subcommand": "arxiv", "category": "Science & Literature", "host": "export.arxiv.org"},
    {"id": 13, "name": "GitHub REST API", "subcommand": "github", "category": "Developer Ecosystems", "host": "api.github.com"},
    {"id": 14, "name": "PyPI Registry", "subcommand": "pkg --ecosystem pypi", "category": "Developer Ecosystems", "host": "pypi.org"},
    {"id": 15, "name": "npm Registry", "subcommand": "pkg --ecosystem npm", "category": "Developer Ecosystems", "host": "registry.npmjs.org"},
    {"id": 16, "name": "HuggingFace Hub", "subcommand": "hf", "category": "AI & Models", "host": "huggingface.co"},
    {"id": 17, "name": "Launch Library 2 (SpaceDevs)", "subcommand": "launches", "category": "Aerospace & Science", "host": "ll.thespacedevs.com"},
    {"id": 18, "name": "DefiLlama Protocol TVL", "subcommand": "defillama", "category": "Web3 & Markets", "host": "api.llama.fi"},
    {"id": 19, "name": "Snapshot DAO Governance", "subcommand": "snapshot", "category": "Web3 & Governance", "host": "hub.snapshot.org"},
    {"id": 20, "name": "Coinbase Public Spot", "subcommand": "crypto-spot", "category": "Web3 & Markets", "host": "api.coinbase.com"},
    {"id": 21, "name": "Kraken Public Ticker", "subcommand": "crypto-spot", "category": "Web3 & Markets", "host": "api.kraken.com"},
    {"id": 22, "name": "ESPN Sports News API", "subcommand": "espn", "category": "Sports", "host": "site.api.espn.com"},
]


def _parse_retry_after(val):
    """Parse Retry-After header (float/int seconds or HTTP-date) into delay seconds."""
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    try:
        sec = float(s)
        return sec if sec >= 0 else None
    except ValueError:
        pass
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delay = (dt.astimezone(timezone.utc) - datetime.now(timezone.utc)).total_seconds()
        return max(0.0, delay)
    except Exception:
        return None


def is_valid_http_url(url: str) -> bool:
    """Return True if url is a syntactically valid http(s) URL without whitespace."""
    if not isinstance(url, str) or not url or re.search(r"\s", url):
        return False
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme.lower() in ("http", "https") and bool(parsed.netloc)


def is_secondary_aggregator_url(url: str) -> str:
    """Return matching secondary prediction-market/odds domain if present, else ''."""
    try:
        host = (urllib.parse.urlparse(url).hostname or "").lower()
    except Exception:
        host = ""
    for dom in SECONDARY_AGGREGATOR_DOMAINS:
        if host == dom or host.endswith("." + dom):
            return dom
    return ""


def http_get_text(url: str, timeout: int = 20, retries: int = 2, user_agent: str = None) -> str:
    """HTTP GET returning decoded UTF-8 text with bounded retry/backoff on 429/5xx."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": user_agent or UA, "Accept": "*/*"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last_err = e
            retryable_status = e.code == 429 or e.code >= 500
            if (not retryable_status) or attempt >= retries:
                raise
            wait_s = _parse_retry_after(e.headers.get("Retry-After") if e.headers else None)
            if wait_s is not None:
                if wait_s > 30.0:
                    raise
                sleep_s = max(0.5, wait_s)
            else:
                sleep_s = (1.5 if e.code == 429 else 1.0) * (attempt + 1)
            time.sleep(sleep_s)
            continue
        except Exception as e:
            last_err = e
            if attempt >= retries:
                raise
        time.sleep(1.0 * (attempt + 1))
    raise last_err


def fetch_fred_series(
    series_id: str,
    limit: int = 12,
    target_yoy_pct: float = None,
    out_csv: str = None,
    lookback_years: int = 15,
):
    """
    Fetch an official FRED CSV series (e.g., CPIAUCSL, UNRATE, DFF).

    Always returns the latest observation, MoM/YoY deltas (when available),
    and the most recent `limit` points. When `target_yoy_pct` is supplied, also
    computes the exact next-month MoM % change required to reach `target_yoy_pct`,
    evaluates the historical calendar-month base rate over `lookback_years`,
    and optionally writes a compact verifiable proof CSV to `out_csv`.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={urllib.parse.quote(series_id)}"
    raw = http_get_text(url)
    rows = []
    for r in csv.reader(io.StringIO(raw)):
        if len(r) >= 2 and re.match(r"^\d{4}-\d{2}-\d{2}$", r[0]) and r[1] not in ("", "."):
            rows.append((r[0], float(r[1])))
    if not rows:
        raise ValueError(f"No valid observations found in FRED series {series_id}")

    latest_date, latest_val = rows[-1]
    prev_val = rows[-2][1] if len(rows) >= 2 else None
    mom_latest = (
        round((latest_val / prev_val - 1.0) * 100.0, 4)
        if prev_val not in (None, 0.0)
        else None
    )

    dt_latest = datetime.strptime(latest_date, "%Y-%m-%d")
    by_ym = {
        (datetime.strptime(d, "%Y-%m-%d").year, datetime.strptime(d, "%Y-%m-%d").month): (d, v)
        for d, v in rows
    }
    prev_yr_entry = by_ym.get((dt_latest.year - 1, dt_latest.month))
    yoy_latest = (
        round((latest_val / prev_yr_entry[1] - 1.0) * 100.0, 4)
        if prev_yr_entry and prev_yr_entry[1] != 0.0
        else None
    )

    result = {
        "series": series_id,
        "source_url": url,
        "observations_total": len(rows),
        "latest_date": latest_date,
        "latest_value": round(latest_val, 4),
        "latest_mom_pct": mom_latest,
        "latest_yoy_pct": yoy_latest,
        "recent_observations": [
            {"date": d, "value": round(v, 4)} for d, v in rows[-max(1, limit):]
        ],
    }

    if target_yoy_pct is not None:
        if len(rows) < 24:
            raise ValueError(f"Insufficient FRED rows for YoY threshold calculation on {series_id}: {len(rows)}")
        next_year = dt_latest.year + (1 if dt_latest.month == 12 else 0)
        next_month = 1 if dt_latest.month == 12 else dt_latest.month + 1
        if (next_year - 1, next_month) not in by_ym:
            raise ValueError(
                f"Missing 12-month prior reference for {next_year}-{next_month:02d} in {series_id}"
            )
        base_date, base_val = by_ym[(next_year - 1, next_month)]
        required_next_val = base_val * (1.0 + target_yoy_pct / 100.0)
        required_mom_pct = (required_next_val / latest_val - 1.0) * 100.0

        hist_moms = []
        for i in range(1, len(rows)):
            d_str, val = rows[i]
            dt = datetime.strptime(d_str, "%Y-%m-%d")
            if dt.month == next_month and rows[i - 1][1] != 0.0:
                mom = (val / rows[i - 1][1] - 1.0) * 100.0
                hist_moms.append((d_str, rows[i - 1][1], val, mom))
        recent = hist_moms[-max(1, lookback_years):]
        hits_gte = sum(1 for _, _, _, m in recent if m >= required_mom_pct)

        threshold_info = {
            "base_date_for_next_yoy": base_date,
            "base_value_for_next_yoy": round(base_val, 4),
            "target_yoy_pct": target_yoy_pct,
            "required_next_value": round(required_next_val, 4),
            "required_next_mom_pct": round(required_mom_pct, 4),
            "next_calendar_month": next_month,
            "lookback_count": len(recent),
            "historical_hits_gte_required": hits_gte,
            "base_rate_pct": round((hits_gte / len(recent)) * 100.0, 2) if recent else 0.0,
        }
        if out_csv:
            parent = os.path.dirname(os.path.abspath(out_csv))
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(out_csv, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([
                    "date",
                    "prev_month_value",
                    "value",
                    "mom_pct",
                    f"ge_required_{required_mom_pct:.4f}_pct",
                ])
                for d_str, pv, v, mom in recent:
                    w.writerow([
                        d_str,
                        f"{pv:.4f}",
                        f"{v:.4f}",
                        f"{mom:.4f}",
                        "YES" if mom >= required_mom_pct else "NO",
                    ])
            threshold_info["csv_path"] = out_csv
        result["threshold_analysis"] = threshold_info

    return result


def fetch_federal_register(term: str, limit: int = 5):
    """Query US Federal Register REST API v1 for rules, notices, and executive orders."""
    q = urllib.parse.urlencode({"conditions[term]": term, "per_page": str(limit), "order": "newest"})
    url = f"https://www.federalregister.gov/api/v1/documents.json?{q}"
    data = json.loads(http_get_text(url))
    out = []
    for d in data.get("results", []):
        out.append({
            "document_number": d.get("document_number"),
            "publication_date": d.get("publication_date"),
            "type": d.get("type"),
            "title": d.get("title"),
            "html_url": d.get("html_url"),
            "pdf_url": d.get("pdf_url"),
        })
    return {"query_url": url, "count": len(out), "results": out}


def fetch_snapshot_proposal(proposal_id: str):
    """Query Snapshot GraphQL API for DAO proposal tally and quorum arithmetic."""
    q = {
        "query": """query($id: String!) {
          proposal(id: $id) {
            id title state choices scores scores_total quorum start end space { id name }
          }
        }""",
        "variables": {"id": proposal_id},
    }
    req = urllib.request.Request(
        "https://hub.snapshot.org/graphql",
        data=json.dumps(q).encode("utf-8"),
        headers={"User-Agent": UA, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8", "ignore"))
    p = (data.get("data") or {}).get("proposal") or {}
    quorum = float(p.get("quorum") or 0)
    total = float(p.get("scores_total") or 0)
    p["quorum_pct_reached"] = round((total / quorum) * 100.0, 2) if quorum > 0 else None
    p["remaining_to_quorum"] = max(0.0, quorum - total) if quorum > 0 else None
    p["source_url"] = "https://hub.snapshot.org/graphql"
    return p


def check_url_readable(url: str, timeout: int = 15, preview_chars: int = 0):
    """
    Verify plain-HTTP fetchability (no JS, no cookies) to detect 403/429/JS walls,
    PDF payloads, and machine-readable structured feeds.
    """
    if not is_valid_http_url(url):
        return {
            "url": url,
            "status": None,
            "error": "Invalid HTTP(S) URL or contains whitespace",
            "judge_readable": False,
            "plain_http_readable": False,
            "needs_attachment": True,
        }
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PrimarySourceFetch/1.0)",
            "Accept": "text/html,application/pdf,application/json,text/csv,*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw_bytes = r.read(65536)
            ct = r.headers.get("Content-Type", "")
            ct_low = ct.lower()
            is_pdf = ("pdf" in ct_low) or urllib.parse.urlparse(url).path.lower().endswith(".pdf")
            is_structured = any(
                t in ct_low
                for t in ("application/json", "text/csv", "text/plain", "application/xml", "text/xml")
            )
            body = raw_bytes.decode("utf-8", errors="ignore")
            js_wall = (not is_pdf) and (not is_structured) and bool(
                re.search(r"just a moment|enable javascript|cf-browser-verification|captcha", body, re.I)
            )
            clean_text = re.sub(
                r"<script\b[\s\S]*?</script>|<style\b[\s\S]*?</style>|<noscript\b[\s\S]*?</noscript>|<[^>]+>",
                " ",
                body,
                flags=re.I,
            )
            clean_text = re.sub(r"\s+", " ", clean_text).strip()
            if is_pdf:
                readable = r.status == 200 and len(raw_bytes) >= 200
            elif is_structured:
                readable = r.status == 200 and len(clean_text) >= 20
            else:
                readable = r.status == 200 and not js_wall and len(clean_text) > 80
            out = {
                "url": url,
                "status": r.status,
                "content_type": ct,
                "sample_bytes": len(raw_bytes),
                "clean_text_len": len(clean_text),
                "plain_http_readable": readable,
                "judge_readable": readable,
                "needs_attachment": (not readable) or is_pdf,
                "js_or_bot_wall": js_wall,
            }
            if preview_chars > 0:
                out["text_preview"] = clean_text[:preview_chars]
            return out
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "error": str(e),
            "plain_http_readable": False,
            "judge_readable": False,
            "needs_attachment": True,
        }


def fetch_sec_edgar_filings(cik: str, form_filter: str = "", limit: int = 8):
    """Fetch official SEC EDGAR recent filings (8-K, 10-Q, 10-K, S-1, etc.) for a CIK."""
    cik_digits = re.sub(r"\D", "", str(cik or ""))
    if not cik_digits:
        raise ValueError("SEC CIK must contain digits (e.g., 0000320193 for Apple)")
    cik_pad = cik_digits.lstrip("0").zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_pad}.json"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": SEC_UA, "Accept-Encoding": "identity"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    recent = (data.get("filings") or {}).get("recent") or {}
    forms = recent.get("form") or []
    dates = recent.get("filingDate") or []
    accs = recent.get("accessionNumber") or []
    docs = recent.get("primaryDocument") or []
    out = []
    cik_int = str(int(cik_pad))
    for fm, dt, acc, doc in zip(forms, dates, accs, docs):
        if form_filter and fm.upper() != form_filter.upper():
            continue
        acc_clean = acc.replace("-", "")
        out.append({
            "form": fm,
            "filing_date": dt,
            "accession": acc,
            "doc_url": f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_clean}/{doc}",
        })
        if len(out) >= limit:
            break
    return {"entity": data.get("name"), "cik": cik_pad, "source_url": url, "filings": out}


def fetch_github_state(repo: str):
    """Fetch machine-readable GitHub primary state: latest release, recent tags, and workflow runs."""
    hdr = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    res = {"repo": repo, "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    for key, ep in [
        ("latest_release", f"https://api.github.com/repos/{repo}/releases/latest"),
        ("recent_tags", f"https://api.github.com/repos/{repo}/tags?per_page=5"),
        ("recent_runs", f"https://api.github.com/repos/{repo}/actions/runs?per_page=5"),
    ]:
        try:
            req = urllib.request.Request(ep, headers=hdr)
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode("utf-8", errors="replace"))
            if key == "latest_release":
                res[key] = {
                    "tag": d.get("tag_name"),
                    "name": d.get("name"),
                    "published_at": d.get("published_at"),
                    "html_url": d.get("html_url"),
                }
            elif key == "recent_tags":
                res[key] = [t.get("name") for t in d[:5]]
            else:
                res[key] = [
                    {
                        "name": x.get("name"),
                        "status": x.get("status"),
                        "conclusion": x.get("conclusion"),
                        "created_at": x.get("created_at"),
                        "html_url": x.get("html_url"),
                    }
                    for x in d.get("workflow_runs", [])[:5]
                ]
        except Exception as e:
            res[key] = {"error": str(e)}
    return res


def fetch_defillama_protocol(slug: str):
    """Fetch official DefiLlama current TVL & 7d delta for a DeFi protocol."""
    url = f"https://api.llama.fi/protocol/{urllib.parse.quote(slug)}"
    data = json.loads(http_get_text(url, timeout=20))
    tvl_series = data.get("tvl") or []
    latest = tvl_series[-1] if tvl_series else {}
    prev_7d = tvl_series[-8] if len(tvl_series) >= 8 else {}
    cur_tvl = float(latest.get("totalLiquidityUSD") or 0)
    old_tvl = float(prev_7d.get("totalLiquidityUSD") or 0)
    return {
        "name": data.get("name"),
        "slug": slug,
        "source_url": url,
        "latest_date_utc": (
            datetime.fromtimestamp(latest["date"], timezone.utc).strftime("%Y-%m-%d")
            if latest.get("date")
            else None
        ),
        "latest_tvl_usd": round(cur_tvl, 2),
        "tvl_7d_ago_usd": round(old_tvl, 2) if old_tvl else None,
        "change_7d_pct": round(((cur_tvl / old_tvl) - 1.0) * 100.0, 2) if old_tvl else None,
    }


def fetch_treasury_fiscal(dataset: str = "tga", limit: int = 5):
    """Fetch official US Treasury Fiscal Data API (TGA operating cash balance or Debt to the Penny)."""
    endpoints = {
        "tga": (
            "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
            f"v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]={limit}"
        ),
        "debt": (
            "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
            f"v2/accounting/od/debt_to_penny?sort=-record_date&page[size]={limit}"
        ),
    }
    url = endpoints.get(dataset, endpoints["tga"])
    data = json.loads(http_get_text(url, timeout=20))
    return {"dataset": dataset, "source_url": url, "rows": data.get("data", [])[:limit]}


def fetch_package_registry(ecosystem: str, name: str):
    """Fetch machine-readable package release timestamp & latest version from PyPI or npm."""
    if ecosystem == "pypi":
        url = f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json"
        data = json.loads(http_get_text(url, timeout=20))
        info = data.get("info") or {}
        ver = info.get("version")
        files = (data.get("releases") or {}).get(ver) or []
        upload_time = files[0].get("upload_time_iso_8601") if files else None
        return {
            "ecosystem": "pypi",
            "name": name,
            "latest_version": ver,
            "published_at_utc": upload_time,
            "source_url": url,
        }
    url = f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='@/')}"
    data = json.loads(http_get_text(url, timeout=20))
    dist_tags = data.get("dist-tags") or {}
    times = data.get("time") or {}
    latest = dist_tags.get("latest")
    return {
        "ecosystem": "npm",
        "name": name,
        "latest_version": latest,
        "published_at_utc": times.get(latest),
        "dist_tags": dist_tags,
        "source_url": url,
    }


def fetch_ecb_fx_rate(currency: str = "USD", limit: int = 10):
    """Fetch official European Central Bank (ECB) daily EUR/<CUR> reference FX rates CSV."""
    cur = currency.strip().upper()
    url = (
        f"https://data-api.ecb.europa.eu/service/data/EXR/D.{cur}.EUR.SP00.A"
        f"?lastNObservations={limit}&format=csvdata"
    )
    raw = http_get_text(url, timeout=20)
    rows = []
    for r in csv.DictReader(io.StringIO(raw)):
        dt = r.get("TIME_PERIOD")
        val = r.get("OBS_VALUE")
        if dt and val:
            rows.append({"date": dt, "rate": float(val)})
    latest = rows[-1] if rows else None
    return {"pair": f"EUR/{cur}", "source_url": url, "latest": latest, "history": rows}


def fetch_open_meteo_daily(lat: float, lon: float, past_days: int = 5, forecast_days: int = 5):
    """Fetch WMO/NOAA/DWD daily max/min temperature & precipitation via Open-Meteo."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=UTC&past_days={past_days}&forecast_days={forecast_days}"
    )
    data = json.loads(http_get_text(url, timeout=20))
    daily = data.get("daily") or {}
    rows = []
    for d, hx, hn, p in zip(
        daily.get("time") or [],
        daily.get("temperature_2m_max") or [],
        daily.get("temperature_2m_min") or [],
        daily.get("precipitation_sum") or [],
    ):
        rows.append({"date_utc": d, "temp_max_c": hx, "temp_min_c": hn, "precip_mm": p})
    return {"latitude": lat, "longitude": lon, "source_url": url, "daily": rows}


def fetch_cisa_kev(keyword: str = "", limit: int = 8):
    """Fetch CISA Known Exploited Vulnerabilities (KEV) live JSON catalog."""
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    data = json.loads(http_get_text(url, timeout=25))
    vulns = data.get("vulnerabilities") or []
    kw = keyword.strip().lower()
    if kw:
        vulns = [v for v in vulns if kw in json.dumps(v).lower()]
    vulns = sorted(vulns, key=lambda x: x.get("dateAdded", ""), reverse=True)[:limit]
    return {
        "catalog_version": data.get("catalogVersion"),
        "date_released": data.get("dateReleased"),
        "source_url": url,
        "matches": vulns,
    }


def _strip_tag(tag: str) -> str:
    """Strip XML namespace prefix cleanly."""
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _parse_feed_entries(xml_text: str, keyword: str = "", limit: int = 8):
    """Parse Atom or RSS 2.0 XML into uniform timestamped items."""
    root = ET.fromstring(xml_text)
    kw = keyword.strip().lower()
    items = []
    for elem in root.iter():
        sname = _strip_tag(elem.tag)
        if sname not in ("entry", "item"):
            continue
        fields = {}
        links = []
        authors = []
        for child in elem:
            cname = _strip_tag(child.tag)
            txt = (child.text or "").strip()
            if cname == "link":
                href = child.attrib.get("href") or txt
                if href:
                    links.append(href)
            elif cname == "author":
                name_el = next(
                    (c.text.strip() for c in child if _strip_tag(c.tag) == "name" and c.text),
                    "",
                )
                if name_el:
                    authors.append(name_el)
            elif txt and cname not in fields:
                fields[cname] = txt
        raw_dt = fields.get("published") or fields.get("updated") or fields.get("pubDate") or ""
        iso_dt = raw_dt
        if raw_dt and sname == "item":
            try:
                iso_dt = (
                    parsedate_to_datetime(raw_dt)
                    .astimezone(timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ")
                )
            except Exception:
                pass
        entry = {
            "title": re.sub(r"\s+", " ", fields.get("title", "")),
            "published_at": iso_dt,
            "url": links[0] if links else fields.get("id", ""),
            "id": fields.get("id") or fields.get("guid", ""),
            "authors": authors[:5],
            "summary": re.sub(
                r"\s+", " ", fields.get("summary") or fields.get("description") or ""
            )[:360],
        }
        if kw and kw not in json.dumps(entry, ensure_ascii=False).lower():
            continue
        items.append(entry)
        if len(items) >= limit:
            break
    return items


def fetch_arxiv_papers(query: str, limit: int = 5):
    """Query official arXiv Atom API for primary preprint IDs and submission timestamps."""
    q = urllib.parse.quote(query)
    url = (
        f"https://export.arxiv.org/api/query?search_query=all:{q}"
        f"&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    )
    xml_text = http_get_text(url, timeout=25)
    return {"query": query, "source_url": url, "papers": _parse_feed_entries(xml_text, limit=limit)}


def fetch_huggingface_model(search: str, limit: int = 8):
    """Query HuggingFace Hub REST API for open-weight model release dates and downloads."""
    q = urllib.parse.quote(search)
    url = f"https://huggingface.co/api/models?search={q}&sort=lastModified&direction=-1&limit={limit}"
    rows = json.loads(http_get_text(url, timeout=20))
    models = []
    for m in rows[:limit]:
        mid = m.get("id") or m.get("modelId") or ""
        models.append({
            "id": mid,
            "created_at": m.get("createdAt"),
            "last_modified": m.get("lastModified"),
            "downloads": m.get("downloads"),
            "likes": m.get("likes"),
            "pipeline_tag": m.get("pipeline_tag"),
            "url": f"https://huggingface.co/{mid}" if mid else "",
        })
    return {"search": search, "source_url": url, "models": models}


def fetch_rss_feed(feed_url: str, keyword: str = "", limit: int = 8):
    """Fetch any authoritative RSS 2.0 or Atom feed for timestamped announcements/releases."""
    xml_text = http_get_text(feed_url, timeout=20)
    return {"feed_url": feed_url, "items": _parse_feed_entries(xml_text, keyword=keyword, limit=limit)}


def fetch_espn_news(sport: str = "basketball", league: str = "nba", keyword: str = "", limit: int = 5):
    """Fetch official ESPN JSON news feed for roster updates, injury reports, and match results."""
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/"
        f"{urllib.parse.quote(sport)}/{urllib.parse.quote(league)}/news?limit={max(limit * 3, 15)}"
    )
    data = json.loads(http_get_text(url, timeout=20, user_agent=BROWSER_UA))
    kw = keyword.strip().lower()
    articles = []
    for a in data.get("articles", []):
        link = ((a.get("links") or {}).get("web") or {}).get("href") or ""
        row = {
            "headline": a.get("headline", ""),
            "published": a.get("published", ""),
            "description": (a.get("description") or "")[:300],
            "url": link,
        }
        if kw and kw not in (row["headline"] + " " + row["description"]).lower():
            continue
        articles.append(row)
        if len(articles) >= limit:
            break
    return {"sport": sport, "league": league, "source_url": url, "articles": articles}


def fetch_clinical_trials(query: str, limit: int = 5):
    """Query NIH/NLM ClinicalTrials.gov REST API v2 for dated drug trial status & milestones."""
    q = urllib.parse.quote(query)
    url = (
        f"https://clinicaltrials.gov/api/v2/studies?query.term={q}"
        f"&pageSize={limit}&sort=LastUpdatePostDate:desc"
    )
    data = json.loads(http_get_text(url, timeout=20))
    studies = []
    for s in data.get("studies", [])[:limit]:
        ps = s.get("protocolSection") or {}
        idm = ps.get("identificationModule") or {}
        stm = ps.get("statusModule") or {}
        dsm = ps.get("designModule") or {}
        spm = (ps.get("sponsorCollaboratorsModule") or {}).get("leadSponsor") or {}
        nct = idm.get("nctId", "")
        studies.append({
            "nct_id": nct,
            "title": idm.get("briefTitle", ""),
            "status": stm.get("overallStatus", ""),
            "last_update_date": (stm.get("lastUpdatePostDateStruct") or {}).get("date", ""),
            "primary_completion_date": (stm.get("primaryCompletionDateStruct") or {}).get("date", ""),
            "phases": dsm.get("phases") or [],
            "sponsor": spm.get("name", ""),
            "url": f"https://clinicaltrials.gov/study/{nct}" if nct else url,
        })
    return {"query": query, "source_url": url, "studies": studies}


def fetch_crypto_spot(base: str = "BTC"):
    """Fetch cross-checked live crypto spot & 24h range from Coinbase and Kraken public APIs."""
    sym = base.strip().upper()
    cb_url = f"https://api.coinbase.com/v2/prices/{urllib.parse.quote(sym)}-USD/spot"
    cb_data = json.loads(http_get_text(cb_url, timeout=15))
    spot_usd = float(cb_data["data"]["amount"])
    kraken_map = {
        "BTC": "XBTUSD",
        "ETH": "ETHUSD",
        "SOL": "SOLUSD",
        "DOGE": "XDGUSD",
        "XRP": "XRPUSD",
        "ADA": "ADAUSD",
    }
    k_pair = kraken_map.get(sym, f"{sym}USD")
    k_url = f"https://api.kraken.com/0/public/Ticker?pair={urllib.parse.quote(k_pair)}"
    kraken_info = {}
    try:
        kd = json.loads(http_get_text(k_url, timeout=15))
        res_map = kd.get("result") or {}
        if res_map:
            t = next(iter(res_map.values()))
            kraken_info = {
                "last_usd": float(t["c"][0]),
                "low_24h_usd": float(t["l"][1]),
                "high_24h_usd": float(t["h"][1]),
                "vol_24h": round(float(t["v"][1]), 2),
                "source_url": k_url,
            }
    except Exception:
        pass
    return {
        "symbol": sym,
        "observed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coinbase_spot_usd": spot_usd,
        "source_url": cb_url,
        "kraken": kraken_info,
    }


def fetch_space_launches(search: str = "", limit: int = 5):
    """Query Launch Library 2 (TheSpaceDevs) for upcoming SpaceX/NASA/orbital launch schedules."""
    qs = f"limit={limit}"
    if search.strip():
        qs += f"&search={urllib.parse.quote(search.strip())}"
    url = f"https://ll.thespacedevs.com/2.2.0/launch/upcoming/?{qs}"
    data = json.loads(http_get_text(url, timeout=20, user_agent=BROWSER_UA))
    launches = []
    for item in data.get("results", [])[:limit]:
        launches.append({
            "name": item.get("name", ""),
            "net_utc": item.get("net", ""),
            "status": (item.get("status") or {}).get("name", ""),
            "provider": (item.get("launch_service_provider") or {}).get("name", ""),
            "pad": (item.get("pad") or {}).get("name", ""),
            "url": item.get("url") or url,
        })
    return {"search": search, "source_url": url, "launches": launches}


def fetch_usgs_earthquakes(min_mag: float = 5.5, limit: int = 5):
    """Query official USGS real-time earthquake GeoJSON feed."""
    url = (
        f"https://earthquake.usgs.gov/fdsnws/event/1/query"
        f"?format=geojson&minmagnitude={min_mag}&limit={limit}&orderby=time"
    )
    data = json.loads(http_get_text(url, timeout=20))
    events = []
    for feat in (data.get("features") or [])[:limit]:
        props = feat.get("properties") or {}
        ms = props.get("time")
        iso = (
            datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if isinstance(ms, (int, float))
            else ""
        )
        events.append({
            "id": feat.get("id", ""),
            "magnitude": props.get("mag"),
            "place": props.get("place", ""),
            "time_utc": iso,
            "tsunami": props.get("tsunami", 0),
            "url": props.get("url") or url,
        })
    return {"min_mag": min_mag, "source_url": url, "events": events}


def fetch_openfda_drug_approvals(query: str, limit: int = 5):
    """Query official US FDA Drugs@FDA database (NDA/BLA approval & submission records)."""
    clean_q = re.sub(r"[^A-Za-z0-9\s\-]", "", query or "").strip()
    if not clean_q:
        raise ValueError("openfda query must contain a non-empty drug name")
    encoded = urllib.parse.quote(f'products.brand_name:"{clean_q}"+openfda.generic_name:"{clean_q}"')
    url = f"https://api.fda.gov/drug/drugsfda.json?search={encoded}&limit={limit}"
    try:
        data = json.loads(http_get_text(url, timeout=20))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            fallback_url = (
                f"https://api.fda.gov/drug/drugsfda.json?search={urllib.parse.quote(clean_q)}&limit={limit}"
            )
            data = json.loads(http_get_text(fallback_url, timeout=20))
            url = fallback_url
        else:
            raise
    approvals = []
    for r in (data.get("results") or [])[:limit]:
        subs = r.get("submissions") or []
        latest_sub = (
            sorted(
                subs,
                key=lambda s: str(s.get("submission_status_date") or ""),
                reverse=True,
            )[0]
            if subs
            else {}
        )
        raw_d = str(latest_sub.get("submission_status_date") or "")
        iso_d = (
            f"{raw_d[:4]}-{raw_d[4:6]}-{raw_d[6:8]}"
            if len(raw_d) == 8 and raw_d.isdigit()
            else raw_d
        )
        approvals.append({
            "application_number": r.get("application_number", ""),
            "sponsor_name": r.get("sponsor_name", ""),
            "latest_submission_type": latest_sub.get("submission_type", ""),
            "latest_submission_status": latest_sub.get("submission_status", ""),
            "latest_status_date": iso_d,
            "url": url,
        })
    return {"query": clean_q, "source_url": url, "approvals": approvals}


def fetch_worldbank_indicator(
    country: str = "USA",
    indicator: str = "NY.GDP.MKTP.KD.ZG",
    limit: int = 5,
):
    """Query official World Bank Open Data v2 macro indicators (GDP growth, CPI, etc.)."""
    c = country.strip().upper()
    ind = indicator.strip()
    url = (
        f"https://api.worldbank.org/v2/country/{urllib.parse.quote(c)}"
        f"/indicator/{urllib.parse.quote(ind)}?format=json&per_page={max(limit * 2, 10)}"
    )
    data = json.loads(http_get_text(url, timeout=20))
    rows = []
    if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
        for r in data[1]:
            if r.get("value") is not None:
                rows.append({
                    "year": r.get("date", ""),
                    "value": round(float(r["value"]), 4),
                    "indicator": (r.get("indicator") or {}).get("value", ind),
                    "country": (r.get("country") or {}).get("value", c),
                })
                if len(rows) >= limit:
                    break
    return {"country": c, "indicator": ind, "source_url": url, "observations": rows}


def validate_citation_bundle(
    note: str,
    links: list,
    files: list,
    check_links: bool = False,
    max_items: int = 3,
    strict_primary: bool = True,
):
    """
    Validate a research citation bundle for ISO-date anchoring, neutral tone,
    URL hygiene, primary-source compliance, attachment integrity, and optional
    live plain-HTTP fetchability.
    """
    issues = []
    note_raw = note or ""
    has_note = bool(note_raw.strip())
    links = list(links or [])
    files = list(files or [])
    item_count = (1 if has_note else 0) + len(links) + len(files)
    if item_count == 0 or (max_items > 0 and item_count > max_items):
        issues.append(f"Item count must be 1..{max_items} (got {item_count})")
    if has_note:
        if len(note_raw) > 8000:
            issues.append(f"Note length {len(note_raw)} > 8000 chars")
        if not re.search(r"\b20\d{2}-\d{2}-\d{2}\b", note_raw):
            issues.append("Note should include an explicit ISO date (YYYY-MM-DD) for the sourced fact")
        for pat in STEERING_PATTERNS:
            if re.search(pat, note_raw, re.I):
                issues.append(f"Non-neutral steering phrasing matched: {pat}")

    seen_links = set()
    for u in links:
        if not isinstance(u, str) or not u:
            issues.append("Empty or non-string link URL")
            continue
        if re.search(r"\s", u):
            issues.append(f"Link URL contains whitespace: {u!r}")
            continue
        if not is_valid_http_url(u):
            issues.append(f"Link URL must use http(s) scheme with valid host: {u!r}")
            continue
        if u in seen_links:
            issues.append(f"Duplicate link URL: {u}")
        else:
            seen_links.add(u)
        if strict_primary:
            agg_dom = is_secondary_aggregator_url(u)
            if agg_dom:
                issues.append(
                    f"Secondary prediction-market/odds domain ({agg_dom}) cited under strict primary mode: {u}"
                )

    total_bytes = 0
    for fp in files:
        ext = os.path.splitext(str(fp))[1].lower()
        if ext not in ALLOWED_ATTACHMENT_EXTENSIONS:
            issues.append(
                f"Disallowed file type ({ext or 'none'}): {fp} "
                "(allowed: PNG/JPEG/WebP/PDF/TXT/DOC/DOCX/CSV)"
            )
        if not os.path.isfile(fp):
            issues.append(f"Missing file: {fp}")
        else:
            total_bytes += os.path.getsize(fp)
    if total_bytes > 10 * 1024 * 1024:
        issues.append(f"Total file size {total_bytes} > 10 MB")

    link_checks = []
    if check_links:
        for u in links:
            chk = check_url_readable(u)
            link_checks.append(chk)
            if not chk.get("plain_http_readable") and not files:
                issues.append(
                    f"Link may not be readable via plain HTTP ({chk.get('status') or chk.get('error')}): "
                    f"{u} -> attach local proof/CSV/PDF"
                )
    return {
        "valid": len(issues) == 0,
        "item_count": item_count,
        "note_chars": len(note_raw) if has_note else 0,
        "file_bytes": total_bytes,
        "link_checks": link_checks,
        "issues": issues,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="research_toolkit.py",
        description=(
            "Zero-dependency CLI for querying 22 official zero-API-key primary data "
            "sources, RSS/Atom feeds, plain-HTTP URL verification, and citation auditing."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-sources", help="List all 22 built-in zero-API-key primary sources")

    p_fred = sub.add_parser("fred", help="Fetch FRED macro CSV series and optional YoY threshold base rate")
    p_fred.add_argument("--series", required=True, help="FRED series ID (e.g. CPIAUCSL, UNRATE, DFF)")
    p_fred.add_argument("--limit", type=int, default=12, help="Number of recent observations to include")
    p_fred.add_argument("--target-yoy", type=float, default=None, help="Optional target YoY %% threshold")
    p_fred.add_argument("--out-csv", default=None, help="Optional output path for historical base-rate CSV")
    p_fred.add_argument("--years", type=int, default=15, help="Lookback years for threshold base rate")

    p_tr = sub.add_parser("treasury", help="Fetch US Treasury Fiscal Data (TGA balance or national debt)")
    p_tr.add_argument("--dataset", choices=["tga", "debt"], default="tga")
    p_tr.add_argument("--limit", type=int, default=5)

    p_fr = sub.add_parser("fedreg", help="Search US Federal Register rules, notices, and executive orders")
    p_fr.add_argument("--term", required=True)
    p_fr.add_argument("--limit", type=int, default=5)

    p_fx = sub.add_parser("ecb-fx", help="Fetch European Central Bank daily EUR/<CUR> reference FX rates")
    p_fx.add_argument("--currency", default="USD", help="3-letter ISO currency code (e.g. USD, JPY, GBP)")
    p_fx.add_argument("--limit", type=int, default=10)

    p_wb = sub.add_parser("worldbank", help="Fetch World Bank Open Data v2 macro indicators")
    p_wb.add_argument("--country", default="USA", help="ISO3 country code (e.g. USA, CHN, DEU, WLD)")
    p_wb.add_argument("--indicator", default="NY.GDP.MKTP.KD.ZG", help="World Bank indicator code")
    p_wb.add_argument("--limit", type=int, default=5)

    p_sec = sub.add_parser("sec", help="Fetch official SEC EDGAR company filings by CIK")
    p_sec.add_argument("--cik", required=True, help="SEC CIK (e.g. 0000320193)")
    p_sec.add_argument("--form", default="", help="Optional form filter (e.g. 10-K, 10-Q, 8-K)")
    p_sec.add_argument("--limit", type=int, default=8)

    p_fda = sub.add_parser("openfda", help="Query US FDA Drugs@FDA approval & submission records")
    p_fda.add_argument("--query", required=True, help="Brand or generic drug name")
    p_fda.add_argument("--limit", type=int, default=5)

    p_ct = sub.add_parser("clinicaltrials", help="Query NIH ClinicalTrials.gov REST API v2")
    p_ct.add_argument("--query", required=True, help="Condition, drug, or sponsor query")
    p_ct.add_argument("--limit", type=int, default=5)

    p_eq = sub.add_parser("usgs-quake", help="Query USGS real-time earthquake GeoJSON feed")
    p_eq.add_argument("--min-mag", type=float, default=5.5)
    p_eq.add_argument("--limit", type=int, default=5)

    p_wx = sub.add_parser("weather", help="Fetch WMO/NOAA/DWD daily weather via Open-Meteo")
    p_wx.add_argument("--lat", type=float, required=True)
    p_wx.add_argument("--lon", type=float, required=True)
    p_wx.add_argument("--past-days", type=int, default=5)
    p_wx.add_argument("--forecast-days", type=int, default=5)

    p_kev = sub.add_parser("kev", help="Query CISA Known Exploited Vulnerabilities (KEV) JSON catalog")
    p_kev.add_argument("--keyword", default="")
    p_kev.add_argument("--limit", type=int, default=8)

    p_ax = sub.add_parser("arxiv", help="Search arXiv preprints sorted by newest submission date")
    p_ax.add_argument("--query", required=True)
    p_ax.add_argument("--limit", type=int, default=5)

    p_gh = sub.add_parser("github", help="Inspect GitHub latest release, tags, and recent Actions runs")
    p_gh.add_argument("--repo", required=True, help="owner/repo")

    p_pkg = sub.add_parser("pkg", help="Query PyPI or npm latest package version and publish timestamp")
    p_pkg.add_argument("--ecosystem", choices=["pypi", "npm"], required=True)
    p_pkg.add_argument("--name", required=True)

    p_hf = sub.add_parser("hf", help="Search HuggingFace Hub open-weight models and release timestamps")
    p_hf.add_argument("--search", required=True)
    p_hf.add_argument("--limit", type=int, default=8)

    p_ln = sub.add_parser("launches", help="Query Launch Library 2 upcoming orbital launch schedules")
    p_ln.add_argument("--search", default="")
    p_ln.add_argument("--limit", type=int, default=5)

    p_dl = sub.add_parser("defillama", help="Fetch DefiLlama protocol TVL and 7-day percentage change")
    p_dl.add_argument("--slug", required=True, help="DefiLlama protocol slug (e.g. aave, lido)")

    p_sn = sub.add_parser("snapshot", help="Fetch Snapshot DAO governance proposal tally and quorum progress")
    p_sn.add_argument("--id", required=True, help="Snapshot proposal ID")

    p_cs = sub.add_parser("crypto-spot", help="Fetch cross-checked Coinbase + Kraken live crypto spot")
    p_cs.add_argument("--base", default="BTC", help="Base ticker (e.g. BTC, ETH, SOL)")

    p_espn = sub.add_parser("espn", help="Fetch ESPN public sports news & injury updates")
    p_espn.add_argument("--sport", default="basketball")
    p_espn.add_argument("--league", default="nba")
    p_espn.add_argument("--keyword", default="")
    p_espn.add_argument("--limit", type=int, default=5)

    p_rss = sub.add_parser("rss", help="Parse any authoritative RSS 2.0 or Atom feed")
    p_rss.add_argument("--url", required=True)
    p_rss.add_argument("--keyword", default="")
    p_rss.add_argument("--limit", type=int, default=8)

    p_chk = sub.add_parser("check-url", help="Verify plain-HTTP / judge-readable accessibility of a URL")
    p_chk.add_argument("--url", required=True)
    p_chk.add_argument("--preview", type=int, default=0, help="Optional clean text preview character count")

    p_val = sub.add_parser("validate", help="Validate a research note, citation links, and attachments")
    p_val.add_argument("--note-file", required=True)
    p_val.add_argument("--link", action="append", default=[])
    p_val.add_argument("--file", action="append", default=[])
    p_val.add_argument("--max-items", type=int, default=3, help="Maximum combined items (0 = unlimited)")
    p_val.add_argument("--allow-secondary", action="store_true", help="Allow secondary odds/prediction-market URLs")
    p_val.add_argument("--check-links", action="store_true", help="Perform live plain-HTTP check on every link")

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == "list-sources":
            out = {"source_count": len(SOURCES_CATALOG), "sources": SOURCES_CATALOG}
        elif args.cmd == "fred":
            out = fetch_fred_series(
                args.series,
                limit=args.limit,
                target_yoy_pct=args.target_yoy,
                out_csv=args.out_csv,
                lookback_years=args.years,
            )
        elif args.cmd == "treasury":
            out = fetch_treasury_fiscal(args.dataset, args.limit)
        elif args.cmd == "fedreg":
            out = fetch_federal_register(args.term, args.limit)
        elif args.cmd == "ecb-fx":
            out = fetch_ecb_fx_rate(args.currency, args.limit)
        elif args.cmd == "worldbank":
            out = fetch_worldbank_indicator(args.country, args.indicator, args.limit)
        elif args.cmd == "sec":
            out = fetch_sec_edgar_filings(args.cik, args.form, args.limit)
        elif args.cmd == "openfda":
            out = fetch_openfda_drug_approvals(args.query, args.limit)
        elif args.cmd == "clinicaltrials":
            out = fetch_clinical_trials(args.query, args.limit)
        elif args.cmd == "usgs-quake":
            out = fetch_usgs_earthquakes(args.min_mag, args.limit)
        elif args.cmd == "weather":
            out = fetch_open_meteo_daily(args.lat, args.lon, args.past_days, args.forecast_days)
        elif args.cmd == "kev":
            out = fetch_cisa_kev(args.keyword, args.limit)
        elif args.cmd == "arxiv":
            out = fetch_arxiv_papers(args.query, args.limit)
        elif args.cmd == "github":
            out = fetch_github_state(args.repo)
        elif args.cmd == "pkg":
            out = fetch_package_registry(args.ecosystem, args.name)
        elif args.cmd == "hf":
            out = fetch_huggingface_model(args.search, args.limit)
        elif args.cmd == "launches":
            out = fetch_space_launches(args.search, args.limit)
        elif args.cmd == "defillama":
            out = fetch_defillama_protocol(args.slug)
        elif args.cmd == "snapshot":
            out = fetch_snapshot_proposal(args.id)
        elif args.cmd == "crypto-spot":
            out = fetch_crypto_spot(args.base)
        elif args.cmd == "espn":
            out = fetch_espn_news(args.sport, args.league, args.keyword, args.limit)
        elif args.cmd == "rss":
            out = fetch_rss_feed(args.url, args.keyword, args.limit)
        elif args.cmd == "check-url":
            out = check_url_readable(args.url, preview_chars=args.preview)
        elif args.cmd == "validate":
            with open(args.note_file, "r", encoding="utf-8") as fh:
                note_text = fh.read()
            out = validate_citation_bundle(
                note_text,
                args.link,
                args.file,
                check_links=args.check_links,
                max_items=args.max_items,
                strict_primary=not args.allow_secondary,
            )
        else:
            parser.error(f"Unknown command: {args.cmd}")
            return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc), "command": args.cmd}, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
