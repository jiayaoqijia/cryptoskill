---
name: watermarks
domain: software-engineering/watermarks
trigger: "Declaring event time complete without lying about the future."
anti_trigger: "Not for market data watermark pipelines, and not for framework choice."
scope: "Declaring event time complete, and the honesty of the declaration."
status: seedling
---

# Watermarks

## Standard

A watermark is the system's assertion about the past: no event older than this will arrive. It is what lets an event-time window close and emit its result, because without the assertion the window would wait forever for data that may never come. The assertion is a guess, and the design work is choosing how bold the guess is: a tight watermark closes windows quickly and discards more late truth; a generous one holds results longer and stays correct longer.

Two failure modes bracket the choice. A watermark too far ahead of reality closes windows early and permanently undercounts the result — the error is silent and looks like a working dashboard. A watermark too far behind delays results past their usefulness and grows state, because nothing can be discarded. The honest configuration states where the watermark comes from, what its lag distribution is, and what happens to events that arrive behind it.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- Record the watermark source: bounded out-of-orderness, percentile of observed lag, or idle-source handling.
- Record the measured lag distribution the bound is based on.
- Record what happens to events behind the watermark: update the result, side output, or discard.
- Record idle-source handling, because a silent partition stalls the watermark for everything.
- Record the worst-case correction a closed window can still make.
- Measure the result emitted before and after a forced late event.

## Procedure

1. Measure the actual out-of-orderness on real traffic.
2. Choose the watermark bound from that distribution, with the reason.
3. Define the late-event path.
4. Define idle-source behaviour.
5. Test with an event injected behind the watermark.
6. Record the observed lag and the correction behaviour.

## Anti-patterns

- The framework default bound, never measured against real lag.
- Watermark from the fastest source, stalling on the slowest.
- Events behind the watermark discarded silently, undercounting forever.
- No idle handling: a quiet night stops all windows from closing.
- A bound tightened at a moment of load, permanently discarding truth for speed.

## Done checklist

- [ ] Watermark source recorded.
- [ ] Lag distribution measured.
- [ ] Late-event path defined.
- [ ] Idle-source handling defined.
- [ ] Late-event test executed.
- [ ] Correction behaviour recorded.

A further honest check is to record the watermark's own stall history: a watermark that stops advancing during a partition outage silently closes nothing, and every downstream consumer interprets the resulting gap as zero activity rather than as unknown activity, which is the more dangerous reading of the two.

## Sources

- Watermark semantics: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Stream modeling patterns: <https://martinfowler.com/>
- Stream processing systems references: <https://dataintensive.net/>
