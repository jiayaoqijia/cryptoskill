---
name: verify-a-third-partys-claim
description: Use when another agent, tool, or person reports a result you are about to depend on. Reproduce the smallest distinguishing check yourself before building on it.
---

# Verify a third party's claim

Trust transfers risk to you. This skill converts "they said it works" into a check you ran yourself, scaled to how much the rest of your work will rest on that claim.

## Procedure

1. Extract the testable core: what, where, and what value. "Migration applied" is untestable; "table users has column mfa_secret" is testable.

2. Write the cheapest command that distinguishes true from false: `psql -c "\d users" | grep -c mfa_secret`.

3. Confirm you are testing the same target the claim refers to — same host, branch, and commit. Check identity with `git rev-parse HEAD` or `hostname`.

4. Run the check and paste the raw output. On a match, mark the claim `reproduced`; on a mismatch, mark it `discrepancy` and name both values.

5. For high-stakes dependencies (irreversible, costly, or cascading), require two independent confirmations from different sources — not the same claim restated.

6. Read the raw output yourself rather than trusting a wrapper's exit code; a 0 from a script can hide a failed inner call.

7. Only after `reproduced` do you build on the claim. On `discrepancy`, report it upstream with your command and output, and pause dependent work.

## Pitfalls

- Checking a different environment than the claim's proves nothing about the claim.
- "It's in the logs" is not verification; grep the specific line yourself and quote it.
- A plausible-looking result can be coincidence; check the exact field, not a general "it works".
- A cached or replicated read can hide a recent change; query the primary when it matters.
- Two people repeating the same unverified claim is still one piece of evidence, not two.

## Verification

    psql -c "\d users" | grep -c mfa_secret   # expect 1; 0 means the claim is false on this target

Report the command and its output, and label the claim reproduced or discrepant, never assumed.
