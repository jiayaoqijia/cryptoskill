#!/usr/bin/env python3
"""extract_toc.py -- build Markdown tables of contents for a local textbook corpus.

Usage
-----
    python3 extract_toc.py BOOK_OR_DIR [BOOK_OR_DIR ...] --out-dir references/textbooks/toc
    python3 extract_toc.py --selftest

For every input file it writes ``<out-dir>/<slug>.md`` containing ONLY
bibliographic information (title/author guessed from metadata or file name) and
the table of contents.  No body text, no figures and no local paths are written,
so the output is safe to commit even when the PDFs themselves are not.

Strategy (in order):
  1. PDF: PyMuPDF ``doc.get_toc()`` (embedded bookmarks).  Bookmarks that are
     useless (e.g. only page numbers "1", "2", ...) are rejected.
  2. PDF fallback: scan the first ``--scan-pages`` pages for a "Contents" page and
     parse lines that look like "3.2 Cyclotomic fields ..... 57" or
     "Chapter 4 Galois theory".  Marked ``source: text-heuristic``.
  3. DjVu: ``djvused -e print-outline`` if the tool is installed; otherwise only a
     bibliographic stub is written (``source: none``).
  4. Anything without a text layer / outline -> stub; a human can fill the TOC
     from the publisher page and mark it "TOC from public source".

Also prints a one-line status per book and, with ``--summary FILE``, writes a
JSON summary (slug, title, author, n_entries, source) for building CATALOG.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field, asdict

try:  # optional dependency
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover - handled at runtime
    fitz = None

BOOK_EXT = {".pdf", ".djvu", ".djv"}

# Noise that downloaded / scanned file names often carry: a trailing "(site.tld, other.tld)"
# source tag, "(auth.)", "high quality".
_FILENAME_NOISE = [
    r"\((?:\s*[\w-]+(?:\.[\w-]+)+\s*,?)+\)",
    r"\(auth\.\)",
    r"\bhigh quality\b",
]


@dataclass
class TocEntry:
    level: int
    title: str
    page: int | None


@dataclass
class BookToc:
    slug: str
    title: str
    author: str
    fmt: str
    pages: int | None
    source: str  # bookmarks | text-heuristic | djvused | none
    entries: list[TocEntry] = field(default_factory=list)
    note: str = ""


# ----------------------------------------------------------------- helpers ---

def clean_filename(stem: str) -> str:
    s = stem
    for pat in _FILENAME_NOISE:
        s = re.sub(pat, "", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" _-")
    return s


def guess_title_author(stem: str, meta: dict | None) -> tuple[str, str]:
    """Prefer the human-curated 'Title (Author)' file-name pattern, then metadata."""
    meta = meta or {}
    cleaned = clean_filename(stem)
    m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", cleaned)
    fn_title, fn_author = (m.group(1), m.group(2)) if m else (cleaned, "")
    fn_author = re.sub(r"\betc\.?|\bet al\.?|\(auth\.?\)", "", fn_author).strip(" ,;")
    t = (meta.get("title") or "").strip()
    a = (meta.get("author") or "").strip()
    junk = r"untitled|microsoft|\.docx?|\.pdf|epapyrus|isbn|^\d|\d{3}-\d|onlinepdf"
    if m or not t or len(t) < 4 or re.search(junk, t, re.I):
        t = fn_title
    if fn_author or not a or re.search(r"unknown|admin|user|^\S+$", a, re.I):
        a = fn_author
    # bilingual titles: keep the Latin-script part ("X=<CJK>", "X <CJK>")
    t = re.split(r"=|[\u3000-\u9fff\uff00-\uffef]", t)[0]
    t = re.sub(r"\s+", " ", t.replace("_", " ")).strip(" :;,.-")
    a = re.sub(r"[\u3000-\u9fff\uff00-\uffef]+", " ", a)
    a = re.sub(r"\s+", " ", a).strip(" ,;()")
    return t, a


def first_author_surname(author: str) -> str:
    if not author:
        return ""
    if re.match(r"^[^,]+,\s*[^,]+$", author) and " and " not in author:
        first = author.split(",")[0]          # "Robert, Alain" -> "Robert"
    else:
        first = re.split(r",|;| and |&", author)[0]
    toks = [t for t in first.split() if not re.fullmatch(r"[A-Z]\.?|[A-Z]\.[A-Z]\.?", t)]
    return toks[-1] if toks else ""


def slugify(title: str, author: str = "") -> str:
    last = first_author_surname(author)
    s = f"{last}-{title}" if last else title
    s = s.encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:70].rstrip("-") or "book"


def toc_is_useless(toc: list) -> bool:
    """Reject bookmark trees that carry no chapter names."""
    if not toc:
        return True
    titles = [str(t[1]).strip() for t in toc]
    informative = [t for t in titles if re.search(r"[A-Za-z一-鿿]{3,}", t)]
    return len(informative) < max(2, 0.3 * len(titles))


_DOTTED = re.compile(r"^(?P<title>.*?[A-Za-z].*?)\s*(?:\.\s*){2,}\s*(?P<page>\d{1,4})\s*$")
_TRAIL_PAGE = re.compile(r"^(?P<title>.*?[A-Za-z].*?)\s+(?P<page>\d{1,4})\s*$")
_PREFIX = re.compile(r"^(?:(?P<kw>chapter|part|appendix|lecture)\s+(?P<n>[0-9IVXLC]+|[A-Z])\.?"
                     r"|(?P<num>\d+(?:\.\d+)*)\.?|§\s*(?P<sec>[0-9IlVX]+))\s*(?P<rest>.*)$", re.I)
_PAGE_ONLY = re.compile(r"^(?:\d{1,4}|[ivxlc]{1,6})$", re.I)


def _looks_like_contents_page(txt: str) -> bool:
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    if len(lines) < 8:
        return False
    short = sum(len(l) < 70 for l in lines) / len(lines)
    numeric = sum(bool(_PAGE_ONLY.match(l)) or bool(re.search(r"\d{1,4}$", l)) or
                  bool(_PREFIX.match(l) and _PREFIX.match(l).group("num")) for l in lines) / len(lines)
    return short > 0.85 and numeric > 0.25


_DICT: set[str] | None = None


def _dictionary() -> set[str]:
    """Optional system word list used to score OCR quality (empty set if absent)."""
    global _DICT
    if _DICT is None:
        _DICT = set()
        for cand in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
            if os.path.exists(cand):
                with open(cand, encoding="utf-8", errors="ignore") as fh:
                    _DICT = {w.strip().lower() for w in fh if w.strip()}
                break
    return _DICT


def ocr_quality(entries: list[TocEntry]) -> float | None:
    """Fraction of alphabetic tokens (len>=4) found in the dictionary; None if no dictionary."""
    d = _dictionary()
    if not d:
        return None
    toks = [t.lower() for e in entries for t in re.findall(r"[A-Za-z]{4,}", e.title)]
    if not toks:
        return 0.0
    return sum(t in d or t.rstrip("s") in d for t in toks) / len(toks)


def _wordlike(line: str) -> bool:
    """Reject OCR garbage: most tokens must look like words."""
    toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", line)
    if not toks:
        return False
    good = [t for t in toks if len(t) == 1 or re.search(r"[aeiouyAEIOUY]", t) and
            not re.search(r"[A-Z]{2,}[a-z]+[A-Z]", t)]
    return len(good) / len(toks) >= 0.75 and len(" ".join(toks)) >= 3


def heuristic_toc_from_text(pages_text: list[str], max_pages: int = 14) -> list[TocEntry]:
    """Parse the printed 'Contents' pages.

    Handles both one-line layouts ("1.2 Title ..... 17") and the split layout that
    PDF text extraction often produces (number, title and page on separate lines).
    Page numbers are the book's PRINTED numbers.
    """
    start = None
    for i, txt in enumerate(pages_text):
        if re.search(r"^\s*(table of )?contents\b", txt, re.I | re.M):
            start = i
            break
    if start is None:
        return []
    pages = [pages_text[start]]
    for txt in pages_text[start + 1:start + max_pages]:
        if not _looks_like_contents_page(txt):
            break
        pages.append(txt)
    entries: list[TocEntry] = []
    garbage = [0]
    pending_kw, pending_num = None, None
    for txt in pages:
        for raw in txt.splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if not line or re.fullmatch(r"(table of )?contents", line, re.I):
                continue
            if _PAGE_ONLY.match(line):
                if entries and entries[-1].page is None and line.isdigit():
                    entries[-1].page = int(line)
                continue
            page = None
            pm0 = _PREFIX.match(line)
            if pm0 and not re.search(r"[A-Za-z]{3,}", pm0.group("rest")) and \
                    (pm0.group("kw") or pm0.group("sec") or not pm0.group("rest").strip()):
                if pm0.group("kw"):
                    pending_kw, pending_num = f"{pm0.group('kw').capitalize()} {pm0.group('n')}", 1
                elif pm0.group("num"):
                    pending_kw, pending_num = pm0.group("num"), 1 + pm0.group("num").count(".")
                else:
                    pending_kw, pending_num = "§" + pm0.group("sec"), 2
                continue
            m = _DOTTED.match(line) or _TRAIL_PAGE.match(line)
            if m:
                line, page = m.group("title").strip(" ."), int(m.group("page"))
            pm = _PREFIX.match(line)
            level, label = 1, ""
            if pm:
                rest = pm.group("rest").strip(" .:")
                if pm.group("kw"):
                    label = f"{pm.group('kw').capitalize()} {pm.group('n')}"
                    level = 1
                elif pm.group("num"):
                    label = pm.group("num")
                    level = 1 + label.count(".")
                else:
                    label = "§" + pm.group("sec")
                    level = 2
                if not re.search(r"[A-Za-z]{3,}", rest):
                    pending_kw, pending_num = label, level   # title on next line
                    continue
                line = rest
            elif pending_kw:
                label, level = pending_kw, pending_num
            if not re.search(r"[A-Za-z]{3,}", line):
                continue
            pending_kw = pending_num = None
            line = re.sub(r"(\s*\.){2,}.*$", "", line).strip()
            if not _wordlike(line):
                garbage[0] += 1
                continue
            title = f"{label} {line}".strip()
            entries.append(TocEntry(min(level, 3), title, page))
    seen, out = set(), []
    for e in entries:
        k = (e.title, e.page)
        if k not in seen:
            seen.add(k)
            out.append(e)
    return out


# ----------------------------------------------------------------- readers ---

def read_pdf(path: str, max_level: int, scan_pages: int) -> BookToc:
    stem = os.path.splitext(os.path.basename(path))[0]
    if fitz is None:
        t, a = guess_title_author(stem, None)
        return BookToc(slugify(t, a), t, a, "pdf", None, "none", note="PyMuPDF not installed")
    doc = fitz.open(path)
    t, a = guess_title_author(stem, doc.metadata)
    book = BookToc(slugify(t, a), t, a, "pdf", doc.page_count, "none")
    toc = doc.get_toc(simple=True)
    if not toc_is_useless(toc):
        book.source = "bookmarks"
        book.entries = [TocEntry(lv, str(ti).strip(), pg if pg > 0 else None)
                        for lv, ti, pg in toc if lv <= max_level and str(ti).strip()]
    else:
        texts = [doc[i].get_text() for i in range(min(scan_pages, doc.page_count))]
        if sum(len(x.strip()) for x in texts) < 200:
            book.note = "no text layer in first pages (scanned); TOC must come from a public source"
        else:
            ents = [e for e in heuristic_toc_from_text(texts) if e.level <= max_level]
            q = ocr_quality(ents)
            if q is not None and q < 0.7:
                book.note = (f"contents page found but OCR text is too noisy (dictionary hit rate "
                             f"{q:.2f}); replace with a public TOC")
            elif len(ents) >= 3:
                book.source = "text-heuristic"
                book.entries = ents
                book.note = "parsed from printed contents pages; page numbers are PRINTED pages"
            else:
                book.note = "no usable bookmarks and no parsable contents page"
        if toc and toc_is_useless(toc):
            book.note += " (embedded bookmarks rejected: no chapter names)"
    doc.close()
    return book


def read_djvu(path: str, max_level: int) -> BookToc:
    stem = os.path.splitext(os.path.basename(path))[0]
    t, a = guess_title_author(stem, None)
    book = BookToc(slugify(t, a), t, a, "djvu", None, "none")
    exe = shutil.which("djvused")
    if not exe:
        book.note = "djvused not installed (apt install djvulibre-bin); bibliographic stub only"
        return book
    try:
        out = subprocess.run([exe, "-e", "print-outline", path], capture_output=True,
                             text=True, timeout=60).stdout
        pages = subprocess.run([exe, "-e", "n", path], capture_output=True, text=True,
                               timeout=60).stdout.strip()
        book.pages = int(pages) if pages.isdigit() else None
    except Exception as exc:  # pragma: no cover
        book.note = f"djvused failed: {exc.__class__.__name__}"
        return book
    # outline syntax: (bookmarks ("Title" "#page" (children...)) ...)
    depth, entries = 0, []
    for tok in re.finditer(r'\(|\)|"((?:[^"\\]|\\.)*)"\s+"#(\d+)"', out):
        s = tok.group(0)
        if s == "(":
            depth += 1
        elif s == ")":
            depth -= 1
        else:
            level = max(1, depth - 1)
            if level <= max_level:
                entries.append(TocEntry(level, tok.group(1), int(tok.group(2))))
    if entries:
        book.source, book.entries = "djvused", entries
    else:
        book.note = "djvu has no outline"
    return book


# ----------------------------------------------------------------- writers ---

def render_md(book: BookToc) -> str:
    lines = [f"# {book.title}", ""]
    lines.append(f"- **Author(s):** {book.author or 'unknown'}")
    lines.append(f"- **Format:** {book.fmt}; pages: {book.pages if book.pages else 'n/a'}")
    lines.append(f"- **TOC source:** {book.source}")
    if book.note:
        lines.append(f"- **Note:** {book.note}")
    lines.append("- **Page convention:** bookmark pages are PDF physical pages (1-based) "
                 "unless the note says otherwise.")
    lines.append("")
    lines.append("## Table of contents")
    lines.append("")
    if not book.entries:
        lines.append("_No machine-extractable TOC. Fill in from the publisher's public "
                     "page and mark it `TOC from public source`._")
    for e in book.entries:
        indent = "  " * (e.level - 1)
        pg = f" — p.{e.page}" if e.page else ""
        title = re.sub(r"\s+", " ", e.title)
        lines.append(f"{indent}- {title}{pg}")
    lines.append("")
    return "\n".join(lines)


def iter_books(inputs: list[str]):
    for inp in inputs:
        if os.path.isdir(inp):
            for name in sorted(os.listdir(inp)):
                p = os.path.join(inp, name)
                if os.path.isfile(p) and os.path.splitext(name)[1].lower() in BOOK_EXT:
                    yield p
        elif os.path.isfile(inp):
            yield inp
        else:
            print(f"[warn] not found: {os.path.basename(inp)}", file=sys.stderr)


def process(inputs, out_dir, max_level=2, scan_pages=25, summary=None):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for path in iter_books(inputs):
        ext = os.path.splitext(path)[1].lower()
        try:
            book = read_pdf(path, max_level, scan_pages) if ext == ".pdf" else read_djvu(path, max_level)
        except Exception as exc:
            print(f"[fail] {os.path.basename(path)}: {exc}", file=sys.stderr)
            continue
        with open(os.path.join(out_dir, book.slug + ".md"), "w", encoding="utf-8") as fh:
            fh.write(render_md(book))
        print(f"[{book.source:14s}] {len(book.entries):4d} entries  {book.slug}")
        rows.append({k: v for k, v in asdict(book).items() if k != "entries"} |
                    {"n_entries": len(book.entries)})
    if summary:
        with open(summary, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2, ensure_ascii=False)
    return rows


# ----------------------------------------------------------------- selftest --

def selftest() -> int:
    assert slugify("Linear Representations of Finite Groups", "Jean-Pierre Serre") == \
        "serre-linear-representations-of-finite-groups"
    t, a = guess_title_author("Algebra (Michael Artin) (example.org, mirror.example.net)", {})
    assert (t, a) == ("Algebra", "Michael Artin"), (t, a)
    assert toc_is_useless([[1, "1", 1], [1, "2", 5], [1, "3", 9]])
    ents = heuristic_toc_from_text(["Contents\n1 Finite fields . . . . . 1\n"
                                    "1.1 Construction .......... 3\n2 Cyclotomy ....... 17\n"])
    assert [e.title for e in ents] == ["1 Finite fields", "1.1 Construction", "2 Cyclotomy"], ents
    assert ents[1].level == 2 and ents[2].page == 17
    ents = heuristic_toc_from_text(["Contents\nCHAPTER 3\nCongruence\n§1 Elementary Observations\n"
                                    "2.1\nThe character of a representation\n10\n"])
    assert [e.title for e in ents] == ["Chapter 3 Congruence", "§1 Elementary Observations",
                                       "2.1 The character of a representation"], ents
    assert ents[2].page == 10 and ents[1].level == 2
    assert slugify("A course in p-adic analysis", "Robert, Alain") == "robert-a-course-in-p-adic-analysis"
    if fitz is None:
        print("selftest: PyMuPDF missing, PDF round-trip skipped; parser tests OK")
        return 0
    with tempfile.TemporaryDirectory() as td:
        pdf = os.path.join(td, "Toy Book (A. Author).pdf")
        doc = fitz.open()
        for i in range(4):
            doc.new_page().insert_text((72, 72), f"page {i + 1}")
        doc.set_toc([[1, "Chapter 1 Groups", 1], [2, "1.1 Cosets", 2], [1, "Chapter 2 Rings", 3]])
        doc.save(pdf)
        doc.close()
        rows = process([td], os.path.join(td, "toc"))
        assert rows and rows[0]["source"] == "bookmarks" and rows[0]["n_entries"] == 3, rows
        md = open(os.path.join(td, "toc", rows[0]["slug"] + ".md"), encoding="utf-8").read()
        assert "1.1 Cosets" in md and td not in md, "path leaked or entry missing"
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", help="book files or directories")
    ap.add_argument("--out-dir", default="references/textbooks/toc")
    ap.add_argument("--max-level", type=int, default=2, help="deepest TOC level kept")
    ap.add_argument("--scan-pages", type=int, default=25, help="pages scanned by the text fallback")
    ap.add_argument("--summary", help="write JSON summary here")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.inputs:
        ap.error("give at least one book file or directory (or --selftest)")
    process(args.inputs, args.out_dir, args.max_level, args.scan_pages, args.summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
