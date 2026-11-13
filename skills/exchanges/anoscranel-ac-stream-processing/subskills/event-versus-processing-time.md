---
name: event-versus-processing-time
domain: software-engineering/event-versus-processing-time
trigger: "Deciding which clock the answer must be correct in."
anti_trigger: "Not for recommending a framework, and not for pipeline plumbing."
scope: "Two clocks, their skew, and which one the answer must be correct in."
status: seedling
---

# Event versus processing time

## Standard

An event carries two times: when it happened, and when the system saw it. The gap between them is skew, and it is never zero and never constant — it is seconds for a well-behaved publisher, minutes for a busy consumer, and hours for a device that buffered while offline. Every aggregate over events is correct in one clock, and the choice must be explicit because the two clocks give different answers to the same question.

The questions make the choice visible. "How many orders were placed yesterday?" is an event-time question; answering it in processing time moves orders across midnight and miscounts both days. "How many events did we ingest per minute?" is a processing-time question about the pipeline itself. Consumer dashboards and operational metrics usually want processing time; anything a business signs or reports wants event time, and paying that cost is the design decision.

Primary sources: <https://nightlies.apache.org/flink/flink-docs-stable/> and <https://martinfowler.com/>.

## Decision rules

- State the clock each output is correct in, per output, with the reason.
- Record the expected skew distribution between the two clocks.
- Record what happens at skew spikes: buffering, window re-emission, or discard.
- Record that an event-time window can only close when its watermark advances.
- Record the timestamp source and trust it over the ingestion timestamp for event time.
- Never build a business aggregate over processing time because it is more convenient.

## Procedure

1. Classify each output as event-time or processing-time.
2. Measure the actual skew distribution on real traffic.
3. Choose per output and record the failure behaviour at skew spikes.
4. Record the timestamp field that carries the event time.
5. Test with deliberately delayed events.
6. Record, per output, the clock the number is true in.

## Anti-patterns

- Ingestion timestamps used silently as event timestamps.
- A daily report on processing time with a midnight that moves orders between days.
- Skew assumed constant because a quiet-hour measurement said so.
- No written choice: the clock is whatever the framework defaulted to.
- Event time chosen without accepting the wait that correctness requires.

## Done checklist

- [ ] Clock stated per output with reason.
- [ ] Skew distribution measured.
- [ ] Spike behaviour recorded.
- [ ] Timestamp source recorded.
- [ ] Delayed-event test executed.
- [ ] Clock recorded per output.

## Sources

- Time semantics in stream processing: <https://nightlies.apache.org/flink/flink-docs-stable/>
- Event streams and modeling: <https://martinfowler.com/>
- Stream processing literature hub: <https://dataintensive.net/>
