"""News feeds for any market: Google News RSS (every market), Yahoo Finance RSS (US tickers),
SEC EDGAR filings (US, via tradekit.sec). Parsing, tagging and "only what is new" state.

All sources are free and need no API key. Headlines are leads, not facts: the skill tells the
agent to open the story or filing before saying something happened.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Iterable, List, Optional, Tuple

from . import config, http

# Google News edition per exchange suffix: (gl country, hl language, ceid)
_EDITIONS = {
    "": ("US", "en-US", "US:en"),
    "NS": ("IN", "en-IN", "IN:en"), "BO": ("IN", "en-IN", "IN:en"),
    "L": ("GB", "en-GB", "GB:en"), "TO": ("CA", "en-CA", "CA:en"), "V": ("CA", "en-CA", "CA:en"),
    "AX": ("AU", "en-AU", "AU:en"), "HK": ("HK", "en-HK", "HK:en"), "SI": ("SG", "en-SG", "SG:en"),
    "T": ("JP", "en-US", "US:en"), "DE": ("DE", "en-US", "US:en"), "PA": ("FR", "en-US", "US:en"),
    "SA": ("BR", "en-US", "US:en"), "JO": ("ZA", "en-ZA", "ZA:en"), "NZ": ("NZ", "en-NZ", "NZ:en"),
}

# keyword -> tag. Order matters only for readability; an item can carry several tags.
TAGS: List[Tuple[str, Tuple[str, ...]]] = [
    ("earnings", ("earnings", "results", "quarter", "q1 ", "q2 ", "q3 ", "q4 ", "profit", "revenue", "eps",
                  "guidance", "outlook", "net income", "loss widens", "beats", "misses", "pat ")),
    ("analyst", ("upgrade", "downgrade", "price target", "target price", "rating", "initiates", "overweight",
                 "underweight", "outperform", "underperform", "brokerage")),
    ("deal", ("acquire", "acquisition", "merger", "merge", "takeover", "buyout", "stake", "deal ", "joint venture",
              "to buy ", "divest", "spin-off", "spinoff")),
    ("capital", ("dividend", "buyback", "repurchase", "split", "bonus issue", "rights issue", "offering", "ipo",
                 "qip", "placement", "fund raise", "fundraise", "debt", "bond")),
    ("people", ("ceo", "cfo", "chairman", "resigns", "steps down", "appoints", "appointed", "managing director")),
    ("legal", ("lawsuit", "sues", "sued", "probe", "investigation", "settlement", "court", "fraud", "penalty",
               "fine ", "antitrust")),
    ("regulatory", ("sec ", "sebi", "fda", "approval", "regulator", "license", "licence", "rbi", "ban ")),
    ("halt", ("halt", "suspended", "circuit", "delist", "trading suspension")),
    ("risk", ("bankruptcy", "insolvency", "default", "restatement", "going concern", "downgrade to junk",
              "recall", "outage", "cyber", "breach", "fire at", "strike at")),
    ("macro", ("fed ", "inflation", "rate cut", "rate hike", "gdp", "jobs report", "cpi", "tariff", "recession",
               "futures", "sensex", "nifty", "s&p 500", "dow jones")),
]


def suffix(symbol: str) -> str:
    s = symbol.split(":")[-1]
    return s.rsplit(".", 1)[1].upper() if "." in s and not s.startswith("^") else ""


def is_us(symbol: str) -> bool:
    s = symbol.split(":")[-1]
    return suffix(symbol) == "" and not s.startswith("^") and "=" not in s and "-USD" not in s.upper() and ":" not in symbol


def base_ticker(symbol: str) -> str:
    s = symbol.split(":")[-1]
    return s.rsplit(".", 1)[0] if suffix(symbol) else s


_TAG_RE = [(tag, re.compile(r"(?<![a-z0-9])(?:" + "|".join(re.escape(w.strip()) for w in words) + r")(?![a-z0-9])"))
           for tag, words in TAGS]


def tag_text(text: str) -> List[str]:
    low = text.lower()
    return [tag for tag, rx in _TAG_RE if rx.search(low)]


def _strip_html(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).replace("\xa0", " ").strip()


def parse_time(value: str) -> Optional[str]:
    """RFC 822 (RSS) or ISO 8601 (Atom) -> ISO UTC 'YYYY-MM-DDTHH:MM:SSZ'."""
    if not value:
        return None
    value = value.strip()
    try:
        t = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError):
        try:
            t = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_rss(text: str, source: str) -> List[Dict]:
    """RSS 2.0 or Atom -> [{id, title, link, published, summary, publisher, source}]."""
    text = text.lstrip("﻿")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        raise RuntimeError(f"{source}: feed is not valid XML ({e})") from None
    items: List[Dict] = []
    atom = "{http://www.w3.org/2005/Atom}"
    for it in root.iter("item"):
        title = _strip_html(it.findtext("title") or "")
        link = (it.findtext("link") or "").strip()
        pub_el = it.find("source")
        publisher = (pub_el.text or "").strip() if pub_el is not None and pub_el.text else ""
        if source == "google" and publisher and title.endswith(" - " + publisher):
            title = title[: -len(publisher) - 3].strip()
        guid = (it.findtext("guid") or link or title).strip()
        items.append({"id": f"{source}:{guid}", "title": title, "link": link,
                      "published": parse_time(it.findtext("pubDate") or ""),
                      "summary": _strip_html(it.findtext("description") or "")[:400] if source != "google" else "",
                      "publisher": publisher, "source": source})
    for e in root.iter(atom + "entry"):
        link_el = e.find(atom + "link")
        link = link_el.get("href", "") if link_el is not None else ""
        title = _strip_html(e.findtext(atom + "title") or "")
        items.append({"id": f"{source}:{(e.findtext(atom + 'id') or link).strip()}", "title": title, "link": link,
                      "published": parse_time(e.findtext(atom + "updated") or e.findtext(atom + "published") or ""),
                      "summary": _strip_html(e.findtext(atom + "summary") or "")[:400], "publisher": "",
                      "source": source})
    return items


def google_url(symbol: str, name: Optional[str] = None, days: int = 2) -> str:
    gl, hl, ceid = _EDITIONS.get(suffix(symbol), _EDITIONS[""])
    tick = base_ticker(symbol)
    terms = [f'"{tick}"']
    if name:
        clean = re.sub(r"\b(inc|ltd|limited|corp|corporation|plc|co|company|holdings|the)\b\.?", "", name,
                       flags=re.I)
        clean = re.sub(r"[^\w&' -]", " ", clean).strip()
        clean = re.sub(r"\s+", " ", clean)
        if clean and clean.lower() != tick.lower():
            terms.append(f'"{clean}"')
    q = "(" + " OR ".join(terms) + f") stock when:{max(1, int(days))}d"
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, "hl": hl, "gl": gl, "ceid": ceid})


def yahoo_url(symbol: str) -> str:
    return ("https://feeds.finance.yahoo.com/rss/2.0/headline?"
            + urllib.parse.urlencode({"s": symbol, "region": "US", "lang": "en-US"}))


def fetch(url: str, source: str) -> List[Dict]:
    raw = http.request("GET", url, headers={"Accept": "application/rss+xml, application/xml, text/xml, */*"})
    return parse_rss(raw.decode("utf-8", "replace"), source)


def relevant(item: Dict, symbol: str, name: Optional[str]) -> bool:
    """Google News search is fuzzy: keep items that mention the ticker or the company's first word."""
    if item["source"] != "google":
        return True
    text = (item["title"] + " " + item.get("summary", "")).lower()
    tick = base_ticker(symbol).lower()
    if re.search(r"(?<![a-z0-9])" + re.escape(tick) + r"(?![a-z0-9])", text):
        return True
    if name:
        first = re.split(r"[\s,.]+", name.strip())[0].lower()
        if len(first) >= 3 and first in text:
            return True
    return False


def dedupe(items: Iterable[Dict]) -> List[Dict]:
    """Same story syndicated many times: keep the earliest copy of each normalised title."""
    seen: Dict[str, Dict] = {}
    for it in sorted(items, key=lambda x: x.get("published") or ""):
        key = re.sub(r"[^a-z0-9]+", " ", it["title"].lower()).strip()[:90]
        if key and key not in seen:
            seen[key] = it
    return sorted(seen.values(), key=lambda x: x.get("published") or "", reverse=True)


def within(items: Iterable[Dict], hours: float, now: Optional[dt.datetime] = None) -> List[Dict]:
    now = now or dt.datetime.now(dt.timezone.utc)
    cut = (now - dt.timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [i for i in items if not i.get("published") or i["published"] >= cut]


# ---------------------------------------------------------------- "only what is new" state

def _state_file():
    return config.path("state", "news.json")


def load_seen() -> Dict[str, str]:
    f = _state_file()
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text()).get("seen", {})
    except json.JSONDecodeError:
        return {}


def item_key(item: Dict) -> str:
    return hashlib.sha1(item["id"].encode()).hexdigest()[:16]


def mark_seen(items: Iterable[Dict], keep_days: int = 30, now: Optional[dt.datetime] = None) -> None:
    now = now or dt.datetime.now(dt.timezone.utc)
    seen = load_seen()
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    for it in items:
        seen[item_key(it)] = stamp
    cut = (now - dt.timedelta(days=keep_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen = {k: v for k, v in seen.items() if v >= cut}
    _state_file().write_text(json.dumps({"seen": seen}, indent=0) + "\n")
