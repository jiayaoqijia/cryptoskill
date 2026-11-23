# Authoring Workflow — idea + scheme + experiments → venue-style paper

This is the operational runbook for the scenario the skill exists for: **given an idea, a scheme body (construction + security), and experiment evidence, produce a paper that meets a named venue's style and quality.** The venue skills (`crypto-venue-paper-writing`, `ccs-writing-style`, `usenixsec-writing-style`) own the numeric thresholds and the instruments; this file only orders the work and says when to run them. **Do not restate a venue threshold here** — the owning skill is the single source; cite it.

## Entry gate — do not draft without these

| Input | Minimum content | If missing |
|---|---|---|
| Idea card | problem, closest work, claimed delta, one falsifiable research question | return a research plan/outline with evidence slots — never a result-bearing draft (skill failure mode) |
| Scheme spec | construction definition, interfaces, security claims with status (proved / conditional / open) | construction and security sections become outlines with `[OPEN]` markers |
| Experiment evidence | claim→command→output ledger, parameters, artifacts, negative results | experiments and parameters sections stay symbolic; no numeric claims |
| Venue decision | one named venue family + current official call fetched and dated | produce a venue-neutral draft; block format/budget claims |

## Step 1 — Freeze the venue family

Choose exactly one family and load its skill; it owns the thresholds, the register, and the instrument:

- **crypto/LNCS** (CRYPTO, EUROCRYPT, ASIACRYPT, LNCS-style) → `crypto-venue-paper-writing`; instrument `count_venue_gates.py`.
- **security four venues** (ACM CCS, IEEE S&P, NDSS) → `ccs-writing-style`; instrument `count_prose_gates.py` (shared gates live in its `references/compression-and-expansion-gates.md`).
- **USENIX Security** → `usenixsec-writing-style`; its four venue-specific slots apply on top of the family gates.

Fetch the current official call for papers (page limit, template, anonymity, ethics/AI/artifact policy) and record **date + URL + snapshot**. A remembered page limit is not a budget.

## Step 2 — Freeze the claim-evidence ledger

Use `references/protocol.md`. Every contribution sentence gets one row: claim ID, exact claim, type (functionality / correctness / security / complexity / empirical / artifact), evidence location, status (`verified` / `provisional` / `open`), allowed wording (`proves` / `claims` / `supports` / `not verified`), limitation. A claim that cannot be filled gets `[OPEN]` and is banned from the abstract as an unqualified result.

## Step 3 — Skeleton with targets (per family)

Build the outline before prose: abstract (write last), 2–5 contributions, technical overview, preliminaries, construction, security, parameters and comparison, implementation and experiments, related work, open problems/limitations, conclusion, appendices. For each section record **its target from the owning skill** (crypto family examples: abstract cap and build share, contributions block/item caps, overview floors and constituents, construction constituents and mass ratio, numeric placement) — copy the numbers from the owning skill at drafting time, never from memory.

## Step 4 — Draft in dependency order

Order matters: later sections constrain earlier prose.

1. **Construction** — formal object, labelled parameter list, correctness claim, step ordering, complexity statement (the venue skill's construction constituents). Every added sentence must restate material already in the scheme spec or an artifact — never a new claim.
2. **Security** — theorem statements with hypotheses, proof status, reduction losses, adversary/setup model; keep proof sketches vs full proofs labeled; move full proofs to appendices when the venue allows supplemental material.
3. **Experiments and parameters** — reproduce from the experiment ledger; concrete values live in the parameters/evaluation region with provenance (the venue skill's numeric-placement rule); theory sections stay symbolic.
4. **Related work** — closest-work comparison at claim level, bounded novelty wording.
5. **Introduction** — problem → barrier → insight → results → evidence; the technical overview hits its constituents and pointer.
6. **Abstract and contributions — last**, summarized from the finished body, then gated (Step 5). Writing the abstract first is how the "correct length, wrong allocation" defect enters.

## Step 5 — Instrument loop (the quality gate)

After each artifact (and before the next), run the family instrument with a **named region map** (abstract, contributions, overview, introduction, related, sections; for the crypto family also `--overview-span` and `--notation`):

```bash
# crypto family
python3 ~/.dsh/skills/crypto-venue-paper-writing/scripts/count_venue_gates.py \
  --manuscript <main.tex> --twin tex --regions regions.json \
  --overview-span A-B --notation A-B

# security family
python3 ~/.dsh/skills/ccs-writing-style/scripts/count_prose_gates.py \
  abstract-contributions <main.tex> --abstract-heading Abstract --contributions-heading "Our contributions"
```

Rules: **measured, no breach** is the exit condition; a `degenerate`/`unmatched` gate is a finding, not a pass; every breach is either repaired (move material, never delete a claim/status/number) or recorded as a human decision with its reason. Re-run after each repair until the gate list is clean or every remaining item is documented. Keep the exit code honest: the instruments' exit codes separate measured-clean (0) from unmatchable (2) and breach (3).

## Step 6 — Review loop

Run `crypto-paper-review` (venue-level critique), plus `zkp-security-review` for ZKP/SNARK claims and `crypto-theorem-review` for theorem/proof obligations. Repair findings, then re-run Step 5. Do not let a review finding close without either a repair or a recorded limitation.

## Step 7 — Freeze and hand off

- Twin parity (markdown/tex) or a recorded decision to decouple them.
- Content-anchored region map (line numbers are non-binding hints) and the allowlist/gate state.
- Double-blind strings and the AI-disclosure sentence per the fetched call; page budget still requires a compile on a machine with the venue template (**human step** when no LaTeX toolchain exists).
- Promotion checklist: submission guide, integration report, package hashes, README.

## Worked example (EVH-MLPC, crypto/LNCS family)

Idea A-04 → scheme spec (EVH-MLPC construction + conditional theorems) → paper-exp experiment ledger → draft → instrument loop. The loop's first pass found two real defects the author had missed: a 153-word contribution block (cap 146) and a 0.5346 largest-child share (cap 0.50). Repairs: relocate the lead sentence into the adjacent paragraph (135 words), split the over-thick subsection into two siblings (0.3512). Second pass: 0 breach; `check_revision.py` PASS; `theory-region` gate 0 unjustified literals. See `research-work/paper/skills-usability-eval/REPORT.md` and `.../skill-gates/PAPER-FIXES.md` in the workspace for the full record.

## Honesty rules (inherited)

Never fabricate results, citations, parameters, measurements, or review outcomes. A threshold that cannot be traced to the owning skill's corpus anchor is not a threshold — write the rule qualitatively or leave it out. An idea without evidence gets a plan, not a paper. A venue rule is asserted only from a dated snapshot.
