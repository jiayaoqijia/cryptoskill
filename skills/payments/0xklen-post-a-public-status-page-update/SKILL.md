---
name: post-a-public-status-page-update
description: Use when updating a public status page during an outage. Sets the component, status level, and next-update fields, and enforces the new-update-not-silent-edit rule so customers see a consistent record.
---

# Post a Public Status Page Update

The status page is the customer's ground truth. A vague component ("API"), a pinned "investigating" that never advances, or a silent edit all cost more trust than the outage itself.

## Procedure

1. Set the affected component as narrowly as the page allows — "Payments API", not "Platform" — so unaffected customers do not panic.
2. Pick the level from impact: `Investigating` -> `Identified` -> `Monitoring` -> `Resolved`. Advance it as facts land; never leave it at `Investigating` once you know the cause.
3. Write the body in customer terms: what they experience, whether data is safe, the workaround, and the next-update time in UTC.
4. Post a NEW timestamped update rather than editing the old one; customers who screenshotted or were emailed the prior text must see the diff.
5. Set the next-update time honestly and honour it; a status page that goes quiet reads as activity being hidden.
6. Post the `Resolved` entry with the end time and a plain cause, even a brief one — an outage that ends with no closing note leaves customers waiting for the other shoe.
7. Keep internal incident slugs and stack names out of the public body.
8. Mirror the entry into the internal incident channel so the two records agree.
9. If the impact scope widens or narrows, post a new entry that says so rather than quietly changing the component.

## Pitfalls

- Marking "Platform" degraded when one payment method failed, alarming everyone.
- Editing the previous update in place, so the page shows a single tidy message and no history.
- Marking `Resolved` before sustained baseline, then reopening ten minutes later.
- Copy-pasting the internal update, leaking service names and internal ticket ids to customers.
- Leaving the page at `Investigating` for hours after mitigation because no one owns the next status change.
- Diverging from the internal channel, so support tells customers one story and the page shows another.

## Verification

```
    grep -E '^(Investigating|Identified|Monitoring|Resolved) [0-9:]+ UTC' incident/public-status.log
    # passes when the component, status, and a next-update time exist for each entry and none is a silent edit
```

Related: keep the internal and public wording aligned by drafting with `draft-a-customer-facing-incident-message`.
