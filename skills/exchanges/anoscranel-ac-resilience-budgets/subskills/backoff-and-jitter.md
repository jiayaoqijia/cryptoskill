---
name: backoff-and-jitter
domain: software-engineering/backoff-and-jitter
trigger: "Choosing a backoff curve and the jitter that stops synchronisation."
anti_trigger: "Not for rate-limit negotiation, and not for queue scheduling."
scope: "Exponential backoff, jitter, and the synchronisation it prevents."
status: seedling
---

# Backoff and jitter

## Standard

Backoff spaces retries so that a recovering dependency is not immediately hit again. Exponential backoff increases the delay on each attempt, which gives the dependency time to recover, and it is the default because it is simple and it works when the failures are independent.

Jitter is what makes it work at scale. Without jitter, every client that failed at the same moment retries at the same moment, so the dependency receives a synchronised pulse instead of a smooth flow, and the pulse can be more damaging than the original traffic. Adding randomness to the delay spreads the retries, and the choice of jitter strategy — full, equal, or decorrelated — determines how well it spreads them.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://sre.google/>.

## Decision rules

- Record the backoff curve: base delay, multiplier, and maximum delay.
- Record the jitter strategy and the range it applies.
- Record the maximum retry count and whether it interacts with the deadline.
- Record the total worst-case delay, computed rather than assumed.
- Record whether the curve applies to client retries and to internal queue redelivery separately.
- Record the behaviour of the first retry, since a long initial delay is often worse than a short one.

## Procedure

1. Record the base delay and multiplier.
2. Record the maximum delay and the retry cap.
3. Choose a jitter strategy and record the range.
4. Compute the worst-case total delay.
5. Record the first-retry delay, which is the most user-visible.
6. Write the policy with the distribution stated.

## Anti-patterns

- Exponential backoff with no jitter, which synchronises clients.
- Jitter applied to the multiplier rather than the delay, which produces an inconsistent curve.
- A first retry delay so long that the user has already given up.
- A maximum delay that exceeds the request deadline.
- Applying the same curve to queue redelivery and to client retries.

## Done checklist

- [ ] Curve parameters recorded.
- [ ] Jitter strategy recorded.
- [ ] Retry cap recorded.
- [ ] Worst-case delay computed.
- [ ] First-retry delay recorded.
- [ ] Separate curves recorded where needed.

The curve also interacts with the breaker: a breaker that opens after a few failures and a backoff that keeps clients retrying for minutes are solving the same problem from two directions, and configuring both without knowing which engages first produces either an idle window longer than intended or retries that never stop.


## Sources

- Retry and backoff guidance: <https://aws.amazon.com/builders-library/>
- Reliability practice: <https://sre.google/>
- Distributed systems context: <https://sre.google/workbook/table-of-contents/>
