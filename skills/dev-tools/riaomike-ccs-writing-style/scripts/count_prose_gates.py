#!/usr/bin/env python3
"""Count the prose gates that the writing-style skills apply.

The skills state numeric gates for the abstract, the contribution list, the
technical overview, the design-versus-analysis mass, the float inventory, the
cross-reference integrity, and the citation density of the related-work region.
A gate that cannot be counted is not a gate, so this script is the counting
instrument the skills refer to. It reports numbers; the gates' pass and fail
conditions are in the skills' reference files (`ccs-writing-style` owns the
family copy), and the move labels that the allocation gate needs are supplied by
the reader, not guessed here.

Basis (declared so that two runs are comparable):

  words       tokens carrying at least one letter or digit, punctuation
              stripped and case preserved
  paragraphs  blank-line separated blocks
  sentences   split on . ! ? followed by whitespace or end of text, after
              protecting common abbreviations and section references
  jaccard     |set(A) & set(B)| / |set(A) | set(B)| over deduplicated,
              case-folded, punctuation-stripped word sets
  trigram     the same index over adjacent word trigrams
  section words
              by default a section's words include its subsections; --direct
              counts the section's own text only
  caption block
              a line that opens a float caption: an optional number, then
              "Figure"/"Fig."/"Table", then the caption number and its
              separator. This is the basis of census rows B1/B2 (security four
              venues, n=35) and is a lower bound on the rendered float count,
              because a caption the extraction merged into a paragraph line is
              not counted.
  reference call
              a LaTeX \\ref/\\eqref/\\autoref/\\cref/\\pageref command against
              the \\label declarations in the same twin.

Usage:

  # abstract and contribution gates (--items any finds bullets, bold run-in labels or paragraphs)
  python3 scripts/count_prose_gates.py abstract-contributions PAPER.md \
      --abstract-heading "Abstract" \
      --contributions-heading "Contributions|Our Contributions|Main Results" \
      --threat-model-heading "Threat Model|Security Model"

  # section mass gates
  python3 scripts/count_prose_gates.py section-mass PAPER.md \
      --section "design:Design|Construction|Protocol|Scheme" \
      --section "analysis:Security Analysis|Proof|Security of" \
      --section "overview:Technical Overview|Our Techniques|Overview"

  # a raw span, for a single gate
  python3 scripts/count_prose_gates.py span --file abstract.txt

  # evidence-apparatus gates
  python3 scripts/count_prose_gates.py evidence PAPER.md --related-work-heading "Related Work"
  python3 scripts/count_prose_gates.py captions PAPER.md
  python3 scripts/count_prose_gates.py crossrefs PAPER.tex
  python3 scripts/count_prose_gates.py math PAPER.md

  # prove every gate fires, in one run
  python3 scripts/count_prose_gates.py --self-test

Exit codes, and why a measurement device needs them:

   0   every requested pattern matched, every count is reportable, and no gate this run
      could evaluate is breached
  1   a gate this run could evaluate IS breached — a float-free draft, an unresolved
      reference target, a related-work region with no citation key. The reason is printed
      on stderr and listed under `breaches`.
  2   **measurement failure** — the input could not be measured: missing file, empty or
      comment-only text, no `--section` given, a heading pattern that matched nothing. The
      report carries `status: "degenerate"` (or `match_status: "unmatched"` for the item
      list) and the fields it could not measure are null. No verdict is implied, and the
      caller must not read a null-per-item gate as a pass. This code means "we could not
      look", never "we looked and it failed".
  4   **not applicable** — the row does not exist for this twin (a markdown draft has no
      LaTeX reference targets to resolve, so `crossrefs` cannot judge it). Distinct from 2
      on purpose (R-32 F-7): a pipeline that treats every non-zero exit as a failure would
      otherwise read a healthy markdown draft as broken. The report carries
      `status: "not_applicable"` and names the rows that were skipped and why.
  non-zero from argparse for a usage error.

A gate that matched nothing cannot fail, so reporting it with a clean-looking zero would be a
false negative. The script therefore refuses to return a pass-shaped result for an empty match.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
from pathlib import Path

# The tokenizer is pinned here and nowhere else. Every count this script prints uses
# exactly this pattern, and the pattern is printed verbatim in the report so a reader can
# reproduce the number without guessing. It is NOT the corpus basis (`[A-Za-z][A-Za-z'\-]*`
# over PDF-extracted text, or whitespace tokens over LaTeX): inline math becomes several
# tokens here, because `x_i` and `3/4` each carry letters or digits.
TOKEN_PATTERN = r"[A-Za-z0-9][A-Za-z0-9'\-]*"
WORD = re.compile(TOKEN_PATTERN)
TOKEN_BASIS = (
    f"tokens matching {TOKEN_PATTERN} (a token starts with a letter or digit and continues "
    "with letters, digits, apostrophes or hyphens)"
)
# Exit contract. `not applicable` and `measurement failed` are different outcomes and must not
# share a code (R-32 F-7).
EXIT_MEASURED = 0
EXIT_BREACH = 1
EXIT_MEASUREMENT_FAILED = 2
EXIT_NOT_APPLICABLE = 4

COMPARISON_TOLERANCE = (
    "compare only counts produced by the same tokenizer on the same text form; a different "
    "tokenizer moves word counts by a few percent (measured spread across four reasonable "
    "tokenizers: 18% relative on a high-overlap pair), so re-run rather than rescaling"
)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
ABBREVIATIONS = (
    "e.g.", "i.e.", "cf.", "et al.", "vs.", "Fig.", "Eq.", "Sec.", "No.",
    "resp.", "approx.", "w.r.t.", "Sect.", "Ch.", "pp.", "vol.",
)
HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
# LaTeX twins: \section / \subsection / \subsubsection headings and the abstract
# environment. Markdown-only heading matching made every heading-based subcommand
# fail on a .tex manuscript with "no heading matched" — a measurement failure, not
# a manuscript defect.
TEX_HEADING = re.compile(r"^\\(?P<cmd>section|subsection|subsubsection)\*?\{(?P<title>[^}]*)\}")
TEX_ABSTRACT_BEGIN = re.compile(r"^\s*\\begin\{abstract\}\s*$")
TEX_ABSTRACT_END = re.compile(r"^\s*\\end\{abstract\}\s*$")
TEX_KEYWORDS = re.compile(r"^\s*\\keywords\b")

# --- evidence-apparatus patterns (census rows B1/B2, and the crypto reference rows) ----
CAPTION_BLOCK = re.compile(
    r"^\s*(?:\d{1,3}\s*[:.]?\s*)?(?:Figure|FIGURE|Fig\.|Table|TABLE)\s*\d{1,3}\s*[:.]",
    re.M,
)
FIG_CAPTION_BLOCK = re.compile(
    r"^\s*(?:\d{1,3}\s*[:.]?\s*)?(?:Figure|FIGURE|Fig\.)\s*\d{1,3}\s*[:.]", re.M
)
TAB_CAPTION_BLOCK = re.compile(
    r"^\s*(?:\d{1,3}\s*[:.]?\s*)?(?:Table|TABLE)\s*\d{1,3}\s*[:.]", re.M
)
# Markdown float proxies. A markdown draft has no float environments, so the LaTeX basis
# (tested above) is the wrong instrument for it: it reports 0 for a draft that carries
# tables, and a floor of 1 then fires on a healthy paper. These two classes are the
# markdown-side basis, and they are NEVER summed with a LaTeX count.
# The census instrument's markdown figure class: `Figure N` / `Fig. N` label lines only, which
# is the row-comparable measure for the figure count on a markdown twin.
MD_FIGURE_LABEL = re.compile(r"^\s*(?:Figure|Fig\.)\s*\d{1,3}\b", re.M)
# A superset used for the FLOOR only: markdown drafts also label tables this way (`Table 1 ...`),
# and a draft with a labelled table is not float-free even when it carries no pipe block.
MD_FLOAT_LABEL = re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*\d{1,3}\b", re.M)
MD_PIPE_TABLE_BLOCK = re.compile(r"(?m)(?:^\|.*\n){2,}")
REF_TEX = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\*?\{([^}]*)\}")
LABEL_TEX = re.compile(r"\\label\{([^}]*)\}")
CITE_TEX = re.compile(
    r"\\(?:cite|citep|citet|citealp|citealt|citeauthor)\*?(?:\[[^\]]*\])*\{([^}]*)\}"
)
CITE_MD = re.compile(r"\[[0-9]{1,3}(?:\s*[,–-]\s*[0-9]{1,3})*\]")
INLINE_MATH_TEX = re.compile(r"(?<!\$)\$(?!\$)([^$\n]{1,400}?)(?<!\$)\$(?!\$)")
DISPLAY_MATH_TEX = re.compile(
    r"\\begin\{(?:equation|align|alignat|gather|multline|flalign|eqnarray|subequations|"
    r"IEEEeqnarray|dmath)\*?\}"
)
INLINE_MATH_MD = INLINE_MATH_TEX
DISPLAY_MATH_MD = re.compile(r"\$\$(.+?)\$\$", re.S)
APPENDIX_HEADING_MD = re.compile(
    r"^(?P<hashes>#{1,6})\s+(?P<title>.*\bAppendix\b.*)$", re.I | re.M
)
APPENDIX_LETTERED_HEADING = re.compile(r"\bAppendix\s+[A-Z]\b")
APPENDIX_HEADING_TEX = re.compile(r"\\(?:appendix)\b|\\(?:section|subsection)\*?\{([^}]*)\}")
APPENDIX_CALL_MD = APPENDIX_LETTERED_HEADING


def words(text: str) -> list[str]:
    """Count every token that carries at least one letter or digit.

    Math markup such as a subscript, a sum index, or a norm bar becomes one
    token each, which is why a count over LaTeX source runs slightly above a
    count over the rendered text. Compare like with like: state which text the
    count was taken from.
    """
    return WORD.findall(text)


def normalize(token: str) -> str:
    return token.lower().strip("'-")


def sentences(text: str) -> list[str]:
    protected = text
    for index, abbreviation in enumerate(ABBREVIATIONS):
        protected = protected.replace(abbreviation, f"\x00{index}\x00")
    protected = re.sub(r"\b(?:[A-Z]|\d+)\.", lambda m: m.group(0).replace(".", "\x01"), protected)
    parts = [part.replace("\x01", ".") for part in SENTENCE_SPLIT.split(protected)]
    restored: list[str] = []
    for part in parts:
        for index, abbreviation in enumerate(ABBREVIATIONS):
            part = part.replace(f"\x00{index}\x00", abbreviation)
        if part.strip():
            restored.append(part.strip())
    return restored


def jaccard(left: list[str], right: list[str]) -> float:
    a, b = set(left), set(right)
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def trigrams(tokens: list[str]) -> list[str]:
    normalized = [normalize(token) for token in tokens if normalize(token)]
    return [
        " ".join(normalized[index : index + 3])
        for index in range(max(0, len(normalized) - 2))
    ]


def paragraphs(text: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text)]
    kept: list[str] = []
    for block in blocks:
        if not block or block.startswith("#"):
            continue
        if re.fullmatch(r"[-*_=~\s]{3,}", block):
            continue
        if re.match(r"^\**[Kk]eywords\**[:\s]", block):
            continue
        kept.append(block)
    return kept


def prose(text: str) -> str:
    """Normalized text for word counting: markup and dash variants removed."""
    cleaned = re.sub(r"\\[a-zA-Z]+\*?(?:\{[^{}]*\})?", " ", text)
    cleaned = cleaned.replace("--", " ").replace("---", " ")
    cleaned = cleaned.replace("\u2014", " ").replace("\u2013", " ")
    return re.sub(r"[\\$*_`{}]", " ", cleaned)


BULLET_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
BOLD_ITEM = re.compile(r"^\s*(?:[-*+]\s+)?\*\*(?P<label>[^*]{1,160})\*\*")
# LaTeX run-in labels: a paragraph whose first line opens with \textbf{...}.
# BOLD_ITEM above is markdown-only, so a .tex twin reported zero bold items even
# when the paper carried \textbf run-in contribution items.
TEX_BOLD_ITEM = re.compile(r"^\s*\\textbf\{[^}]{1,160}\}")


def contribution_items(text: str, mode: str) -> tuple[list[str], str]:
    """Return (items, match_status).

    match_status is "matched" when the requested pattern found at least one item, and
    "unmatched" when it found none. An unmatched result is never reported as a clean
    count: the caller turns it into a degenerate marker, because a per-item gate that
    matches zero items cannot fail and must not look like a pass.
    """
    if mode == "bullet":
        lines = [line for line in text.split("\n") if BULLET_ITEM.match(line)]
        return lines, ("matched" if lines else "unmatched")
    if mode == "bold":
        lines = [line.strip() for line in text.split("\n") if BOLD_ITEM.match(line)]
        if lines:
            return lines, "matched"
        tex_blocks = [b.strip() for b in paragraphs(text) if TEX_BOLD_ITEM.match(b)]
        return tex_blocks, ("matched" if tex_blocks else "unmatched")
    if mode == "paragraph":
        blocks = paragraphs(text)
        return blocks, ("matched" if blocks else "unmatched")
    if mode == "any":
        bullets = [line for line in text.split("\n") if BULLET_ITEM.match(line)]
        if bullets:
            return bullets, "matched"
        bolds = [line.strip() for line in text.split("\n") if BOLD_ITEM.match(line)]
        if bolds:
            return bolds, "matched"
        tex_blocks = [b.strip() for b in paragraphs(text) if TEX_BOLD_ITEM.match(b)]
        if tex_blocks:
            return tex_blocks, "matched"
        blocks = paragraphs(text)
        return blocks, ("matched" if blocks else "unmatched")
    return [], "unmatched"


def clean_span(text: str) -> str:
    """Drop a leading heading line, a trailing rule, and a keywords block."""
    lines = text.split("\n")
    if lines and HEADING.match(lines[0]):
        lines = lines[1:]
    body = "\n".join(lines)
    body = re.split(r"\n\s*[-*_=~]{3,}\s*(\n|$)", body)[0]
    body = re.split(r"\n\s*\**[Kk]eywords\**[:\s]", body)[0]
    return body.strip()


def parse_sections(text: str) -> list[tuple[int, str, int, int]]:
    """Return (level, title, start offset, end offset) per heading."""
    lines = text.split("\n")
    offsets: list[tuple[int, str, int]] = []
    position = 0
    for line in lines:
        match = HEADING.match(line)
        if match:
            offsets.append((len(match.group("hashes")), match.group("title"), position))
        else:
            tex = TEX_HEADING.match(line)
            if tex:
                level = {"section": 2, "subsection": 3, "subsubsection": 4}[tex.group("cmd")]
                offsets.append((level, tex.group("title"), position))
            elif TEX_ABSTRACT_BEGIN.match(line):
                offsets.append((2, "Abstract", position + len(line) + 1))
            elif TEX_KEYWORDS.match(line) or TEX_ABSTRACT_END.match(line):
                offsets.append((2, "__end_abstract__", position))
        position += len(line) + 1
    offsets.append((0, "__end__", position))
    result: list[tuple[int, str, int, int]] = []
    for index in range(len(offsets) - 1):
        level, title, start = offsets[index]
        end = offsets[index + 1][2]
        result.append((level, title, start, end))
    return result


def section_spans(text: str, pattern: str, direct: bool) -> list[tuple[str, str]]:
    """Return every (title, body) whose heading matches pattern."""
    regex = re.compile(pattern, re.IGNORECASE)
    sections = parse_sections(text)
    found: list[tuple[str, str]] = []
    for index, (level, title, start, _end) in enumerate(sections):
        if not regex.search(title):
            continue
        cut = len(text)
        for later_level, _later_title, later_start, _later_end in sections[index + 1 :]:
            if later_level and later_level <= level:
                cut = later_start
                break
        if direct:
            for later_level, _later_title, later_start, _later_end in sections[index + 1 :]:
                if later_level:
                    cut = later_start
                    break
        found.append((title, text[start:cut]))
    return found


def select_section(text: str, pattern: str, direct: bool) -> tuple[str, str]:
    """Return (title, body) for the first heading whose title matches pattern.

    A section spans to the next heading of the same or a shallower level, so
    subsections are included unless direct is set.
    """
    spans = section_spans(text, pattern, direct)
    if not spans:
        raise SystemExit(f"no heading matched {pattern!r}")
    return spans[0]


def spanning_section(text: str, heading_pattern: str) -> str:
    _title, body = select_section(text, heading_pattern, direct=False)
    return body


# --------------------------------------------------------------------------------------
# Evidence-apparatus measurements
# --------------------------------------------------------------------------------------


def strip_tex_comments(text: str) -> str:
    """Remove `%` comments, keeping an escaped `\\%`."""
    out: list[str] = []
    for line in text.splitlines():
        cut = len(line)
        for index, char in enumerate(line):
            if char == "%" and (index == 0 or line[index - 1] != "\\"):
                cut = index
                break
        out.append(line[:cut])
    return "\n".join(out)


def reader_twin(path: Path) -> str:
    return "tex" if path.suffix.lower() == ".tex" else "md"


def float_inventory(text: str, twin: str, venue_family: str = "security") -> dict[str, object]:
    """Float inventory, on the basis that belongs to the twin being read.

    Two bases, one per twin, and they are never mixed (R-24.1, R-32 F-3):

    * **LaTeX twin** — `\\begin{figure}` and `\\begin{table|longtable|sidewaystable}`
      environments. This is the crypto-corpus basis.
    * **markdown twin** — `Figure N` / `Fig. N` / `Table N` label lines plus **pipe-table
      blocks** (two or more consecutive `|` lines). Markdown has no float environments, so
      reading it with the LaTeX basis reports 0 for a draft that plainly carries tables and
      makes the floor fire on a healthy paper. The markdown classes are **proxies**: they are
      not interchangeable with the LaTeX float count and must not be summed with it. This is
      the same proxy the census instrument uses for a markdown twin
      (`skills-work/audit/tools/evidence/count_evidence_gates.py`).
    """
    if twin == "tex":
        text = strip_tex_comments(text)
        figures = len(re.findall(r"\\begin\{figure\*?\}", text))
        tables = len(re.findall(r"\\begin\{(?:table\*?|longtable|sidewaystable)\}", text))
        label_lines = 0
        pipe_table_blocks = 0
        basis = (
            "LaTeX float environments (\\begin{figure} and \\begin{table|longtable|"
            "sidewaystable}). This is the crypto-corpus basis and is NOT the markdown basis; "
            "never average the two."
        )
        proxy = False
    else:
        figure_labels = len(MD_FIGURE_LABEL.findall(text))
        label_lines = len(MD_FLOAT_LABEL.findall(text))
        pipe_table_blocks = len(MD_PIPE_TABLE_BLOCK.findall(text))
        figures = figure_labels
        tables = pipe_table_blocks
        basis = (
            "markdown proxies (R-24.1, R-32 F-3): the `figures` row counts `Figure N` / `Fig. N` "
            "label lines (the census instrument's markdown figure class, so the two instruments "
            "agree row for row), the `tables` row counts pipe-table blocks (2+ consecutive `|` "
            "lines, the census's `tab_blocks`), and the floor is applied to their union plus any "
            "`Table N` label line. PROXY COUNTS - they are NOT interchangeable with a LaTeX float "
            "count and must never be summed or compared with one. A markdown draft has no float "
            "environments, which is why the LaTeX basis must not be used on it."
        )
        proxy = True
    float_forms = label_lines + pipe_table_blocks if twin == "md" else figures + tables
    security_floor = venue_family == "security"
    return {
        "figures": figures,
        "tables": tables,
        "total": float_forms,
        "float_forms": float_forms,
        "caption_label_lines": label_lines if twin == "md" else None,
        "figure_label_lines": figure_labels if twin == "md" else None,
        "pipe_table_blocks": pipe_table_blocks if twin == "md" else None,
        "basis": basis,
        "proxy": proxy,
        "proxy_warning": (
            "proxy counts; not interchangeable with a LaTeX float count (R-24.1, R-32 F-3)"
            if proxy else
            "LaTeX environment counts; not interchangeable with the markdown proxy"
        ),
        "scope": (
            "per paper: census rows B1/B2 count caption blocks per paper, and this floor is applied "
            "to the same per-paper total, so the bound and its row share one scope (R-27)"
        ),
        "venue_family": venue_family,
        "floor": 1 if security_floor else None,
        "floor_basis": (
            "security four venues n=35: 34 of 35 papers carry at least one caption block (the one "
            "zero-total paper is usenix2024-angel); figures min 0 / q1 5 / median 10 / q3 13 / "
            "max 20 with 2 of 35 at zero; tables min 0 / q1 0 / median 2 / q3 5 with 12 of 35 at "
            "zero and NDSS median 0 of 8. The floor is 1 on the figure-plus-table total because "
            "34 of 35 clear it; a table floor would be a venue rule, so tables are counted and "
            "reported, never floored."
            if security_floor else
            "not applied: the float floor is calibrated on the security four-venue corpus, and "
            "this run declared the cryptography family. Report the counts; do not fail a "
            "cryptography-family draft on a security-family floor."
        ),
        # The outlier statement the SKILL text requires (a zero-figure count is reported as an
        # outlier, not failed) is computed here rather than promised to the reader: t8 T8-04 found
        # that on a markdown twin the merged proxy total could not distinguish "figures present,
        # zero" from "figures zero, tables present".
        "figure_outlier": figures == 0 and float_forms > 0,
        "figure_outlier_note": (
            "zero figure and a non-zero float total: in the security four-venue corpus 2 of 35 papers "
            "sit on this row (census row B1), so it is reported as an outlier, never as a breach"
        ),
        "breach": float_forms == 0 and security_floor,
        "breach_reason": (
            "the draft carries no figure label, no table caption block and no pipe-table block on "
            "the markdown basis (or no figure and no table environment on the LaTeX basis), which "
            "34 of 35 security-venue corpus papers do not"
        ),
        "context_non_binding": {
            "scope": "per paper (census B1/B2)",
            "per_venue_medians": {"S&P": {"n": 4, "figures": 8.5}, "CCS": {"n": 5, "figures": 5,
                                                                        "tables": 5},
                                  "USENIX": {"n": 18, "figures": 9, "tables": 3},
                                  "NDSS": {"n": 8, "figures": 11.5, "tables": 0}},
            "note": (
                "directional only: the venue subsamples are 4 to 18 papers, so a per-venue or "
                "per-float-type threshold is not licensed. Tables are reported and never floored, "
                "because the NDSS median of 0 of 8 against the CCS median of 5 of 5 shows the "
                "table habit is a venue preference rather than corpus practice"
            ),
        },
    }


def reference_integrity(text: str, twin: str) -> dict[str, object]:
    """Every reference target must be declared in the same twin (census gap G-E4)."""
    if twin == "tex":
        text = strip_tex_comments(text)
        refs: list[str] = []
        for group in REF_TEX.findall(text):
            refs.extend(part.strip() for part in group.split(",") if part.strip())
        labels = [label.strip() for label in LABEL_TEX.findall(text)]
        basis = "LaTeX \\ref/\\eqref/\\autoref/\\cref/\\pageref targets against \\label declarations"
    else:
        refs = []
        labels = []
        basis = (
            "markdown drafts carry no resolvable reference targets. This row is NOT APPLICABLE to "
            "this twin: it is neither a pass nor a failure, and the instrument distinguishes it by "
            "exit code 4 rather than the measurement-failure code 2 (R-32 F-7)"
        )
    label_set = set(labels)
    unresolved = sorted({ref for ref in refs if ref not in label_set})
    return {
        "basis": basis,
        "binding": (
            "no numeric threshold: this row is a resolvability property of the draft "
            "(every reference target must be declared), not a corpus-calibrated bound. The "
            "cryptography figures below are whole-paper context, non-binding under R-27, and "
            "may not be applied to a section span."
        ),
        "reference_calls": len(refs),
        "labels": len(labels),
        "unresolved": unresolved,
        "measured": twin == "tex",
        "status": "measured" if twin == "tex" else "not_applicable",
        "breach": bool(unresolved),
        "breach_reason": (
            "reference target(s) with no \\label declaration in the same file: a broken pointer is "
            "a measurement failure, not a silent pass"
        ),
        "context_non_binding": {
            "scope": "whole paper, per 1000 words (census A10) and per paper (census A11)",
            "population": "cryptography tier-A, n=62",
            "reference_calls_per_1000w": {"min": 0.0, "q1": 2.778, "median": 3.468, "q3": 5.687},
            "labels_per_paper": {"min": 2, "median": 49.5},
            "papers_with_zero_labels": "0 of 62",
            "note": (
                "printed for orientation only: it is another family's whole-paper distribution, so "
                "it is neither a floor for this draft nor a section-scoped yardstick"
            ),
        },
    }


def citation_density(text: str, twin: str, span: str | None) -> dict[str, object]:
    """Citation keys (or bracketed numbers) in the related-work region (census gap G-E5)."""
    if span is None:
        return {
            "measured": False,
            "basis": "no related-work region was supplied; pass --related-work-heading",
            "breach": False,
            "breach_reason": None,
        }
    body = clean_span(span)
    keys: list[str] = []
    if twin == "tex":
        for group in CITE_TEX.findall(body):
            keys.extend(part.strip() for part in group.split(",") if part.strip())
    else:
        keys = CITE_MD.findall(body)
    return {
        "measured": True,
        "basis": (
            "LaTeX citation keys (\\cite, \\citep, \\citet and friends), or bracketed numeric "
            "citations in a markdown draft"
        ),
        "binding": (
            "presence over the named region (at least one citation key), derived from no corpus "
            "quantile - the requirement is that the section is not empty of prior art, not that it "
            "reaches a density"
        ),
        "related_work_words": len(words(prose(body))),
        "citation_keys": len(keys),
        "distinct_citation_keys": len(set(keys)),
        "breach": len(keys) == 0,
        "breach_reason": (
            "the related-work region carries zero citation key: a section that places no work "
            "against prior art is a word-count floor with nothing in it"
        ),
        "context_non_binding": {
            "scope": "whole paper, per 1000 words (census A12)",
            "population": "cryptography tier-A, n=62",
            "citation_keys_per_1000w": {"min": 1.108, "q1": 3.736, "median": 4.798, "q3": 6.199},
            "note": (
                "non-binding: a whole-paper quantile from another family may not be applied to this "
                "section scope, and no section-scoped corpus row exists (R-27)"
            ),
        },
    }


def appendix_reachability(text: str, twin: str) -> dict[str, object]:
    """Deferred material must be reachable (census gap G-E6)."""
    if twin == "tex":
        text = strip_tex_comments(text)
        headings = [
            match.group(1).strip()
            for match in APPENDIX_HEADING_TEX.finditer(text)
            if match.group(1) and re.search(r"appendix|^[A-Z]\.", match.group(1), re.I)
        ]
        if r"\appendix" in text:
            headings.append("appendix")
        return {
            "measured": True,
            "basis": "LaTeX appendix markers and section titles",
            "appendix_headings": len(headings),
            "breach": False,
            "breach_reason": None,
            "note": (
                "on a LaTeX twin the reachability question is the cross-reference row above: "
                "deferred material that nothing calls from the body shows up there as an "
                "unresolved reference, not here"
            ),
        }
    text_without_headings = APPENDIX_HEADING_MD.sub("", text)
    lettered = APPENDIX_LETTERED_HEADING.findall(text)
    calls = len(APPENDIX_LETTERED_HEADING.findall(text_without_headings))
    return {
        "measured": True,
        "basis": (
            "lettered appendix headings (the unit census row B4 counts: 8 of 35 papers) against "
            "body calls of the form 'Appendix <letter>'"
        ),
        "appendix_headings": len(lettered),
        "appendix_calls": calls,
        "breach": bool(lettered) and calls == 0,
        "breach_reason": (
            "the draft carries an appendix heading that no body sentence calls: relocated "
            "material is unreachable, which is what the relocation rule forbids (security four "
            "venues n=35: only 8 of 35 papers carry a lettered appendix, so an appendix is never "
            "a pass condition and only its reachability is judged)"
        ),
    }


def math_density(text: str, twin: str) -> dict[str, object]:
    """Inline and display math counts.

    Reported, with the corpus reference distribution named, and NEVER emitted as a verdict on
    the security side: the security corpus is PDF text without LaTeX sources, so the same
    quantity cannot be measured there, and a threshold borrowed from a population that was not
    measured on this one would be fabricated. See the reference file's boundary note.
    """
    if twin == "tex":
        text = strip_tex_comments(text)
        inline = len(INLINE_MATH_TEX.findall(text))
        display = len(DISPLAY_MATH_TEX.findall(text))
        basis = "LaTeX $...$ occurrences and equation-family environments"
    else:
        inline = len(INLINE_MATH_MD.findall(text))
        display = len(DISPLAY_MATH_MD.findall(text))
        basis = "markdown $...$ and $$...$$ regions"
    return {
        "inline_math": inline,
        "display_math": display,
        "basis": basis,
        "verdict_emitted": False,
        "binding": "NONE - reported diagnostic (R-24a.2); verdict_emitted is false by construction",
        "reference_distribution": (
            "cryptography three-venue corpus, tier-A n=62, LaTeX twin, **whole-paper basis** (the "
            "row is measured over each paper's entire source, not over a section): inline math per "
            "1000 words min 4.700, q1 46.082, median 54.940, q3 64.373; 0 of 62 at zero. Anchor: "
            "`skills-work/audit/evidence-structure-census.md`, row A1 (and row C2 for the calibration manuscript). The frozen calibration "
            "manuscript measures 1180 inline regions over 22182 words = 53.196 per 1000 words "
            "(census C2), which is why it sits inside that distribution. Non-binding under R-27: "
            "another family's whole-paper quantiles may not be applied to this draft, and no "
            "section-scoped corpus row exists on either side."
        ),
        "why_no_verdict_here": (
            "the security four-venue corpus has no LaTeX source, so this quantity was never "
            "measured on that population. A threshold transferred from the cryptography corpus "
            "would be fabricated; the count is reported and the judgement stays with the human "
            "author, who must file a recorded reason when the formal regions carry no formula at "
            "all."
        ),
    }


def build_evidence_report(
    path: Path, related_work_heading: str | None, venue_family: str = "security"
) -> dict[str, object]:
    twin = reader_twin(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    word_count = len(words(prose(text)))
    if word_count == 0:
        return {
            "status": "degenerate",
            "reason": f"{path} carries no countable word after parsing",
            "file": str(path),
            "verdict_implied": None,
        }
    related_span = None
    if related_work_heading:
        spans = section_spans(text, related_work_heading, direct=False)
        if not spans:
            return {
                "status": "degenerate",
                "reason": (
                    f"--related-work-heading {related_work_heading!r} matched no heading in "
                    f"{path}; the citation-density row cannot be measured"
                ),
                "file": str(path),
                "remedy": "check the heading spelling, or pass a broader pattern",
                "verdict_implied": None,
            }
        related_span = spans[0][1]
    floats = float_inventory(text, twin, venue_family)
    xrefs = reference_integrity(text, twin)
    citations = citation_density(text, twin, related_span)
    appendix = appendix_reachability(text, twin)
    rows = (
        ("float-floor", floats),
        ("cross-reference-integrity", xrefs),
        ("related-work-citation-density", citations),
        ("appendix-reachability", appendix),
    )
    breaches = [
        {"gate": name, "reason": row.get("breach_reason") or row.get("basis")}
        for name, row in rows
        if row.get("breach")
    ]
    not_applicable = [
        {"row": name, "reason": row.get("basis")}
        for name, row in rows
        if row.get("status") == "not_applicable" or row.get("measured") is False
    ]
    return {
        "status": "measured",
        "file": str(path),
        "twin": twin,
        "words": word_count,
        "tokenizer": TOKEN_PATTERN,
        "basis": TOKEN_BASIS,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "floats": floats,
        "cross_references": xrefs,
        "citations": citations,
        "appendix": appendix,
        "math": math_density(text, twin),
        "venue_family": venue_family,
        "not_applicable_rows": not_applicable,
        "exit_contract": (
            "0 measured and unbreached; 1 a breached gate; 2 measurement failure (no verdict); "
            "4 a row that is not applicable to this twin, which is NOT a failure (R-32 F-7)"
        ),
        "binding_thresholds": {
            "float-floor": "1 caption block per paper (census B1/B2, per paper - scope matches)",
            "cross-reference-integrity": "no numeric threshold (draft property)",
            "related-work-citation-density": "no numeric threshold (presence over the related-work region)",
            "formal-content": "no threshold: reported diagnostic, never a verdict",
            "rule": (
                "R-27: every bound's scope equals its corpus row's scope. All other printed numbers "
                "are non-binding context, marked as such where they print."
            ),
        },
        "breaches": breaches,
    }


# --------------------------------------------------------------------------------------
# Reports
# --------------------------------------------------------------------------------------


def report_abstract_contributions(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    abstract = clean_span(spanning_section(text, args.abstract_heading))
    contributions = clean_span(spanning_section(text, args.contributions_heading))

    abstract_tokens = words(prose(abstract))
    abstract_sentences = sentences(prose(abstract))
    longest = max((len(words(sentence)) for sentence in abstract_sentences), default=0)
    mean = (len(abstract_tokens) / len(abstract_sentences)) if abstract_sentences else 0.0
    blocks = paragraphs(abstract)
    allocation = [
        {"paragraph": index + 1, "words": len(words(block)), "first_line": block.split("\n")[0][:120]}
        for index, block in enumerate(blocks)
    ]

    items, item_status = contribution_items(contributions, args.items)
    item_words = [len(words(prose(item))) for item in items]
    contribution_tokens = words(prose(contributions))

    result = {
        "tokenizer": TOKEN_PATTERN,
        "basis": TOKEN_BASIS,
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "paragraph_basis": "paragraphs = blank-line separated blocks, keyword lines and horizontal rules excluded",
        "jaccard_basis": "deduplicated word sets and adjacent-word-trigram sets, case-folded, punctuation stripped",
        "abstract": {
            "words": len(abstract_tokens),
            "sentences": len(abstract_sentences),
            "longest_sentence_words": longest,
            "mean_sentence_words": round(mean, 1),
            "paragraphs": len(blocks),
            "allocation": allocation,
            "manual_step_required": "label each paragraph context / gap / build / result; the allocation gate fails when no paragraph names what is built",
        },
        "contributions": {
            "item_mode": args.items,
            "match_status": item_status,
            "items": (len(items) if item_status == "matched" else None),
            "words_total": len(contribution_tokens),
            "words_per_item": (item_words if item_status == "matched" else None),
            "words_per_item_max": (max(item_words, default=0) if item_status == "matched" else None),
            "items_over_72_words": (
                sum(1 for count in item_words if count > 72) if item_status == "matched" else None
            ),
            "items_over_150_words": (
                sum(1 for count in item_words if count > 150) if item_status == "matched" else None
            ),
            "degenerate": (
                None if item_status == "matched" else
                f'item_mode {args.items!r} matched no item in the contributions span; the per-item '
                "gates cannot fire on this draft and NO verdict is implied. Re-run with --items "
                "bold, --items paragraph or --items any."
            ),
        },
        "duplication": {
            "abstract_vs_contributions_word_jaccard": round(
                jaccard(abstract_tokens, contribution_tokens), 4
            ),
            "abstract_vs_contributions_trigram_jaccard": round(
                jaccard(trigrams(abstract_tokens), trigrams(contribution_tokens)), 4
            ),
            "shared_trigrams_count": len(
                set(trigrams(abstract_tokens)) & set(trigrams(contribution_tokens))
            ),
            "shared_trigrams": sorted(
                set(trigrams(abstract_tokens)) & set(trigrams(contribution_tokens))
            )[:40],
        },
    }

    if args.threat_model_heading:
        threat = clean_span(spanning_section(text, args.threat_model_heading))
        threat_tokens = words(prose(threat))
        result["duplication"]["contributions_vs_threat_model_word_jaccard"] = round(
            jaccard(contribution_tokens, threat_tokens), 4
        )
        result["threat_model"] = {
            "words": len(threat_tokens),
            "manual_step_required": (
                "map each promised security goal to the threat-model sentence stating what "
                "the adversary may do, and list the capabilities, assumptions, or non-goals "
                "the model adds"
            ),
        }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    if item_status != "matched":
        return 2
    return 0


def report_section_mass(args: argparse.Namespace) -> int:
    if not args.section:
        print(json.dumps({
            "status": "degenerate",
            "reason": "no --section was given, so no section mass could be measured",
            "sections": None,
            "ratios": None,
            "remedy": (
                "pass one or more --section NAME:PATTERN (or NAME+=PATTERN to sum several "
                "matches), e.g. --section 'design+=^3\\. |^4\\. ' --section 'analysis:^5\\. '"
            ),
            "verdict_implied": None,
        }, indent=2, ensure_ascii=False))
        return 2
    text = Path(args.file).read_text(encoding="utf-8")
    sections: dict[str, dict[str, object]] = {}
    for spec in args.section:
        accumulate = "+=" in spec and (":" not in spec or spec.index("+=") < spec.index(":"))
        if accumulate:
            name, pattern = spec.split("+=", 1)
        elif ":" in spec:
            name, pattern = spec.split(":", 1)
        else:
            raise SystemExit(f"--section needs NAME:PATTERN or NAME+=PATTERN, got {spec!r}")
        spans = section_spans(text, pattern, direct=args.direct)
        if not spans:
            print(json.dumps({
                "status": "degenerate",
                "reason": f"the pattern for section {name!r} matched no heading in {args.file}",
                "pattern": pattern,
                "sections": None,
                "ratios": None,
                "remedy": "check the heading spelling, or pass a broader pattern",
                "verdict_implied": None,
            }, indent=2, ensure_ascii=False))
            return 2
        bodies = [body for _title, body in spans]
        direct_bodies = [body for _title, body in section_spans(text, pattern, direct=True)]
        sections[name] = {
            "matched_headings": [title for title, _body in spans],
            "matched_heading": spans[0][0],
            "word_per_match": [len(words(prose(body))) for body in bodies],
            "words": sum(len(words(prose(body))) for body in bodies),
            "direct_words": sum(len(words(prose(body))) for body in direct_bodies),
            "paragraphs": sum(len(paragraphs(body)) for body in bodies),
        }

    body_text = text.split("\n#")[0] if args.body_until_appendix else text
    body_words = len(words(prose(body_text)))

    ratios: dict[str, float] = {}
    if "design" in sections and "analysis" in sections:
        design = sections["design"]["words"]
        analysis = sections["analysis"]["words"]
        ratios["design_over_analysis"] = round(design / analysis, 4) if analysis else 0.0
        ratios["design_share_of_body"] = round(design / body_words, 4) if body_words else 0.0

    result = {
        "status": "matched",
        "tokenizer": TOKEN_PATTERN,
        "basis": (
            "words: " + TOKEN_BASIS + "; section words include subsections unless --direct; body "
            "words are counted to the first top-level appendix heading when --body-until-appendix "
            "is passed"
        ),
        "comparison_tolerance": COMPARISON_TOLERANCE,
        "direct_only": bool(args.direct),
        "sections": sections,
        "body_words": body_words,
        "ratios": ratios,
        "manual_step_required": (
            "mark each required constituent present with its line or absent: overview needs "
            "intuition, mechanism sentence, named sub-blocks, forward references, and a cost or "
            "leakage statement; the design section needs step ordering, a named reused object, a "
            "complexity or cost expression, a parameter reason, and a protocol box or flow figure, "
            "plus one mechanism sentence per mechanism"
        ),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def report_span(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    tokens = words(prose(text))
    sentence_list = sentences(prose(text))
    print(
        json.dumps(
            {
                "tokenizer": TOKEN_PATTERN,
                "basis": TOKEN_BASIS,
                "words": len(tokens),
                "sentences": len(sentence_list),
                "longest_sentence_words": max(
                    (len(words(sentence)) for sentence in sentence_list), default=0
                ),
                "paragraphs": len(paragraphs(text)),
            },
            indent=2,
        )
    )
    return 0


def report_evidence(args: argparse.Namespace) -> int:
    report = build_evidence_report(Path(args.file), args.related_work_heading, args.venue)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "measured":
        print(f"MEASUREMENT FAILED: {report.get('reason')}", file=sys.stderr)
        return EXIT_MEASUREMENT_FAILED
    for row in report["not_applicable_rows"]:
        print(f"NOT APPLICABLE ({row['row']}): {row['reason']}", file=sys.stderr)
    for breach in report["breaches"]:
        print(f"BREACH ({breach['gate']}): {breach['reason']}", file=sys.stderr)
    return EXIT_BREACH if report["breaches"] else EXIT_MEASURED


def report_captions(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"MEASUREMENT FAILED: {path} does not exist", file=sys.stderr)
        return EXIT_MEASUREMENT_FAILED
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(words(prose(text))) == 0:
        print(
            f"MEASUREMENT FAILED: {path} carries no countable word, so a float inventory "
            "cannot be taken and no breach may be reported",
            file=sys.stderr,
        )
        return EXIT_MEASUREMENT_FAILED
    twin = reader_twin(path)
    report = float_inventory(text, twin, args.venue)
    report["file"] = str(path)
    report["twin"] = twin
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["breach"]:
        print(
            f"BREACH (float-floor): {path} carries no figure label, no table caption block and "
            f"no pipe-table block on the {twin} basis. "
            f"{report['floor_basis']}",
            file=sys.stderr,
        )
        return 1
    return 0


def report_crossrefs(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"MEASUREMENT FAILED: {path} does not exist", file=sys.stderr)
        return EXIT_MEASUREMENT_FAILED
    twin = reader_twin(path)
    report = reference_integrity(path.read_text(encoding="utf-8", errors="replace"), twin)
    report["file"] = str(path)
    report["twin"] = twin
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["measured"]:
        print(
            f"NOT APPLICABLE: {path} is a markdown twin, which has no \\ref/\\label targets to "
            "resolve; this row is neither a pass nor a failure (exit 4, distinct from the "
            "measurement-failure code 2)",
            file=sys.stderr,
        )
        return EXIT_NOT_APPLICABLE
    if report["breach"]:
        print(
            f"BREACH (cross-reference-integrity): unresolved target(s) "
            f"{', '.join(report['unresolved'])}",
            file=sys.stderr,
        )
        return 1
    return 0


def report_math(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"MEASUREMENT FAILED: {path} does not exist", file=sys.stderr)
        return EXIT_MEASUREMENT_FAILED
    twin = reader_twin(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    report = math_density(text, twin)
    report["words"] = len(words(prose(text)))
    report["file"] = str(path)
    report["twin"] = twin
    if report["words"] == 0:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"DEGENERATE: {path} carries no countable word", file=sys.stderr)
        return 2
    report["inline_math_per_1000w"] = round(1000.0 * report["inline_math"] / report["words"], 3)
    report["display_math_per_1000w"] = round(1000.0 * report["display_math"] / report["words"], 3)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


# --------------------------------------------------------------------------------------
# Self-test: a gate that cannot be shown to fire is not a gate
# --------------------------------------------------------------------------------------

BOLD_RUN_IN_CONTRIBUTIONS = """# Paper

## Abstract

Prior systems are slow. We present a new protocol that removes the bottleneck by batching
proofs. It is 3.4x faster on the corpus benchmark, measured over 1000 runs.

## Contributions

**(1) A batched proof system.** We present the first construction whose server-to-server
communication stays constant as clients are added.

**(2) A security analysis.** We prove the construction secure against a malicious client
that observes every server message.

**(3) An implementation.** We build the system and measure it over 1000 runs.

**(4) A measurement study.** We compare against two baselines on the same hardware.

**(5) An open artifact.** We release the code and the raw measurements.

**(6) A negative result.** We show the naive batching approach fails under churn.
"""

PLAIN_BULLET_CONTRIBUTIONS = """# Paper

## Abstract

Prior systems are slow. We present a new protocol.

## Contributions

- A batched proof system with constant server-to-server communication.

- A security analysis against malicious clients.

- An implementation measured over 1000 runs.
"""

FLOATLESS_DRAFT = """# Paper

## Abstract

We present a system that collects statistics without learning any individual input, which
prior systems could not do at this scale.

## 1 Introduction

We study the problem and state what we build.

## 2 Related Work

Prior work studied the same problem and our version differs in scope, model, and
measurement methodology, which this section describes at length.
"""

EVALUABLE_DRAFT = """# Paper

## Abstract

We present a system that collects statistics without learning any individual input.

## 1 Introduction

We study the problem and state what we build.

## 2 Related Work

Prior work studied the same problem [1], [2], [3] and our version differs in scope.

Figure 1. System overview.
Table 1. Evaluation parameters.

Figure 1 shows the pipeline and Table 1 lists the parameters.

| Variant | Prover | Verifier |
|---|---|---|
| A | 12 ms | 3 ms |
| B | 15 ms | 2 ms |
"""

UNRESOLVED_TEX = r"""\documentclass{article}
\begin{document}
\section{Introduction}
As shown in Table~\ref{tab:results}, our system is fast.
\begin{table}\caption{Results}\label{tab:other}\end{table}
\end{document}
"""

RESOLVED_TEX = r"""\documentclass{article}
\begin{document}
\section{Introduction}
As shown in Table~\ref{tab:results}, our system is fast.
\begin{table}\caption{Results}\label{tab:results}\end{table}
\end{document}
"""


def run_self_test() -> int:
    """Prove, in one run, that every gate fires on an input that violates it and stays quiet
    on an input that does not. A self-test that only walks the happy path proves nothing, so
    each case below is paired with its counter-case."""
    failures: list[str] = []
    total = 0

    def check(name: str, got: object, want: object) -> None:
        nonlocal total
        total += 1
        ok = got == want
        if not ok:
            failures.append(name)
        print(f"  self-test {name:52s} {'ok' if ok else 'NOT DETECTED'}  (got={got!r})")

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        bold_path = tmpdir / "bold.md"
        bold_path.write_text(BOLD_RUN_IN_CONTRIBUTIONS, encoding="utf-8")
        bullet_path = tmpdir / "bullet.md"
        bullet_path.write_text(PLAIN_BULLET_CONTRIBUTIONS, encoding="utf-8")
        floatless = tmpdir / "floatless.md"
        floatless.write_text(FLOATLESS_DRAFT, encoding="utf-8")
        evaluable = tmpdir / "evaluable.md"
        evaluable.write_text(EVALUABLE_DRAFT, encoding="utf-8")
        unresolved = tmpdir / "unresolved.tex"
        unresolved.write_text(UNRESOLVED_TEX, encoding="utf-8")
        resolved = tmpdir / "resolved.tex"
        resolved.write_text(RESOLVED_TEX, encoding="utf-8")

        # F8 — bold run-in contribution items must be recognised, not silently zeroed.
        text = bold_path.read_text(encoding="utf-8")
        contributions = clean_span(spanning_section(text, r"Contributions"))
        items, status = contribution_items(contributions, "any")
        check("F8 bold run-in items are counted", (status, len(items)), ("matched", 6))
        items_bold, status_bold = contribution_items(contributions, "bold")
        check("F8 --items bold counted directly", (status_bold, len(items_bold)), ("matched", 6))
        bullet_text = bullet_path.read_text(encoding="utf-8")
        bullet_items, bullet_status = contribution_items(
            clean_span(spanning_section(bullet_text, r"Contributions")), "any"
        )
        check("bullet items still counted", (bullet_status, len(bullet_items)), ("matched", 3))
        empty_items, empty_status = contribution_items(bold_path.read_text(encoding="utf-8"), "none")
        check("--items none is unmatched, never 0 items", (empty_status, empty_items), ("unmatched", []))

        # F9 — a missing structural input must be refused with a non-zero exit.
        no_section = report_section_mass(argparse.Namespace(
            file=str(evaluable), section=[], direct=False, body_until_appendix=False
        ))
        check("F9 section-mass without --section exits 2", no_section, 2)

        # Float floor: fires on a float-free draft, quiet on a draft that carries a float.
        floatless_report = build_evidence_report(floatless, "Related Work")
        crypto_family = build_evidence_report(floatless, "Related Work", "crypto")
        check("float floor is not applied to the cryptography family",
              [breach["gate"] for breach in crypto_family["breaches"]],
              ["related-work-citation-density"])
        check("float floor and empty related work both fire",
              [breach["gate"] for breach in floatless_report["breaches"]],
              ["float-floor", "related-work-citation-density"])
        evaluable_report = build_evidence_report(evaluable, "Related Work")
        check("no breach on a draft with floats and citations", evaluable_report["breaches"], [])
        check("caption blocks counted on the markdown proxy basis (labels incl. the in-text call)",
              (evaluable_report["floats"]["caption_label_lines"],
               evaluable_report["floats"]["pipe_table_blocks"],
               evaluable_report["floats"]["total"]), (3, 1, 4))
        check("related-work citations counted", evaluable_report["citations"]["citation_keys"], 3)
        check("math density reported inside evidence", evaluable_report["math"]["verdict_emitted"], False)

        # Cross-reference integrity, both directions.
        bad = reference_integrity(UNRESOLVED_TEX, "tex")
        check("unresolved reference target is caught", bad["unresolved"], ["tab:results"])
        check("unresolved reference is a breach", bad["breach"], True)
        good = reference_integrity(RESOLVED_TEX, "tex")
        check("resolved reference is not a breach", good["breach"], False)
        md_xrefs = reference_integrity("# T\n\nSee Figure 1.\n", "md")
        check("markdown twin reports not-measured", md_xrefs["measured"], False)

        # Appendix reachability, both directions. The census counts *lettered* appendices
        # (8 of 35), so a letter-less "Appendix" heading is not a float of this rule.
        uncalled = appendix_reachability(
            "# T\n\n## Appendix A\n\nExtra material.\n", "md"
        )
        check("uncalled lettered appendix heading is a breach", uncalled["breach"], True)
        called = appendix_reachability(
            "# T\n\nSee Appendix A for proofs.\n\n## Appendix A\n\nProofs.\n", "md"
        )
        check("called appendix heading is not a breach", called["breach"], False)
        unlettered = appendix_reachability("# T\n\n## Appendix\n\nMaterial.\n", "md")
        check("letter-less appendix heading is not this rule's unit",
              (unlettered["appendix_headings"], unlettered["breach"]), (0, False))

        # Math density: measured, and explicitly un-verdicted.
        math = math_density("We use $x$ and $y$ here.\n\n$$a=b$$\n", "md")
        check("inline math counted", math["inline_math"], 2)
        check("display math counted", math["display_math"], 1)
        check("math emits no verdict", math["verdict_emitted"], False)

        # R-27 — a bound's scope must equal its corpus row's scope, and everything else must
        # print as non-binding context. Asserted here so a later edit cannot quietly turn a
        # whole-paper cryptography quartile into a section- or security-scoped threshold.

        tables_only = tmpdir / "tables_only.md"
        tables_only.write_text(
            "# Paper\n\n## Abstract\n\nWe present a system.\n\n"
            "| Variant | Prover | Verifier |\n|---|---|---|\n| A | 12 ms | 3 ms |\n| B | 15 ms | 2 ms |\n\n"
            "Table 1. Evaluation parameters.\n",
            encoding="utf-8",
        )
        check("figure_outlier is true when figures are zero and tables are present (markdown twin)",
              build_evidence_report(tables_only, None)["floats"]["figure_outlier"], True)
        check("figure_outlier is false when a figure label is present",
              evaluable_report["floats"]["figure_outlier"], False)
        check("figure_outlier is not a breach on its own",
              build_evidence_report(tables_only, None)["floats"]["breach"], False)
        check("float floor stays the only bound and is per paper",
              (evaluable_report["floats"]["floor"], "per paper" in evaluable_report["floats"]["scope"]),
              (1, True))
        check("cross-reference row declares no numeric threshold",
              evaluable_report["cross_references"]["binding"].startswith("no numeric threshold"), True)
        check("cross-reference context is scope-labelled whole paper",
              "whole paper" in evaluable_report["cross_references"]["context_non_binding"]["scope"], True)
        check("citation row is a presence test, not a density threshold",
              evaluable_report["citations"]["binding"].startswith("presence over the named region"), True)
        check("citation context is scope-labelled whole paper",
              "whole paper" in evaluable_report["citations"]["context_non_binding"]["scope"], True)
        check("math row declares itself non-binding",
              evaluable_report["math"]["binding"].startswith("NONE"), True)
        check("evidence report names the binding thresholds",
              evaluable_report["binding_thresholds"]["float-floor"].startswith("1 caption block per paper"), True)
        check("no per-1000-word threshold is bound anywhere in the report",
              all("per_1000" not in key for key in evaluable_report["binding_thresholds"]), True)

        # Degenerate inputs never return a pass-shaped result. The fixture carries no word
        # once markup is stripped, which is the state a detector must report as degenerate
        # rather than as a clean zero.
        empty = tmpdir / "empty.txt"
        empty.write_text("---\n\n- - -\n", encoding="utf-8")
        check("empty draft is degenerate", build_evidence_report(empty, None)["status"], "degenerate")
        check("missing related-work heading is degenerate",
              build_evidence_report(evaluable, "No Such Section")["status"], "degenerate")

        # Exit codes, with each reporter's own JSON suppressed so the self-test reads as a
        # checklist. The reporters still print, and their stderr reasons still surface.
        def quiet(result):
            with contextlib.redirect_stdout(io.StringIO()):
                return result()

        check("evidence exits 1 on a breached draft",
              quiet(lambda: report_evidence(argparse.Namespace(
                  file=str(floatless), related_work_heading="Related Work", venue="security"))), 1)
        check("evidence exits 0 on a clean draft",
              quiet(lambda: report_evidence(argparse.Namespace(
                  file=str(evaluable), related_work_heading="Related Work", venue="security"))), 0)
        check("captions on an empty file is a measurement failure, not a breach",
              quiet(lambda: report_captions(argparse.Namespace(file=str(empty), venue="security"))),
              EXIT_MEASUREMENT_FAILED)
        check("captions on a missing file is a measurement failure",
              quiet(lambda: report_captions(argparse.Namespace(file=str(tmpdir / "nope.md"),
                                                               venue="security"))),
              EXIT_MEASUREMENT_FAILED)
        check("captions exits 1 on a float-free draft",
              quiet(lambda: report_captions(argparse.Namespace(
                  file=str(floatless), venue="security"))), 1)
        check("captions exits 0 on a draft that carries a float",
              quiet(lambda: report_captions(argparse.Namespace(
                  file=str(evaluable), venue="security"))), 0)
        check("crossrefs exits 1 on an unresolved target",
              quiet(lambda: report_crossrefs(argparse.Namespace(file=str(unresolved)))), 1)
        check("crossrefs on a markdown twin is not-applicable, not a failure",
              quiet(lambda: report_crossrefs(argparse.Namespace(file=str(evaluable)))),
              EXIT_NOT_APPLICABLE)
        check("not-applicable and measurement-failure do not share a code",
              EXIT_NOT_APPLICABLE != EXIT_MEASUREMENT_FAILED, True)
        check("markdown float floor uses the proxy basis (F-3)",
              (build_evidence_report(evaluable, "Related Work")["floats"]["proxy"],
               build_evidence_report(evaluable, "Related Work")["floats"]["pipe_table_blocks"]),
              (True, 1))
        check("markdown draft with a pipe table and no caption label does not breach F-3",
              [b["gate"] for b in build_evidence_report(evaluable, "Related Work")["breaches"]], [])
        check("markdown evidence run reports the not-applicable row explicitly",
              [row["row"] for row in
               build_evidence_report(evaluable, "Related Work")["not_applicable_rows"]],
              ["cross-reference-integrity"])
        check("math exits 2 on an unmeasurable file",
              quiet(lambda: report_math(argparse.Namespace(file=str(empty)))), 2)

    print(f"self-test: {total - len(failures)}/{total} as expected")
    return 3 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="prove every gate fires on a violating fixture and stays quiet on a clean one",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    condensation = subparsers.add_parser("abstract-contributions", help="condensation gate counts")
    condensation.add_argument("file")
    condensation.add_argument("--abstract-heading", default=r"Abstract")
    condensation.add_argument(
        "--contributions-heading",
        default=r"Contributions|Our Contributions|Main Results|Our Results",
    )
    condensation.add_argument("--threat-model-heading", default="")
    condensation.add_argument(
        "--items",
        choices=("bullet", "bold", "paragraph", "any", "none"),
        default="any",
        help=(
            "how the contribution list is written: bullet lines, bold run-in labels, "
            "paragraphs, any of those (default), or not counted"
        ),
    )
    condensation.set_defaults(func=report_abstract_contributions)

    mass = subparsers.add_parser("section-mass", help="expansion gate counts")
    mass.add_argument("file")
    mass.add_argument(
        "--section",
        action="append",
        default=[],
        metavar="NAME:PATTERN",
        help="NAME:PATTERN takes the first match; NAME+=PATTERN sums every match",
    )
    mass.add_argument("--direct", action="store_true", help="count each section's own text only")
    mass.add_argument(
        "--body-until-appendix",
        action="store_true",
        help="stop the body word count at the first top-level appendix heading",
    )
    mass.set_defaults(func=report_section_mass)

    span = subparsers.add_parser("span", help="count one raw span")
    span.add_argument("--file", required=True)
    span.set_defaults(func=report_span)

    evidence = subparsers.add_parser(
        "evidence",
        help=(
            "evidence-apparatus gates: float floor, cross-reference integrity, citation density, "
            "appendix reachability"
        ),
    )
    evidence.add_argument("file")
    evidence.add_argument(
        "--related-work-heading",
        default="",
        help="heading pattern of the related-work region, for the citation-density row",
    )
    evidence.add_argument(
        "--venue",
        choices=("security", "crypto"),
        default="security",
        help=(
            "which venue family's calibration governs the floors (default security: the float "
            "floor is calibrated on the security four-venue corpus and is not applied to a "
            "cryptography-family draft)"
        ),
    )
    evidence.set_defaults(func=report_evidence)

    captions = subparsers.add_parser(
        "captions", help="figure/table caption inventory against the float floor"
    )
    captions.add_argument("file")
    captions.add_argument(
        "--venue",
        choices=("security", "crypto"),
        default="security",
        help="venue family whose calibration governs the floor (default security)",
    )
    captions.set_defaults(func=report_captions)

    crossrefs = subparsers.add_parser(
        "crossrefs", help="LaTeX reference/label integrity: every target must be declared"
    )
    crossrefs.add_argument("file")
    crossrefs.set_defaults(func=report_crossrefs)

    math = subparsers.add_parser(
        "math",
        help="inline and display math counts, reported without a verdict on the security side",
    )
    math.add_argument("file")
    math.set_defaults(func=report_math)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    if not getattr(args, "command", None):
        parser.error("a subcommand is required (or pass --self-test)")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
