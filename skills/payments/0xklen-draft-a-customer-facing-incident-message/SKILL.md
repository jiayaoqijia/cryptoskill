---
name: draft-a-customer-facing-incident-message
description: Use when writing the customer-visible notice for an outage. Keeps to plain language, owns the impact, avoids speculation and internal jargon, and commits to the next update time.
---

# Draft a Customer-Facing Incident Message

Customers read the notice under stress and decide whether to trust you. Internal words ("the LB is flapping"), false precision, and blaming a vendor all cost trust you then spend weeks rebuilding.

## Procedure

1. Open with what customers experience, in their words: "You may be unable to complete checkout. Payments and logins are unaffected."
2. Say when it started and, if mitigated, that it is mitigated — do not leave them guessing whether to retry.
3. Give the workaround if one exists: "retry after 14:30 UTC; no data was lost."
4. Give the next update time as an absolute time with timezone, and honour it even with no news.
5. Ban internal jargon and unverified cause: no "latency in the payment-orchestration tier", and do not name a vendor until the cause is confirmed. Say "we are still confirming the cause."
6. Never blame a third party in a first notice; if a dependency failed, describe the effect, not the culprit.
7. Include the concrete scope: which regions, plans, and features. "Some customers in EU" invites everyone to assume it is them.
8. Keep the promise honest — if two hours of instability is possible, say so rather than a confidently wrong 15 minutes.
9. State data safety explicitly: "no customer data was lost or exposed" or an honest caveat, because that is the first thing customers worry about.
10. Read it once aloud substituting "I am a customer"; if a sentence needs a metric to make sense, cut it.

## Pitfalls

- Writing "intermittent elevated error rates" when the truth is "checkout is down", which reads as evasive.
- Promising a resolution time you cannot hold to look competent.
- Using the internal incident slug in the public notice, leaking product topology.
- Silent edits to the public status entry instead of a new timestamped update, so customers who screenshotted the old text feel gaslit.
- Naming a root cause the review later contradicts, forcing an awkward retraction.
- Writing in the third person ("the service is experiencing issues") so nobody owns the problem.

## Verification

```
    grep -Ei 'you may|is unaffected|next update|workaround|data' incident/public/*.md
    # passes when the notice states the customer-visible impact, scope, next-update time, and an honest cause status
```

Related: back the message's impact claim with `quantify-incident-customer-impact` before it ships.
