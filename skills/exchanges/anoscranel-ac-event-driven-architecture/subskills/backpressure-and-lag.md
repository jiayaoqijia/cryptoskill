---
name: backpressure-and-lag
domain: software-engineering/backpressure-and-lag
trigger: "Handling a consumer that cannot keep up with its producer."
anti_trigger: "Not for capacity planning of the broker, and not for rate limiting an API."
scope: "Consumer lag, flow control, and the failure a slow consumer creates."
status: seedling
---

# Backpressure and lag

## Standard

A queue absorbs a difference between production and consumption rates for as long as its retention allows, and then it stops absorbing. Until that point the lag is invisible to the producer, which is why a consumer that degrades slowly becomes a growing lag rather than an alert, and why the lag metric matters more than the consumer's error rate.

Backpressure is the mechanism that makes the imbalance visible to the producer. Without it, the producer continues at full rate while the consumer falls further behind, and the eventual recovery is either a large backlog processing or a retention expiry that silently drops messages. The record states the lag threshold that triggers action, what action it triggers, and what happens when retention is exceeded.

Primary sources: <https://www.cncf.io/> and <https://martinfowler.com/>.

## Decision rules

- Record the current lag and its trend, per partition rather than in aggregate.
- Record the retention period and the time to expiry at the current lag growth rate.
- Record the alert threshold and the action it triggers.
- Record whether the producer can be slowed, and the mechanism if so.
- Record the consumer's scaling behaviour and its limit.
- Record what happens to messages when retention expires, since silent loss is the worst outcome.

## Procedure

1. Record lag per partition and its growth rate.
2. Compute time to retention expiry at that rate.
3. Record the alert threshold and the runbook action.
4. Record the producer's flow control capability.
5. Record consumer scaling and its ceiling.
6. Record the retention-expiry behaviour and its observability.

## Anti-patterns

- Monitoring aggregate lag, which hides a single stuck partition.
- Alerting on lag without a stated action.
- Scaling consumers beyond the partition count and expecting more throughput.
- Assuming retention is long enough to absorb an incident.
- Letting retention expiry drop messages without recording the loss.

## Done checklist

- [ ] Lag recorded per partition with trend.
- [ ] Time to expiry computed.
- [ ] Alert threshold and action recorded.
- [ ] Producer flow control recorded.
- [ ] Consumer scaling limit recorded.
- [ ] Expiry behaviour recorded.

The retention-expiry case deserves explicit instrumentation rather than an assumption: a broker metric that counts expired messages is the only evidence that loss occurred, and a design that relies on lag alerts alone will record an incident as a slowdown when it was also a data loss. Watching both turns the ambiguity into a fact.


## Sources

- Streaming and messaging operations: <https://www.cncf.io/>
- Distributed systems practice: <https://martinfowler.com/>
- Reliability and SLO guidance: <https://sre.google/>
