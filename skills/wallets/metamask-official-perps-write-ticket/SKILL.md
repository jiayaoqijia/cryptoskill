---
name: perps-write-ticket
description: Interactively author one clean, complete perps ticket — bug, EPIC, or initiative — that states intent and expected outcome without implementation. Use when a PM (or a Claude acting for one) has a raw perps observation, feature idea, or strategic goal and wants a single well-formed ticket ready for engineering to break down. This is the first (product) pass; the engineering split + layer routing is a separate pass (perps-breakdown-tickets). Captures what/expected/repro, makes the ticket surfaceable so it doesn't get lost, and stops before implementation or repo routing.
maturity: experimental
---

# Write Perps Ticket

Turn a raw perps observation, idea, or goal into **one clean, complete ticket**
the product team can file and engineering can break down as-is. You describe
*what* and *what's expected* — never *how*.

## When To Use

- A PM (or a Claude acting for one) reports a perps bug, proposes a feature, or
  frames a strategic goal and wants a well-formed ticket.
- The input is raw: a Slack message, a screenshot, a one-line idea.

This is the **first (product) pass**. The technical split — which repos/layers
change, dependency order, component routing — is the engineer's job and lives in
`perps-breakdown-tickets`. Do not do it here.

Not for: engineering task breakdown, or routing a ticket across Core/clients
(→ `perps-breakdown-tickets`).

## Operating principle: intent, not implementation

You own the *what* and the *why*. The engineer owns the *how*. A product ticket
that prescribes implementation boxes engineering into the wrong solution and goes
stale the moment the code moves.

- State expected behavior as a **testable outcome**, not a fix. "Size shows USD
  value" — not "call `abs(size) * entryPrice` in `position-card`".
- No file paths, no component names you'd have to guess, no layer routing.
- 2-3 sentences per field. One concern per ticket — split multi-bug reports.
- If you can't state the expected outcome in one testable line, it's not a
  ticket yet — ask the reporter.

## Pick the type

Ask which kind, or infer it and confirm. Each has its own shape:

- **Bug** — something is broken now. → behavior + repro.
- **EPIC** — a shippable, user-facing capability. → outcome + feature-level
  acceptance; tasks are deferred to engineering.
- **Initiative** — a strategic goal spanning multiple EPICs. → why + measurable
  success; no features yet.

## Workflow (interactive)

1. **Intake.** Read the raw input. Identify the type. Ask only what you can't
   infer: the expected outcome (as a testable line), and for bugs the repro path
   and required wallet state. Don't ask for anything an engineer derives later.
2. **One concern.** If the input bundles several bugs or goals, split into
   separate tickets — list them and confirm before writing.
3. **Draft the ticket** in the matching format below.
4. **Make it surfaceable** (see below) so it doesn't vanish into the backlog.
5. **Stop at the product boundary.** Do not add implementation, file paths, or a
   layer split. Hand off: a bug/EPIC is ready for `perps-breakdown-tickets`.

## Surfacing (so bugs don't get lost)

A filed ticket nobody triages is a lost ticket. On every ticket set:

- **Severity / priority** — for bugs, one line: user impact + how often it hits
  (every user / edge case). For EPICs/initiatives, the outcome's value.
- **Area label** — `perps` + the surface in plain words (e.g. "order entry",
  "position card"). Enough for triage to route; not a component path.
- **Type** correctly set (Bug / EPIC / Initiative) so it lands in the right
  queue, not an undifferentiated pile.

## Ticket formats

Keep every field tight. Plain language — the engineer maps surfaces to
components during breakdown.

### Bug

**Title** — `[bug] <one-line user-visible symptom>`
**What's broken** — actual behavior today: which screen, what the user sees,
what value/element is wrong. 1-2 sentences.
**Expected** — what should happen instead, as a **testable** "when X, then Y"
line. This becomes the acceptance criteria.
**Steps to reproduce** — numbered, from app open to bug visible.
**Surface** — the screen/area in plain words ("Perps home position card").
**Pre-conditions** — required wallet/app state (unlocked, open BTC position,
deposited balance). Only the ones that apply.
**Severity** — user impact + frequency.

For displayed numbers, describe the **semantic** ("shows the asset price",
"shows USD value of the position"), never a decimal count — precision is
range-adaptive (a $0.001 alt behaves differently from BTC).

### EPIC

**Title** — `[epic] <user-facing capability>`
**Outcome** — what the user can do after this ships that they can't today. 1-3
sentences.
**Acceptance (feature-level)** — testable "when X, then Y" lines describing the
capability working end to end. Not implementation steps.
**Scope** — in / out, in one line each. What this EPIC does NOT cover.
**Surface** — the perps area(s) affected, in plain words.
**Parent initiative** — link if one exists.

### Initiative

**Title** — `[initiative] <strategic goal>`
**Why** — the problem/opportunity and who it's for. 1-3 sentences.
**Success metric** — how we'll know it worked (measurable; a number or a clear
observable change), not a feature list.
**Scope boundary** — what's in and explicitly out at this level.
**Child EPICs** — known candidate EPICs (titles only; they get their own
tickets). Leave open if not yet decided.

## Quality bar (reject before filing)

- Bug with no repro or no testable expected line → ask the reporter; don't file.
- Implementation prescribed (file paths, "call X", layer routing) → strip it;
  that's the engineer's pass.
- Multi-bug / multi-goal in one ticket → split.
- "Investigate and fix" / "looks wrong" / "see recording" → narrow to a concrete
  expected outcome first.
- EPIC/initiative with no measurable success or acceptance → not ready.

## Handoff

A bug or EPIC produced here is the **input** to `perps-breakdown-tickets`, which
(with codebase access) routes it across Core/Core-release/Mobile/Extension and
emits the engineering task tickets. Keep this skill on the product side of that
line.

## References (read installed, don't duplicate)

- `../../knowledge/screens.md` — screen/area names, if you want to use precise
  surface labels (optional; plain words are fine for a product ticket).
- `../../knowledge/formatting-rules.md` — number semantics, to describe expected
  values correctly without prescribing decimals.
- Related skills: `perps-breakdown-tickets` (engineering split + routing — the
  next pass), `recipe-fix-ticket` (implement a fix).
