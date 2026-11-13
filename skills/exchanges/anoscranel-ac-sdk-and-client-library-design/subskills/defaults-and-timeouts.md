---
name: defaults-and-timeouts
domain: software-engineering/defaults-and-timeouts
trigger: "Choosing the retry and timeout behaviour a client inherits silently."
anti_trigger: "Not for service-side resilience budgets, and not for load testing."
scope: "Retry and timeout defaults, and the danger of inheriting them silently."
status: seedling
---

# Defaults and timeouts

## Standard

A library's defaults are its most-used configuration, because most callers never change them. That makes a default a decision made on the caller's behalf, and an aggressive retry default chosen to improve reliability for one caller becomes an amplifier when ten thousand callers inherit it against a struggling service.

The safe defaults are modest and visible. A short timeout that the caller can extend, one retry at most, and no retry for non-idempotent operations are defensible; a five-retry policy with long backoff is not, because it makes the caller's request take longer than their own deadline allows. The documentation should state the defaults prominently, since a caller who does not know them cannot reason about their own latency.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9110> and <https://sre.google/>.

## Decision rules

- Record the default timeout and whether it exceeds a typical caller's own budget.
- Record the default retry count and which operations are retried.
- Record whether retries apply to non-idempotent requests, which they should not without a key.
- Record how a caller overrides each default and whether the override is per call or per client.
- Record the defaults' documentation location, since an undocumented default is an accident.
- Record the interaction between the client's timeout and any server-provided retry hint.

## Procedure

1. Record each default and its rationale.
2. Check the timeout against a typical caller budget.
3. Record retry count and the operations covered.
4. Record override granularity.
5. Record documentation placement.
6. Write the defaults with their trade-offs stated.

## Anti-patterns

- Retrying five times by default, which multiplies load without the caller's knowledge.
- Retrying a POST without an idempotency key.
- A timeout longer than most callers' own request deadlines.
- Overrides that require constructing a new client rather than a per-call option.
- Defaults that change in a minor version, which silently alters caller behaviour.

## Done checklist

- [ ] Defaults recorded with rationale.
- [ ] Timeout checked against caller budget.
- [ ] Retry count and scope recorded.
- [ ] Override granularity recorded.
- [ ] Documentation placement recorded.
- [ ] Server hint interaction recorded.

The default's visibility in logs matters as much as its value: a caller investigating slow requests needs the effective timeout and retry count recorded per request, and a library that applies defaults invisibly leaves the caller to discover them by reading source rather than output.


## Sources

- HTTP retry and idempotency semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- Reliability practice on retries: <https://sre.google/>
- Client behaviour context: <https://semver.org/>
