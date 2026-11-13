---
name: load-shedding
domain: software-engineering/load-shedding
trigger: "Deciding what to drop when demand exceeds capacity."
anti_trigger: "Not for autoscaling policy, and not for rate limiting alone."
scope: "Admission control and dropping work deliberately rather than failing."
status: seedling
---

# Load shedding

## Standard

When demand exceeds capacity, something gives. Without a decision, the system gives in the worst way: queues grow, latency rises for every request, and eventually everything times out, so the service serves nobody while consuming its full resources. Load shedding is the alternative — refusing a defined fraction of work early so that the rest is served within its deadline.

The design question is which work to refuse. A shedder that drops requests at random preserves fairness but sacrifices the most important requests along with the least; one that drops by priority preserves the critical path but needs a priority signal it can trust; one that drops the oldest queued work preserves latency but surprises clients whose requests had waited longest. The record should state the criterion, because the criterion is the policy.

Primary sources: <https://sre.google/> and <https://aws.amazon.com/builders-library/>.

## Decision rules

- Record the admission criterion: random, priority, age, or a cost-weighted mix.
- Record the signal that drives shedding, since latency-based shedding responds to the symptom while queue-depth shedding responds to the cause.
- Record the shedding fraction and how it is computed.
- Record what the client receives when shed, and whether it is distinguishable from an error.
- Record the interaction with retries, since a shed response that invites an immediate retry undoes the shedding.
- Record the priority source and how it is validated, since a client-declared priority can be gamed.

## Procedure

1. Choose the admission criterion and record the reason.
2. Record the signal and its threshold.
3. Record the fraction and its computation.
4. Record the response to a shed request.
5. Record retry interaction and backoff guidance.
6. Write the policy with the criterion stated.

## Anti-patterns

- Letting queues grow until everything times out.
- Shedding at random when a reliable priority signal exists.
- Returning a 500 for a shed request, which reads as a bug and invites retries.
- Client-declared priority with no validation.
- Shedding based on latency alone, which reacts after the queue has already built.

## Done checklist

- [ ] Admission criterion recorded.
- [ ] Driving signal and threshold recorded.
- [ ] Shed fraction recorded.
- [ ] Response recorded.
- [ ] Retry interaction recorded.
- [ ] Priority validation recorded.

The shed response should also be honest about duration: a client told to retry immediately will do so, which is the amplification problem again, so the response should carry a retry-after hint sized to the overload and the client should honour it. Shedding without that guidance is shedding that invites its own reversal.


## Sources

- Load shedding and admission control: <https://sre.google/>
- Distributed systems practice: <https://aws.amazon.com/builders-library/>
- Overload handling: <https://sre.google/workbook/table-of-contents/>
