#!/usr/bin/env python3
"""Check that every gate name a pointer file *uses* resolves in its owning file.

The security-venue skills publish one doctrine: a family-wide rule is stated once, in its
owning file, and other files point at it **by name**. A pointer is only useful if the name
it uses can be found at the other end, and a gate name that exists nowhere is a broken
instruction — a reader cannot run it, and no test of the skill text notices, because the
pointer itself reads perfectly.

Why this script exists next to the shared checker (R-20a). The shared checker
`skills-work/tools/rule-trace-check.py` implements the same discipline as its C15 check, but
`skills-work/tools/` is **not part of the published skill**: after installation to
`~/.dsh/skills`, C15 does not exist. This script is the portable form of the discipline — it
ships inside the skill and travels with it. Both instruments are kept, and the two must agree
on the historical defect; the cross-check is recorded in `skills-work/reports/author-style-notes.md`.

**The mention-vs-use guard (R-20a.1).** A scan that requires *every* `Gate-*` token in a
pointer file to resolve has a permanent false positive: a pointer file may safely warn that a
name a reader might expect **does not exist** ("a reader may expect a `Gate-Expand-Design`; no
such gate exists"). That sentence *mentions* the name; it does not *use* it. Failing it would
pressure authors to delete the very clause that makes the pointer safe, so this script
classifies each line before judging:

  * **mention** — the line asserts the name does not exist, or contrasts it with the canonical
    name (renamed / deprecated / "instead of" / "rather than" / "not a gate"). Excluded from
    the verdict, and reported as an exclusion with its reason and the matched cue.
  * **use** — the name is quoted in backticks, or the line carries an invocation verb
    (invoke / call / apply / run / use / check / verify / grep / look up), or the name sits in
    a table cell or list item that hands the reader a task, or the name is named with no
    mention cue at all. Must resolve in the owning file.

`--self-test` exercises both directions **in the same run**: the historical warning sentence
must not be reported unresolved, and the same name on a genuine instruction line must still be
reported unresolved. A guard proven in only one direction is not a guard.

Run it when: a gate is renamed, a pointer file gains a sentence that names a gate, or a new
skill starts pointing at another skill's gates. Expected output: one line per pointer/owner
pair with `OK` or `FAIL`, a line for each mention exclusion, then
`RESULT: PASS (n/n gate names resolve)` and `exit 0`. Exit is 1 when any used name does not
resolve, and 2 on a setup error (a pointer or owner file is missing), because a check that
cannot run must not report success.

Usage:

    python3 scripts/check_pointer_resolution.py
    python3 scripts/check_pointer_resolution.py --json
    python3 scripts/check_pointer_resolution.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (pointer file, owning file) pairs, relative to the skills root. Extend this table when a new
# pointer file appears; a pointer file that is not listed here is not checked, so the report
# also prints how many pairs it actually inspected.
POINTER_PAIRS = (
    (
        "usenixsec-writing-style/references/compression-and-expansion-gates.md",
        "ccs-writing-style/references/compression-and-expansion-gates.md",
    ),
    (
        "usenixsec-writing-style/references/compression-and-expansion-gates.md",
        "ccs-writing-style/SKILL.md",
    ),
    (
        "ccs-writing-style/references/compression-and-expansion-gates.md",
        "ccs-writing-style/references/compression-and-expansion-gates.md",
    ),
)

# Declared aliases: a pointer file may name a gate by a word its own prose uses, provided the
# owning file really declares the canonical name and the pointer text names that canonical name
# too (R-19.3). The pairing is declared here rather than inferred, so an undeclared second name
# cannot silently pass.
ALIASES = {
    "Gate-Expand-Design": "Gate-Expand-Scheme",
}

GATE_NAME = re.compile(r"Gate-[A-Za-z]+(?:-[A-Za-z]+)*")
NAME_DELIMITER = re.compile(r"(?=$|[\s\-—:.,)])")

# A line that rules the name out, or contrasts it with the canonical name. Two cue classes,
# because English uses both directions and the direction is what decides which name is warned
# about (see line_is_mention):
#   * LEADING — may expect / is not a / instead of / renamed …: the cue precedes the name it warns
#     about, e.g. "a reader may expect `Gate-Expand-Design`".
#   * TRAILING — "no such gate", "X is not a gate", "X was renamed": the cue is anaphoric and
#     points back at the name just written, e.g. "… `Gate-Expand-Design`; no such gate exists".
# "no such" is deliberately NOT a leading cue: it refers back, and treating it as forward-looking
# made it swallow the canonical name a warning ends by recommending.
MENTION_CUE = re.compile(
    r"(?:does not exist|doesn't exist|do not exist|never existed|is not a|not a real|"
    r"may expect|might expect|used to name|formerly named|renamed|deprecated|superseded|"
    r"instead of|rather than|rather than as|quietly writing|no separate|there is no|"
    r"is not (?:a |the )?(?:gate|separate gate)|not a gate)",
    re.IGNORECASE,
)

# Contrast cues compare two names instead of ruling one out: "there is no separate balance gate,
# the owner folds the reading into `Gate-Expand-Scheme`" warns about the *other* name on the line
# and merely tells the reader where the reading lives. When a contrast cue's subject is a gate name
# further along the sentence, the cue is not about the name being tested; see line_is_mention.
CONTRAST_CUE = re.compile(
    r"(?:instead of|rather than|no separate|is not (?:a |the )?(?:replacement|substitute)|"
    r"not a replacement|rather than as)",
    re.IGNORECASE,
)

# Cues that keep their authority when they FOLLOW the name: they introduce the replacement or
# assert non-existence about the thing just named, so they bind backwards.
TRAILING_MENTION_CUE = re.compile(
    r"^\s*(?:[)\]]|\*\*)?\s*(?:(?:is|are|was|were)\s+)?"
    r"(?:not a gate|no such (?:gate|thing)|does not exist|doesn't exist|was renamed|"
    r"was deprecated|was superseded|is deprecated|is superseded|is not declared)"
    r"\b",
    re.IGNORECASE,
)

# A line that hands the reader a task. A quoted name on such a line is a use even when the same
# file also warns about it elsewhere.
INVOKE_CUE = re.compile(
    r"\b(?:invoke|invokes|invoked|call|calls|called|apply|applies|applied|run|runs|ran|"
    r"use|uses|used|check|checks|checked|verify|verifies|verified|grep|looks? up|"
    r"report|reports|record|records|count|counts|measure|measures)\b",
    re.IGNORECASE,
)

BACKTICKED = re.compile(r"`[^`]*`")

# The cue must sit near the NAME it rules out, not merely somewhere on the line. A warning
# sentence contrasts two names ("a reader may expect a `Gate-Expand-Design`; no such gate exists
# — the owner declares `Gate-Expand-Scheme`"), and a line-scoped test would swallow the canonical
# name it points at. The window is measured from the occurrence of the name in question.
MENTION_WINDOW = 110

# A sentence boundary in Markdown prose: a stop (possibly followed by closing emphasis or a
# bracket) and then whitespace. "**There is no separate balance gate.** The owning file …" is two
# sentences, and a cue in the first must not bind to a name in the second.
SENTENCE_BOUNDARY = re.compile(r"[.;!?][)\]*`*}\*]*\s")


def named_gates(text: str) -> list[str]:
    """Every gate name the text names, in first-appearance order, deduplicated (R-20a guard
    included: names named only inside a mention line are returned by `classify` separately)."""
    seen: list[str] = []
    for match in GATE_NAME.finditer(text):
        name = match.group(0).rstrip("-")
        if name not in seen:
            seen.append(name)
    return seen


def line_is_mention(line: str, name: str) -> str:
    """Return the mention cue that rules THIS name out, or "" when the line does not.

    One rule, and it is grammatical: **a cue in the same sentence, before the name, binds to the
    nearest following gate name.** A warning necessarily states the cue first and then names the
    thing it warns about, so:

      * "a reader may expect `Gate-Expand-Design`; **no such gate exists**" — "may expect" sits
        before the design gate, so the design gate is a mention;
      * the trailing "**no such gate exists**" in that same sentence comes after the design gate
        and belongs to it, so it cannot also be read as a cue for a name that follows later;
      * "the owner declares `Gate-Expand-Scheme`" names the canonical gate with no cue before it,
        so the canonical gate is a use and must resolve.

    A cue that follows the name it warns about is handled by the trailing set, for the forms
    where that is idiomatic ("`Gate-Design` is not a gate"). Gate names are masked before the cue
    search so a cue phrase containing a gate name cannot match itself.
    """
    masked = GATE_NAME.sub(lambda m: " " * len(m.group(0)), line)
    for occurrence in re.finditer(re.escape(name), line):
        trailing = masked[occurrence.end():occurrence.end() + MENTION_WINDOW]
        cue = TRAILING_MENTION_CUE.search(trailing)
        if cue:
            return cue.group(0).strip()
        # Sentence start: the cue must be in the same sentence, not an earlier one.
        sentence_start = max(0, occurrence.start() - MENTION_WINDOW)
        for boundary in SENTENCE_BOUNDARY.finditer(line[:occurrence.start()]):
            sentence_start = max(sentence_start, boundary.end())
        segment = masked[sentence_start:occurrence.start()]
        # The cue binds to the nearest following name, so a name already inside the same sentence
        # consumes any earlier cue. A sentence boundary resets the binding (the cue belonged to the
        # earlier sentence): "**There is no separate balance gate.** The owning file folds the mass
        # reading into `Gate-Expand-Scheme`" warns in sentence 1 and *sends the reader to* the gate
        # in sentence 2, so the gate in sentence 2 is a use and must resolve.
        name_between = GATE_NAME.search(line, sentence_start, occurrence.start())
        if name_between:
            boundary = None
            for candidate in SENTENCE_BOUNDARY.finditer(line[name_between.end():occurrence.start()]):
                boundary = name_between.end() + candidate.end()
            if boundary is None:
                continue
            sentence_start = boundary
            segment = masked[sentence_start:occurrence.start()]
        cue = MENTION_CUE.search(segment)
        if not cue:
            continue
        # A contrast cue is about the name it compares against, not about this one, whenever a gate
        # name follows it before this occurrence: "there is no separate `Gate-Expand-Balance`: the
        # owner folds the reading into `Gate-Expand-Scheme`" warns about the first name and sends the
        # reader to the second. Only cue text after the contrast (if any) binds here.
        contrast = CONTRAST_CUE.search(segment)
        if contrast and GATE_NAME.search(line, sentence_start + contrast.end(), occurrence.start()):
            inner = MENTION_CUE.search(segment[contrast.end():])
            if not inner:
                continue
            cue = inner
        return cue.group(0)
    return ""


def line_is_use(line: str, name: str) -> bool:
    """True when the line hands the reader the name as a task (or names it with no cue at all)."""
    if line_is_mention(line, name):
        return False
    if INVOKE_CUE.search(line):
        return True
    for span in BACKTICKED.finditer(line):
        if name in span.group(0):
            return True
    # A name in a table cell or list item that points at an owner is a use: the reader is being
    # sent to it. A name in ordinary prose with no cue is treated as a use too, because the
    # fail-closed default for an unresolvable instruction is FAIL (R-19.2).
    if line.lstrip().startswith(("|", "-", "*")) or "ccs-writing-style" in line:
        return True
    return True


def classify_line(line: str, name: str) -> str:
    """`"mention"` or `"use"` for one (line, name) pair, with the mention guard applied first."""
    if line_is_mention(line, name):
        return "mention"
    return "use"


def resolves(owner_text: str, name: str) -> tuple[bool, str]:
    """True when the owner declares this name as a heading or a bold lead-in."""
    if f"### {name}" in owner_text:
        return True, "heading"
    if f"**{name}" in owner_text:
        return True, "bold lead-in"
    # A name declared on a heading or bold line followed by prose. The match must end at a
    # delimiter, so a longer name that merely starts with this one is a different gate.
    for line in owner_text.split("\n"):
        stripped = line.lstrip()
        if not (stripped.startswith("#") or stripped.startswith("**")):
            continue
        for match in re.finditer(re.escape(name), line):
            if NAME_DELIMITER.match(line, match.end()):
                return True, "heading or bold line declaring the name"
    return False, "absent"


# The historical defect, verbatim in shape: the pointer file used to name a design gate the
# owner never declared, and a separate balance gate that does not exist (R-19's reason).
HISTORICAL_USE = (
    "## Invocation list\n"
    "Invoke the owner's `Gate-Expand-Design` and `Gate-Expand-Balance` before the budget check.\n"
    "Here `Gate-Expand-Design` \u2261 `Gate-Expand-Scheme`, so the declared alias resolves it; "
    "`Gate-Expand-Balance` has no alias and no declaration, so it must be reported unresolved.\n"
    "`Gate-Condense-SomethingElse` is named with no declaration anywhere and must fail too.\n"
)
# The historical safety warning, verbatim in shape: mention only, must NOT be judged.
HISTORICAL_MENTION = (
    "A reader may expect a `Gate-Expand-Design`; **no such gate exists** — the owner declares "
    "`Gate-Expand-Scheme`.\n"
)
OWNER_SAMPLE = (
    "### Gate-Expand-Scheme\n\nSome rule text.\n\n"
    "**Gate-Expand-Overview — Overview floor.** Some rule text.\n"
)


def judge_lines(text: str, owner_text: str = OWNER_SAMPLE) -> dict[str, object]:
    """Run the same classification the CLI runs, over an in-memory text and owner."""
    used: list[dict[str, str]] = []
    mentioned: list[dict[str, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        for name in dict.fromkeys(GATE_NAME.findall(line)):
            name = name.rstrip("-")
            cls = classify_line(line, name)
            if cls == "mention":
                mentioned.append({"gate": name, "line": number,
                                  "cue": line_is_mention(line, name)})
                continue
            canonical = ALIASES.get(name, name)
            ok, how = resolves(owner_text, canonical)
            declared = canonical == name or f"`{canonical}`" in text
            used.append({"gate": name, "canonical": canonical,
                         "resolved": bool(ok and declared), "how": how, "line": number})
    return {
        "used": used,
        "mentioned": mentioned,
        "unresolved": [u for u in used if not u["resolved"]],
    }


def run_self_test(output: list[str] | None = None) -> int:
    """A checker that cannot fail proves nothing, and a guard proven in one direction is not a
    guard: mention and use of the same name are exercised in the same run.

    `output`, when given, receives the LABEL of every assertion this run actually executed
    (t7/F-1) — an enumeration of the run itself rather than a second reading of the source, so a
    harness can assert the printed total equals the number of assertions performed.

    The total is COUNTED — one entry per assertion actually executed — because the literal
    `len(cases) + 7` this function used to print had drifted from the code: it reported 13 against
    the 14 assertions it ran (t7, finding F-1).  `assertions` is what `self-test: N/N` prints, and
    `self_test_assertion_names()` reads the same call sites out of this file, so the reported count
    and the executed count cannot disagree again.
    """
    failures = 0
    assertions: list[str] = []

    def checked(label: str, ok: bool) -> None:
        """Account for exactly one assertion.  Every check below goes through here."""
        assertions.append(label)
        if output is not None:
            output.append(label)
        if not ok:
            failures += 1

    # --- unit level: the resolver itself ------------------------------------------------
    cases = {
        "heading-resolves": ("Gate-Expand-Scheme", True),
        "bold-lead-in-resolves": ("Gate-Expand-Overview", True),
        "longer-name-is-not-the-same-gate": ("Gate-Expand-SchemeRENAMED", False),
        "absent-name-fails": ("Gate-Condense-SomethingElse", False),
        "legacy-design-name-is-absent-here": ("Gate-Expand-Design", False),
        "absent-balance-name-fails": ("Gate-Expand-Balance", False),
    }
    for label, (name, expected) in cases.items():
        ok, how = resolves(OWNER_SAMPLE, name)
        checked(label, ok == expected)
        status = "ok" if ok == expected else "NOT DETECTED"
        print(f"  self-test {label:38s} {status} (resolved={ok}, how={how})")

    # The alias table must map the legacy name onto a canonical name the owner sample declares,
    # which is what makes the alias path meaningful rather than a bypass.
    alias_ok = all(resolves(OWNER_SAMPLE, canonical)[0] for canonical in set(ALIASES.values()))
    checked("alias-targets-resolve-in-owner", alias_ok)
    print(f"  self-test {'alias-targets-resolve-in-owner':38s} {'ok' if alias_ok else 'NOT DETECTED'}")

    # --- mention-vs-use guard: BOTH directions in this one run (R-20a.1) ---------------
    mention_result = judge_lines(HISTORICAL_MENTION)
    mention_names = {m["gate"] for m in mention_result["mentioned"]}
    mention_admitted = "Gate-Expand-Design" in mention_names
    mention_clean = not mention_result["unresolved"]
    print(f"  self-test {'warning-sentence-is-a-mention-not-a-use':38s} "
          f"{'ok' if (mention_admitted and mention_clean) else 'NOT DETECTED'} "
          f"(mentioned={sorted(mention_names)}, unresolved={[u['gate'] for u in mention_result['unresolved']]})")
    checked("warning-sentence-is-a-mention-not-a-use", mention_admitted and mention_clean)

    use_result = judge_lines(HISTORICAL_USE)
    use_names = {u["gate"] for u in use_result["unresolved"]}
    # The instruction line must still fail on every name that is neither declared nor covered by a
    # declared alias. `Gate-Expand-Design` resolves only because the file declares the R-19.3 alias,
    # which is the intended behaviour and is asserted separately below.
    use_fires = {"Gate-Expand-Balance", "Gate-Condense-SomethingElse"} <= use_names
    design_alias_resolved = not any(u["gate"] == "Gate-Expand-Design" for u in use_result["unresolved"])
    print(f"  self-test {'instruction-line-still-FAILs':38s} "
          f"{'ok' if use_fires else 'NOT DETECTED'} (unresolved={sorted(use_names)})")
    checked("instruction-line-still-FAILs", use_fires)
    print(f"  self-test {'declared-alias-resolves-on-instruction-line':38s} "
          f"{'ok' if design_alias_resolved else 'NOT DETECTED'}")
    checked("declared-alias-resolves-on-instruction-line", design_alias_resolved)

    # A contrast cue must not silence the gate it recommends: "there is no separate balance gate,
    # the owner folds the reading into `Gate-Expand-Scheme`" warns about the first name only, and
    # the second name must still be judged (which here means it must resolve).
    contrast_line = (
        "There is no separate `Gate-Expand-Balance`: the owner folds the reading into "
        "`Gate-Expand-Scheme`.\n"
    )
    contrast_result = judge_lines(contrast_line)
    contrast_ok = (
        {m["gate"] for m in contrast_result["mentioned"]} == {"Gate-Expand-Balance"}
        and {u["gate"] for u in contrast_result["used"]} == {"Gate-Expand-Scheme"}
        and not contrast_result["unresolved"]
    )
    print(f"  self-test {'contrast-cue-does-not-silence-the-owner':38s} "
          f"{'ok' if contrast_ok else 'NOT DETECTED'} "
          f"(mentioned={sorted({m['gate'] for m in contrast_result['mentioned']})}, "
          f"judged_as_use={sorted({u['gate'] for u in contrast_result['used']})})")
    checked("contrast-cue-does-not-silence-the-owner", contrast_ok)

    # Same name, no alias declared in the file: a legacy name with no remedy must FAIL, which is
    # what proves the alias path is not a blanket escape hatch.
    undeclared = judge_lines("Invoke `Gate-Expand-Design` for the scheme gate.\n")
    undeclared_fires = {u["gate"] for u in undeclared["unresolved"]} == {"Gate-Expand-Design"}
    print(f"  self-test {'undeclared-legacy-name-FAILs':38s} "
          f"{'ok' if undeclared_fires else 'NOT DETECTED'} "
          f"(unresolved={sorted({u['gate'] for u in undeclared['unresolved']})})")
    checked("undeclared-legacy-name-FAILs", undeclared_fires)

    # One run must show both verdicts for the SAME name, which is the property the guard is for:
    # the name is excluded where the text warns about it, and simultaneously judged where the text
    # hands it to the reader. The judgement may be resolve (declared alias) or FAIL (no remedy) —
    # what matters is that the guard did not silence the use.
    used_or_failed = {u["gate"] for u in use_result["used"]}
    both = ("Gate-Expand-Design" in mention_names and "Gate-Expand-Design" in used_or_failed)
    print(f"  self-test {'same-name-both-directions-one-run':38s} {'ok' if both else 'NOT DETECTED'} "
          f"(mentioned={sorted(mention_names)}, judged_as_use={sorted(used_or_failed)})")
    checked("same-name-both-directions-one-run", both)

    # --- the guard in the real POINTER_PAIRS shape (pointer text -> owner text) ---------
    pointer_text = HISTORICAL_MENTION + HISTORICAL_USE
    owner_text = OWNER_SAMPLE
    judged = judge_lines(pointer_text, owner_text)
    mixed_ok = (
        {m["gate"] for m in judged["mentioned"]} == {"Gate-Expand-Design"}
        and {u["gate"] for u in judged["unresolved"]} == {"Gate-Expand-Balance", "Gate-Condense-SomethingElse"}
    )
    print(f"  self-test {'mixed-file-splits-mention-from-use':38s} {'ok' if mixed_ok else 'NOT DETECTED'}")
    checked("mixed-file-splits-mention-from-use", mixed_ok)

    total = len(assertions)          # COUNTED, never computed from a literal (t7, F-1)
    print(f"self-test: {total - failures}/{total} as expected")
    return 1 if failures else 0


def self_test_assertion_names() -> list[str]:
    """The label of every assertion `run_self_test()` executes, obtained by RUNNING it.

    Exists so the count is a fact a harness can check rather than something only the run states:
    `--list-assertions` prints this enumeration beside the suite's own `N/N`, and the two come
    from one execution, so they cannot disagree.  (An earlier version re-read the source with a
    regex, which would have been a second implementation of the same claim; it was replaced.)
    """
    executed: list[str] = []
    run_self_test(output=executed)
    return executed


def check_pairs(skills_root: Path) -> tuple[list[dict], list[dict], list[str], int]:
    """Returns (used findings, mention exclusions, pointer files inspected, setup error code)."""
    findings: list[dict[str, object]] = []
    mentions: list[dict[str, object]] = []
    for pointer_rel, owner_rel in POINTER_PAIRS:
        pointer = skills_root / pointer_rel
        owner = skills_root / owner_rel
        if not pointer.is_file():
            print(f"setup error: pointer file missing: {pointer}", file=sys.stderr)
            return [], [], [], 2
        if not owner.is_file():
            print(f"setup error: owning file missing: {owner}", file=sys.stderr)
            return [], [], [], 2
        owner_text = owner.read_text(encoding="utf-8")
        pointer_text = pointer.read_text(encoding="utf-8")
        for number, line in enumerate(pointer_text.splitlines(), 1):
            for name in dict.fromkeys(GATE_NAME.findall(line)):
                name = name.rstrip("-")
                cls = classify_line(line, name)
                if cls == "mention":
                    mentions.append({"pointer": pointer_rel, "line": number, "gate": name,
                                     "cue": line_is_mention(line, name)})
                    continue
                canonical = ALIASES.get(name, name)
                ok, how = resolves(owner_text, canonical)
                declared = canonical == name or f"`{canonical}`" in pointer_text
                findings.append({
                    "pointer": pointer_rel, "owner": owner_rel, "gate": name,
                    "canonical": canonical, "resolved": bool(ok and declared),
                    "how": (how if canonical == name
                            else f"{how} via declared alias {name} -> {canonical}"),
                    "alias_declared_in_pointer": declared, "line": number,
                })
    pointer_files = sorted({f["pointer"] for f in findings})
    return findings, mentions, pointer_files, 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="repository root containing skills/ (default: the checkout containing this script)",
    )
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="prove the check can fail, and that a warning sentence is not punished",
    )
    parser.add_argument(
        "--list-assertions",
        action="store_true",
        help="print one line per assertion --self-test executes, read from this file, and exit 0. "
             "The printed self-test total is counted from the same call sites, so a harness can "
             "check the two agree (t7, F-1).",
    )
    args = parser.parse_args(argv)

    if args.list_assertions:
        # Run the suite for real and print the assertions it EXECUTED, so the enumeration and the
        # printed total come from one execution rather than two readings of the source.
        executed: list[str] = []
        rc = run_self_test(output=executed)
        for i, name in enumerate(executed, 1):
            print(f"{i:3d}  {name}")
        print(f"assertions: {len(executed)}")
        print(f"run returned: {rc}")
        return 0

    if args.self_test:
        return run_self_test()

    skills_root = args.repo / "skills"
    if not skills_root.is_dir():
        print(f"setup error: {skills_root} is not a directory", file=sys.stderr)
        return 2

    findings, mentions, pointer_files, setup_error = check_pairs(skills_root)
    if setup_error:
        return setup_error

    unresolved = [f for f in findings if not f["resolved"]]
    if not findings and not mentions:
        # A vacuous run must not read as success: the pairs were declared but named nothing.
        print("setup error: no gate names found in any declared pointer file", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "pairs_checked": len(POINTER_PAIRS),
            "pointer_files_checked": pointer_files,
            "gate_names_used": sorted({f["gate"] for f in findings}),
            "gate_names_mentioned_only": sorted({m["gate"] for m in mentions}),
            "resolved": sum(1 for f in findings if f["resolved"]),
            "unresolved": unresolved,
            "mentions_excluded": mentions,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"pointer/owner pairs checked: {len(POINTER_PAIRS)} "
              f"({len(pointer_files)} pointer file(s), {len(findings)} gate name(s) used)")
        for entry in findings:
            status = "OK  " if entry["resolved"] else "FAIL"
            print(f"  {status} {entry['gate']:45s} -> {entry['owner']} ({entry['how']})")
        for entry in mentions:
            print(f"  skip {entry['gate']:45s} -> mention, not a use "
                  f"({entry['pointer']}:{entry['line']}, cue: \"{entry['cue']}\")")
        print(f"RESULT: {'PASS' if not unresolved else 'FAIL'} "
              f"({len(findings) - len(unresolved)}/{len(findings)} gate names resolve)")
        for entry in unresolved:
            print(f"  unresolved: {entry['gate']} is used by {entry['pointer']}:{entry['line']} "
                  f"but does not appear as a heading or bold lead-in in {entry['owner']}")

    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
