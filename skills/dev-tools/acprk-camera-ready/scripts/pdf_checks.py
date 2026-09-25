#!/usr/bin/env python3
"""pdf_checks.py - final-compile checks for submission and camera-ready PDFs.

Checks (each can be run alone):
  pages     page count; page on which 'References' starts; last body page;
            page of 'Conclusion'; body-page limit check (--limit N)
  refs      unresolved references/citations: '??' in PDF text and LaTeX log warnings
  boxes     overfull/underfull \\hbox warnings from the .log (with size in pt)
  fonts     every font embedded (pdffonts 'emb' column) and no Type 3 bitmap fonts
  meta      PDF metadata (Title/Author/...; informational or anonymity check)
  width     approximate text-block width in cm on a body page (LNCS default ~12.2 cm)
  overlap   words whose bounding boxes overlap across lines (overprinting after
            negative vspace near floats); known false positives: radicals, big braces

Usage:
  python3 pdf_checks.py main.pdf [--log main.log] [--limit 30] [--checks pages,refs,fonts]
  python3 pdf_checks.py --selftest

Requires poppler-utils (pdftotext, pdffonts, pdfinfo) for PDF checks; the
parsers are pure Python and covered by --selftest.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str]) -> str:
    if not shutil.which(cmd[0]):
        raise RuntimeError(f"{cmd[0]} not found (install poppler-utils)")
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace").stdout


# ---------------------------------------------------------------- pure parsers
def parse_pages(text: str) -> dict:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    ref_page = concl_page = None
    for i, p in enumerate(pages, 1):
        if ref_page is None and re.search(r"^\s*(References|Bibliography)\s*$", p, re.M):
            ref_page = i
        if re.search(r"^\s*\d+\s+Conclusions?\b", p, re.M):
            concl_page = i
    body_last = (ref_page - 1) if ref_page else len(pages)
    # if References starts mid-page, that page still carries body text
    if ref_page:
        head = pages[ref_page - 1].split("References")[0]
        if len(head.strip()) > 200:
            body_last = ref_page
    return {"pages": len(pages), "references_page": ref_page, "conclusion_page": concl_page,
            "body_last_page": body_last}


def parse_log(log: str) -> dict:
    undef = re.findall(r"(?:Reference|Citation) `([^']+)' on page \d+ undefined", log)
    multiply = re.findall(r"Label `([^']+)' multiply defined", log)
    overfull = [(float(m.group(1)), m.group(0)) for m in
                re.finditer(r"Overfull \\[hv]box \(([\d.]+)pt too \w+\)[^\n]*", log)]
    underfull = len(re.findall(r"Underfull \\[hv]box", log))
    rerun = "Rerun to get" in log or "Label(s) may have changed" in log
    return {"undefined": sorted(set(undef)), "multiply_defined": sorted(set(multiply)),
            "overfull": overfull, "underfull_count": underfull, "rerun_needed": rerun}


def parse_pdffonts(out: str) -> dict:
    lines = out.splitlines()
    rows = []
    for ln in lines[2:]:
        if not ln.strip():
            continue
        # columns: name type encoding emb sub uni object ID ; 'emb' is the 3rd-from-... use regex
        m = re.match(r"^(\S+)\s+(.+?)\s+(\S+)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", ln)
        if m:
            rows.append({"name": m.group(1), "type": m.group(2).strip(), "emb": m.group(4) == "yes"})
    not_emb = [r["name"] for r in rows if not r["emb"]]
    type3 = [r["name"] for r in rows if r["type"].startswith("Type 3")]
    return {"fonts": len(rows), "not_embedded": not_emb, "type3": type3}


def overlaps_from_bbox(xml: str, footer_y: float = 680.0) -> list[tuple[int, list]]:
    res = []
    for pi, pg in enumerate(xml.split("<page ")[1:], 1):
        words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in re.findall(
            r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', pg)]
        words = [w for w in words if w[1] < footer_y]
        hits = []
        for i in range(len(words)):
            for j in range(i + 1, min(i + 40, len(words))):
                a, b = words[i], words[j]
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 2 and oy > 3 and abs(a[1] - b[1]) > 2 and len(a[4]) > 1 and len(b[4]) > 1:
                    hits.append((a[4], b[4], int(a[1]), int(b[1])))
        if hits:
            res.append((pi, hits))
    return res


def width_from_bbox(xml: str) -> float | None:
    xs = [float(m) for m in re.findall(r'xMin="([\d.]+)"', xml)]
    xe = [float(m) for m in re.findall(r'xMax="([\d.]+)"', xml)]
    if not xs:
        return None
    return (max(xe) - min(xs)) / 72 * 2.54


# ---------------------------------------------------------------- checks
def check(pdf: Path, log: Path | None, limit: int | None, which: set[str]) -> int:
    bad = 0
    text = _run(["pdftotext", "-layout", str(pdf), "-"]) if which & {"pages", "refs"} else ""
    if "pages" in which:
        p = parse_pages(text)
        print(f"[pages] total={p['pages']} references_start={p['references_page']} "
              f"conclusion={p['conclusion_page']} body_last={p['body_last_page']}")
        if limit and p["body_last_page"] > limit:
            print(f"  FAIL body ends on page {p['body_last_page']} > limit {limit} "
                  "(check what the CFP counts: appendices? acknowledgements?)")
            bad += 1
    if "refs" in which:
        q = text.count("??")
        print(f"[refs] '??' occurrences in PDF text: {q}")
        bad += q > 0
        if log and log.exists():
            L = parse_log(log.read_text(errors="replace"))
            print(f"[refs] undefined: {len(L['undefined'])} {L['undefined'][:10]}; "
                  f"multiply defined: {L['multiply_defined'][:10]}; rerun needed: {L['rerun_needed']}")
            bad += bool(L["undefined"]) + bool(L["multiply_defined"]) + L["rerun_needed"]
    if "boxes" in which and log and log.exists():
        L = parse_log(log.read_text(errors="replace"))
        big = [o for o in L["overfull"] if o[0] > 1.0]
        print(f"[boxes] overfull: {len(L['overfull'])} (>{1.0}pt: {len(big)}); underfull: {L['underfull_count']}")
        for sz, line in sorted(big, reverse=True)[:10]:
            print("   ", line[:120])
        bad += bool(big)
    if "fonts" in which:
        F = parse_pdffonts(_run(["pdffonts", str(pdf)]))
        print(f"[fonts] {F['fonts']} fonts; not embedded: {F['not_embedded']}; Type 3: {F['type3']}")
        bad += bool(F["not_embedded"])
    if "meta" in which:
        info = _run(["pdfinfo", str(pdf)])
        for ln in info.splitlines():
            if ln.split(":")[0] in {"Title", "Author", "Subject", "Keywords", "Creator", "Producer", "Page size", "Pages"}:
                print("[meta]", ln)
    if "width" in which:
        xml = _run(["pdftotext", "-bbox", "-f", "3", "-l", "3", str(pdf), "-"])
        w = width_from_bbox(xml)
        print(f"[width] text block on page 3 ≈ {w:.1f} cm (LNCS default ≈ 12.2 cm)" if w else "[width] n/a")
    if "overlap" in which:
        last = limit or 999
        xml = _run(["pdftotext", "-bbox", "-f", "1", "-l", str(last), str(pdf), "-"])
        ov = overlaps_from_bbox(xml)
        print(f"[overlap] pages with overlapping words: {[p for p, _ in ov]}")
        for p, hits in ov[:10]:
            print(f"   page {p}: {hits[:3]}")
    print("RESULT:", "OK" if bad == 0 else f"{bad} problem(s)")
    return 1 if bad else 0


def selftest() -> int:
    t = "Title\n1 Introduction\ntext\f2 Body\f7 Conclusion\nWe presented\f\nReferences\n1. A\f"
    p = parse_pages(t)
    assert p == {"pages": 4, "references_page": 4, "conclusion_page": 3, "body_last_page": 3}, p
    log = ("LaTeX Warning: Reference `sec:x' on page 3 undefined on input line 5.\n"
           "LaTeX Warning: Citation `foo24' on page 1 undefined on input line 9.\n"
           "Overfull \\hbox (12.5pt too wide) in paragraph at lines 10--12\n"
           "Overfull \\hbox (0.32pt too wide) in paragraph at lines 20--21\n"
           "Underfull \\hbox (badness 10000) in paragraph\n"
           "LaTeX Warning: Label `eq:1' multiply defined.\n")
    L = parse_log(log)
    assert L["undefined"] == ["foo24", "sec:x"] and L["multiply_defined"] == ["eq:1"]
    assert [o[0] for o in L["overfull"]] == [12.5, 0.32] and L["underfull_count"] == 1
    pf = ("name                                 type              encoding         emb sub uni object ID\n"
          "------------------------------------ ----------------- ---------------- --- --- --- ---------\n"
          "ABCDEF+CMR10                         Type 1            Builtin          yes yes no       4  0\n"
          "Helvetica                            Type 1            Standard         no  no  no       9  0\n"
          "[none]                               Type 3            Custom           yes no  no      12  0\n")
    F = parse_pdffonts(pf)
    assert F["fonts"] == 3 and F["not_embedded"] == ["Helvetica"] and F["type3"] == ["[none]"], F
    xml = ('<page width="595" height="842">'
           '<word xMin="100.0" yMin="200.0" xMax="160.0" yMax="210.0">overlap</word>'
           '<word xMin="110.0" yMin="204.0" xMax="170.0" yMax="214.0">printed</word>'
           '<word xMin="100.0" yMin="300.0" xMax="445.9" yMax="310.0">fine</word></page>')
    ov = overlaps_from_bbox(xml)
    assert ov and ov[0][0] == 1 and ov[0][1][0][:2] == ("overlap", "printed"), ov
    assert abs(width_from_bbox(xml) - 12.2) < 0.1
    print("selftest: PASS")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--log", help="LaTeX .log (default: <pdf stem>.log if present)")
    ap.add_argument("--limit", type=int, help="last allowed body page")
    ap.add_argument("--checks", default="pages,refs,boxes,fonts,meta,width,overlap")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.pdf:
        ap.print_usage()
        return 2
    pdf = Path(a.pdf)
    log = Path(a.log) if a.log else pdf.with_suffix(".log")
    return check(pdf, log if log.exists() else None, a.limit, set(a.checks.split(",")))


if __name__ == "__main__":
    sys.exit(main())
