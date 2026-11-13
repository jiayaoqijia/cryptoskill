---
name: retry-budgets
domain: software-engineering/retry-budgets
trigger: "Setting retry policy without amplifying an outage."
anti_trigger: "Not for a provider SDK's internal retries, and not for idempotency design."
scope: "Why retries amplify, and the budget that bounds them."
status: seedling
---

# Retry budgets

## Standard

A retry is a bet that the failure was transient, and the bet is usually right. It is also load: when a dependency degrades, every caller retries, and the dependency receives the original traffic plus the retries, which makes the degradation worse and produces more failures to retry. At sufficient scale a retry policy converts a partial degradation into a complete outage without any component behaving incorrectly.

The mechanism that bounds it is a budget rather than a per-call count. A retry budget allocates a ratio of retries to successful requests, so that retries can absorb a small failure rate but cannot multiply traffic when failures dominate. The budget is global to the client, not per request, which is what makes it respond to the aggregate state rather than to an individual failure.

Primary sources: <https://sre.google/> and <https://aws.amazon.com/builders-library/>.

## Decision rules

- Record the retry policy: which errors are retried, how many times, and with what delay.
- Record whether a retry budget exists and the ratio it permits.
- Record whether retries are counted against the deadline, since a retry after the deadline is pure waste.
- Record the idempotency of the operation, since a non-idempotent retry can duplicate a write.
- Record the amplification at the current failure rate, computed rather than assumed.
- Record the behaviour when the budget is exhausted: fail fast rather than retry.

## Procedure

1. Record the retryable error classes.
2. Record the count and delay per retry.
3. Compute the traffic amplification at a stated failure rate.
4. Introduce a budget with a ratio and record it.
5. Confirm retries respect the deadline.
6. Write the policy with the amplification arithmetic.

## Anti-patterns

- Retrying every error, including permanent ones.
- Three retries per request with no aggregate budget.
- Retrying a non-idempotent write without a key.
- Retrying after the deadline has expired.
- Assuming the dependency can absorb the retry load because it is "just a retry".

## Done checklist

- [ ] Retryable classes recorded.
- [ ] Count and delay recorded.
- [ ] Amplification computed.
- [ ] Budget and ratio recorded.
- [ ] Deadline interaction recorded.
- [ ] Idempotency recorded.

The budget's ratio also needs to reflect how the dependency fails: a service that fails fast returns capacity quickly and tolerates a higher retry ratio, while one that fails slowly holds connections and tolerates almost none. The same ratio applied to both is a ratio that is wrong for one of them.


## Sources

- Reliability guidance on retries: <https://sre.google/>
- Distributed systems patterns: <https://aws.amazon.com/builders-library/>
- Timeout and retry interaction: <https://sre.google/workbook/table-of-contents/>
