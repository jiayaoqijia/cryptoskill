"""Public trade disclosures.

US Congress (House)  The House Clerk's yearly index of financial disclosures and each Periodic
                     Transaction Report (PTR) PDF. STOCK Act: a trade must be reported within 45 days.
India bulk / block   NSE's daily bulk-deal and block-deal files: any client trading over 0.5% of a
                     company's shares in a day (bulk), or a single trade of 5 lakh shares / Rs 10 crore
                     or more in the block window (block).

PDF text is extracted with the standard library (Flate streams, ToUnicode maps, RC4 encryption
used by the Clerk's PDFs). If a PDF uses something this reader cannot decode, the skill tells the
agent to open the saved PDF directly.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import re
import xml.etree.ElementTree as ET
import zipfile
import zlib
from typing import Dict, List, Optional

HOUSE_INDEX_URL = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
HOUSE_PTR_URL = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc}.pdf"
SENATE_SEARCH_URL = "https://efdsearch.senate.gov/search/"
NSE_BULK_URL = "https://archives.nseindia.com/content/equities/bulk.csv"
NSE_BLOCK_URL = "https://archives.nseindia.com/content/equities/block.csv"
NSE_PIT_PAGE = "https://www.nseindia.com/companies-listing/corporate-filings-insider-trading"

FILING_TYPES = {"P": "periodic transaction report", "A": "amendment", "C": "candidate report",
                "O": "annual report", "X": "extension", "W": "withdrawal", "D": "duplicate", "T": "termination"}
OWNERS = {"SP": "spouse", "JT": "joint", "DC": "dependent child", "": "member"}
TX_TYPES = {"P": "purchase", "S": "sale", "S (partial)": "partial sale", "E": "exchange"}
ASSET_TYPES = {"ST": "stock", "OP": "option", "GS": "government security", "CS": "corporate bond",
               "MF": "mutual fund", "EF": "ETF", "OT": "other", "PS": "stock (not public)", "RE": "real estate"}


# ---------------------------------------------------------------- PDF text (standard library)

_PAD = bytes.fromhex("28BF4E5E4E758A4164004E56FFFA01082E2E00B6D0683E802F0CA9FE6453697A")


def _rc4(key: bytes, data: bytes) -> bytes:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 255
        s[i], s[j] = s[j], s[i]
    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) & 255
        j = (j + s[i]) & 255
        s[i], s[j] = s[j], s[i]
        out.append(b ^ s[(s[i] + s[j]) & 255])
    return bytes(out)


def _file_key(d: bytes) -> Optional[bytes]:
    m = re.search(rb"/Encrypt\s+(\d+)\s+0\s+R", d)
    if not m:
        return None
    em = re.search(rb"[\r\n]%d\s+0\s+obj(.*?)endobj" % int(m.group(1)), d, re.S)
    if not em or b"/Standard" not in em.group(1):
        raise ValueError("this PDF uses an encryption this reader does not support")
    e = em.group(1)
    v = int(re.search(rb"/V\s+(\d+)", e).group(1))
    r = int(re.search(rb"/R\s+(\d+)", e).group(1))
    if v > 2 or r > 3:
        raise ValueError("this PDF uses AES encryption, which the standard library cannot decode")
    owner = bytes.fromhex(re.search(rb"/O\s*<([0-9A-Fa-f]+)>", e).group(1).decode())
    perms = int(re.search(rb"/P\s+(-?\d+)", e).group(1))
    file_id = bytes.fromhex(re.search(rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>", d).group(1).decode())
    lm = re.search(rb"/Length\s+(\d+)", e)
    n = int(lm.group(1)) // 8 if (r >= 3 and lm) else 5
    h = hashlib.md5(_PAD + owner + (perms & 0xFFFFFFFF).to_bytes(4, "little") + file_id).digest()
    if r >= 3:
        for _ in range(50):
            h = hashlib.md5(h[:n]).digest()
    return h[:n]


def _objects(d: bytes) -> Dict[int, tuple]:
    out: Dict[int, tuple] = {}
    key = _file_key(d)
    for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", d, re.S):
        body, stream = m.group(2), None
        sm = re.search(rb"stream\r?\n(.*?)\r?\nendstream", body, re.S)
        if sm:
            raw = sm.group(1)
            if key:
                okey = hashlib.md5(key + int(m.group(1)).to_bytes(3, "little") + b"\x00\x00").digest()
                raw = _rc4(okey[: min(len(key) + 5, 16)], raw)
            if b"FlateDecode" in body[: sm.start()]:
                try:
                    raw = zlib.decompress(raw)
                except zlib.error:
                    raw = b""
            stream, body = raw, body[: sm.start()]
        out[int(m.group(1))] = (body, stream)
    return out


def _cmap(data: bytes) -> Dict[int, str]:
    m: Dict[int, str] = {}
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
        for a, b in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            m[int(a, 16)] = bytes.fromhex(b.decode()).decode("utf-16-be", "replace")
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
        for a, b, c in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            start = int(c, 16)
            for i, code in enumerate(range(int(a, 16), int(b, 16) + 1)):
                m[code] = chr(start + i)
    return m


_TOKENS = re.compile(rb"/(\w+)\s+[\d.]+\s+Tf|([-\d.]+)\s+([-\d.]+)\s+Td|[\d.-]+ [\d.-]+ [\d.-]+ [\d.-]+ ([\d.-]+) ([\d.-]+) Tm"
                     rb"|<([0-9A-Fa-f]*)>\s*Tj|\(((?:\\.|[^\\)])*)\)\s*Tj")


def pdf_text(data: bytes) -> str:
    """Text lines of a PDF, in drawing order. Good for form-like reports; not a general PDF engine."""
    if not data.startswith(b"%PDF"):
        raise ValueError("not a PDF file")
    objs = _objects(data)
    fonts: Dict[str, tuple] = {}
    for body, _ in objs.values():
        for name, ref in re.findall(rb"/(\w+)\s+(\d+)\s+0\s+R", body):
            ob = objs.get(int(ref))
            if ob and re.search(rb"/Type\s*/Font", ob[0]):
                tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", ob[0])
                width = 4 if re.search(rb"/Subtype\s*/Type0", ob[0]) else 2   # composite fonts: 2-byte codes
                cmap = _cmap(objs[int(tu.group(1))][1] or b"") if tu and int(tu.group(1)) in objs else {}
                fonts[name.decode()] = (cmap, width)
    lines: List[str] = []
    for _, stream in objs.values():
        if not stream or b"BT" not in stream:
            continue
        font: Dict[int, str] = {}
        width = 2
        cur: List[str] = []
        for tok in _TOKENS.finditer(stream):
            if tok.group(1):
                font, width = fonts.get(tok.group(1).decode(), ({}, 2))
            elif tok.group(2) is not None:
                if abs(float(tok.group(3))) > 0.5 and cur:
                    lines.append("".join(cur))
                    cur = []
            elif tok.group(4) is not None:
                if cur:
                    lines.append("".join(cur))
                    cur = []
            elif tok.group(6) is not None:
                h = tok.group(6).decode()
                cur.append("".join(font.get(int(h[i:i + width], 16), "") if font else chr(int(h[i:i + width], 16))
                                   for i in range(0, len(h), width)))
            elif tok.group(7) is not None:
                cur.append(re.sub(rb"\\(.)", rb"\1", tok.group(7)).decode("latin-1"))
        if cur:
            lines.append("".join(cur))
    text = "\n".join(ln.rstrip() for ln in lines if ln.strip())
    return re.sub(r"[\x00-\x08\x0b-\x1f]", "", text)


# ---------------------------------------------------------------- House Clerk index + PTRs

def _date(us: str) -> Optional[str]:
    try:
        return dt.datetime.strptime(us.strip(), "%m/%d/%Y").date().isoformat()
    except (ValueError, AttributeError):
        return None


def parse_house_index(zip_bytes: bytes) -> List[Dict]:
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        name = next((n for n in z.namelist() if n.lower().endswith(".xml")), None)
        if not name:
            raise ValueError("House index zip has no XML file")
        root = ET.fromstring(z.read(name))
    rows = []
    for m in root.iter("Member"):
        first, last = (m.findtext("First") or "").strip(), (m.findtext("Last") or "").strip()
        rows.append({
            "name": " ".join(x for x in ((m.findtext("Prefix") or "").strip(), first, last,
                                         (m.findtext("Suffix") or "").strip()) if x),
            "first": first, "last": last, "district": (m.findtext("StateDst") or "").strip(),
            "type": (m.findtext("FilingType") or "").strip(), "filed": _date(m.findtext("FilingDate") or ""),
            "doc_id": (m.findtext("DocID") or "").strip(), "year": (m.findtext("Year") or "").strip(),
        })
    return rows


def member_matches(row: Dict, query: str) -> bool:
    q = query.strip().lower().replace(",", " ")
    parts = [p for p in q.split() if p]
    hay = f"{row['first']} {row['last']}".lower()
    return all(p in hay for p in parts)


def ptr_url(row: Dict) -> str:
    return HOUSE_PTR_URL.format(year=row.get("year") or (row.get("filed") or "")[:4], doc=row["doc_id"])


_ROW = re.compile(
    r"(?P<asset>[^\[]+?)\s*\[(?P<atype>[A-Z]{2})\]\s+"
    r"(?P<tx>S \(partial\)|P|S|E)\s+(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<notified>\d{2}/\d{2}/\d{4})\s+"
    r"(?P<amount>\$[\d,]+\s*-\s*\$[\d,]+|Over \$[\d,]+|\$[\d,]+)")
_STATUS = re.compile(r"F\s*S\s*:\s*(?:New|Amended)\s*")
_DESC = re.compile(r"^\s*D\s*:\s*")
_OWNER = re.compile(r"(?:^|\s)(SP|JT|DC)\s+")
_PAGE = re.compile(r"Filing ID #\d+\s+ID\s+Owner\s+Asset.*?\$200\?")
_OPTION = re.compile(r"(?P<n>[\d,]+)\s+(?P<kind>call|put)\s+options?.*?strike price of \$(?P<strike>[\d,.]+)"
                     r"(?:.*?expiration date of (?P<exp>\d{1,2}/\d{1,2}/\d{2,4}))?", re.I)


def _split_lead(raw: str):
    """Text before a row's asset type marker = [previous row's status + description] [owner] asset."""
    desc = ""
    rest = raw.strip()
    m = _STATUS.search(rest)
    if m:
        rest = rest[m.end():]
        dm = _DESC.match(rest)
        if dm:
            rest = rest[dm.end():]
            owners = list(_OWNER.finditer(rest))
            if owners:
                desc, rest = rest[:owners[-1].start()], rest[owners[-1].start():]
            else:
                cut = rest.rfind(". ")
                desc, rest = (rest[:cut + 1], rest[cut + 2:]) if cut >= 0 else ("", rest)
    om = re.match(r"\s*(SP|JT|DC)\s+", rest)
    owner = om.group(1) if om else ""
    if om:
        rest = rest[om.end():]
    return desc.strip(), owner, rest.strip()


def _tail_desc(tail: str) -> str:
    m = _STATUS.search(tail)
    if not m:
        return ""
    t = tail[m.end():]
    dm = _DESC.match(t)
    return t[dm.end():].strip() if dm else ""


def parse_ptr(text: str, filed: Optional[str] = None) -> Dict:
    """Rows of a House PTR from its text (this module's pdf_text, or `pdftotext -layout` output)."""
    text = re.sub(r"[\x00-\x08\x0b-\x1f]", "", text)
    head: Dict = {}
    m = re.search(r"Name:\s*(.+)", text)
    if m:
        head["member"] = m.group(1).strip()
    m = re.search(r"State/District:\s*(\S+)", text)
    if m:
        head["district"] = m.group(1).strip()
    m = re.search(r"Filing ID #(\d+)", text)
    if m:
        head["doc_id"] = m.group(1)
    m = re.search(r"Digitally Signed:.*?(\d{2}/\d{2}/\d{4})", text, re.S)
    filed = filed or (_date(m.group(1)) if m else None)
    head["filed"] = filed
    start = text.find("$200?")
    body = text[start + 5:] if start >= 0 else text
    end = body.find("* For the complete list")
    if end >= 0:
        body = body[:end]
    flat = _PAGE.sub(" ", re.sub(r"\s+", " ", body))
    matches = list(_ROW.finditer(flat))
    rows: List[Dict] = []
    for i, mm in enumerate(matches):
        desc_prev, owner, asset = _split_lead(mm.group("asset"))
        if rows and desc_prev:
            rows[-1]["description"] = desc_prev
        tk = re.findall(r"\(([A-Z][A-Z.\-]{0,6})\)", asset)
        trade = _date(mm.group("date"))
        row = {
            "owner": OWNERS.get(owner, owner), "asset": re.sub(r"\s+", " ", asset), "ticker": tk[-1] if tk else None,
            "asset_type": ASSET_TYPES.get(mm.group("atype"), mm.group("atype")),
            "type": TX_TYPES.get(mm.group("tx"), mm.group("tx")), "trade_date": trade,
            "notified": _date(mm.group("notified")), "amount": re.sub(r"\s+", " ", mm.group("amount")),
            "description": "",
        }
        if trade and filed:
            row["days_to_disclose"] = (dt.date.fromisoformat(filed) - dt.date.fromisoformat(trade)).days
            row["late"] = row["days_to_disclose"] > 45
        rows.append(row)
    if rows:
        rows[-1]["description"] = _tail_desc(flat[matches[-1].end():])
    for row in rows:
        om = _OPTION.search(row["description"])
        if om:
            row["option"] = {"contracts": int(om.group("n").replace(",", "")), "kind": om.group("kind").lower(),
                             "strike": float(om.group("strike").replace(",", "")), "expires": om.group("exp")}
    head["rows"] = rows
    return head


# ---------------------------------------------------------------- NSE bulk / block deals (India)

def parse_nse_deals(text: str, kind: str) -> List[Dict]:
    rows = []
    rdr = csv.reader(io.StringIO(text.lstrip("﻿")))
    header = None
    for rec in rdr:
        if not rec or not any(c.strip() for c in rec):
            continue
        if header is None:
            header = [h.strip().lower() for h in rec]
            continue
        r = dict(zip(header, (c.strip() for c in rec)))
        if not r.get("symbol"):
            continue
        try:
            date = dt.datetime.strptime(r.get("date", ""), "%d-%b-%Y").date().isoformat()
        except ValueError:
            date = r.get("date")
        qty = float((r.get("quantity traded") or "0").replace(",", "") or 0)
        price = float((r.get("trade price / wght. avg. price") or r.get("trade price") or "0").replace(",", "") or 0)
        rows.append({"kind": kind, "date": date, "symbol": r["symbol"], "yahoo": r["symbol"] + ".NS",
                     "company": r.get("security name", ""), "client": r.get("client name", ""),
                     "side": (r.get("buy/sell") or "").upper(), "qty": qty, "price": price,
                     "value": round(qty * price, 2), "remarks": "" if r.get("remarks") in ("-", None) else r["remarks"]})
    return rows


def crore(v: float) -> str:
    return f"Rs {v / 1e7:,.2f} cr"


# ---------------------------------------------------------------- SEBI insider trades (India), user-downloaded CSV

_PIT_COLS = {
    "symbol": ("symbol",),
    "company": ("company",),
    "person": ("name of the acquirer", "acquirer/disposer", "acquirer / disposer", "name of person"),
    "category": ("category of person", "category"),
    "qty": ("no. of securities (acquired", "no. of security (acquired", "number of securities acquired",
            "securities acquired/disposed", "no of securities"),
    "value": ("value of security (acquired", "value of securities (acquired", "value of security", "value"),
    "type": ("acquisition/disposal transaction type", "transaction type", "acq/disp"),
    "mode": ("mode of acquisition", "mode"),
    "date_from": ("date of allotment/acquisition from", "acquisition from", "date from"),
    "date_to": ("date of allotment/acquisition to", "acquisition to", "date to"),
    "intimated": ("date of intimation to company", "intimation to company", "broadcast date", "date of intimation"),
}


def _num(s: str) -> Optional[float]:
    s = (s or "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return None


def _any_date(s: str) -> Optional[str]:
    s = (s or "").strip()
    for fmt in ("%d-%b-%Y", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%b-%Y %H:%M", "%d-%b-%Y %H:%M:%S"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return s or None


def parse_nse_pit_csv(text: str) -> List[Dict]:
    """Insider trades (SEBI PIT disclosures) from the CSV the user downloads on nseindia.com.
    NSE blocks automated access to its site, so the user downloads the file and the skill reads it.
    Columns are matched by name, so small header changes on NSE's side do not break it."""
    rdr = list(csv.reader(io.StringIO(text.lstrip("﻿"))))
    if not rdr:
        return []
    header = [re.sub(r"\s+", " ", h.strip().lower()) for h in rdr[0]]
    idx: Dict[str, int] = {}
    for key, pats in _PIT_COLS.items():
        for pat in pats:
            hit = next((i for i, h in enumerate(header) if pat in h and i not in idx.values()), None)
            if hit is not None:
                idx[key] = hit
                break
    if "symbol" not in idx or "person" not in idx:
        raise ValueError("this does not look like NSE's insider-trading CSV (no symbol / acquirer columns)")
    rows = []
    for rec in rdr[1:]:
        if not rec or not any(c.strip() for c in rec):
            continue
        get = lambda k: rec[idx[k]].strip() if k in idx and idx[k] < len(rec) else ""  # noqa: E731
        typ = get("type")
        side = "buy" if re.search(r"buy|acqui|purchase", typ, re.I) else "sell" if re.search(r"sell|sale|dispos", typ, re.I) else typ.lower()
        rows.append({"symbol": get("symbol"), "yahoo": get("symbol") + ".NS", "company": get("company"),
                     "person": get("person"), "category": get("category"), "side": side, "type": typ,
                     "qty": _num(get("qty")), "value": _num(get("value")), "mode": get("mode"),
                     "date_from": _any_date(get("date_from")), "date_to": _any_date(get("date_to")),
                     "intimated": _any_date(get("intimated"))})
    return rows
