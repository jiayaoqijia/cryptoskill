---
name: perps-breakdown-tickets
description: Interactively break a perps product requirement into split, dispatch-ready technical tickets across MetaMask Core, its release, Mobile, and Extension. Use when a product manager (or a codebase-aware Claude acting for one) has a perps bug or feature and needs engineering-grade tickets, correctly routed now that @metamask/perps-controller is the Core source of truth. Triages where the change actually lives, emits only the applicable layer tickets with dependency links, and enforces token-efficient, signal-over-noise tickets agents can act on directly.
maturity: experimental
---

# Breakdown Perps Tickets

Turn one perps product requirement into the **minimum set of technical tickets**,
each routed to the right layer and written for direct agent ingestion. You have
codebase access — use it to decide the split from the actual code, not guesswork.

## When To Use

- A PM (e.g. via a codebase-aware Claude) has a perps bug or feature and wants
  tickets engineering can dispatch as-is.
- A requirement may span Core logic and one or both clients, and you need it
  split correctly instead of filed as one vague ticket against one repo.

This is the **second pass**: the PM states *what's broken / expected* (no
implementation); this skill does the technical breakdown + routing. It converts
a bug or EPIC into engineering task tickets — it does not author initiatives/EPICs.

Not for: pure investigation/spikes (narrow to a concrete behavior first), or
non-perps work.

## Operating principle: signal over noise

The tickets you emit are consumed by autonomous agents. **Every word costs
inference and dilutes focus.** Write the minimum that lets an agent reproduce and
fix — no preamble, no restated context, no hedging.

- 2-3 sentences per field, max. Cut anything an agent can derive from the code.
- One concern per ticket. Split multi-bug / multi-layer requests.
- Concrete > narrative: a route, a component, a testable assertion — not a story.
- No screenshots-as-spec, no Figma links, no "investigate and fix", no "see recording".
- If you can't state the expected behavior in one testable line, the ticket isn't ready — ask.

## The layer model

`@metamask/perps-controller` lives in **Core**; Mobile and Extension consume it
(`"@metamask/perps-controller": "^9.x"`). A perps change can touch up to four
layers, in dependency order:

1. **Core** — change in `@metamask/perps-controller` (shared logic / source of truth).
2. **Core release** — bump + publish the package so clients can pull it. *Separate ticket; blocks the clients.*
3. **Mobile** — bump the dep + Mobile UI/integration work.
4. **Extension** — bump the dep + Extension UI/integration work.

Emit **only the layers that apply**. Most pure-UI bugs are client-only (no Core
chain). Anything touching shared business logic (pricing, order/position math,
stream transforms, validation, **analytics event constants**) is Core-first →
release → clients.

### Dependencies & validation gating

Chain the tickets with **Jira "blocks / is blocked by"** links — and the gate is
real, not cosmetic:

- Core **blocks** Core-release **blocks** each client ticket.
- A client ticket **cannot be validated or closed until the Core release is
  published AND the client has bumped `@metamask/perps-controller` to it.** Make
  that the client ticket's first acceptance line.
- Set the link on every emitted ticket (`is blocked by` → the upstream).

## Workflow (interactive)

0. **Confirm repos (once, up front).** Triage is done *from the code*, so you
   need the checkouts. Ask the user to confirm the local paths for the three
   repos before analyzing — don't assume; they differ per machine and reviewer
   checkouts often live at `*-ref` paths:
   - **Core** (`@metamask/perps-controller` at `packages/perps-controller`)
   - **Mobile**
   - **Extension**
   If any is missing, say which and proceed only against the ones you have
   (e.g. client-only triage without Core). Don't hardcode paths into tickets.

1. **Intake.** Read the requirement. Ask only the questions you can't answer from
   the code (expected behavior as a testable line, affected surface, required
   wallet state). Don't ask what the codebase already tells you.

2. **Triage the layer — from the code.** Decide where the root cause/change lives:
   - Shared logic (controller state, math, stream/data transforms, validation)
     → **Core** + release + affected clients.
   - Rendering/formatting/navigation specific to one app → that **client only**.
   - Use `knowledge/architecture.md` and `knowledge/mobile-extension-map.md` to
     confirm whether a screen/util exists on both clients or diverges. Mobile is
     source of truth for behavior.
   - **Watch for hidden Core dependencies.** A task can look client-only but
     need a shared capability that lives in Core — most commonly a **new
     analytics event/property** (source of truth: `@metamask/perps-controller`,
     `packages/perps-controller/src/constants/eventNames.ts` + the metametrics
     reference doc), but also new controller state, selectors, or shared
     types/constants. If the client must emit a value/type the published package
     doesn't expose yet, it's Core-first. Grep the package before calling it
     client-only.
   - State your routing decision and the evidence (file/package) in one line.

3. **Decide the split.** Map to the minimum ticket set:
   - Client-only bug → 1 client ticket (or 2 if both clients diverge from spec).
   - Shared-logic change → Core ticket → Core-release ticket → 1 ticket per
     affected client (each: dep bump + that client's UI/integration).
   - Don't create a layer ticket with no real work in it.

4. **Emit the tickets** in the format below, with explicit dependency links, and a
   one-line breakdown summary at top (what split you chose and why).

## Hidden Core dependencies & the interim-constant pattern

The classic trap: a single client task that secretly needs a Core change first —
most often **new analytics events**. Perps event constants are owned by
`@metamask/perps-controller` (`.../constants/eventNames.ts`) + the metametrics
doc; a client can't use a typed value the published package doesn't expose.

Two ways to sequence it — pick by urgency, and **state which you chose**:

- **Interim-constant decoupling (preferred when the client can't wait).** Client
  ships now with a *local interim constant* (marked TODO → the Core ticket), so
  delivery isn't blocked. Then Core adds + publishes the constant, and a client
  follow-up replaces the local copy with the typed value and removes the TODO.
  → **3 tickets** (client feature → core → client replace).
- **Strict gating.** Client is blocked until the Core release lands. Fewer
  tickets, slower delivery.

Real example — the shape to emit (TAT-3398 / TAT-3429 / TAT-3430):

- `[mobile] Enable RoE sign toggle on Auto Close TP/SL` — feature; ships an
  interim local `tpsl_roe_sign_toggled` constant with a TODO.
- `[core] Add tpsl_roe_sign_toggled + roe_sign to @metamask/perps-controller` —
  add to `eventNames.ts`, update the metametrics doc, **cut & publish**.
  *(folds the Core-release step in, or split it out as its own ticket.)*
- `[mobile][extension] Replace local tpsl_roe_sign_toggled constant with the
  typed value` — bump the dep, drop the local constant + TODO. **Blocked by** the
  Core ticket. AC: no bespoke string literal remains; analytics uses the typed
  constant.

## Ticket format (per layer, agent-ingestion)

Keep every field tight. Pull routes/components from `knowledge/screens.md` and
`knowledge/mobile-extension-map.md`; pull number rules from
`knowledge/formatting-rules.md` — don't restate them.

**Title** — `[core|core-release|mobile|extension] <one-line outcome>`

**What / change** — actual behavior (bug) or the capability to add (feature). 1-2 sentences.
**Expected (acceptance criteria)** — **numbered** testable "when X, then Y" lines; the
downstream agent turns these directly into its AC matrix + recipe. Tag each with a proof
mode so it knows how to verify: `[state]` (controller/store value), `[visual]` (rendered
UI), `[mixed]`. E.g. `AC1 [visual] When a Long position is open, the size shows its USD value.`
**Affected** — package/route/component (e.g. `@metamask/perps-controller` symbol, or `perps-order-entry-page`). Cite the real path.
**Pre-conditions** — required wallet/app state (unlocked, open BTC position, etc.). Only the ones that apply.
**Depends on** — upstream ticket(s) via Jira `is blocked by` (every client ticket is blocked by the Core-release; a "replace interim constant" ticket is blocked by the Core ticket).

Layer specifics:
- **Core**: name the controller behavior + the symbol/file. Acceptance = controller-level outcome (unit-testable).
- **Core release**: title `[core-release] bump @metamask/perps-controller → <target version>`; body = "publish containing <core ticket>; clients bump to it." Depends on the Core ticket.
- **Mobile / Extension**: first line = "bump `@metamask/perps-controller` to <version> (from <release ticket>)", then the client-side UI/integration work + acceptance. For number display, state the *semantic* ("shows USD value of position"), never "2 decimals" — precision is range-adaptive (see formatting-rules).

## Quality bar (reject before emitting)

- No steps / no affected component / no testable acceptance line → not ready; ask.
- A ticket that just says "investigate" → narrow it or drop it.
- Same fix needed on both clients but only one ticket → split.
- A Core change with no release + client tickets → incomplete chain.
- Verbose restated context the agent can read from code → cut it.

## References (read installed, don't duplicate)

- `knowledge/architecture.md` — where perps logic lives across Core/clients.
- `knowledge/mobile-extension-map.md` — screen/route/component parity + divergences.
- `knowledge/screens.md` — route/component names for the "Affected" field.
- `knowledge/formatting-rules.md` — perps number/precision rules for acceptance criteria.
- `knowledge/shared-package-analysis.md` — duplicated utilities to check both sides.
- Related skills: `recipe-fix-ticket` (implement a client fix), `perps-review-pr` (review the resulting PRs).
