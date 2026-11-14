"""SEC EDGAR (US companies): ticker -> CIK, recent filings, XBRL quarterly facts, Form 4 insider trades.

SEC asks every automated client to identify itself with a name and an email address in the
User-Agent. Set it once with trading-setup (`setup.py set data.sec_user_agent "Your Name you@x.com"`)
or the SEC_USER_AGENT environment variable. Without it, SEC calls are skipped with a plain note.
SEC's fair-access limit is 10 requests a second; this client stays far below it.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from . import config, http

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"
FILING_INDEX_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/"

# 8-K items worth flagging (item -> plain words)
IMPORTANT_8K = {
    "1.01": "material agreement", "1.03": "bankruptcy", "1.05": "cybersecurity incident",
    "2.01": "acquisition or disposal completed", "2.02": "earnings results", "2.05": "restructuring costs",
    "2.06": "impairment", "3.01": "delisting notice", "4.01": "auditor change",
    "4.02": "past financials no longer reliable", "5.01": "change in control", "5.02": "officer or director change",
    "7.01": "Reg FD disclosure", "8.01": "other events",
}

FORM4_CODES = {
    "P": "open-market buy", "S": "open-market sale", "A": "grant or award", "M": "option exercise",
    "F": "shares withheld for tax", "G": "gift", "C": "conversion", "D": "returned to company",
    "X": "option exercise", "J": "other", "W": "inheritance", "I": "discretionary",
}

_last_call = [0.0]


class SECError(RuntimeError):
    pass


def user_agent() -> Optional[str]:
    ua = os.environ.get("SEC_USER_AGENT") or config.get_key(config.load(), "data.sec_user_agent")
    if ua and "@" in str(ua):
        return str(ua)
    return None


def require_ua() -> str:
    ua = user_agent()
    if not ua:
        raise SECError("SEC needs your name and email in the request header. Set it once: "
                       "setup.py set data.sec_user_agent \"Your Name you@example.com\" "
                       "(or the SEC_USER_AGENT environment variable)")
    return ua


def _get(url: str) -> bytes:
    ua = require_ua()
    wait = 0.15 - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.time()
    try:
        return http.request("GET", url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
    except http.HTTPError as e:
        if e.status == 403:
            raise SECError("SEC refused the request (403). Check data.sec_user_agent is 'Name email@domain'") from None
        if e.status == 404:
            raise SECError(f"not found on SEC: {url}") from None
        raise


def _cached_json(name: str, url: str, max_age_hours: float) -> Dict:
    f = config.path("cache", "sec", name)
    if f.exists() and (time.time() - f.stat().st_mtime) < max_age_hours * 3600:
        try:
            return json.loads(f.read_text())
        except json.JSONDecodeError:
            pass
    data = json.loads(_get(url).decode("utf-8"))
    f.write_text(json.dumps(data))
    return data


def cik_for(ticker: str, tickers: Optional[Dict] = None) -> Dict:
    t = ticker.upper().replace(".", "-")
    table = tickers if tickers is not None else _cached_json("company_tickers.json", TICKERS_URL, 24 * 7)
    for row in table.values():
        if str(row.get("ticker", "")).upper() == t:
            return {"cik": int(row["cik_str"]), "ticker": row["ticker"], "name": row.get("title", "")}
    raise SECError(f"{ticker}: not in SEC's ticker list (only US-listed companies file with the SEC)")


def submissions(cik: int) -> Dict:
    return _cached_json(f"submissions-{cik}.json", SUBMISSIONS_URL.format(cik=cik), 1)


def company_facts(cik: int) -> Dict:
    return _cached_json(f"companyfacts-{cik}.json", FACTS_URL.format(cik=cik), 12)


def recent_filings(subs: Dict, forms: Optional[List[str]] = None, since: Optional[str] = None) -> List[Dict]:
    r = (subs.get("filings") or {}).get("recent") or {}
    cik = int(subs.get("cik", 0) or 0)
    out = []
    for i, acc in enumerate(r.get("accessionNumber", [])):
        form = r["form"][i]
        if forms and form not in forms:
            continue
        filed = r["filingDate"][i]
        if since and filed < since:
            continue
        items = [x.strip() for x in (r.get("items", [""] * (i + 1))[i] or "").split(",") if x.strip()]
        doc = r.get("primaryDocument", [""] * (i + 1))[i]
        acc_nd = acc.replace("-", "")
        out.append({
            "form": form, "filed": filed, "accepted": (r.get("acceptanceDateTime") or [""] * (i + 1))[i],
            "report_date": (r.get("reportDate") or [""] * (i + 1))[i], "accession": acc, "items": items,
            "important": [f"{it} {IMPORTANT_8K[it]}" for it in items if it in IMPORTANT_8K and it not in ("7.01", "8.01")],
            "document": doc,
            "url": ARCHIVE_URL.format(cik=cik, acc=acc_nd, doc=doc) if doc else FILING_INDEX_URL.format(cik=cik, acc=acc_nd),
            "index_url": FILING_INDEX_URL.format(cik=cik, acc=acc_nd),
        })
    return out


# ---------------------------------------------------------------- XBRL quarterly facts

REVENUE = ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet",
           "RevenueFromContractWithCustomerIncludingAssessedTax", "RevenuesNetOfInterestExpense")
CONCEPTS = {
    "revenue": REVENUE,
    "gross_profit": ("GrossProfit",),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss", "ProfitLoss"),
    "eps": ("EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted", "EarningsPerShareBasic"),
}


def _days(a: str, b: str) -> int:
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def _series(facts: Dict, names, unit_hint: str) -> Dict[str, Dict[str, float]]:
    """{'Q': {end: val}, 'FY': {end: val}, 'Q_start': {end: start}} from the first concept that has data."""
    gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    best: Dict[str, Dict] = {"Q": {}, "FY": {}, "start": {}}
    for name in names:
        units = (gaap.get(name) or {}).get("units") or {}
        unit = next((u for u in units if u == unit_hint), None) or next(iter(units), None)
        if not unit:
            continue
        q: Dict[str, tuple] = {}
        fy: Dict[str, tuple] = {}
        for f in units[unit]:
            if not f.get("start") or f.get("form") not in ("10-Q", "10-K", "10-Q/A", "10-K/A", "20-F", "40-F"):
                continue
            span = _days(f["start"], f["end"])
            key = f["end"]
            rec = (f.get("filed", ""), float(f["val"]), f["start"])
            if 80 <= span <= 100:
                if key not in q or rec[0] > q[key][0]:
                    q[key] = rec
            elif 350 <= span <= 380:
                if key not in fy or rec[0] > fy[key][0]:
                    fy[key] = rec
        if len(q) > len(best["Q"]):
            best = {"Q": {k: v[1] for k, v in q.items()}, "FY": {k: v[1] for k, v in fy.items()},
                    "start": {k: v[2] for k, v in fy.items()}, "concept": name, "filed": {k: v[0] for k, v in q.items()}}
    return best


def quarters_from_facts(facts: Dict, limit: int = 12) -> List[Dict]:
    """Quarterly rows from XBRL company facts. A fourth quarter is the 10-K year minus the three
    quarters inside it (companies file no Q4 10-Q); those rows are marked derived."""
    series = {k: _series(facts, v, "USD/shares" if k == "eps" else "USD") for k, v in CONCEPTS.items()}
    ends = set()
    for s in series.values():
        ends |= set(s["Q"])
    # derive Q4 from the fiscal year
    rev = series["revenue"]
    derived_ends = set()
    for fy_end, fy_start in rev.get("start", {}).items():
        inside = sorted(e for e in rev["Q"] if fy_start < e < fy_end and _days(fy_start, e) > 60)
        if len(inside) == 3 and fy_end not in rev["Q"]:
            derived_ends.add(fy_end)
    rows = []
    for end in sorted(ends | derived_ends):
        row = {"period_end": end, "derived": end in derived_ends, "currency": "USD"}
        for k, s in series.items():
            if end in s["Q"]:
                row[k] = s["Q"][end]
            elif end in s.get("FY", {}) and s.get("start"):
                fy_start = s["start"][end]
                inside = [s["Q"][e] for e in s["Q"] if fy_start < e < end and _days(fy_start, e) > 60]
                row[k] = s["FY"][end] - sum(inside) if len(inside) == 3 else None
            else:
                row[k] = None
        rows.append(row)
    rows = [r for r in rows if r.get("revenue") is not None or r.get("net_income") is not None]
    return rows[-limit:]


# ---------------------------------------------------------------- Form 4 (insider trades)

def _v(node, path: str) -> Optional[str]:
    el = node.find(path)
    if el is None:
        return None
    val = el.find("value")
    txt = (val.text if val is not None else el.text) or ""
    return txt.strip() or None


def parse_form4(xml_text: str) -> Dict:
    """Parse an SEC ownership document (Form 3/4/5 XML) into owner + transaction rows."""
    root = ET.fromstring(xml_text.strip().encode("utf-8"))
    issuer = {"name": root.findtext("issuer/issuerName", "").strip(),
              "ticker": root.findtext("issuer/issuerTradingSymbol", "").strip()}
    owners = []
    for ro in root.findall("reportingOwner"):
        rel = ro.find("reportingOwnerRelationship")
        roles = []
        if rel is not None:
            if (rel.findtext("isDirector") or "").strip() in ("1", "true"):
                roles.append("director")
            if (rel.findtext("isOfficer") or "").strip() in ("1", "true"):
                roles.append((rel.findtext("officerTitle") or "officer").strip())
            if (rel.findtext("isTenPercentOwner") or "").strip() in ("1", "true"):
                roles.append("10% owner")
            if (rel.findtext("isOther") or "").strip() in ("1", "true"):
                roles.append((rel.findtext("otherText") or "other").strip())
        owners.append({"name": ro.findtext("reportingOwnerId/rptOwnerName", "").strip(), "roles": roles})
    rows = []
    for table, kind in (("nonDerivativeTable/nonDerivativeTransaction", "stock"),
                        ("derivativeTable/derivativeTransaction", "derivative")):
        for t in root.findall(table):
            code = (t.findtext("transactionCoding/transactionCode") or "").strip()
            shares = _v(t, "transactionAmounts/transactionShares")
            price = _v(t, "transactionAmounts/transactionPricePerShare")
            rows.append({
                "kind": kind, "security": _v(t, "securityTitle") or "", "date": _v(t, "transactionDate"),
                "code": code, "meaning": FORM4_CODES.get(code, code),
                "acquired_disposed": _v(t, "transactionAmounts/transactionAcquiredDisposedCode"),
                "shares": float(shares) if shares else None, "price": float(price) if price else None,
                "value": round(float(shares) * float(price), 2) if shares and price else None,
                "owned_after": float(_v(t, "postTransactionAmounts/sharesOwnedFollowingTransaction") or 0) or None,
                "direct": (_v(t, "ownershipNature/directOrIndirectOwnership") or "D") == "D",
            })
    return {"issuer": issuer, "owners": owners, "period": root.findtext("periodOfReport", "").strip(),
            "transactions": rows}


def form4_xml_url(cik_issuer: int, filing: Dict) -> str:
    """The raw XML of a Form 4 (primaryDocument often points at the XSL-rendered HTML view)."""
    doc = filing.get("document") or ""
    doc = re.sub(r"^xslF345X\d+/", "", doc)
    return ARCHIVE_URL.format(cik=cik_issuer, acc=filing["accession"].replace("-", ""), doc=doc)


def fetch_form4(cik_issuer: int, filing: Dict) -> Dict:
    return parse_form4(_get(form4_xml_url(cik_issuer, filing)).decode("utf-8", "replace"))
