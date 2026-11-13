---
name: incident-log-and-postmortem
domain: crypto-trading/incident-log-and-postmortem
trigger: "Writing the record of a trading operations incident and the change that follows it."
anti_trigger: "Not for assigning blame, and not for strategy review."
scope: "The incident record: timeline, impact, cause, fix, and the runbook change that follows."
status: seedling
---

# Incident log and postmortem

## Standard

An incident that is not written down will recur, usually with a different name. The postmortem exists to convert a bad hour into a permanent procedure: a timeline that anyone can follow, an impact stated in numbers, a cause stated as a mechanism rather than a mood, and one or more concrete changes with owners and dates.

The culture matters more than the template. A blameless record is one where the person who took the action can describe it fully, because the aim is to find the missing guardrail, not the guilty party. A postmortem that ends with "be more careful" has produced nothing.

Primary sources: <https://sre.google/sre-book/postmortem-culture/> and <https://sre.google/sre-book/table-of-contents/>.

## Decision rules

- Every incident gets a written record within a stated window, even a small one; small incidents are the rehearsal for large ones.
- The timeline uses venue and system timestamps, not recollection.
- Impact is stated in numbers: notional affected, fees paid, positions changed, time out of the market.
- Causes are mechanisms ("the cancel was sent to the wrong endpoint"), never dispositions ("carelessness").
- Every postmortem produces at least one change, and each change has an owner and a date.
- Recurring incidents of the same signature escalate: the guardrail is missing, not the attention.

## Procedure

1. Open the record at detection time and append timestamps as events happen.
2. Close the record with impact, cause, and the changes decided.
3. Distinguish trigger (what happened first) from cause (why the system allowed it to matter).
4. Write changes as edits to the runbook or the automation, not as intentions.
5. Set a date to verify each change is in place.
6. File the record where the desk will find it at the next pre-flight.

## Anti-patterns

- Writing the postmortem from memory days later.
- Naming a person as the cause.
- Ending without a changed procedure.
- Recording impact qualitatively ("some loss") instead of numerically.
- Filing the record somewhere nobody looks.

## Done checklist

- [ ] Record opened at detection and appended contemporaneously.
- [ ] Timeline uses system timestamps.
- [ ] Impact quantified.
- [ ] Trigger and cause separated.
- [ ] At least one change recorded with owner and date.
- [ ] Record filed and reachable at pre-flight.

## Sources

- Blameless postmortem practice: <https://sre.google/sre-book/postmortem-culture/>
- Reliability engineering reference: <https://sre.google/sre-book/table-of-contents/>
- Venue incident communications as an input to the timeline: <https://www.bybit.com/en/help-center>
