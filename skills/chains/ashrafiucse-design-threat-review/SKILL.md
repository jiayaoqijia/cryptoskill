---
name: design-threat-review
description: Threat-models a design BEFORE implementation — spec/PRD/data-model/route sketch in, THREAT-MODEL.md out with actor×asset inventory, data flows across trust boundaries, STRIDE sweep mapped to the repo's detection skills, per-persona abuse cases, and an audit contract (the actor×surface matrix + acceptance criteria) the future security-audit must disposition. Use when the user shares a design doc, spec, PRD, or architecture, or asks to threat-model a system before or during early build — before the code exists to audit.
license: MIT
---

# Design Threat Review

Security decisions are cheapest before code exists. This skill runs at design
time and produces the ONE artifact that `../security-audit/SKILL.md` Phase 0/2
consumes at audit time — a shared actor×surface matrix plus acceptance
criteria. Design → implementation → audit: one artifact, no seams.

## Ground rules

- Input is prose/diagrams as readily as code — absence of code is the point.
- Output is ONE file: `THREAT-MODEL.md` in the project root (the only file you create).
- Every threat gets a code-phase detector (sibling skill) AND an acceptance
  criterion. A threat with no detector becomes a design-protected control —
  never leave a threat with neither.

## Step 0 — Gather inputs

Read whatever exists: spec/PRD, ERD/data model, route sketches, integration
list, personas. If thin, ask or record assumptions:

- Which account types/roles exist? Who grants them?
- What does each role SUBMIT that another role OPENS? (moderation surfaces)
- Where does money/entitlement change hands? What artifact marks "paid"?
- What PII/secrets exist, and where do they flow — including logs, emails,
  support tools, third parties?
- What calls INTO the system (webhooks, SSO, imports, postbacks)?

## Step 1 — Assets & actors

- **ASSETS**: content/IP, money & entitlements, PII, credentials/secrets,
  admin power, availability.
- **ACTORS**: anonymous, authenticated user, staff/moderator,
  admin/tenant-admin, service/webhook caller, third-party integration.
- Build the actor×asset power matrix: each cell = the actor's legitimate
  power over that asset. Illegitimate power is exactly what Step 3/4 hunt.

## Step 2 — Data flows & trust boundaries

Sketch the flows (e.g. student submits review → stored → pending queue →
staff opens detail view → approve → public page). Mark EVERY trust-boundary
crossing: browser↔app, app↔db, app↔third-party, queue/worker, email render,
admin origin. Each crossing becomes a coverage-matrix cell. Content that
crosses a boundary UNPURIFIED and is opened by a HIGHER-privilege actor is
the highest-priority cell class (see `../laravel-security/SKILL.md` Step 4
privilege-direction table and `../course-platform-security/SKILL.md` §6.5).

## Step 3 — Threat sweep (STRIDE → repo detection skills)

For each flow element, sweep STRIDE; tag each credible threat with the
sibling skill that must catch it in code:

| STRIDE | Ask at each boundary | Detector skill |
|---|---|---|
| Spoofing | can a weaker actor pose as a stronger one at this boundary? | `../auth-review/SKILL.md` |
| Tampering | does content cross unpurified and get rendered? (stored→rendered) | `../injection-flaws/SKILL.md` + framework skill (e.g. laravel Step 4) |
| Repudiation | do money/state transitions leave tamper-evident traces? | `../flow-security/SKILL.md` |
| Info disclosure | does a boundary leak gated/PII data (catalog, preview, logs)? | `../data-exposure/SKILL.md`, `../course-platform-security/SKILL.md` |
| DoS | can one cheap request cause expensive work? | `../config-hardening/SKILL.md`, `../graphql-security/SKILL.md` |
| Elevation | does unprivileged input reach privileged surfaces? | `../auth-review/SKILL.md` + course skill §6.5 |

Domain lenses: course/e-learning → the course skill's three personas;
payments/subscriptions → flow-security state machines (what fulfills an
entitlement, what can replay).

## Step 4 — Abuse cases per persona

For each actor, write the attacker version: what do they WANT (free content,
another user's data, a staff session, a refund) and which cell do they
abuse? Defaults that must not be argued away:

- Unprivileged→privileged content flows (moderation) default to
  **severity-if-missed: Critical** — the approval workflow itself is the
  delivery mechanism (MISSES.md 2026-09-23: student review → staff detail
  view → admin ATO).
- Preview/free-tier flows default to Critical-if-full-content.

## Step 5 — Write THREAT-MODEL.md (the audit contract)

1. Actor×asset power matrix (Step 1) and flows+boundaries (Step 2).
2. Threat list — one section per threat, same shape as security-audit Phase 3
   findings so the scorer and future audits parse both the same way
   (`T-NNN` ids; the spec anchor is the citable `file:line` evidence):

   ```markdown
   ### T-01: <threat title> — <severity-if-missed>
   - **Actor → Asset:** student → admin power
   - **Surface:** moderation detail view
   - **Spec anchor:** spec.md:17-19
   - **Detector skill:** ../laravel-security/SKILL.md Step 4 (privilege direction) + ../course-platform-security/SKILL.md §6.5
   - **Acceptance criterion:** <the control implementation MUST show, stated as a checkable fact>
   ```

   The acceptance criterion is checkable — e.g. "review body passes through
   e() before any formatting in EVERY staff view — list AND detail — or is
   stored purified" — never "input is handled safely".
3. The pre-seeded actor×surface coverage matrix, all cells ⬜ — the exact
   artifact `../security-audit/SKILL.md` Phase 0 loads and Phase 2 (gate v2)
   forces to disposition.
4. Handoff notes: acceptance criteria are the implementation's security
   requirements; the first audit reads THREAT-MODEL.md, runs the detector
   skills, and disposition-checks every threat row and every matrix cell.

## Reporting

End with a 3-line verbal summary: highest severity-if-missed threat, the
single acceptance criterion most likely to be skipped in implementation,
and the detector skill that will catch it later if it is.
