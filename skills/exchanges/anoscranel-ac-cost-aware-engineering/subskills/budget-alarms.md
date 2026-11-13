---
name: budget-alarms
domain: software-engineering/budget-alarms
trigger: "Setting a cost alarm that triggers an action rather than a notification."
anti_trigger: "Not for financial approval, and not for vendor negotiation."
scope: "Alarms that trigger an action rather than a notification."
status: seedling
---

# Budget alarms

## Standard

A budget alarm that sends an email is a notification, not a control. It arrives after the spend has occurred, in a channel that is read at some cadence, and its only effect is to inform someone who may not have the authority or the context to act. A control needs a threshold, an action, and an owner who can execute it.

The effective design connects the alarm to a mechanism. A cost anomaly can trigger a rate limit, a scaling cap, a queue drain, or an automatic rollback of the change correlated with the increase. Those actions cost something themselves — a rate limit has users, a rollback has a feature — so the record states the trade-off rather than the threshold alone.

Primary sources: <https://www.finops.org/> and <https://sre.google/>.

## Decision rules

- Record the threshold and whether it is absolute, per-unit, or rate-of-change.
- Record the action the alarm triggers, and that it is automatic.
- Record the owner and the escalation path.
- Record the false-positive rate and what a false positive costs.
- Record the manual override and who holds it.
- Record the correlated change detection, since cost anomalies usually follow a deploy.

## Procedure

1. Choose the threshold type and record the reasoning.
2. Connect the alarm to an automatic action.
3. Record the owner and escalation.
4. Measure the false-positive rate over a period.
5. Record the override and its holder.
6. Record the deploy correlation and how it is detected.

## Anti-patterns

- An alarm that only sends a message.
- An absolute threshold that is meaningless on the first of the month.
- An automatic action with no override, so a false positive becomes an outage.
- No correlation with deploys, so the cause is investigated from scratch.
- Setting the threshold without measuring the false-positive rate.

## Done checklist

- [ ] Threshold type recorded.
- [ ] Automatic action recorded.
- [ ] Owner and escalation recorded.
- [ ] False-positive rate measured.
- [ ] Override and holder recorded.
- [ ] Deploy correlation recorded.

The anomaly case is where automatic action earns its place: a spend rate that triples in an hour is almost always a deploy or a runaway loop rather than business growth, and a control that throttles or rolls back within minutes prevents a month's damage that a monthly review would only document afterwards.


## Sources

- FinOps anomaly management: <https://www.finops.org/>
- Reliability alerting practice: <https://sre.google/>
- Cloud native operations guidance: <https://www.cncf.io/>
