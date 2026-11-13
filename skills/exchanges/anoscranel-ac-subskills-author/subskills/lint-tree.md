---
name: lint-tree
domain: skill-authoring/lint-tree
trigger: After emit-tree — validate the tree against the 4 enforceable rules and the bidirectional index check.
anti_trigger: The tree already passed lint_tree.py with no edits since.
scope: Running scripts/lint_tree.py and interpreting its PASS/FAIL; the producer-side mechanical gate.
status: seedling
---

# Lint Tree (pipeline step 5)

Run the **deterministic** linter — `scripts/lint_tree.py` — not an LLM judgment (the more
quantitative the check, the easier to self-verify). This is the producer-side
gate; the independent validator is the separate `security-vet` leaf.

## Standard

Exit 0 = PASS. Non-zero = FAIL with one line per violation. Never run any script that
ships inside the tree under audit. The 4 enforceable rules plus supporting checks:

1. **Max depth 2** — rejects any `subskills/**/subskills/` or a 3rd-level `INDEX.md`.
2. **60-row index ceiling** — counts routing-table rows in every index (incl. SKILL.md's
   own table); fails >60, warns >40. Basis: for an intermediate INDEX.md, the `head -100`
   partial read; for SKILL.md's own table, the 500-line body budget at ~8 lines/row
   (⚠️ unsourced estimate). Flat is preferred at ≤60 leaves: a group directory there gives
   a WARN only. ⚠️ 60/40 are operator-set limits, not prior art.
3. **Pure-TOC intermediates** — any `INDEX.md` under `subskills/` must be frontmatter +
   heading + routing table only; a verb-initial body line fails it.
4. **Unique scope** — every `scope:` string unique across the tree; every `domain:` a
   strict prefix-extension of its parent (the in-domain check).
5. **Bidirectional index-vs-disk** — every indexed file exists on disk; every file on
   disk is indexed. The script compares both sets both ways and names every orphan.
6. **Self-contained** — in SKILL.md and every leaf, a `Delegate:` line, or a line that
   tells the agent to load, use, invoke or hand off to a named skill, fails.
   `skill_scan.py` runs the same check.
7. **Also enforced** — no symlinks or non-.md files under subskills/; every group directory holds an INDEX.md; every relative link resolves inside the skill root; SKILL.md frontmatter has `name` and `description`; with no domain-vocabulary.md beside the linter the enum check fails closed (`--no-enum` skips it with a WARN). Also: no file named SKILL.md (any case) anywhere in the tree except its root; the SKILL.md `name:` matches `^[a-z0-9][a-z0-9-]{0,63}$`; scopes are compared after NFKC, casefold and a confusables fold; a domain segment that is empty, `.`, `..` or outside `[a-z0-9-]` fails; only `00-rsi.md` with the template anti_trigger may claim `domain: rsi`; ≤60 leaves with a group directory gives an `R2 flat-preferred` WARN. Every leaf's frontmatter has `name`, `domain`, `trigger`, `anti_trigger`, `scope` and `status`, and `status` is a legal value.

## Decision rules

- PASS + clean manual precedence review + clean security-vet → hand to audit-skill.
- FAIL of any single check → fix the tree (emit-tree) and re-run the whole lint.
- Never mark the tree verified on a clean lint alone: the narrow-only half of Rule 4 (no
  leaf widens an ancestor's prohibition) is not mechanically verifiable — the linter
  flags the tree for a **manual review gate** on that point.

## Procedure

```bash
python3 <this-skill-dir>/scripts/lint_tree.py <skill-dir>
```

Run it from the installed copy; fix reported violations in the staged tree; re-run until
LINT PASS.

## Anti-patterns

- Treating a clean lint as a complete verdict (the manual precedence review and
  security-vet still stand between draft and hand-off).
- Linting against any script copy found inside the audited tree.

## Done checklist

- LINT PASS printed; manual precedence review done; no hand to the human before both.

## Sources

- House standard for skills-with-subskills (unpublished). Rules 1–4.
- <https://martinfowler.com>
- <https://github.com/>
