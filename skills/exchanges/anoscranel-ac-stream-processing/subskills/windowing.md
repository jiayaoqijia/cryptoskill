---
name: windowing
domain: software-engineering/windowing
trigger: "Grouping unbounded events into bounded questions."
anti_trigger: "Not for recommending a framework, and not for UI windows."
scope: "Tumbling, sliding, session, and global windows, and what each answers."
status: seedling
---

# Windowing

## Standard

A window is the cut that turns an unbounded stream into bounded groups a computation can finish. The types answer different questions, and the match is the design work. Tumbling windows are fixed, non-overlapping buckets — five-minute counts that neither overlap nor gap, for a periodic answer. Sliding windows move continuously and overlap — a rolling average over the last ten minutes, updated as the window slides. Session windows group events by gaps in activity — a user's burst of clicks ends when they stop for thirty minutes, which is the shape that matches a human behaviour rather than a clock.

Session windows are the most useful and the most expensive: their boundaries depend on the data, so state cannot be pre-allocated, and a session can stay open indefinitely while the system waits to see whether the gap is a pause or an end. Global windows have no end at all and are correct only with a custom trigger — they exist mostly as a warning that a computation without a cut cannot produce a result.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- Record the question each output answers, and match it to a window type.
- Record the window size and slide, and the reason for both.
- Record the trigger that emits: window close, count threshold, or custom.
- Record the alignment: does the tumbling window align to the wall clock or the stream start.
- For sessions, record the gap threshold and the maximum session length.
- Record the state cost per window type and the expected concurrent window count.

## Procedure

1. Write the question each output answers.
2. Choose the window type per output.
3. Fix size, slide, and alignment.
4. For sessions, fix the gap and the maximum length.
5. Estimate the concurrent window state.
6. Test boundary events: the event that arrives exactly at the edge.

## Anti-patterns

- Sliding windows chosen for a question that is actually periodic.
- Sessions without a maximum length, holding state for an idle user forever.
- Window edges assumed inclusive on both ends, double-counting edge events.
- Alignment left to the default, so "hourly" means hourly from job start.
- A global window with no trigger, a computation that never emits.

## Done checklist

- [ ] Window type matched to question.
- [ ] Size and slide recorded.
- [ ] Trigger recorded.
- [ ] Alignment recorded.
- [ ] Session gap and maximum recorded.
- [ ] Boundary events tested.

## Sources

- Windowing semantics: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Stream modeling: <https://martinfowler.com/>
- Stream processing references: <https://dataintensive.net/>
