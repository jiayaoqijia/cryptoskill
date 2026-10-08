---
name: build-a-red-team-failure-taxonomy
description: Use when red-team findings are a loose pile of examples. Organises them into a taxonomy with severity and repro so they can be triaged and fixed.
---

# Build a Red-Team Failure Taxonomy

A red-team report that is a hundred anecdotes cannot be prioritised. Sort every finding into classes, attach severity and a minimal repro, and the fix order falls out.

## Procedure

1. Define the top-level classes before triage: instruction override, data exfiltration, unsafe content, policy evasion, tool misuse, hallucinated capability.
2. Give each class sub-types. Exfiltration sub-types: markdown image, link auto-render, encoded payload in a code block.
3. Score severity on two axes: impact (what a success gives the attacker) and exploitability (how few attempts it takes). High/High first.
4. Require a minimal repro per finding: exact input, model version, observed output. No repro, no ticket.
5. Deduplicate variants of the same root cause; ten phrasings of one bypass is one ticket with ten examples.
6. Record mitigation status (open, mitigated, accepted) and re-test after each model or guardrail change.
7. Roll the classes into counts so the report leads with "class X: 12/40 attempts succeed", not the scariest screenshot.

```markdown
## Exfiltration (severity: High, exploitability: Medium)
- sub: markdown image callback   (3 repros, open)
- sub: base64 in tool arg        (1 repro, mitigated by egress allowlist)
```

## Pitfalls

- Sorting by recency puts the last-found bug on top; sort by severity and exploitability.
- Marking "mitigated" without a re-test; the guardrail may only catch the sample.
- Burying a class with zero successes; that is a useful negative result, not an omission.
- Triage drifts without fixed class names; freeze them per campaign.
- Counting attempts, not successes, makes a weak attack look strong.

## Verification

    python3 triage.py findings.jsonl --by class --sort severity   # per-class success counts

Report: "40 attempts, 6 classes; exfiltration 12/40 succeed (High/High) is the only ship blocker; unsafe-content 0/40 noted as a held line."
