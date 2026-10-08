---
name: correct-for-survivorship-bias
description: Use when analysis only includes entities that still exist. Rebuilds the sample with failures and dropouts before drawing conclusions.
---

# Correct for Survivorship Bias

Datasets built from what still exists exclude what failed, and that exclusion is not random. Every conclusion about performance, quality, or retention has to survive adding back the dead and the departed.

## Procedure

1. Ask what had to happen for a row to be present: did the entity survive, keep paying, stay listed, or answer the survey?
2. Find the survival filter in the pipeline — a JOIN to a current table, a `status='active'` predicate, or a partner API that returns only live accounts.
3. Reconstruct the full universe. Keep churned users with their churn date; for delisted funds or dead tokens, source historical listings externally (exchange archives, dated snapshots).
4. Add the dropouts and recompute. If a headline reverses, the original was a survivorship artefact:
   ```sql
   -- include accounts closed before today, with their closing date
   SELECT account_id, opened_at, closed_at, realized_pnl
   FROM accounts        -- no WHERE status='active'
   WHERE opened_at <= '2026-01-01';
   ```
5. For survey or review data, compare the respondent profile to the eligible population; differences in the tail are the bias.
6. For backtests, include the assets that went to zero and the funds that shut — a universe of today's largest names is a look-ahead filter.
7. State coverage explicitly: "n=1,204 of an estimated 1,880 eligible (64% observed)".

## Pitfalls

- A vendor API returning only currently-listed symbols silently drops every delisting.
- A "current customers" cohort for churn analysis cannot see people who already left — retention is overstated.
- Fund databases that list only survivors overstate average returns by the failed-fund drag.
- Snapshot tables overwritten nightly lose the rows that later disappeared; keep dated snapshots.
- Adding back failures narrows the gap but rarely closes it, because failure records are thinner.

## Verification

    psql "$DSN" -c "SELECT (SELECT count(*) FROM accounts) observed, (SELECT count(*) FROM account_openings) eligible;"
    # coverage number must be reported alongside the corrected estimate

Report: "Rebuilt the sample with 212 closed accounts added (observed 1,204 of 1,880 eligible, 64%); median return fell from 7.1% to 4.3% — the earlier figure was survivorship."
