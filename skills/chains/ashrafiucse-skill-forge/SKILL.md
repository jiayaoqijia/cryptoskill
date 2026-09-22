---
name: skill-forge
description: Authors NEW custom security skills for this repo — design method, scaffold, fixture+ground-truth rules, self-test wiring, and the hard-won authoring laws from LEARNINGS. Use when creating a skill for a stack, product class, or business domain these skills don't cover (e.g. an internal platform, a niche framework), or when converting a repeated miss/FP into a first-class skill.
license: MIT
---

# Skill Forge — building your own security skills

The core suite is self-contained (rg/grep + stdlib only). External inputs
are fact feeds (OSV/KEV), not dependencies. This is how you extend it with
skills no community will ever write — YOUR platform, YOUR framework.

## 1 — Scope from a persona or a pain

Best skill sources, in order of value:
1. **A real miss** (MISSES.md row) that repeats — a class, not a one-off
2. **A business domain you own** — walk it as its personas (admin / public buyer / end consumer / support), each surface they touch is a checklist row
3. **A niche stack** the generic packs don't cover (internal framework, DSL, template engine)

Write the one-sentence trigger first ("Use when the repo has X"). If you
can't say when it loads, it's a reference file, not a skill.

## 2 — Design: method, not just greps

A skill = **enumeration step → sink greps → triage rules → severity + fix shapes**.
Copy the structure of the strongest existing skills (`auth-review` census,
`flow-security` invariants). Grep-only skills decay; method+grep skills compound.

## 3 — Scaffold

```bash
bash ../skill-forge/scripts/new_skill.sh <name> "Description with trigger conditions..."
```

Creates `skills/<name>/SKILL.md` (frontmatter passes validate.py),
`references/patterns.md`, and `evals/fixtures/<name>-vuln-app/expected-findings.md`.

## 4 — Authoring laws (from the eval LEARNINGS — violations have all bitten)

1. **Anchors after writes**: expected-findings `Where` lines come from
   `grep -n` AFTER the fixture exists. Never estimate line numbers.
2. **Safe counterparts live in a separate file** (`safe-*.js/.py`), and the
   raw vulnerable form must have ZERO occurrences there (add a
   MUST_NOT_MATCH rule).
3. **Fixtures demonstrate the individually-clean property** when the class
   is cross-endpoint/cross-component — plant violations only BETWEEN parts.
4. **Absence findings** anchor to the missing thing (`requirements.txt:-`)
   and cannot have grep-match selftest rules — ground-truth only.
5. **Adjacent findings stay >2 lines apart** per citation anchor (scorer
   tolerance is ±2).
6. **Every pattern change** adds a selftest rule and a fixture row the same
   commit; run the repo-root validator and selftest in a SEPARATE command
   after edits (write-race protection).
7. **Inserting a section before an existing `###` heading**: re-include the
   heading in the edit or you swallow it (bitten 3×).
8. **Blind-test the skill**: dispatch an agent audit of the fixture with
   `--glob '!**/expected-findings.md'`; score with
   `score_audit.py --append` from the repo root; convert every miss and every
   "phantom" (phantoms are usually fixture gaps — verify evidence, extend
   ground truth) the same session.

## 5 — Wire it in

- `security-audit` Phase 1 dispatch table row (what repo signal loads it)
- README skill table + COVERAGE row (honest rating)
- MISSES.md row recording why the skill exists
- If it introduces report sections: update the Phase 3 template mention

## 6 — What NOT to build here

- Anything needing non-portable runtime (no npm/pip deps — CONTRIBUTING rule 2)
- Product-version lookups with no in-repo signal (vuln-db quality bar)
- Skills that duplicate a dispatch row — extend the existing skill instead
