---
name: routing-eval
domain: skill-authoring/routing-eval
trigger: Measure whether a skill's description and index route real tasks to the right leaf, before any leaf is marked verified or a new skill installs.
anti_trigger: Checking file structure, headers or scope uniqueness (lint-tree), or vetting files for injection (security-vet).
scope: Blind index-routing measurement (step 5b) plus a description self-check; the Level-1 entrance stays unmeasured.
status: seedling
---

# Routing Eval (pipeline step 5b)

Lint proves the interior, not that a task reaches the right leaf (the entrance problem). This leaf measures the route index → leaf blind, plus a description self-check. ⚠️ It does not measure the Level-1 entrance.

## Standard

The skill's producer plays none of the three roles:

| Actor | Sees | Writes |
|---|---|---|
| Label writer | the whole tree | `tasks.md`, `labels.md` |
| Sealed router | `tasks.md` + SKILL.md only | the routes table |
| Scorer | routes + labels | verdict via `scripts/route_score.py` |

Default PASS bars (a job may tighten with `--need GROUP=N`, `--min-pct P`; never loosen after routes exist):

| Group | Bar |
|---|---|
| Content rows, per skill | top-1 ≥ 80% (`ceil(0.8 × n)`) |
| Negatives | ≥ 3 of 4, or ≥ 75% for other counts |

⚠️ The bars are operator-set thresholds, not prior art; the 80% bar is illustrative.

## Decision rules

- Any leaf may move to `status: verified` only after a PASS.
- A NEW skill installs (on human approval or through the operator's fail-closed gate) only after a PASS.
- After an edit to an installed skill's index or triggers, re-run as a regression.

## Procedure

1. **Description check.** The loader sees only the `description` at startup: list 5–10 things a user would actually say when they need the skill; confirm the description names them in user words and says when NOT to use the skill; add missing common phrasings.
2. **Label writer:** at least one task per content leaf; at least 4 negatives that look in-domain but are out of scope (`expected` = `none`); phrase tasks as a user talks; rows `| Txx | skill | expected | alternates |` (`-` = none); commit labels to the run log before the router runs — then frozen.
3. **Sealed router:** never sees labels, leaves, findings or evidence; returns exactly `| id | rsi_first | first | second | confidence | index_enough |`, `first` = a leaf filename or `none`.
4. **Scorer:** record the scorer's sha256 and the exact command, with every flag, in the run log BEFORE the router runs — other flags void the run. Top-1 counts toward PASS; top-2 is reported only.

## Anti-patterns

- Editing labels to make a run pass — forbidden.
- Re-using a router that saw an earlier run — it is no longer blind.
- Tightening label versions mid-run: if a label is wrong, the label writer (never the producer or scorer) publishes a new labels version, one reason per changed row, BEFORE the next run; score later runs against BOTH versions (operator precedent: the projects-audit j6 runs).
- Fixing anything on FAIL other than the index wording, leaf `trigger`/`anti_trigger`, or the description.

## Done checklist

- PASS bars met on content rows and negatives; scorer command+hash logged before routing; verdict logged. Precedent (j6 run 4): content 10/10 and 15/16, negatives 4/4, PASS — read ambiguity notes even on a PASS.

## Sources

- House standard for skills-with-subskills (unpublished). The 80% bar is illustrative.
- <https://arxiv.org>
- <https://github.com/>
