---
name: streaming-joins
domain: software-engineering/streaming-joins
trigger: "Joining two unbounded inputs without waiting forever."
anti_trigger: "Not for batch joins and star schemas, and not for framework choice."
scope: "Joining unbounded inputs, and the state each join type requires."
status: seedling
---

# Streaming joins

## Standard

A batch join waits for both sides to be complete. A stream join cannot: both inputs are unbounded, so the join must decide when to stop waiting for the match that may still arrive. The design question is the retention interval — how long each side's record is held in state before the join gives up — and it is the same watermark arithmetic that governs windows, applied twice.

Each join shape has its own state cost. A windowed join holds both sides for a window; an interval join holds one side for a time range around the other; an outer join must additionally remember that it emitted, so the later match can retract the null. The table lookup join inverts the problem — one side flows, the other is a slowly changing table held whole in state — and its cost is the table's size, refreshed on its own cadence.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- Record the join type and which side drives the retention interval.
- Record the retention per side, from the measured skew between the two streams.
- Record the state cost as the worst-case retention times arrival rate.
- Record what an unmatched record does: emit null, drop, or count.
- For a table join, record the table's size, refresh cadence, and the version seen during refresh.
- Test with the slow side delayed by more than the retention.

## Procedure

1. Choose the join type per output.
2. Measure inter-stream skew and set retention from it.
3. Compute worst-case retained state.
4. Define unmatched-record behaviour.
5. For table joins, record size, cadence, and refresh visibility.
6. Inject a delay past the retention and observe the unmatched path.

## Anti-patterns

- Retention guessed rather than derived from measured inter-stream skew.
- An outer join that emits nulls and never retracts when the match arrives later.
- A table join refreshing the whole table mid-stream, briefly joining against an empty side.
- Unbounded retention "to be safe", holding both sides indefinitely.
- Unmatched records vanishing with no count of how many did.

## Done checklist

- [ ] Join type recorded.
- [ ] Retention derived from measured skew.
- [ ] Worst-case state computed.
- [ ] Unmatched behaviour defined.
- [ ] Table refresh behaviour recorded.
- [ ] Over-retention delay tested.

## Sources

- Stream join semantics: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Stream data patterns: <https://martinfowler.com/>
- Stream processing references: <https://dataintensive.net/>
