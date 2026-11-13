---
name: dependency-failure
domain: software-engineering/dependency-failure
trigger: "Testing what happens when a dependency slows or stops."
anti_trigger: "Not for security testing, and not for vendor selection."
scope: "Partial degradation when a dependency slows or stops."
status: seedling
---

# Dependency failure

## Standard

A dependency that fails cleanly is the easy case: the call errors, the caller handles it, and the user sees a degraded page. The hard case is a dependency that slows without failing, because the caller's threads, connections, or queue slots fill while waiting, and the caller fails for reasons that have nothing to do with the dependency's own errors.

That slow-failure mode is what makes timeout and circuit-breaker design a system property rather than a library setting. The timeout must be shorter than the caller's own budget, the breaker must open before the caller's resources are exhausted, and the degradation must be a designed state rather than an exception propagating upward. The record states the budgets at each layer and how a slow dependency is contained.

Primary sources: <https://sre.google/> and <https://www.cncf.io/>.

## Decision rules

- Record the dependency's timeout at the caller and the caller's own latency budget.
- Record the retry policy and whether retries amplify load during the failure.
- Record the circuit-breaker threshold and its half-open behaviour.
- Record the bulkhead: how many resources the dependency can consume before others are affected.
- Record the degraded behaviour the user sees when the dependency is unavailable.
- Record the test that simulates slowness rather than failure.

## Procedure

1. Record the latency budget at each layer.
2. Set the timeout below the caller's budget and record the margin.
3. Record the retry policy and its amplification risk.
4. Record the breaker threshold and recovery behaviour.
5. Record the bulkhead limits.
6. Test with injected latency, not only injected errors.

## Anti-patterns

- Testing only the error case and never the slow case.
- Retries without jitter, which synchronise the retry storm.
- A timeout equal to the caller's budget, leaving no time to respond.
- A circuit breaker that opens after the caller's pool is exhausted.
- No designed degraded state, so the failure surfaces as an exception.

## Done checklist

- [ ] Latency budgets recorded per layer.
- [ ] Timeout and margin recorded.
- [ ] Retry policy and amplification recorded.
- [ ] Breaker threshold and recovery recorded.
- [ ] Bulkhead limits recorded.
- [ ] Slowness tested, not only errors.

The test that matters most is the one nobody runs: injecting latency at exactly the timeout boundary, where some requests succeed and others fail, produces the partial-failure state that reveals whether the caller's degradation is graceful or whether half its threads are waiting on a dependency that is only slightly slow.


## Sources

- Reliability engineering guidance: <https://sre.google/>
- Cloud native resilience practice: <https://www.cncf.io/>
- Distributed systems reference: <https://martinfowler.com/>
