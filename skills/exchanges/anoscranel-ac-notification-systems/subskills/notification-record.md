---
name: notification-record
domain: software-engineering/notification-record
trigger: "Writing the record of notification routing policy and outcomes."
anti_trigger: "Not for campaign analytics, and not for the templates themselves."
scope: "The written record of routing, policies, and outcomes."
status: seedling
---

# Notification record

## Standard

The notification record ties the system together for the person who inherits it: the channel policy table in force with its exceptions, the preference and quiet-hours model as shipped, the batching windows per category, per-channel delivery outcomes over time, and the mute and disable rates that measure whether attention is being respected. Each artefact carries its version and date, because every one of them drifts — templates change, policies get overridden, channels get deprecated — and the record is what turns that drift into changes a reviewer can see.

The outcome half of the record is read at two moments. In design review, the outcome history answers: has this category earned the interruption budget it asks for? In incident review, it answers: what did the user actually receive, on which channels, in the minutes that mattered? Without the record, both questions are reconstructed from vendor dashboards and memory, which is exactly where the disagreement about whose fault the 3am SMS was usually lands.

Primary sources: <https://developer.apple.com/documentation/usernotifications> and <https://firebase.google.com/docs/cloud-messaging>.

## Decision rules

- Record the channel policy table, the exception list, and their review dates.
- Record the preference model as shipped: per-category controls, quiet-hours policy, timezone handling.
- Record batching and digest windows per event class with their rationale.
- Record per-category, per-channel outcome metrics: delivered, opened, muted — with dates and any discussion of trend.
- Record mute and disable rates as first-class attention metrics, with the same weight as delivery.
- Every template overhaul or policy exception gets a dated entry; the record is the audit trail of what the system interrupts users with and why.

## Procedure

1. Assemble the policy table, preference model, and batching windows as sections with versions.
2. Wire outcome metrics per category and channel into the record on a cadence, not on incident.
3. Add a dated entry for every template, policy, or exception change.
4. Read the attention metrics in design review: a category requesting more interruptions must show respect for the current budget.
5. Read the routing snapshot in incident review: which channels, which categories, which times — from the record and not from memory.
6. Version the whole record; a change to it is a change to the system's contract with the user.

## Anti-patterns

- A policy table that exists only in the routing code, unreadable without a debugger.
- Delivery metrics kept in the vendor dashboard where nobody but the incident responder ever looks.
- Template changes shipped without a dated record entry, so wording regressions cannot be traced.
- Quiet-hours overrides granted verbally in an incident and never written down.
- Mute-rate improvements counted as a win without asking whether the category still merits sending.

## Done checklist

- [ ] Policy, preferences, and batching sections with versions.
- [ ] Outcome metrics wired on a cadence.
- [ ] Dated entries for all changes.
- [ ] Attention metrics read in design review.
- [ ] Routing snapshot read in incident review.
- [ ] Record versioned as the system contract.

## Sources

- Apple notifications overview: <https://developer.apple.com/documentation/usernotifications>
- FCM delivery metrics: <https://firebase.google.com/docs/cloud-messaging>
- Web push lifecycle: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
