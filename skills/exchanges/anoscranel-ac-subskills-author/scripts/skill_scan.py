#!/usr/bin/env python3
"""skill_scan.py: static, read-only safety scan of one skill directory.

Stdlib only. No network. It never imports, runs or evaluates scanned
content. Each path is checked with lstat first; each regular file is opened
once, read-only, without following links.

Usage: python3 -B skill_scan.py <dir> [--json]
Exit:  0 PASS, 1 FAIL, 2 usage error.

Checks (FAIL unless marked INFO):
  shape      symlinks, special files (fifo, socket, device), hardlinks,
             hidden names (leading dot), __pycache__, files over 256 KiB
  allowlist  .md anywhere; .py .sh .json .yaml only under scripts/ (INFO)
  encoding   text must be strict UTF-8 with no NUL byte
  hidden     zero-width and bidi control characters; a byte-order mark
             anywhere except offset 0 (offset 0 = INFO)
  comment    HTML comments in .md files
  inject     instruction-override, role-switch, system-prompt and
             keep-it-from-the-user phrasing (every text file)
  cred       credential-file paths (every text file)
  exfil      download or decode piped into a shell; netcat exec flag
             (.md and .sh files)
  code       dynamic code execution, a shell flag set true, unsafe
             deserialisation, network-module imports (scripts/ .py, .sh)
  delegate   a Delegate line, or a line that tells the agent to load, use,
             invoke or hand off to a named skill (SKILL.md, subskills/)

Suppression: only in scripts/ .py and .sh files, a line that carries the
comment "#" + " scan:allow <reason>" suppresses the inject, cred, exfil and
code checks on that line. The reason is required. Every allow is printed.
An allow never applies to .md files, and never to the shape, encoding,
hidden, comment or delegate checks.

Limits: one line at a time after unwrapping prose continuation lines
(outside code fences), so a phrase wrapped mid-list-item, across a blank
line or inside a fence is still missed. Patterns, not semantics: a clean
scan is necessary, not sufficient. Pattern strings below are written
(character classes, \\s+) so that they do not match their own source text.
"""
import json
import os
import re
import stat
import sys

MAX_BYTES = 256 * 1024
SCRIPT_EXT = {".py", ".sh", ".json", ".yaml"}
ALLOW_EXT = {".py", ".sh"}

HIDDEN_RX = re.compile(
    "[\u00ad\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff"
    "\U000e0000-\U000e007f]")
ALLOW_RX = re.compile(r"(?:^|\s)#\s*scan:allow\b[ \t]*(.*)$")

INJECT = [
    ("ignore-prior", r"\b(?:ignore|forget)\s+(?:all\s+|any\s+)?(?:of\s+)?"
                     r"(?:the\s+|your\s+)?(?:previous|prior|earlier|above)\s+"
                     r"(?:instructions|rules|prompts|guidance|directions)\b"),
    ("role-switch", r"\byou\s+are\s+now\b"),
    ("system-prompt", r"\bsystem\s+prompt"),
    ("drop-guidance", r"\bdis[r]egard\b"),
    ("hide-from-user", r"\b(?:do\s+not|don['\u2019]t|never)\s+"
                       r"(?:tell|inform|alert|notify)\s+the\s+user\b"
                       r"|\bwithout\s+(?:telling|informing|notifying)\s+the\s+user\b"),
    ("auditor-note", r"\bnote\s+to\s+the\s+(?:auditor|reviewer|scanner)\b"
                     r"|\bpre-?reviewed\s+by\b"),
    ("override", r"\boverride\s+(?:the\s+)?(?:system|safety|security)\b"),
]
CRED = [
    ("cred-path", r"~/[.]ssh\b|[.]ssh/|[.]aws/credentials|keys[.]env\b"
                  r"|[.]config/opencode\b"
                  r"|\bid_(?:rsa|dsa|ecdsa|ed25519)\b|[.]netrc\b"
                  r"|[.]git-credentials\b|[.]bash_history\b|/etc/[s]hadow\b"
                  r"|\bauth[.]json\b"),
]
EXFIL = [
    ("pipe-to-shell", r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:ba|z|da|k)?sh\b"),
    ("pipe-bash", r"\|\s*bash\b"),
    ("b64-to-shell", r"\bbase64\s+(?:-d|--decode)\b[^\n|]*\|\s*(?:ba|z|da|k)?sh\b"),
    ("netcat-e", r"\b(?:nc|ncat|netcat)\b[^\n|]*\s-e\b"),
]
CODE = [
    ("eval", r"\beval\s*\("),
    ("exec", r"\bexec\s*\("),
    ("os-exec", r"\bos\s*\.\s*(?:system|popen|exec[lv]p?e?|spawn[lv]p?e?)\s*\("),
    ("shell-true", r"\bshell\s*=\s*True\b"),
    ("dunder-import", r"__import__\s*\("),
    ("dynamic-import", r"\bimportlib\s*\.\s*import_module\s*\("),
    ("unsafe-load", r"\b(?:pickle|cPickle|marshal|dill)\s*\.\s*loads?\s*\("),
    ("bare-compile", r"(?<![\w.])compile\s*\("),
    ("net-import", r"^\s*(?:import\s+(?:[\w.]+\s*,\s*)*|from\s+)"
                   r"(?:urllib\d?|urllib3|requests|httpx|aiohttp|socket|http"
                   r"|ftplib|smtplib|telnetlib|websockets?|paramiko)\b"),
]
SH_CODE = [("sh-eval", r"(?:^|[;&|]\s*)eval\s")]

INJECT = [(k, re.compile(p, re.I)) for k, p in INJECT]
CRED = [(k, re.compile(p, re.I)) for k, p in CRED]
EXFIL = [(k, re.compile(p, re.I)) for k, p in EXFIL]
CODE = [(k, re.compile(p)) for k, p in CODE]
SH_CODE = [(k, re.compile(p)) for k, p in SH_CODE]

# ---- self-contained rule. lint_tree.py carries the same
# patterns; keep the two copies identical.
_DVERBS = (r"(?:load|use|invoke|call|run|open|consult|apply|follow|read|see|"
           r"delegate\s+to|defer\s+to|switch\s+to|"
           r"pass(?:\s+(?:it|this|work))?\s+to|route(?:\s+(?:it|this))?\s+to|"
           r"hand(?:\s+(?:it|this|work))?\s+(?:off\s+|over\s+)?to)")
DELEG_LINE = re.compile(r"^\s*(?:[>*+-]\s*|\d+\.\s*)?delegate\s*:", re.I)
DELEG_TICK = re.compile(r"\b" + _DVERBS +
                        r"\s+(?:the\s+)?`([a-z0-9][a-z0-9_-]*)`\s+skill\b", re.I)
DELEG_THE = re.compile(r"\b" + _DVERBS +
                       r"\s+the\s+([a-z0-9][a-z0-9_-]*)\s+skill\b(?!['\u2019]s)", re.I)
DELEG_HYPH = re.compile(r"\b" + _DVERBS +
                        r"\s+([a-z0-9]+(?:-[a-z0-9]+)+)\s+skill\b(?!['\u2019]s)", re.I)
DELEG_HAND = re.compile(
    r"\b(?:delegate|defer|hand(?:\s+(?:it|this|work))?\s+(?:off|over)"
    r"|pass(?:\s+(?:it|this|work))?|route(?:\s+(?:it|this))?)\s+to\s+"
    r"(?:the\s+)?`([a-z0-9][a-z0-9_-]*)`", re.I)
DELEG_STOP = {
    "this", "that", "the", "a", "an", "its", "their", "our", "your", "my",
    "new", "own", "same", "parent", "target", "whole", "entire", "each",
    "every", "any", "other", "another", "owning", "owner", "installed",
    "existing", "emitted", "created", "child", "meta", "given", "current",
    "next", "previous", "prior", "scanned", "audited", "staged", "live",
    "old", "flat", "nested", "first", "second", "one", "host", "source",
    "named", "matching", "relevant", "right", "wrong", "correct", "real",
    "finished", "draft", "full", "single", "main", "root", "top", "base",
    "local", "remote", "third-party", "self-authored", "self-contained",
}


# ---- a delegation line wrapped across two physical lines
# matched nothing, because every pattern ran one line at a time, and R1 is
# the law the rebuild enforces. Join a line that ends without terminal
# punctuation with the next line of the same paragraph, then match on the
# unwrapped text. Markdown prose only: inside a code fence a wrap is layout,
# not content. lint_tree.py carries the identical block; keep the two copies
# identical.
TERMINAL_RX = re.compile(r"[.!?:;]\s*$")
FENCE_RX = re.compile(r"^\s*(?:```|~~~)")


def unwrap(text):
    """Return (lines, orig) with wrapped continuation lines joined.

    A line ending without terminal punctuation is collapsed with the next
    line of the same paragraph, so a phrase wrapped across two lines matches
    as one. Blank lines, table rows, headings and every line inside a code
    fence are left as they are. orig[i] is the 1-based original line number
    of lines[i], so a finding still points at the line the reader sees.
    """
    lines = text.split("\n")
    out, orig = [], []
    infence = False
    i = 0
    while i < len(lines):
        ln = lines[i]
        if FENCE_RX.match(ln):
            infence = not infence
            out.append(ln)
            orig.append(i + 1)
            i += 1
            continue
        if infence or not ln.strip() or ln.lstrip().startswith(("|", "#")):
            out.append(ln)
            orig.append(i + 1)
            i += 1
            continue
        cur = ln
        start = i + 1
        while (i + 1 < len(lines) and not TERMINAL_RX.search(cur)
               and not FENCE_RX.match(lines[i + 1])
               and lines[i + 1].strip() and lines[i + 1][:1] not in (" ", "\t")):
            i += 1
            cur += " " + lines[i].lstrip()
        out.append(cur)
        orig.append(start)
        i += 1
    return out, orig


def delegation_hits(text, self_name=""):
    """Return [(line_no, reason)] for lines that hand work to another skill.

    Continuation lines are joined first (unwrap), so a hand-off split across
    two lines still matches; the reported line number is the original one.
    """
    own = {self_name.lower()} if self_name else set()
    hits = []
    lines, orig = unwrap(text)
    for idx, ln in enumerate(lines):
        if DELEG_LINE.match(ln):
            hits.append((orig[idx], "Delegate line"))
            continue
        named = [m.group(1) for rx in (DELEG_TICK, DELEG_HAND) for m in rx.finditer(ln)]
        if any(x.lower() not in own for x in named):
            hits.append((orig[idx], "hands work to a named skill"))
            continue
        loose = [m.group(1) for rx in (DELEG_THE, DELEG_HYPH) for m in rx.finditer(ln)]
        if any(x.lower() not in DELEG_STOP and x.lower() not in own for x in loose):
            hits.append((orig[idx], "hands work to a named skill"))
    return hits


def clip(s, n=80):
    out = []
    for ch in s:
        o = ord(ch)
        out.append(ch if 32 <= o < 127 else "\\u%04x" % o)
    s = "".join(out)
    return s if len(s) <= n else s[:n] + "..."


def skill_name(root):
    p = os.path.join(root, "SKILL.md")
    try:
        if not stat.S_ISREG(os.lstat(p).st_mode):
            return ""
        with open(p, "rb") as f:
            head = f.read(8192).decode("utf-8", "replace")
    except OSError:
        return ""
    m = re.match(r"^---\s*\n(.*?)\n---", head, re.S)
    if not m:
        return ""
    n = re.search(r"^name:\s*['\"]?([a-z0-9][a-z0-9-]*)['\"]?\s*$", m.group(1), re.M)
    return n.group(1) if n else ""


def read_file(p):
    """Open without following links; refuse anything but a regular file."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(p, flags)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError("not a regular file at open time")
        chunks, total = [], 0
        while True:
            b = os.read(fd, 65536)
            if not b:
                break
            chunks.append(b)
            total += len(b)
            if total > MAX_BYTES:
                raise OSError("grew past the size cap while reading")
        return b"".join(chunks)
    finally:
        os.close(fd)


def scan(root):
    findings, allows = [], []

    def add(sev, check, rel, line, detail):
        findings.append({"severity": sev, "check": check, "file": rel,
                         "line": line, "detail": detail})

    if stat.S_ISLNK(os.lstat(root).st_mode):
        add("FAIL", "symlink", ".", 0, "scan root is a symlink")
        return findings, allows, 0
    name = skill_name(root)
    files = []

    def walk_err(e):
        add("FAIL", "unreadable", os.path.relpath(e.filename or root, root), 0, str(e)[:80])

    for dp, dns, fns in os.walk(root, topdown=True, followlinks=False, onerror=walk_err):
        keep = []
        for d in sorted(dns):
            p = os.path.join(dp, d)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                add("FAIL", "symlink", rel, 0, "symlinked directory")
            elif d.startswith("."):
                add("FAIL", "hidden", rel, 0, "hidden directory")
            elif d == "__pycache__":
                add("FAIL", "build-artifact", rel, 0, "__pycache__ directory")
            else:
                keep.append(d)
        dns[:] = keep
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                add("FAIL", "symlink", rel, 0, "symlinked file")
                continue
            if not stat.S_ISREG(st.st_mode):
                add("FAIL", "special-file", rel, 0, "not a regular file")
                continue
            if st.st_nlink > 1:
                add("FAIL", "hardlink", rel, 0, "link count %d" % st.st_nlink)
                continue
            if fn.startswith("."):
                add("FAIL", "hidden", rel, 0, "hidden file")
                continue
            ext = os.path.splitext(fn)[1]
            in_scripts = rel.startswith("scripts/")
            if ext == ".md":
                pass
            elif ext in SCRIPT_EXT and in_scripts:
                add("INFO", "script-file", rel, 0, "code or data file under scripts/")
            else:
                add("FAIL", "allowlist", rel, 0,
                    "type %s not allowed here" % (ext or "(none)"))
                continue
            if st.st_size > MAX_BYTES:
                add("FAIL", "size", rel, 0, "%d bytes > %d" % (st.st_size, MAX_BYTES))
                continue
            files.append((rel, p, ext, in_scripts))

    for rel, p, ext, in_scripts in files:
        try:
            data = read_file(p)
        except OSError as e:
            add("FAIL", "unreadable", rel, 0, str(e)[:80])
            continue
        if b"\0" in data:
            add("FAIL", "encoding", rel, data[:data.index(b"\0")].count(b"\n") + 1,
                "NUL byte (binary content)")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as e:
            add("FAIL", "encoding", rel, data[:e.start].count(b"\n") + 1,
                "not UTF-8 at byte %d" % e.start)
            continue
        is_md = ext == ".md"
        deleg_scope = is_md and (rel == "SKILL.md" or rel.startswith("subskills/"))
        can_allow = in_scripts and ext in ALLOW_EXT
        content = list(INJECT) + list(CRED)
        if is_md or ext == ".sh":
            content += EXFIL
        if in_scripts and ext in ALLOW_EXT:
            content += CODE
        if in_scripts and ext == ".sh":
            content += SH_CODE
        pos = 0
        for n, ln in enumerate(text.split("\n"), 1):
            for m in HIDDEN_RX.finditer(ln):
                if m.group(0) == "\ufeff" and pos + m.start() == 0:
                    add("INFO", "bom-start", rel, n, "byte-order mark at offset 0")
                else:
                    add("FAIL", "hidden-char", rel, n, "U+%04X" % ord(m.group(0)))
            pos += len(ln) + 1
            if is_md and "<!--" in ln:
                add("FAIL", "html-comment", rel, n, "HTML comment in markdown")
            allowed = None
            if can_allow:
                am = ALLOW_RX.search(ln)
                if am:
                    reason = am.group(1).strip()
                    if reason:
                        allowed = reason
                    else:
                        add("FAIL", "allow-no-reason", rel, n, "allow marker without a reason")
            hit = [(k, m) for k, rx in content for m in [rx.search(ln)] if m]
            if hit and allowed:
                allows.append({"file": rel, "line": n, "reason": clip(allowed),
                               "suppressed": [k for k, _ in hit]})
            else:
                for k, m in hit:
                    add("FAIL", k, rel, n, clip(m.group(0), 60))
        if deleg_scope:
            for n, why in delegation_hits(text, name):
                add("FAIL", "delegate", rel, n, why)
    return findings, allows, len(files)


def main(argv):
    args = [a for a in argv if a != "--json"]
    as_json = len(args) != len(argv)
    if len(args) != 1 or len(argv) - len(args) > 1 or args[0].startswith("-"):
        sys.stderr.write("usage: python3 -B skill_scan.py <dir> [--json]\n")
        return 2
    root = args[0].rstrip("/") or "/"
    if not os.path.lexists(root) or not (os.path.isdir(root) or os.path.islink(root)):
        sys.stderr.write("usage error: not a directory: %s\n" % root)
        return 2
    findings, allows, n = scan(root)
    fails = [f for f in findings if f["severity"] == "FAIL"]
    verdict = "FAIL" if fails else "PASS"
    if as_json:
        print(json.dumps({"tool": "skill_scan", "version": 1, "root": root,
                          "verdict": verdict, "files_scanned": n,
                          "fail": len(fails), "info": len(findings) - len(fails),
                          "findings": findings, "allows": allows}, indent=1))
    else:
        for f in findings:
            print("%-4s  %-15s %s:%d  %s" % (f["severity"], f["check"], f["file"],
                                            f["line"], f["detail"]))
        for a in allows:
            print("ALLOW %s:%d  [%s]  %s" % (a["file"], a["line"],
                                            ",".join(a["suppressed"]), a["reason"]))
        print("SCAN %s (%d files, %d fail, %d info, %d allow%s)" % (
            verdict, n, len(fails), len(findings) - len(fails), len(allows),
            "" if len(allows) == 1 else "s"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
