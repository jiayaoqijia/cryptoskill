---
name: 00-rsi
domain: rsi
trigger: Always — passively, after any leaf in this skill fires, to log the event.
anti_trigger: Never blocks a task; never rewrites a file; never installs anything.
scope: Append this skill's (ac-subskills-author's) routing events to the central log. Queue nothing in Stage 1. Acts on no other skill and on no shared core.
status: seedling
---

# RSI — self-improvement logger + proposer (this skill only)

This leaf NEVER edits a file, NEVER installs, and NEVER blocks a task. It only appends. Append-only is a HARD rule (SPEC-rsi-skills.md §4 rule 1), not just an instruction.

## Standard

Stage 1 posture is log-only. One append-only event log lives outside every skill tree.
`outcome` and `validator_verdict` live in a separate outcome record written by the HARNESS
or validator, NOT by this skill — a skill never records its own outcome (SPEC-rsi-skills.md §4 rule 3). The
Stage-1 gate thresholds are ≥100 events, ≥95 in 100 joined to an independent outcome
record, intact append-only, ≥30 days (SPEC-rsi-skills.md §0 house-set thresholds, not derived from prior art).

## Decision rules

- Every routing event in THIS skill → append one line (never batch, never skip).
- An optimization pass (run by the operator, or the shared `ac-rsi` core from Stage 2) →
  surface proposals the core wrote for this skill as evidence cards. Never apply them.
- Prune-lane proposals are the default; additive proposals get the strictest review.

## Procedure

1. If the operator has enabled RSI logging, append one line to the log path they
   configured (opencode default `~/.local/share/opencode/rsi/leaf-events.jsonl`, outside
   every skill tree) with:

```
{ ts, skill, leaf_routed, trigger_text, model, sessionID, callID }
```

   If logging is not enabled, do nothing.

2. Never write a file inside a skill tree at run time.
3. On demand (Stage 2 only), hand the core's proposals for THIS skill to the human + validator gate
   (SPEC-rsi-skills.md §4 rule 5). Apply nothing yourself.

## Anti-patterns

- Editing, deleting or truncating ANY file — including the log itself.
- Logging secrets, credentials or personal data; `trigger_text` is the index trigger,
  never the user's words.
- Recording this skill's own outcome, or acting on another skill or the shared core.

## Done checklist

- One jsonl line per routing event, schema-conformant, appended, never rewritten.
- Proposals surface as evidence cards only; zero self-applied edits.

The proposal is only actionable when it names the line it would change, because a proposal at the level of intent cannot be reviewed and cannot be safely rejected. Line-level proposals are cheap to evaluate and cheap to discard, which is what makes an optimisation pass tolerable.

## Sources

- SPEC-rsi-skills §0/§4/§6/§7: https://github.com/anoscranel/rsi-skills/blob/main/docs/SPEC-rsi-skills.md
- Event schema: `ac-rsi/schema/log-schema.md` in https://github.com/anoscranel/rsi-skills (install `ac-rsi` alongside this skill).
