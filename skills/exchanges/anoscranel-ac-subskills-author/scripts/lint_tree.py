#!/usr/bin/env python3
"""lint_tree.py — deterministic linter for skills-with-subskills (house standard, rules 1-4).

Checks the 4 enforceable rules + the bidirectional index-vs-disk check,
plus the self-contained rule (no Delegate or hand-off line).
Exit 0 = PASS, 1 = FAIL. Prints one line per violation, plus warnings and
manual-review flags.

Desk law 6: this is a deterministic script, not an LLM judge. It does NOT check
the narrow-only half of Rule 4 (a leaf widening an ancestor's prohibition) —
that is flagged for the manual review gate instead.

Usage: python3 lint_tree.py [--no-enum] <skill-dir>
"""
import os
import re
import sys
import unicodedata

WARN_ROWS = 40
MAX_ROWS = 60
MAX_DEPTH = 2  # index -> index -> leaf

# Frontmatter fields a subskill/leaf must carry.
REQUIRED_FIELDS = ["name", "domain", "trigger", "anti_trigger", "scope", "status"]
LEGAL_STATUS = {"seedling", "growing", "verified", "stale", "deprecated"}

VERB_INITIAL = re.compile(
    r"^\s*(?:[-*]\s+|\d+\.\s+)?("
    r"run|write|read|check|verify|create|add|edit|delete|remove|install|use|do|"
    r"never|always|confirm|ensure|halt|stop|fix|set|keep|map|name|split|merge|"
    r"validate|lint|vet|emit|decide|record|report|present|hand|open|close|list"
    r")\b",
    re.IGNORECASE,
)


# ---- self-contained rule. skill_scan.py carries the same
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
# not content. skill_scan.py carries the identical block; keep the two copies
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


def fail(msg, errs):
    errs.append(msg)


def parse_frontmatter(text):
    """Return (fm_dict, body) or (None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    block = text[3:end].strip("\n")
    body = text[end + 4:]
    fm = {}
    for line in block.splitlines():
        # accept an optionally quoted key; strip one pair of matching
        # quotes from the value.
        m = re.match(r"""^(["']?)([A-Za-z_]+)\1:\s*(.*)$""", line)
        if m:
            v = m.group(3).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fm[m.group(2)] = v
    return fm, body


def count_table_rows(body):
    """Count markdown routing-table data rows (| ... | ... |), excluding the
    header separator row (|---|) and the header row itself."""
    rows = 0
    lines = body.splitlines()
    for i, ln in enumerate(lines):
        s = ln.strip()
        # a line is a table row when it starts with "|" (no trailing
        # "|" required)
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+$", s):  # separator row
            continue
        rows += 1
    # subtract one header row per contiguous table block
    # (approximation: each table contributes one header line)
    headers = 0
    prev_blank = True
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("|"):
            if prev_blank:
                headers += 1
            prev_blank = False
        else:
            prev_blank = True
    return max(0, rows - headers)


# small confusables map (Cyrillic/Greek lowercase lookalikes ->
# Latin), applied after casefold. NFKC alone does not fold these.
CONFUSABLES = str.maketrans({
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0441": "c", "\u0443": "y", "\u0445": "x", "\u0456": "i",
    "\u0458": "j", "\u0455": "s", "\u0501": "d", "\u04bb": "h",
    "\u03bf": "o", "\u03b1": "a", "\u03b9": "i", "\u03ba": "k",
    "\u03bd": "v", "\u03c1": "p", "\u03c5": "u",
})


def norm_scope(s):
    """NFKC, casefold, fold confusables, strip one pair of matching outer
    quotes, collapse all Unicode whitespace and U+200B to one space, strip
    trailing .;,"""
    s = unicodedata.normalize("NFKC", s).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    s = s.casefold().translate(CONFUSABLES)
    s = re.sub(r"[\s\u200b]+", " ", s).strip()
    s = re.sub(r"[.;,]+$", "", s).strip()
    return s


def is_pure_toc(body):
    """An intermediate INDEX.md body may hold only headings, table rows, blank
    lines, and the frontmatter. Any verb-initial body line makes it content-
    bearing -> forbidden."""
    for ln in body.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):  # heading: verb test on the heading text
            if VERB_INITIAL.match(s.lstrip("#").strip()):
                return False, s
            continue
        if s.startswith("|"):  # table row: verb test on every cell
            for cell in s.strip("|").split("|"):
                if VERB_INITIAL.match(cell.strip()):
                    return False, s
            continue
        if VERB_INITIAL.match(s):
            return False, s
        # a non-heading non-table prose line: treat as content if it has words
        if re.search(r"[A-Za-z]{4,}", s):
            return False, s
    return True, None


def main():
    args = sys.argv[1:]
    no_enum = "--no-enum" in args
    args = [a for a in args if a != "--no-enum"]
    if len(args) != 1:
        print("usage: python3 lint_tree.py [--no-enum] <skill-dir>")
        return 2
    root = args[0].rstrip("/")
    errs, warns, manual = [], [], []

    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        print("FAIL: no SKILL.md at %s" % skill_md)
        return 1
    sub_root = os.path.join(root, "subskills")
    has_subs = os.path.isdir(sub_root)

    # ---- parent domain chain ---------------------------------------------
    try:
        ptext = open(skill_md, encoding="utf-8").read()
    except OSError as e:
        print("FAIL: read: SKILL.md unreadable (%s)" % e)
        return 1
    except UnicodeDecodeError as e:  # fail closed, no traceback
        print("FAIL: read: SKILL.md is not valid UTF-8 (%s) — fail-closed" % e)
        return 1
    pfm, pbody = parse_frontmatter(ptext)
    parent_domain = (pfm or {}).get("domain", "")
    # Agent Skills spec: non-spec keys belong under `metadata:`. Accept
    # `metadata:\n  domain: x` as well as a legacy top-level `domain:`.
    if pfm is not None and not parent_domain:
        mm = re.search(r"^metadata:[ \t]*\n((?:[ \t]+[^\n]*\n?)*)", ptext.split("\n---", 1)[0], re.M)
        if mm:
            dm = re.search(r"^[ \t]+domain:[ \t]*[\"']?([^\"'\n]+?)[\"']?[ \t]*$", mm.group(1), re.M)
            if dm:
                parent_domain = dm.group(1).strip()
                pfm["domain"] = parent_domain
    # FAIL-CLOSED: a SKILL.md with no frontmatter or no domain cannot anchor the
    # domain chain — every parent-level check (enum, rsi guard, prefix rule) is
    # meaningless without it. Reject rather than skip (closes the pre-existing
    # fail-open where a frontmatter-less SKILL.md escaped the whole chain).
    if not pfm:
        fail("header: SKILL.md has no YAML frontmatter — cannot anchor the "
             "domain chain (name/domain required)", errs)
    elif not parent_domain:
        fail("header: SKILL.md frontmatter missing required 'domain:' — the "
             "domain chain cannot be checked without it", errs)
    # the Agent Skills spec defines a Skill by name and description.
    if pfm:
        for f in ("name", "description"):
            if not pfm.get(f):
                fail("header: SKILL.md frontmatter missing required '%s:'" % f, errs)

    # ---- closed top-segment enum (from domain-vocabulary.md) --------------
    # The top segment of any domain: must be in the closed enum, or the lint
    # fails. Enum lives in ac-subskills-author/subskills/domain-vocabulary.md.
    # FAIL-CLOSED: a missing/unparseable/empty enum is a LINT FAIL, not a pass.
    # Scoped: only rows under the "## The enum" heading count as legal segments.
    enum_segments = set()
    enum_ok = False
    vocab = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "subskills", "domain-vocabulary.md")
    if os.path.isfile(vocab):
        try:
            vtext = open(vocab, encoding="utf-8").read()
        except OSError as e:
            fail("read: domain-vocabulary.md unreadable (%s)" % e, errs)
            vtext = ""
        except UnicodeDecodeError as e:  # fail closed
            fail("read: domain-vocabulary.md is not valid UTF-8 (%s) — "
                 "fail-closed" % e, errs)
            vtext = ""
        # isolate the "## The enum" section (up to the next "## " heading or EOF)
        sec = re.search(r"^##\s+The enum.*?\n(.*?)(?=^##\s|\Z)",
                        vtext, re.MULTILINE | re.DOTALL)
        if sec:
            for m in re.finditer(r"^\|\s*`([a-z0-9-]+)`\s*\|", sec.group(1),
                                 re.MULTILINE):
                seg = m.group(1)
                if seg not in ("top-segment", "segment"):
                    enum_segments.add(seg)
        enum_ok = bool(enum_segments)
    # the meta-skill linting itself ships the enum; a lint run on a FOREIGN
    # skill (no sibling vocab) skips the enum check. But when the vocab exists
    # and yields nothing, that is a broken closed-enum -> fail closed.
    vocab_present = os.path.isfile(vocab)
    # no vocabulary beside the linter -> fail closed unless --no-enum.
    if not vocab_present:
        if no_enum:
            warns.append("closed-enum check SKIPPED (no vocabulary beside the "
                          "linter; --no-enum passed)")
        else:
            fail("R3 enum: no domain-vocabulary.md beside the linter — closed-enum "
                 "check cannot run; failing closed (pass --no-enum to skip)", errs)
    if vocab_present and not enum_ok:
        fail("R3 enum: domain-vocabulary.md present but no enum segments parsed "
             "(missing '## The enum' table or format drift) — closed enum is "
             "void; failing closed", errs)

    # reject any domain segment that is empty, ".", "..", or outside
    # [a-z0-9-].
    def bad_segments(d):
        return [g for g in d.split("/")
                if g in ("", ".", "..") or not re.fullmatch(r"[a-z0-9-]+", g)]
    if parent_domain and bad_segments(parent_domain):
        fail("R3 domain: SKILL.md domain '%s' has an illegal segment (empty, '.', "
             "'..', or outside [a-z0-9-])" % parent_domain, errs)

    # parent SKILL.md's own top domain segment must be in the enum too
    if parent_domain and enum_ok:
        ptop = parent_domain.split("/")[0]
        if ptop not in enum_segments:
            fail("R3 enum: SKILL.md top domain segment '%s' not in closed enum "
                 "(domain-vocabulary.md)" % ptop, errs)

    # Reserved parent domain: only the GENUINE rsi core may declare parent
    # `domain: rsi`. The core is identified by name == "rsi", a real
    # schema/log-schema.md (existence AND non-trivial content mentioning the
    # schema), AND zero subskills/ leaves (the core is a flat skill). Any OTHER
    # skill whose SKILL.md declares `domain: rsi` is smuggling its whole tree
    # under the reserved segment (which would disable the per-leaf prefix check)
    # -> lint error. A bare `name: rsi` + empty marker file fails the
    # content check; since R2 a file holding the single token `task_outcome`
    # padded past 200 bytes fails too (word-boundary + word-count fingerprint,
    # an earlier audit). A forgery written as real prose still passes: the manual
    # review in audit-skill stage 5 is the binding check.
    if parent_domain and parent_domain.split("/")[0] == "rsi":
        parent_name = (pfm or {}).get("name", "")
        marker = os.path.join(root, "schema", "log-schema.md")
        marker_ok = False
        if os.path.isfile(marker):
            try:
                mtext = open(marker, encoding="utf-8").read()
                # content fingerprint: a real schema names
                # task_outcome as a whole word and is written prose (>= 20
                # whitespace-separated words, > 200 bytes). A 2-byte marker or
                # a single token padded past 200 bytes fails.
                marker_ok = (bool(re.search(r"\btask_outcome\b|\bcallID\b.*\boutcome\b", mtext, re.S))
                             and len(mtext.split()) >= 20 and len(mtext) > 200)
            except OSError:
                marker_ok = False
            except UnicodeDecodeError:  # fail closed
                marker_ok = False
        has_leaves = os.path.isdir(sub_root) and any(
            fn.endswith(".md")
            for _, _, fns in os.walk(sub_root) for fn in fns)
        is_genuine_core = (parent_name in ("rsi", "ac-rsi") and marker_ok and not has_leaves)
        if not is_genuine_core:
            fail("R3 rsi: SKILL.md declares reserved parent domain 'rsi' but is "
                 "not the genuine rsi core (name='%s'). Only the rsi core (name "
                 "'rsi' or 'ac-rsi', real schema/log-schema.md, no subskills) may hold "
                 "parent domain 'rsi'." % (parent_name or "?"), errs)

    # ---- Rule 1: max depth 2 ---------------------------------------------
    if has_subs:
        for dirpath, dirnames, filenames in os.walk(sub_root):
            rel = os.path.relpath(dirpath, sub_root)
            depth = 0 if rel == "." else rel.count(os.sep) + 1
            # a nested subskills/ under subskills/ -> depth violation
            if os.path.basename(dirpath) == "subskills" and rel != ".":
                fail("R1 depth: nested subskills/ at %s" % dirpath, errs)
            # INDEX.md deeper than one group level -> 3rd-level index
            if "INDEX.md" in filenames and depth > 1:
                fail("R1 depth: INDEX.md at depth %d (>2): %s"
                     % (depth + 1, dirpath), errs)
            # subskills/<group>/<leaf>.md is the deepest legal form.
            for fn in filenames:
                if fn.endswith(".md") and depth + 1 > 2:
                    fail("R1 depth: %s has %d path segments under subskills/ "
                         "(max 2)" % (os.path.join(rel, fn), depth + 1), errs)
            # a group directory that holds leaves needs an INDEX.md.
            if depth >= 1 and "INDEX.md" not in filenames and any(
                    fn.endswith(".md") for fn in filenames):
                fail("R1 group: %s holds leaves but no INDEX.md" % rel, errs)

    # ---- word band (450-650) on SKILL.md and every leaf --------------------
    # Added 2026-11-11 after a desk audit found 56 files outside the band while
    # lint reported PASS: the band was enforced only by an ad-hoc shell loop.
    # A gate that is not mechanical is not a gate.
    WORD_LO, WORD_HI = 450, 650

    def _wc(path):
        try:
            return len(open(path, encoding="utf-8").read().split())
        except (OSError, UnicodeDecodeError):
            return -1

    # SKILL.md is a router, not a leaf: many shipped skills carry a compact
    # index. The 450 floor is enforced on LEAVES (the stated spec); for
    # SKILL.md a short body is a warning, an overlong one is a failure.
    n_parent = _wc(skill_md)
    if n_parent > 0:
        if n_parent < WORD_LO:
            warns.append("word band: SKILL.md has %d words, below the %d floor "
                         "(warning only; leaves are gated)" % (n_parent, WORD_LO))
        elif n_parent > WORD_HI:
            warns.append("word band: SKILL.md has %d words, above the %d ceiling "
                         "(warning only; SKILL.md is a router index)"
                         % (n_parent, WORD_HI))

    # ---- collect leaf / intermediate files --------------------------------
    md_files = []
    if has_subs:
        for dirpath, dirnames, filenames in os.walk(sub_root):
            # FAIL any symlink under subskills/ (files and directories).
            for n in dirnames + filenames:
                p = os.path.join(dirpath, n)
                if os.path.islink(p):
                    fail("symlink: %s is a symlink (forbidden under subskills/)"
                         % os.path.relpath(p, root), errs)
            dirnames[:] = [d for d in dirnames
                           if not os.path.islink(os.path.join(dirpath, d))]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                if os.path.islink(p):
                    continue
                # no file named SKILL.md under subskills/ --
                # opencode's skills/**/SKILL.md glob would register it as a
                # global skill.
                if fn.lower() == "skill.md":
                    fail("skillmd: %s is a SKILL.md under subskills/ (opencode's "
                         "skills/**/SKILL.md glob would register it as a global "
                         "skill)" % os.path.relpath(p, root), errs)
                # every file under subskills/ must end in lowercase .md.
                if not fn.endswith(".md"):
                    fail("non-md: %s under subskills/ does not end in lowercase "
                         ".md" % os.path.relpath(p, root), errs)
                    continue
                md_files.append(p)

    # flat is preferred, not
    # mandatory. A tree with <= 60 leaves that still uses a group directory
    # gets a WARN, never a FAIL (60 is a house number, not measured).
    if has_subs:
        n_leaves = sum(1 for p in md_files if os.path.basename(p) != "INDEX.md")
        groups = sorted(d for d in os.listdir(sub_root)
                        if os.path.isdir(os.path.join(sub_root, d))
                        and not os.path.islink(os.path.join(sub_root, d)))
        if groups and n_leaves <= MAX_ROWS:
            warns.append("R2 flat-preferred: %d leaves (<= %d) but group "
                         "director%s %s under subskills/; flat depth-1 is "
                         "preferred (house limit, not measured)"
                         % (n_leaves, MAX_ROWS, "y" if len(groups) == 1 else "ies",
                            ", ".join(groups)))

    scopes = {}
    indexed_targets = set()

    # ---- SKILL.md index rows (Rule 2) + gather index targets -------------
    def scan_index(body, src):
        rows = count_table_rows(body)
        if rows > MAX_ROWS:
            fail("R2 index ceiling: %s has %d rows (> %d)" % (src, rows, MAX_ROWS), errs)
        elif rows > WARN_ROWS:
            warns.append("R2 warn: %s has %d rows (> %d)" % (src, rows, WARN_ROWS))
        # collect index targets only from table rows outside HTML
        # comments; accept `subskills/...md` and ](subskills/...md) forms.
        nocomment = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        for ln in nocomment.splitlines():
            if not ln.strip().startswith("|"):
                continue
            for m in re.finditer(
                    r"`(subskills/[^`]+?\.md)`|\]\((subskills/[^)\s]+?\.md)\)", ln):
                indexed_targets.add(m.group(1) or m.group(2))

    # resolve every relative markdown link and backticked relative path
    # (a backticked token starting with ./ or ../) against the file's own
    # directory; FAIL when the target is missing or resolves outside the root.
    real_root = os.path.realpath(root)

    def check_links(body, fpath, offset=0):
        src = os.path.relpath(fpath, root)
        infence = False
        for n, ln in enumerate(body.splitlines(), 1 + offset):
            if re.match(r"^\s*(```|~~~)", ln):
                infence = not infence
                continue
            if infence:
                continue
            tgts = [m.group(1) for m in
                    re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", ln)]
            tgts += [m.group(1) for m in
                     re.finditer(r"`(\.{1,2}/[^`\s]+)`", ln)]
            for t in tgts:
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", t) or t.startswith(
                        ("#", "/", "~")):
                    continue
                path = t.split("#")[0]
                if not path:
                    continue
                full = os.path.realpath(os.path.join(os.path.dirname(fpath), path))
                if not (full == real_root or full.startswith(real_root + os.sep)):
                    fail("link: %s (line %d) -> %s resolves outside the skill "
                         "root" % (src, n, t), errs)
                elif not os.path.exists(full):
                    fail("link: %s (line %d) -> %s target missing"
                         % (src, n, t), errs)

    check_links(pbody, skill_md, ptext[:len(ptext) - len(pbody)].count("\n"))
    self_name = (pfm or {}).get("name", "")
    for n, why in delegation_hits(ptext, self_name):  # R1 self-contained
        fail("R1 self-contained: SKILL.md line %d: %s (a skill depends on no "
             "other skill; write the procedure in-tree)" % (n, why), errs)

    scan_index(pbody, "SKILL.md")

    # ---- per-file checks ---------------------------------------------------
    for path in sorted(md_files):
        rel = os.path.relpath(path, root)
        try:
            text = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError) as e:
            fail("read: %s is not valid UTF-8 (%s) — fail-closed" % (rel, e), errs)
            continue
        fm, body = parse_frontmatter(text)
        base = os.path.basename(path)
        is_index = base == "INDEX.md"
        check_links(body, path, text[:len(text) - len(body)].count("\n"))
        for n, why in delegation_hits(text, self_name):  # R1 self-contained
            fail("R1 self-contained: %s line %d: %s (a leaf holds its full "
                 "procedure; no hand-off to another skill)" % (rel, n, why), errs)

        if fm is None:
            fail("header: %s missing frontmatter" % rel, errs)
            continue

        # required fields
        for f in REQUIRED_FIELDS:
            if f not in fm or not fm[f]:
                fail("header: %s missing required field '%s'" % (rel, f), errs)

        # status legal
        st = fm.get("status", "")
        if st and st not in LEGAL_STATUS:
            fail("header: %s illegal status '%s'" % (rel, st), errs)

        # Rule 4: unique scope
        sc = fm.get("scope", "")
        if sc:
            key = norm_scope(sc)
            if key in scopes:
                fail("R4 unique-scope: scope claimed twice: '%s' in %s and '%s' "
                     "in %s" % (scopes[key][1], scopes[key][0], sc, rel), errs)
            else:
                scopes[key] = (rel, sc)

        # Rule 3 / in-domain: domain must be a strict prefix-extension of parent.
        # EXCEPTION: the reserved `rsi` segment is exempt from the prefix rule (an
        # RSI leaf observes its parent, it does not join the parent's chain), but is
        # held to a STRICTER template check: only a leaf named
        # `00-rsi` with the template anti_trigger may claim `domain: rsi`.
        dom = fm.get("domain", "")
        if dom and bad_segments(dom):
            fail("R3 domain: %s domain '%s' has an illegal segment (empty, '.', "
                 "'..', or outside [a-z0-9-])" % (rel, dom), errs)
        is_rsi = dom.split("/")[0] == "rsi" if dom else False
        if parent_domain and dom and not is_rsi:
            if not (dom == parent_domain or dom.startswith(parent_domain + "/")):
                fail("R3 in-domain: %s domain '%s' not under parent '%s'"
                     % (rel, dom, parent_domain), errs)
        if is_rsi:
            base = os.path.basename(path)
            anti = fm.get("anti_trigger", "")
            if base != "00-rsi.md":
                fail("R3 rsi: %s claims reserved domain 'rsi' but is not named "
                     "00-rsi.md" % rel, errs)
            required_anti = ("Never blocks a task; never rewrites a file; "
                             "never installs anything.")
            if anti != required_anti:
                fail("R3 rsi: %s anti_trigger must be the RSI template "
                     "('%s')" % (rel, required_anti), errs)
            # (c): scope must claim THIS skill only. Positive requirement:
            # the scope must anchor to a single skill (the word "this" + "skill"),
            # AND must not claim multiple/all skills (broad synonym net). The
            # manual review backstops novel phrasings; lint is the speed bump.
            sc = fm.get("scope", "")
            low = sc.lower()
            # whole-word anchor
            has_single_anchor = bool(re.search(r"\bthis skill\b", low))
            # phrase-with-spaces patterns (not bare substrings) so the legit
            # phrase "no other skill" does NOT trip "other skills".
            multi = any(p in low for p in (
                "all skills", "every skill", "each skill", "other skills",
                "across skills", "any skill", "all the skills", "every leaf",
                "all leaves", "every subskill", "all subskills",
                "whole pipeline", "all pipeline", "every pipeline"))
            # any plural "skills", or every/each/any/other/sibling before
            # "skill" not preceded by "no ", is multi-skill.
            if re.search(r"\bskills\b", low) or re.search(
                    r"(?<!\bno )\b(?:every|each|any|other|sibling)\s+skill\b",
                    low):
                multi = True
            if multi:
                fail("R3 rsi: %s scope claims multiple/all skills ('%s') — an "
                     "RSI leaf observes THIS skill only (house rule)"
                     % (rel, sc), errs)
            elif not has_single_anchor:
                fail("R3 rsi: %s scope must anchor to a single skill (contain "
                     "'this ... skill'); got '%s' (house rule)" % (rel, sc), errs)

        # Closed enum: the top segment of the domain must be in the enum
        if dom and enum_ok:
            top = dom.split("/")[0]
            if top not in enum_segments:
                fail("R3 enum: %s top domain segment '%s' not in closed enum "
                     "(domain-vocabulary.md)" % (rel, top), errs)

        # Rule 3 pure-TOC: INDEX.md intermediates must be pure TOC
        if is_index:
            ok, line = is_pure_toc(body)
            if not ok:
                fail("R3 pure-TOC: %s has content-bearing line: %s" % (rel, line), errs)
            scan_index(body, rel)  # intermediates also count toward R2 + index targets

    # ---- R3 (J9 ranks 3-4): install-name charset; one SKILL.md per tree ----
    # The name becomes the install directory name, so it must be a plain slug.
    pname = (pfm or {}).get("name", "")
    if pname and not re.match(r"^[a-z0-9][a-z0-9-]{0,63}$", pname):
        fail("header: SKILL.md name '%s' must match ^[a-z0-9][a-z0-9-]{0,63}$ "
             "(it becomes the install directory)" % pname, errs)
    # no file named SKILL.md (any case) anywhere in the tree
    # except the root one. Under subskills/ the walk above already reports it.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if not os.path.islink(os.path.join(dirpath, d))
                       and os.path.join(dirpath, d) != sub_root]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            if fn.lower() == "skill.md" and p != skill_md:
                fail("skillmd: %s is a second SKILL.md in the tree (only the root "
                     "one is allowed; opencode's skills/**/SKILL.md glob would "
                     "register it as a global skill)" % os.path.relpath(p, root), errs)

    # ---- Bidirectional index-vs-disk (Rule 4 / D6.2) -----------------------
    on_disk = set()
    for path in md_files:
        on_disk.add(os.path.relpath(path, root).replace(os.sep, "/"))
    # every indexed file exists
    for t in sorted(indexed_targets):
        if t not in on_disk:
            fail("bidirectional: indexed file missing on disk: %s" % t, errs)
    # every file on disk is indexed
    for t in sorted(on_disk):
        if t not in indexed_targets:
            fail("bidirectional: file on disk not indexed: %s" % t, errs)

    # ---- word band on every leaf ------------------------------------------
    for path in md_files:
        if os.path.basename(path) == "INDEX.md":
            continue
        n = _wc(path)
        if n <= 0:
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        # A pure reference leaf (table-dominant, under 40% prose) is a lookup
        # artefact: its length is set by the data it maps, not by argument.
        try:
            _txt = open(path, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            _txt = ""
        _prose = sum(len(ln.split()) for ln in _txt.splitlines()
                     if not ln.lstrip().startswith(("|", "-", "#", ">", "```")))
        if n > 0 and (_prose / n) < 0.40:
            warns.append("word band: %s has %d words but is table-dominant "
                         "(%.0f%% prose) — reference leaf exempt from band"
                         % (rel, n, 100.0 * _prose / n))
            continue
        if n < WORD_LO:
            fail("word band: %s has %d words, below the %d floor"
                 % (rel, n, WORD_LO), errs)
        elif n > WORD_HI:
            fail("word band: %s has %d words, above the %d ceiling"
                 % (rel, n, WORD_HI), errs)

    # ---- Code-damage guard ------------------------------------------------
    # The 2026-10-21 publish lost every empty () and code indentation in the
    # family (release-audit A-20). Fail any leftover instance.
    dmg_rx = [
        (re.compile(r"def [A-Za-z_]\w*:\s*$", re.M), "python def with no parens"),
        (re.compile(r"\.(click|analyze|getClient|isVisible|toBeVisible|integers)\s*;"), "method call with no parens"),
        (re.compile(r"\(\s*=>|\{ ?=>"), "JS arrow with empty pseudo-parens"),
    ]
    for dpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            pth = os.path.join(dpath, fn)
            try:
                txt = open(pth, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue  # unreadable files are already failed elsewhere
            for rx, msg in dmg_rx:
                if rx.search(txt):
                    fail("damage: %s looks publish-stripped (%s)"
                         % (os.path.relpath(pth, root), msg), errs)

    # ---- manual-review flag (the half the linter cannot check) ------------
    manual.append("manual review: confirm no leaf widens an ancestor's "
                  "prohibition (Rule 4 narrow-only half is not mechanical).")

    # ---- report -------------------------------------------------------------
    for w in warns:
        print("WARN: " + w)
    for m in manual:
        print("MANUAL: " + m)
    if errs:
        for e in errs:
            print("FAIL: " + e)
        print("LINT FAIL (%d error%s)" % (len(errs), "" if len(errs) == 1 else "s"))
        return 1
    print("LINT PASS (%d file%s checked, %d scope%s)"
          % (len(md_files), "" if len(md_files) == 1 else "s",
             len(scopes), "" if len(scopes) == 1 else "s"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
