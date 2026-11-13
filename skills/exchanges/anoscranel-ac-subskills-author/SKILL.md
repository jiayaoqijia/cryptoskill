---
name: ac-subskills-author
description: "Authors new self-contained Agent Skills that contain subskills, and audits skills before install (install only after a human approves, or through a fail-closed install gate the operator runs). Every emitted leaf holds its full procedure and hands no work to another skill. Use when creating a skill-with-subskills, decomposing an oversized skill into a subskills/ layout, rebuilding a skill so it depends on no other skill, vetting a third-party skills.sh skill for install, scanning a skill tree for injection or hand-off lines (scripts/skill_scan.py), linting a subskill tree against the 4 enforceable rules, or running a blind routing evaluation (does a task reach the right leaf?) on a skill's description and index. Not for writing a small flat skill with no subskills."
license: MIT
metadata:
  domain: skill-authoring
---

# Skill Author — authoring skills that contain subskills

## Overview

`ac-subskills-author` is the meta-skill that creates other skills-with-subskills. It encodes the
full gated pipeline: research the domain → map the domain → decide flat-vs-nested → emit
the tree → lint it → routing-test it → vet it → **install only on human approval or through a fail-closed
gate the operator runs**. It
is the reference implementation of the subskills standard and **obeys every rule it
enforces** (it is itself flat depth-1, 10 leaves, far under the 60-leaf ceiling (a house limit ⚠️)).

**Self-contained rule (v3).** A skill this pipeline emits depends on no other skill. Every
leaf holds its full procedure. A subdomain another skill covers is re-researched from
primary sources and written in the new skill's own words, never copied, never handed off.
`lint_tree.py` and
`skill_scan.py` FAIL any `Delegate:` line or hand-off line. This skill follows the rule
too: its own scanner, `scripts/skill_scan.py`, does the deterministic scan.

The governing standard is the house standard for skills-with-subskills (unpublished); this skill operationalizes it.

## When to Use

- Creating a new skill that will contain a `subskills/` directory
- Decomposing an existing oversized skill into a `subskills/` layout
- Converting a bare `references/` folder into routed subskills
- Vetting any skill (third-party or self-authored) for install through the robust audit pipeline
- Linting any skill-with-subskills against the 4 enforceable rules
- Testing whether a skill's description and index route real tasks to the right leaf (blind routing eval)

**When NOT to use:** writing a small flat skill with no subskills (write SKILL.md
directly). Not for debugging why a harness loads no skills at runtime — this skill cannot observe runtime loading (see Status & honest limits). Install only after a human approves, or through a fail-closed gate the operator runs (see audit-skill.md stage 7); never copy a tree in by hand. A skill that fails is quarantined and flagged to
the operator, never installed.

## The Pipeline (gated, in order — do not skip a step)

Each step routes to exactly one subskill. Do not advance until the current step's gate
passes. **Dedup is decided, not asked** — the pipeline runs end-to-end to a verdict,
quarantining + flagging the operator on any failure; install follows step 7 and needs
human approval unless the operator has set up a fail-closed gate. Every pipeline
decision is logged to the run log for after-the-fact audit.

Enter at the step your task needs. Start at step 1 when you build or decompose a skill (research-gate confirms the domain, then domain-map does the split). A lint-only task starts at step 5. A routing or trigger test starts at step 5b. A vet-only or install task starts at step 6, then 6b. A question about `domain:` values goes to `subskills/domain-vocabulary.md`. 'Do not skip a step' applies once you are running the full build.

| Step | Task | Subskill to read |
|------|------|------------------|
| 1 | Verify the domain is researched (HALT if not); autonomous dedup — extend vs new | `subskills/research-gate.md` |
| 2 | Decompose the target domain into atomic, uniquely-claimed scopes | `subskills/domain-map.md` |
| 3 | Decide flat depth-1 vs nested (overflow valve only) | `subskills/flat-or-nest.md` |
| 4 | Write SKILL.md + subskills/ with valid routing headers + index | `subskills/emit-tree.md` |
| 5 | Run the 4 enforceable rules + bidirectional index check + the self-contained (no hand-off) check | `subskills/lint-tree.md` |
| 5b | Description check + blind routing eval (sealed router, pre-registered scorer `scripts/route_score.py`); PASS needed before `verified` or a new install | `subskills/routing-eval.md` |
| 6 | Vet every file: `scripts/skill_scan.py` (mechanical), then poisoned-leaf, trifecta, injection surface | `subskills/security-vet.md` |
| 6b | **Robust audit pipeline** — the single install gate for any skill; stage 3 runs `scripts/skill_scan.py --json` | `subskills/audit-skill.md` |
| 7 | **Install decision** (sole owner) — audit PASS → human approves, or the operator's fail-closed gate re-checks and installs; fail → quarantine + flag the operator | `subskills/audit-skill.md` |

## Precedence rule (Rule 4)

The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string
is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by
an ancestor — **leaves narrow, never override upward.** Each pipeline step has exactly one owning leaf. audit-skill.md owns steps 6b and 7; 00-rsi.md and domain-vocabulary.md sit outside the pipeline. On overlap, the leaf for the current pipeline step governs. The install decision belongs to step 7 (audit-skill.md).

## Subskills (10 — flat, no intermediates)

| Leaf | domain segment | scope (one line) |
|------|----------------|------------------|
| `subskills/00-rsi.md` | rsi | Observe this skill's trigger/outcome events; queue typed edit proposals (log-only in Stage 1). Background only — never open it for a user task, and never before a content leaf. |
| `subskills/research-gate.md` | research-gate | Is the domain researched enough? Halts if not; autonomous dedup (extend vs new). |
| `subskills/domain-map.md` | domain-map | Decompose the domain into a closed map of atomic scopes. |
| `subskills/flat-or-nest.md` | flat-or-nest | The flat-vs-nested decision (flat-first; nest only past ~60 leaves). |
| `subskills/emit-tree.md` | emit-tree | Write the SKILL.md + subskills/ tree with headers and index. |
| `subskills/lint-tree.md` | lint-tree | Run scripts/lint_tree.py — the 4 rules + bidirectional check. |
| `subskills/routing-eval.md` | routing-eval | Blind index-routing measurement (step 5b) plus a description self-check; the Level-1 entrance stays unmeasured. |
| `subskills/domain-vocabulary.md` | domain-vocabulary | The closed enum of legal top-level `domain:` segments. |
| `subskills/security-vet.md` | security-vet | `skill_scan.py` plus poisoned-leaf / trifecta / injection-surface vetting of every file (step 6). Makes no install decision; passes its result to audit-skill.md. |
| `subskills/audit-skill.md` | audit-skill | The 7-stage audit (steps 6b-7): the single install gate and the install-or-quarantine decision; writes an evidence card; re-run after any edit to a passed skill. |

## The 4 enforceable rules (what lint-tree checks)

1. **Max depth 2** — at most one pure-TOC intermediate level below SKILL.md.
2. **60-row index ceiling** — no index exceeds 60 rows (warn at 40); flat preferred ≤60 leaves (lint WARN, not FAIL). ⚠️ House-engineered limits (60 from the `head -100` partial-read mechanism; 40 is an unsourced margin), not published prior art.
3. **Pure-TOC intermediates** — an intermediate holds frontmatter + heading + routing table only.
4. **Unique scope + leaves-narrow-never-widen** — every `scope:` unique; no upward override.

Plus the **bidirectional index-vs-disk check**: every indexed file exists; every file on
disk is indexed. Plus the **self-contained check**: no `Delegate:` line and no line that
tells the agent to load, use, invoke or hand off to a named skill.

## Status & honest limits

`status: seedling` for every leaf until the entrance problem is measured: this
skill can enforce the *interior* rules mechanically, but cannot enforce whether a created
skill's subskills are actually triggered at runtime. Any skill it emits must pass the
routing-eval gate (step 5b, `subskills/routing-eval.md`) before a leaf is marked `verified`. Flat-first is the default
precisely because the entrance is the unmeasured flank.

**Install honesty:** The card is evidence, not permission. Install needs one of two things: a human's explicit approval, or a PASS from a fail-closed install gate that the operator set up and authorized for unattended use. With neither, do not install. A REJECTED is final: never edit the skill or the gate to pass it. The audit gate is a real
check, but it is not a guarantee. A passed scan reduces risk; it does not eliminate it.
Every install and every quarantine is logged to the run log so the operator can audit the
decisions. Fail-closed always: an inconclusive audit is a NO-INSTALL, never a
maybe.
