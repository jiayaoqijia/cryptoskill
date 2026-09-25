#!/usr/bin/env python3
"""anon_check.py - pre-submission anonymity scanner for papers and artifacts.

Scans LaTeX sources, .bib files, code/text files, zip archives and PDFs for
identity leaks that commonly cause desk rejection in double-blind review:

  * author names / account names / affiliations from a configurable deny-list
  * \\author, \\institute, \\thanks, e-mail addresses, acknowledgement sections
  * first-person self-citations ("our previous work [12]", "in our earlier paper")
  * URLs to personal code hosts (github/gitlab/bitbucket/personal pages)
  * local file-system paths (/home/<user>, /Users/<user>, C:\\Users\\<user>)
  * PDF metadata (Author, Title, Subject, Keywords, Creator, Producer) and
    embedded source paths (PTEX.FileName) and raw-byte hits of deny-list terms
  * a .git directory or VCS remote URLs inside an artifact

Usage
-----
  python3 anon_check.py PATH [PATH ...] [--deny "Alice Smith,asmith,Example Univ"]
                         [--deny-file denylist.txt] [--allow-url REGEX ...]
                         [--json] [--min-severity LOW|MEDIUM|HIGH]
  python3 anon_check.py --selftest

Deny-list file: one term per line, '#' starts a comment. A line starting with
're:' is a Python regular expression, otherwise matching is case-insensitive
substring on word boundaries.

Exit status: 0 = no HIGH findings, 1 = at least one HIGH finding, 2 = usage error.

Dependencies: standard library only. Optional: PyMuPDF (fitz) or poppler's
`pdfinfo`/`pdftotext` for PDF text/metadata (raw-byte scanning always works).
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
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

SEVERITIES = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}

TEX_EXT = {".tex", ".sty", ".cls", ".ltx"}
BIB_EXT = {".bib"}
TEXT_EXT = {
    ".py", ".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".rs", ".go", ".java", ".js",
    ".ts", ".sage", ".m", ".jl", ".sh", ".bash", ".zsh", ".md", ".txt", ".rst",
    ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".cmake", ".mk", ".lean",
    ".csv", ".log", ".ipynb", ".r", ".pl",
}
TEXT_NAMES = {"Makefile", "CMakeLists.txt", "Dockerfile", "README", "LICENSE", "config"}
SKIP_DIRS = {"__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", ".pytest_cache"}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL_RE = re.compile(r"https?://[^\s\"'<>}{)\]]+", re.I)
PERSONAL_HOST_RE = re.compile(
    r"https?://(?:www\.)?(github\.com|gitlab\.com|bitbucket\.org|codeberg\.org|"
    r"huggingface\.co|sites\.google\.com|[a-z0-9-]+\.github\.io|scholar\.google\.[a-z.]+|"
    r"orcid\.org|linkedin\.com|twitter\.com|x\.com|dblp\.org/pid)[^\s\"'<>}{)\]]*",
    re.I,
)
DEFAULT_ALLOW_URL = [
    r"anonymous\.4open\.science",
    r"doi\.org",
    r"eprint\.iacr\.org",
    r"iacr\.org",
    r"arxiv\.org",
    r"ctan\.org",
]
LOCAL_PATH_RE = re.compile(
    r"(/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+|[A-Za-z]:\\\\?Users\\\\?[A-Za-z0-9._-]+)"
)
SELF_CITE_RE = re.compile(
    r"\b(?:our|my)\s+(?:own\s+)?(?:previous|prior|earlier|recent|companion|preceding)\s+"
    r"(?:work|paper|result|construction|implementation|analysis|article|submission)s?\b"
    r"|\bin\s+our\s+(?:previous|prior|earlier)\b"
    r"|\bwe\s+(?:previously|earlier)\s+(?:showed|proposed|proved|introduced|presented)\b"
    r"|\b(?:extends|extending|builds on|building on)\s+our\s+(?:work|paper)\b"
    r"|\bour\s+(?:work|paper)\s*~?\\cite",
    re.I,
)
TEX_ID_MACROS = re.compile(r"\\(author|institute|thanks|email|affiliation|address|orcid)\s*(\[[^\]]*\])?\s*\{", re.I)
ACK_RE = re.compile(
    r"\\(?:section|subsection|paragraph)\*?\s*\{\s*acknowledg|\\begin\{acks\}|\\acknowledgments?\b",
    re.I,
)
FUNDING_RE = re.compile(r"\b(?:supported by|funded by|grant (?:no\.?|number)|this work was (?:partially )?supported)\b", re.I)
CAMERA_RE = re.compile(r"\bcamera[- ]ready\b|\bde-?anonymi[sz]", re.I)
ANON_AUTHOR_RE = re.compile(r"anonymous|submission|paper\s*#?\s*\d*|\\anon", re.I)


@dataclass
class Finding:
    severity: str
    kind: str
    file: str
    line: int
    text: str

    def fmt(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line else self.file
        return f"[{self.severity:6}] {self.kind:18} {loc}  {self.text}"


# ---------------------------------------------------------------- deny-list
class DenyList:
    def __init__(self, terms: Iterable[str]):
        self.patterns: list[tuple[str, re.Pattern]] = []
        for t in terms:
            t = t.strip()
            if not t or t.startswith("#"):
                continue
            if t.startswith("re:"):
                self.patterns.append((t, re.compile(t[3:], re.I)))
            else:
                self.patterns.append((t, re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", re.I)))

    @classmethod
    def load(cls, inline: str | None, files: list[str] | None) -> "DenyList":
        terms: list[str] = []
        if inline:
            terms += [x for x in inline.split(",")]
        for f in files or []:
            terms += Path(f).read_text(encoding="utf-8", errors="replace").splitlines()
        return cls(terms)

    def hits(self, text: str) -> list[str]:
        return [label for label, p in self.patterns if p.search(text)]

    def __bool__(self) -> bool:
        return bool(self.patterns)


# ---------------------------------------------------------------- scanners
def _is_comment_line(line: str, ext: str) -> bool:
    s = line.lstrip()
    if ext in TEX_EXT or ext in BIB_EXT:
        return s.startswith("%")
    return s.startswith(("#", "//", "/*", "*", "--"))


def _url_findings(line: str, allow: list[re.Pattern], deny: DenyList, where: str, ln: int, sev_scale: int) -> list[Finding]:
    out = []
    for m in URL_RE.finditer(line):
        url = m.group(0)
        if any(a.search(url) for a in allow):
            continue
        if deny and deny.hits(url):
            out.append(Finding("HIGH", "url-deny-term", where, ln, url))
        elif PERSONAL_HOST_RE.match(url):
            out.append(Finding(_scale("MEDIUM", sev_scale), "personal-host-url", where, ln,
                               url + "  (third-party repos are fine; own repos must be anonymous)"))
    return out


def _scale(sev: str, delta: int) -> str:
    v = max(0, min(2, SEVERITIES[sev] + delta))
    return [k for k, x in SEVERITIES.items() if x == v][0]


def scan_text(text: str, where: str, ext: str, deny: DenyList, allow: list[re.Pattern]) -> list[Finding]:
    out: list[Finding] = []
    is_tex = ext in TEX_EXT
    is_bib = ext in BIB_EXT
    for i, line in enumerate(text.splitlines(), 1):
        comment = _is_comment_line(line, ext)
        # comments ship with source uploads (e.g. arXiv/Overleaf sharing): one level lower
        delta = -1 if comment else 0
        snippet = line.strip()[:160]
        if deny:
            for term in deny.hits(line):
                if is_bib and not comment:
                    # IACR-style rules: self-citations in 3rd person keep real authors in .bib
                    out.append(Finding("LOW", "deny-term-in-bib", where, i, f"'{term}': {snippet}"))
                else:
                    out.append(Finding(_scale("HIGH", delta), "deny-term", where, i, f"'{term}': {snippet}"))
        for m in EMAIL_RE.finditer(line):
            if m.group(0).lower().endswith(("example.com", "example.org")):
                continue
            out.append(Finding(_scale("HIGH", delta), "email", where, i, m.group(0)))
        for m in LOCAL_PATH_RE.finditer(line):
            out.append(Finding(_scale("HIGH", delta), "local-path", where, i, m.group(0)))
        if not is_bib:
            out += _url_findings(line, allow, deny, where, i, delta)
        if is_tex and not comment:
            m = TEX_ID_MACROS.search(line)
            if m:
                rest = line[m.end():]
                body = rest.split("}")[0]
                if body.strip() and not ANON_AUTHOR_RE.search(body):
                    out.append(Finding("HIGH", f"tex-\\{m.group(1).lower()}", where, i, snippet))
            if ACK_RE.search(line):
                out.append(Finding("HIGH", "acknowledgements", where, i, snippet))
            if FUNDING_RE.search(line):
                out.append(Finding("MEDIUM", "funding-statement", where, i, snippet))
        if (is_tex or ext in {".md", ".txt", ".rst"}) and SELF_CITE_RE.search(line):
            out.append(Finding(_scale("MEDIUM", delta), "first-person-self-cite", where, i, snippet))
        if CAMERA_RE.search(line):
            out.append(Finding("LOW", "revealing-wording", where, i, snippet))
    return out


def _pdf_metadata(path: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    try:
        import fitz  # type: ignore
        with fitz.open(str(path)) as doc:
            for k, v in (doc.metadata or {}).items():
                if v:
                    meta[k.capitalize()] = str(v)
        return meta
    except Exception:
        pass
    if shutil.which("pdfinfo"):
        r = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, errors="replace")
        for line in r.stdout.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def _pdf_text(path: Path) -> str:
    try:
        import fitz  # type: ignore
        with fitz.open(str(path)) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception:
        pass
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, errors="replace")
        return r.stdout
    return ""


_STREAM_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)


def _pdf_raw_with_streams(raw: bytes) -> str:
    """Raw PDF bytes plus every Flate-decodable stream, decompressed.

    Object streams (compressed metadata, XMP, PTEX.FileName entries) are otherwise
    invisible to a plain byte search.
    """
    import zlib
    parts = [raw.decode("latin-1")]
    for m in _STREAM_RE.finditer(raw):
        try:
            parts.append(zlib.decompress(m.group(1)).decode("latin-1"))
        except Exception:
            continue
    return "\n".join(parts)


def scan_pdf(path: Path, deny: DenyList, allow: list[re.Pattern]) -> list[Finding]:
    out: list[Finding] = []
    where = str(path)
    meta = _pdf_metadata(path)
    for key in ("Author", "Title", "Subject", "Keywords"):
        val = meta.get(key, "")
        if val:
            sev = "HIGH" if key == "Author" else "MEDIUM"
            if deny and deny.hits(val):
                sev = "HIGH"
            out.append(Finding(sev, f"pdf-meta-{key.lower()}", where, 0, val[:120]))
    for key in ("Creator", "Producer"):
        val = meta.get(key, "")
        if val and ((deny and deny.hits(val)) or LOCAL_PATH_RE.search(val)):
            out.append(Finding("HIGH", f"pdf-meta-{key.lower()}", where, 0, val[:120]))
        elif val:
            out.append(Finding("LOW", f"pdf-meta-{key.lower()}", where, 0, val[:120] + "  (informational)"))
    text = _pdf_text(path)
    if text:
        for f in scan_text(text, where + "#text", ".txt", deny, allow):
            f.kind = "pdf-text-" + f.kind
            out.append(f)
    raw = path.read_bytes()
    raw_s = _pdf_raw_with_streams(raw)
    for m in re.finditer(r"/PTEX\.FileName\s*\(([^)]*)\)", raw_s):
        val = m.group(1)
        sev = "HIGH" if (LOCAL_PATH_RE.search(val) or (deny and deny.hits(val))) else "LOW"
        out.append(Finding(sev, "pdf-embedded-path", where, 0, val[:120]))
    if deny:
        for term in deny.hits(raw_s):
            out.append(Finding("HIGH", "pdf-raw-bytes", where, 0,
                               f"deny term '{term}' present in raw PDF bytes (metadata/XMP/objects)"))
    for m in set(LOCAL_PATH_RE.findall(raw_s)):
        out.append(Finding("HIGH", "pdf-raw-path", where, 0, m))
    return out


def scan_zip(path: Path, deny: DenyList, allow: list[re.Pattern]) -> list[Finding]:
    out: list[Finding] = []
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            name = info.filename
            where = f"{path}!{name}"
            if "/.git/" in "/" + name or name.startswith(".git/"):
                out.append(Finding("HIGH", "vcs-dir-in-archive", where, 0, "remove .git from the archive"))
                continue
            if deny and deny.hits(name):
                out.append(Finding("HIGH", "deny-term-in-name", where, 0, name))
            ext = Path(name).suffix.lower()
            if info.is_dir() or info.file_size > 20_000_000:
                continue
            if ext in TEX_EXT | BIB_EXT | TEXT_EXT or Path(name).name in TEXT_NAMES:
                data = z.read(info).decode("utf-8", errors="replace")
                out += scan_text(data, where, ext, deny, allow)
            elif ext == ".pdf":
                with tempfile.TemporaryDirectory() as td:
                    p = Path(td) / "x.pdf"
                    p.write_bytes(z.read(info))
                    for f in scan_pdf(p, deny, allow):
                        f.file = where
                        out.append(f)
    return out


def iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if ".git" in dirnames:
            yield Path(dirpath) / ".git"
            dirnames.remove(".git")
        for fn in filenames:
            yield Path(dirpath) / fn


def scan_path(root: Path, deny: DenyList, allow: list[re.Pattern]) -> list[Finding]:
    out: list[Finding] = []
    for p in iter_files(root):
        if p.name == ".git":
            out.append(Finding("MEDIUM", "vcs-dir", str(p), 0,
                               "exclude .git from submitted archives / anonymous mirrors"))
            cfg = p / "config"
            if cfg.is_file():
                for f in scan_text(cfg.read_text(errors="replace"), str(cfg), ".cfg", deny, allow):
                    out.append(f)
            continue
        if deny and deny.hits(p.name):
            out.append(Finding("HIGH", "deny-term-in-name", str(p), 0, p.name))
        ext = p.suffix.lower()
        try:
            if ext in TEX_EXT | BIB_EXT | TEXT_EXT or p.name in TEXT_NAMES:
                if p.stat().st_size > 20_000_000:
                    continue
                out += scan_text(p.read_text(encoding="utf-8", errors="replace"), str(p), ext, deny, allow)
            elif ext == ".pdf":
                out += scan_pdf(p, deny, allow)
            elif ext == ".zip":
                out += scan_zip(p, deny, allow)
        except (OSError, zipfile.BadZipFile) as e:
            out.append(Finding("LOW", "unreadable", str(p), 0, str(e)))
    return out


# ---------------------------------------------------------------- CLI
def run(paths: list[str], deny: DenyList, allow_urls: list[str], min_sev: str = "LOW") -> list[Finding]:
    allow = [re.compile(a, re.I) for a in DEFAULT_ALLOW_URL + list(allow_urls)]
    findings: list[Finding] = []
    for p in paths:
        findings += scan_path(Path(p), deny, allow)
    th = SEVERITIES[min_sev]
    findings = [f for f in findings if SEVERITIES[f.severity] >= th]
    findings.sort(key=lambda f: (-SEVERITIES[f.severity], f.file, f.line))
    return findings


def selftest() -> int:
    """Build a synthetic submission and check that the scanner catches each leak class."""
    # TOY: synthetic identities only
    tex = r"""\documentclass{llncs}
\title{Packed Test Polynomials}
\author{Alice Example\inst{1}}
\institute{Example University, \email{alice@uni.example.net}}
\begin{document}
As shown in our previous work~\cite{ex24}, packing helps.
Code: \url{https://github.com/aexample/lutpack} and \url{https://anonymous.4open.science/r/lutpack-1234}.
Third party: \url{https://github.com/thirdparty/lib}.
% compiled from /home/aexample/papers/lut
\section*{Acknowledgements} We thank Bob. This work was supported by grant no. 42.
\end{document}
"""
    clean = r"""\documentclass[runningheads]{llncs}
\title{Packed Test Polynomials}
\author{Anonymous Submission}
\institute{}
\begin{document}
As shown by Example et al.~\cite{ex24}, packing helps.
Code: \url{https://anonymous.4open.science/r/lutpack-1234}.
\end{document}
"""
    bib = "@misc{ex24, author={Alice Example and Carol Other}, title={{PBS} tricks}, year={2024}}\n"
    code = "# author: aexample\nDATA = '/home/aexample/data'\n"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "leaky"
        d.mkdir()
        (d / "main.tex").write_text(tex)
        (d / "refs.bib").write_text(bib)
        (d / "run.py").write_text(code)
        zpath = Path(td) / "artifact.zip"
        with zipfile.ZipFile(zpath, "w") as z:
            z.writestr("artifact/.git/config", "[remote]\nurl = https://github.com/aexample/lutpack\n")
            z.writestr("artifact/README.md", "Extends our prior work on packing.\n")
        c = Path(td) / "clean"
        c.mkdir()
        (c / "main.tex").write_text(clean)
        (c / "refs.bib").write_text(bib)

        deny = DenyList(["Alice Example", "aexample", "Example University"])
        f_leaky = run([str(d), str(zpath)], deny, [])
        kinds = {f.kind for f in f_leaky}
        expected = {"deny-term", "email", "tex-\\author", "tex-\\institute", "first-person-self-cite",
                    "url-deny-term", "local-path", "acknowledgements", "funding-statement",
                    "vcs-dir-in-archive", "deny-term-in-bib", "personal-host-url"}
        missing = expected - kinds
        f_clean = run([str(c)], deny, [])
        high_clean = [f for f in f_clean if f.severity == "HIGH"]
        anon_flagged = any("anonymous.4open.science" in f.text and "url" in f.kind
                           for f in f_leaky + f_clean)

        pdf_ok = True
        if shutil.which("pdflatex"):
            p = Path(td) / "pdf"
            p.mkdir()
            (p / "t.tex").write_text(
                "\\documentclass{article}\\usepackage{hyperref}"
                "\\hypersetup{pdfauthor={Alice Example},pdftitle={Packed}}"
                "\\begin{document}Hello from aexample.\\end{document}\n")
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "t.tex"], cwd=p,
                               capture_output=True, text=True)
            if (p / "t.pdf").exists():
                pk = {f.kind for f in run([str(p / "t.pdf")], deny, [])}
                pdf_ok = "pdf-meta-author" in pk and "pdf-raw-bytes" in pk
            else:
                print("selftest: pdflatex present but compile failed; skipping PDF part")
    ok = not missing and not high_clean and not anon_flagged and pdf_ok
    print(f"selftest: {len(f_leaky)} findings on leaky sample; missing kinds: {sorted(missing) or 'none'}")
    print(f"selftest: HIGH findings on clean sample: {len(high_clean)}; anonymous mirror flagged: {anon_flagged}; pdf ok: {pdf_ok}")
    for f in high_clean:
        print("   ", f.fmt())
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="files or directories (.tex/.bib/.pdf/.zip/code)")
    ap.add_argument("--deny", help="comma-separated deny terms (names, accounts, affiliations)")
    ap.add_argument("--deny-file", action="append", help="deny-list file (one term per line; 're:' for regex)")
    ap.add_argument("--allow-url", action="append", default=[], help="regex of URLs that are fine (third-party repos)")
    ap.add_argument("--min-severity", default="LOW", choices=list(SEVERITIES))
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the built-in synthetic test")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.paths:
        ap.print_usage()
        return 2
    deny = DenyList.load(a.deny, a.deny_file)
    if not deny:
        print("warning: empty deny-list; only generic patterns are checked (pass --deny or --deny-file)",
              file=sys.stderr)
    findings = run(a.paths, deny, a.allow_url, a.min_severity)
    if a.json:
        print(json.dumps([asdict(f) for f in findings], indent=1))
    else:
        for f in findings:
            print(f.fmt())
        n = {s: sum(f.severity == s for f in findings) for s in SEVERITIES}
        print(f"\nsummary: HIGH={n['HIGH']} MEDIUM={n['MEDIUM']} LOW={n['LOW']}")
    return 1 if any(f.severity == "HIGH" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
