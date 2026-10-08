---
name: re-screen-customers-on-list-update
description: Use when a sanctions or PEP list changes and the existing customer base must be re-screened against the delta, either on a schedule or immediately after a designation.
---

# Re-screen the customer base on a list change

Onboarding screens new customers; re-screening protects the ones already there. A designation is
retroactive to the relationship, so a changed list creates an obligation on a book of business
that a point-in-time check never touches.

## Procedure

1. Take the delta from the list refresh, not the whole list, and keep the row so the trigger is
   reproducible:

```
       diff <(sort prev.csv) <(sort sdn.csv) | grep '^>' | cut -d, -f1-2 > delta.csv
       wc -l delta.csv
```

2. Run the delta against the customer index within the internal SLA of the list landing. Whole-
   file re-screens are for the periodic cycle; delta screens are for timeliness.

3. Match on address for wallet-linked customers and on identity fields for others. For addresses,
   exact match only. For names, the identity fields from KYC are what disambiguate:

       python3 - <<'PY'
       import csv
       delta = {r[1].lower().lstrip("0x") for r in csv.reader(open("delta.csv")) if len(r) > 1}
       cust  = {r[0].lower().lstrip("0x"): r[1] for r in csv.reader(open("cust_addrs.csv"))}
       hits  = [(a, cust[a]) for a in delta & cust.keys()]
       print(hits or "no exact address hits")
       PY

4. Run the periodic full re-screen on its own cadence (commonly daily to monthly by risk tier)
   and record the coverage: how many customers were in scope, how many screened, how many
   skipped for missing data.

5. Route hits to the escalation queue as new alerts, not as updates to a closed case. A
   designation on an existing customer is a new event with its own clock.

6. Freeze or restrict per policy on a true match, and record who made the call and when.

## Pitfalls

- Screening only new signups and calling the programme current. Regulators test exactly this:
  whether the book, not just the funnel, is covered.
- Re-running the whole list nightly and reporting a huge alert count, which buries the one fresh
  designation in old false positives. Delta-first keeps the signal.
- Skipping customers whose stored identifier is a name only, which is the segment most likely to
  be missed and therefore the boundary you must report.
- Failing to record coverage numbers, so no one can tell whether the re-screen ran or ran
  partially.
- Closing a reopened case by editing it; version the case so the timeline of the list change and
  the decision is legible.

## Verification

    awk 'END{print NR-1" customers screened"}' cust_addrs.csv
    grep -c "^" delta.csv

Compare the delta row count to the alert count produced; a delta with rows and zero alerts means
the join key is wrong, not that nothing matched.

Report the delta size, in-scope and screened counts, skipped customers with the reason, and hits
raised. Determining what a hit obliges you to do is a compliance and legal decision for a
qualified officer.
