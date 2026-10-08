---
name: report-uncertainty-with-confidence-levels
description: Use when stating a result, estimate, or diagnosis that could be wrong. Attach an explicit basis token and confidence band, plus the evidence that would change it.
---

# Report uncertainty with confidence levels

Flat assertions hide the difference between "I ran the test this session" and "I think I recall it". This skill makes every non-trivial claim carry a basis token, a numbered band, and a falsifier.

## Procedure

1. Classify the claim's basis with exactly one token: `verified` (you ran a command now and read its output), `corroborated` (two independent sources agree), `inferred` (follows from verified facts but untested), or `assumed` (a working belief with no evidence).

2. Assign a numeric band tied to the token: 90-99 for verified, 70-89 for corroborated, 40-69 for inferred, below 40 for assumed. Never quote a decimal place you cannot justify from a measurement.

3. Name the single observation that would move the band down, in the same breath: "drops to 20% if `pytest -k token_duration` fails".

4. Put the band inline in the sentence, not in a footnote: "the cache expires after 60s (verified, 95%)".

5. For anything under 70%, state the concrete step that would raise it and its rough cost in minutes.

6. Keep a running log at `notes/confidence.md`, one line per claim: `token | band | basis | falsifier | date`. When a band changes, append the new line with the reason and date.

7. Never average bands across a chain. A sequence of inferred steps is only as strong as the weakest link, so log the minimum.

8. At report time, `grep -cE "\((verified|corroborated|inferred|assumed)" notes/confidence.md` and reconcile the count against the number of behavioural claims you make.

## Pitfalls

- "Probably" without a number lets the reader assume 95%; commit to the token and band.
- A high band for something you did not personally test is borrowed confidence, not yours.
- Below 70% means gather evidence, not just add a caveat and move on.
- Mixing units of confidence (0-1 and 0-100) in one report confuses the reader; pick one scale.
- A falsifier you cannot run is decoration; write one you could actually execute.

## Verification

    grep -cE "\((verified|corroborated|inferred|assumed)" notes/confidence.md

Report the count and any behavioural claim missing a basis token; fix before sending.
