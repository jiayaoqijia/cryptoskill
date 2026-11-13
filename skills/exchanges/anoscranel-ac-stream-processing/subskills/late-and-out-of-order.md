---
name: late-and-out-of-order
domain: software-engineering/late-and-out-of-order
trigger: "Deciding what happens to events that miss their window."
anti_trigger: "Not for framework configuration dumps, and not for retry policy."
scope: "Late-arrival policy, allowed lateness, and where discarded events go."
status: seedling
---

# Late and out of order

## Standard

Out-of-order and late are different conditions and get different treatment. Out-of-order events arrive behind the current watermark but within the lateness a window still permits — the result is a corrected emission, and the design only has to allow updates. Late events arrive after the window has closed and its state discarded — the design must decide where they go, and "away" is a decision that undercounts silently.

The policy has three honest parts. Allowed lateness is how long a closed window can still be corrected, which is state held open and a cost paid per window. The side output is where late events are routed when the window is beyond correction, so they can be counted, replayed, or inspected rather than vanishing. And the reconciliation path is the periodic job that tells everyone how many events took the side-output route, because a lateness policy without a measurement of its own consequences is a guess wearing a configuration file.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- Record allowed lateness per output and the state cost it implies.
- Record the side output every late event is routed to.
- Record the periodic count of side-output events, per source and per hour.
- Record what a corrected window does to its downstream: re-emit, upsert, or retract.
- Record the point at which an event is dropped entirely, and who is told.
- Test by injecting events at one, ten, and sixty minutes behind the watermark.

## Procedure

1. Choose allowed lateness from the measured lag distribution.
2. Define the side output for beyond-lateness events.
3. Add the reconciliation job that counts side-output volume.
4. Define the downstream behaviour on window correction.
5. Define the absolute-drop threshold and its notification.
6. Inject controlled late events at increasing delays and observe all three paths.

## Anti-patterns

- Allowed lateness set generously forever, paying state for correctness nobody verified.
- Late events dropped with no side output, so the undercount is invisible.
- Corrections emitted without retraction, so downstream sums double.
- No measurement of side-output volume over time.
- Lateness tightened during an incident, discarding truth to make a dashboard move.

## Done checklist

- [ ] Allowed lateness recorded with state cost.
- [ ] Side output defined.
- [ ] Side-output volume measured.
- [ ] Correction behaviour downstream defined.
- [ ] Drop threshold and notification recorded.
- [ ] Delayed-event test executed at three delays.

## Sources

- Lateness semantics: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Stream design patterns: <https://martinfowler.com/>
- Stream processing references: <https://dataintensive.net/>
