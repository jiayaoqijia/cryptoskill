#!/usr/bin/env python3
"""verify_bib.py -- check every BibTeX entry against IACR ePrint / Crossref / DBLP.

Why: fabricated or garbled references (invented co-authors, placeholder
"Chen and others", wrong venue, a key pointing at a different paper) are a
research-integrity problem and an instant credibility loss with reviewers.
LLM-drafted bibliographies are especially prone to this.  This script is the
mechanical half of the `bib-verify` gate; the human/agent half is reading the
flagged entries.

Usage
-----
    python3 verify_bib.py refs.bib                       # Markdown report on stdout
    python3 verify_bib.py refs.bib --json report.json    # + machine-readable report
    python3 verify_bib.py refs.bib --offline             # static lint only
    python3 verify_bib.py refs.bib --only key1,key2      # re-check a few entries
    python3 verify_bib.py --selftest

Resolution order per entry
--------------------------
1. ePrint id (from `eprint=`, `url=`, `howpublished=`, `note=`, `journal=` text
   such as "Cryptology ePrint Archive, Paper 2018/421")  ->  ePrint OAI-PMH record.
2. `doi=`  ->  Crossref /works/<doi>, falling back to DataCite (Zenodo, LIPIcs, arXiv DOIs).
3. otherwise title search: DBLP (if reachable) then Crossref bibliographic query.

Each entry gets a status:
  VERIFIED     title similarity >= 0.90 and >= 1 author surname overlap (and year +-1 if given)
  MISMATCH     a record was found for the id/DOI but title or authors disagree
  WEAK         best title-search hit is similar but not conclusive (0.75..0.90) -> check by hand
  NOT_FOUND    nothing plausible found -> treat as fabricated until proven otherwise
  UNCHECKED    offline / service error
plus static LINT flags (placeholder authors, "and others" only, missing year/title,
`% UNVERIFIED` marker in the .bib, duplicate titles, ...).

Exit status: 0 if every entry is VERIFIED (lint warnings allowed), 1 if any entry
is MISMATCH/NOT_FOUND/WEAK/UNCHECKED, 3 on usage errors.  Use it as a gate.
"""
from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "crypto-research-agents/0.1 bib-verify (low rate; mailto not set)"
EPRINT_OAI = ("https://eprint.iacr.org/oai?verb=GetRecord&identifier=oai:eprint.iacr.org:{id}"
              "&metadataPrefix=oai_dc")
CROSSREF = "https://api.crossref.org/works"
DATACITE = "https://api.datacite.org/dois"
DBLP = "https://dblp.org/search/publ/api"
EPRINT_ID = re.compile(r"(?:eprint\.iacr\.org/|ePrint Archive,?\s*(?:Paper|Report)?\s*|^)"
                       r"((?:19|20)\d{2})/(\d{1,5})\b", re.I)


# ------------------------------------------------------------- bib parsing ---

def parse_bib(text: str) -> list[dict]:
    """Small dependency-free BibTeX parser (handles nested braces and quotes).

    Returns dicts with keys: type, key, fields (lower-cased names), unverified_marker.
    A line `% UNVERIFIED` directly above an entry sets unverified_marker=True.
    """
    entries = []
    i, n = 0, len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*([{(])", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        if etype in ("comment", "preamble", "string"):
            i = at + m.end()
            continue
        preceding = text[text.rfind("\n", 0, max(0, text.rfind("\n", 0, at))) + 1:at]
        marker = "UNVERIFIED" in preceding.upper()
        j = at + m.end()
        depth, k = 1, j
        while k < n and depth:
            c = text[k]
            if c in "{(":
                depth += 1
            elif c in "})":
                depth -= 1
            k += 1
        body = text[j:k - 1]
        key, _, rest = body.partition(",")
        fields = {}
        p = 0
        while p < len(rest):
            fm = re.match(r"\s*([\w\-:]+)\s*=\s*", rest[p:])
            if not fm:
                break
            name = fm.group(1).lower()
            p += fm.end()
            if p < len(rest) and rest[p] == "{":
                d, q = 1, p + 1
                while q < len(rest) and d:
                    d += {"{": 1, "}": -1}.get(rest[q], 0)
                    q += 1
                val = rest[p + 1:q - 1]
                p = q
            elif p < len(rest) and rest[p] == '"':
                q = p + 1
                while q < len(rest) and not (rest[q] == '"' and rest[q - 1] != "\\"):
                    q += 1
                val = rest[p + 1:q]
                p = q + 1
            else:
                vm = re.match(r"[^,]*", rest[p:])
                val = vm.group(0).strip()
                p += vm.end()
            fields[name] = re.sub(r"\s+", " ", val).strip()
            cm = re.match(r"\s*,", rest[p:])
            if cm:
                p += cm.end()
        entries.append({"type": etype, "key": key.strip(), "fields": fields,
                        "unverified_marker": marker})
        i = k
    return entries


# ----------------------------------------------------------- normalisation ---

_LATEX_ACCENT = re.compile(r"\\[`'^\"~=.uvHtcdbk]\s*\{?\s*([A-Za-z])\s*\}?")


def delatex(s: str) -> str:
    s = _LATEX_ACCENT.sub(r"\1", s or "")
    s = re.sub(r"\\(ss|o|O|l|L|aa|AA|ae|AE)\b", lambda m: {"ss": "ss", "o": "o", "O": "O", "l": "l",
                                                        "L": "L", "aa": "a", "AA": "A",
                                                        "ae": "ae", "AE": "AE"}[m.group(1)], s)
    s = re.sub(r"\$[^$]*\$", " ", s)            # math in titles
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ")
    s = unicodedata.normalize("NFKD", html.unescape(s))
    return "".join(c for c in s if not unicodedata.combining(c))


def norm_title(s: str) -> str:
    s = delatex(s).lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_sim(a: str, b: str) -> float:
    a, b = norm_title(a), norm_title(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    # tolerate a subtitle present on one side only
    if a.startswith(b) or b.startswith(a):
        short = min(len(a), len(b))
        if short >= 25:
            return 0.93
    return difflib.SequenceMatcher(None, a, b).ratio()


def surnames_from_bib(author_field: str) -> list[str]:
    out = []
    for a in re.split(r"\s+and\s+", delatex(author_field or "")):
        a = a.strip()
        if not a or a.lower() in ("others", "et al", "et al."):
            continue
        last = a.split(",")[0] if "," in a else a.split()[-1]
        out.append(norm_title(last).replace(" ", ""))
    return [x for x in out if x]


def surname_of(full: str) -> str:
    full = delatex(full).strip()
    if "," in full:
        return norm_title(full.split(",")[0]).replace(" ", "")
    return norm_title(full.split()[-1] if full.split() else "").replace(" ", "")


# ---------------------------------------------------------------- services ---

class Blocked(OSError):
    pass


def http_get(url: str, timeout: float = 25.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_eprint(eid: str) -> dict | None:
    xml = http_get(EPRINT_OAI.format(id=eid))
    if "<dc:title>" not in xml:
        return None
    title = html.unescape(re.search(r"<dc:title>(.*?)</dc:title>", xml, re.S).group(1)).strip()
    authors = [html.unescape(x).strip() for x in re.findall(r"<dc:creator>(.*?)</dc:creator>", xml, re.S)]
    date = re.search(r"<dc:date>(\d{4})", xml)
    return {"title": title, "authors": authors, "year": int(eid.split("/")[0]),
            "last_year": int(date.group(1)) if date else None, "source": f"ePrint {eid}"}


def fetch_crossref_doi(doi: str) -> dict | None:
    """Crossref first; DataCite for DOIs Crossref does not know (Zenodo, LIPIcs, arXiv...)."""
    try:
        data = json.loads(http_get(f"{CROSSREF}/{urllib.parse.quote(doi)}"))
        return _crossref_item(data.get("message", {}))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    try:
        data = json.loads(http_get(f"{DATACITE}/{urllib.parse.quote(doi)}"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    at = data.get("data", {}).get("attributes", {})
    names = []
    for c in at.get("creators", []):
        if c.get("givenName") or c.get("familyName"):
            names.append(f"{c.get('givenName', '')} {c.get('familyName', '')}".strip())
        else:
            nm = c.get("name", "")
            names.append(" ".join(reversed(nm.split(", "))) if ", " in nm else nm)
    return {"title": " ".join(t.get("title", "") for t in at.get("titles", [])[:1]),
            "authors": names, "year": at.get("publicationYear"),
            "venue": at.get("publisher", ""), "source": f"DataCite doi:{doi}"}


def _crossref_item(it: dict) -> dict:
    year = None
    for k in ("published-print", "published-online", "issued"):
        dp = (it.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    return {"title": " ".join(it.get("title") or []),
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in it.get("author", [])],
            "year": year, "venue": " ".join(it.get("container-title") or []),
            "source": f"Crossref doi:{it.get('DOI', '')}"}


def search_crossref(title: str, author_hint: str) -> list[dict]:
    q = {"query.bibliographic": title, "rows": 5,
         "select": "title,author,DOI,issued,published-print,published-online,container-title"}
    if author_hint:
        q["query.author"] = author_hint
    data = json.loads(http_get(f"{CROSSREF}?{urllib.parse.urlencode(q)}"))
    return [_crossref_item(it) for it in data.get("message", {}).get("items", [])]


def search_dblp(title: str) -> list[dict]:
    raw = http_get(f"{DBLP}?{urllib.parse.urlencode({'q': title, 'format': 'json', 'h': 5})}")
    if raw.lstrip().startswith("<"):
        raise Blocked("DBLP bot challenge")
    out = []
    for h in json.loads(raw).get("result", {}).get("hits", {}).get("hit") or []:
        info = h.get("info", {})
        au = info.get("authors", {}).get("author", [])
        au = au if isinstance(au, list) else [au]
        out.append({"title": html.unescape(info.get("title", "")).rstrip("."),
                    "authors": [re.sub(r"\s+\d{4}$", "", a.get("text", "") if isinstance(a, dict) else str(a))
                                for a in au],
                    "year": int(info.get("year", 0) or 0) or None,
                    "venue": info.get("venue", "") if isinstance(info.get("venue"), str) else "",
                    "source": f"DBLP {info.get('key', '')}"})
    return out


# ---------------------------------------------------------------- checking ---

def find_eprint_id(f: dict) -> str | None:
    for k in ("eprint", "url", "howpublished", "note", "journal", "booktitle", "publisher"):
        v = f.get(k, "")
        m = EPRINT_ID.search(v) if k != "eprint" else re.search(r"((?:19|20)\d{2})/(\d{1,5})", v)
        if m:
            return f"{m.group(1)}/{int(m.group(2)):03d}"
    return None


def lint(e: dict) -> list[str]:
    f, flags = e["fields"], []
    au = f.get("author", "")
    if not f.get("title"):
        flags.append("missing title")
    if not au and e["type"] not in ("misc", "book", "manual", "online"):
        flags.append("missing author")
    if re.fullmatch(r"\s*\{?\s*\w+\s+and\s+others\s*\}?\s*", au or ""):
        flags.append("placeholder author list ('X and others' only)")
    if re.search(r"\b(anonymous|author\d|firstname|lastname|tbd|todo|xxx)\b", au, re.I):
        flags.append("placeholder author name")
    if not f.get("year") and not f.get("date"):
        flags.append("missing year")
    if re.search(r"\b(tbd|todo|xxx|\?\?)\b", " ".join(f.values()), re.I):
        flags.append("TODO/TBD text in entry")
    if e["unverified_marker"]:
        flags.append("marked % UNVERIFIED in source")
    return flags


def judge(entry: dict, rec: dict | None, how: str) -> tuple[str, float, str]:
    f = entry["fields"]
    if rec is None:
        return "NOT_FOUND", 0.0, f"no record via {how}"
    ts = title_sim(f.get("title", ""), rec["title"])
    bib_s = set(surnames_from_bib(f.get("author", "")))
    rec_s = {surname_of(a) for a in rec["authors"]}
    overlap = len(bib_s & rec_s)
    missing = sorted(bib_s - rec_s)
    year_ok = True
    if f.get("year", "").strip()[:4].isdigit() and rec.get("year"):
        y = int(f["year"].strip()[:4])
        years = {rec["year"], rec.get("last_year") or rec["year"]}
        year_ok = any(abs(y - yy) <= 1 for yy in years if yy)
    detail = (f"{rec['source']}: \"{rec['title'][:80]}\"; title_sim={ts:.2f}; "
              f"author overlap {overlap}/{len(bib_s) or '?'}")
    if missing and bib_s:
        detail += f"; bib surnames not in record: {', '.join(missing)}"
    if not year_ok:
        detail += f"; year {f.get('year')} vs {rec.get('year')}"
    if ts >= 0.90 and (overlap >= 1 or not bib_s) and not missing and year_ok:
        return "VERIFIED", ts, detail
    if ts >= 0.90 and overlap >= 1 and year_ok and len(missing) <= max(0, len(bib_s) // 4):
        return "VERIFIED", ts, detail + " (minor author-name variance)"
    if how.startswith("id"):
        return "MISMATCH", ts, detail
    if ts >= 0.75:
        return "WEAK", ts, detail
    return "NOT_FOUND", ts, detail


def check_entry(e: dict, offline: bool, state: dict) -> dict:
    f = e["fields"]
    res = {"key": e["key"], "type": e["type"], "title": delatex(f.get("title", ""))[:120],
           "lint": lint(e), "status": "UNCHECKED", "score": 0.0, "detail": ""}
    if offline:
        res["detail"] = "offline mode"
        return res
    try:
        eid = find_eprint_id(f)
        if eid:
            res["status"], res["score"], res["detail"] = judge(e, fetch_eprint(eid), f"id ePrint {eid}")
            if res["status"] == "VERIFIED" or not f.get("doi"):
                return res
        if f.get("doi"):
            doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", f["doi"].strip())
            res["status"], res["score"], res["detail"] = judge(e, fetch_crossref_doi(doi), f"id doi {doi}")
            return res
        title = delatex(f.get("title", ""))
        if not title:
            res["status"], res["detail"] = "NOT_FOUND", "no title, no id"
            return res
        cands, used = [], []
        if not state.get("dblp_blocked"):
            try:
                cands += search_dblp(title)
                used.append("DBLP")
            except (Blocked, ValueError):
                state["dblp_blocked"] = True
        first = (surnames_from_bib(f.get("author", "")) or [""])[0]
        cands += search_crossref(title, first)
        used.append("Crossref")
        best = max(cands, key=lambda r: title_sim(title, r["title"]), default=None)
        res["status"], res["score"], res["detail"] = judge(e, best, "search " + "+".join(used))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        res["status"], res["detail"] = "UNCHECKED", f"service error: {exc}"
    finally:
        time.sleep(state.get("delay", 1.0))
    return res


def duplicate_titles(entries: list[dict]) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for e in entries:
        t = norm_title(e["fields"].get("title", ""))
        if t:
            seen.setdefault(t, []).append(e["key"])
    return {t: ks for t, ks in seen.items() if len(ks) > 1}


def render(results: list[dict], dups: dict) -> str:
    order = {"MISMATCH": 0, "NOT_FOUND": 1, "WEAK": 2, "UNCHECKED": 3, "VERIFIED": 4}
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["# bib-verify report", "",
             "Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: order[kv[0]])),
             "", "| status | key | score | lint | detail |", "|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: (order[r["status"]], r["key"])):
        lines.append(f"| {r['status']} | `{r['key']}` | {r['score']:.2f} | {'; '.join(r['lint'])} | "
                     f"{r['detail'].replace('|', '/')} |")
    if dups:
        lines += ["", "## Duplicate titles", ""] + [f"- {', '.join(ks)}" for ks in dups.values()]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- selftest ---

SELFTEST_BIB = r"""
@misc{cggi-tfhe,
  author = {Ilaria Chillotti and Nicolas Gama and Mariya Georgieva and Malika Izabach{\`e}ne},
  title = {{TFHE}: Fast Fully Homomorphic Encryption over the Torus},
  howpublished = {Cryptology ePrint Archive, Paper 2018/421},
  year = 2018,
}
% UNVERIFIED
@article{fake,
  author = "Chen and others",
  title = {A Paper That Does Not Exist About Quantum Fuzzy Toys},
  journal = {IEEE TIFS}, year = {2024}
}
"""


def selftest(online: bool) -> int:
    es = parse_bib(SELFTEST_BIB)
    assert [e["key"] for e in es] == ["cggi-tfhe", "fake"], es
    assert es[0]["fields"]["year"] == "2018" and not es[0]["unverified_marker"]
    assert es[1]["unverified_marker"]
    assert find_eprint_id(es[0]["fields"]) == "2018/421"
    assert surnames_from_bib(es[0]["fields"]["author"])[-1] == "izabachene"
    assert "placeholder author list ('X and others' only)" in lint(es[1])
    assert title_sim("{TFHE}: Fast Fully", "TFHE: fast fully") == 1.0
    print("selftest (offline part): OK")
    if online:
        st = {"delay": 0.5}
        r0, r1 = check_entry(es[0], False, st), check_entry(es[1], False, st)
        print(f"  online: {r0['key']} -> {r0['status']} ({r0['detail'][:90]})")
        print(f"  online: {r1['key']} -> {r1['status']} ({r1['detail'][:90]})")
        if r0["status"] == "UNCHECKED":
            print("  network unavailable: online part skipped")
        else:
            assert r0["status"] == "VERIFIED", r0
            assert r1["status"] in ("NOT_FOUND", "WEAK"), r1
            print("selftest (online part): OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bib", nargs="?")
    ap.add_argument("--offline", action="store_true", help="static lint only, no network")
    ap.add_argument("--only", help="comma-separated keys to check")
    ap.add_argument("--json", help="write JSON report to this file")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between network lookups")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-online", action="store_true", help="selftest incl. two live lookups")
    a = ap.parse_args(argv)
    if a.selftest or a.selftest_online:
        return selftest(a.selftest_online)
    if not a.bib:
        ap.print_usage()
        return 3
    with open(a.bib, encoding="utf-8") as fh:
        entries = parse_bib(fh.read())
    if a.only:
        keep = set(a.only.split(","))
        entries = [e for e in entries if e["key"] in keep]
    state = {"delay": 0.0 if a.offline else a.delay}
    results = []
    for idx, e in enumerate(entries, 1):
        r = check_entry(e, a.offline, state)
        results.append(r)
        print(f"[{idx}/{len(entries)}] {r['status']:9s} {r['key']}", file=sys.stderr)
    if state.get("dblp_blocked"):
        print("note: DBLP served a bot challenge; title searches used Crossref only", file=sys.stderr)
    dups = duplicate_titles(entries)
    print(render(results, dups))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"results": results, "duplicates": dups}, fh, indent=2, ensure_ascii=False)
    bad = [r for r in results if r["status"] != "VERIFIED"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
