---
name: output-screening
domain: software-engineering/output-screening
trigger: "Checking what an agent emits before a user or a system receives it."
anti_trigger: "Not for content-adjudication policy, and not for injection analysis."
scope: "Checking agent emission before a user or a downstream system receives it."
status: seedling
---

# Output screening

## Standard

The emission bus screens what the agent sends, not what it meant. The screens differ by destination: what is acceptable into a sandbox (raw exploratory output) differs from what is acceptable into a user's chat (personal data, abusive language, fabricated citations) which differs again from what is acceptable into a shell command or a database write (injection-shaped strings, control characters, quoted-metacharacter exploits). The screen set is a property of the destination, written per destination class, not a single global filter.

Screen results are tri-state: pass, hold-for-review, block. The middle state is the honest one for a probabilistic screen — the classifier cannot be certain, and converting every uncertain verdict into either a pass or a block is a strictness-tuning decision that should be made consciously, per destination, and recorded in the record. A screen's false-positive rate and false-negative rate are both estimated from a labelled sample before the screen is trusted with enforcement, and both are recorded.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://en.wikipedia.org/wiki/Precision_and_recall>.

## Decision rules

- Screen per destination class, not globally; write per-destination screen sets.
- Tri-state results everywhere; where to route a holds is a stated, conscious decision.
- Parseable destinations (shell, SQL, JSON, browser) get deterministic structural screens; free-text destinations get probabilistic screens.
- Estimate FP/FN from a labelled sample before the screen enforces; record both.
- Every blocked or held emission is retained with the verdict and the reason.
- Screen for instruction-shaped text in agent output that will reach another agent — cross-agent spoofing is a destination class of its own.

## Procedure

1. Enumerate destinations: user chat, shell, database, other agents, external APIs.
2. For each destination, define the screen set and its block/hold/pass rule.
3. Build the labelled sample; estimate FP/FN per screen.
4. Wire screens into the emission bus as enforcing checks.
5. Record every firing with input, verdict, and outcome.
6. Review firing rates monthly; retune thresholds as a recorded decision.

## Anti-patterns

- One global content filter for every destination.
- Probabilistic screens on parseable destinations where a parser screen would be deterministic.
- Treating screens as optional logging when the bus can enforce.
- Unreviewed permanent silence — every screen with zero firings over a period is audited for a wiring defect.
- No holds: everything either passed or blocked, with no review queue.

## Done checklist

- [ ] Destinations enumerated with their screen sets.
- [ ] Block/hold/pass routing decided per destination.
- [ ] FP/FN estimated and recorded per screen.
- [ ] Screens wired into the emission bus as enforcing.
- [ ] Firings retained with reasons.
- [ ] Regular review of firing rates.

## Sources

- OWASP LLM Top 10, output-handling framings: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Precision and recall for screen evaluation: <https://en.wikipedia.org/wiki/Precision_and_recall>
- Related screen design in content moderation: <https://casp-uk.net/casp-tools-checklists/>
