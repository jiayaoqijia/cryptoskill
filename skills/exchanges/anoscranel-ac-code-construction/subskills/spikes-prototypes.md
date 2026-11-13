---
name: spikes-prototypes
domain: software-engineering/spikes-prototypes
trigger: "\"quick prototype to test this\", \"can we even do this\", \"spike this for two days\", \"throwaway demo\"."
anti_trigger: "Shipping the experiment as a step of real work (subskills/incremental-delivery.md); measuring a shipped system against a target; reducing risk in a plan or estimate; recording the decision."
scope: "Time-boxed throwaway experiments that answer one question"
status: "seedling"
---

# Spikes & Prototypes

## Standard

- **XP spike solution** (http://www.extremeprogramming.org/rules/spike.html): a very simple program to explore a potential solution. Most spikes are not good enough to keep, so expect to throw the code away. The goal is to reduce the risk of a technical problem or to make an estimate reliable.
- **Time-box norms**: Scrum Alliance puts a spike at a maximum of one sprint; XP guidance is a week or two for a pair.
- **Exit artefact** is the answer, not the code: a finding, a number, a decision, a revised estimate.
- **Spikes may be demonstrated** (https://framework.scaledagile.com/spikes): the result is shown, the code is not kept.

## Decision rules

1. One spike answers one question. Write the question before the timer starts.
2. The box is short: one day for a library check, one week for a protocol question. Beyond one sprint it is a project, not a spike.
3. Spike code is never merged. If it earns production, rewrite it under test (subskills/incremental-delivery.md).
4. A spike that answers "no" is a success and ends the debate.
5. No production credentials, no real user data, no live traffic (out of scope for this leaf: the full security rules behind this).
6. The answer is written down before the box closes.
7. If the question needs more than one box, split the question.

## Procedure

1. Write the question in one sentence: "Can X handle Y within Z?"
2. Write the success bar: what result answers yes, what answers no.
3. Set the timer and the scope: which endpoints, which data, which environment.
4. Build the smallest path that touches the risky part. Skip setup that does not touch the question.
5. Record numbers as you go: latency, payload size, failure mode, API friction.
6. At the halfway point, decide whether the question is already answered. Early stop is allowed.
7. Stop at the box even if the answer is "unknown so far".
8. Write the answer:
   ```markdown
   ## Spike: can X hold 500 req/s at a 300 ms p99?
   Result: yes, 720 req/s, p99 210 ms, one worker.
   Friction: no batch API; one call per row.
   Cost: 3 h. Verdict: adopt, batch via the job queue.
   ```
9. If the answer is yes, hand the numbers to the estimate and the design (out of scope for this leaf: estimation and the decision record).
10. Delete the spike branch. Keep the finding, not the code.

## Anti-patterns

- A spike with no question, so it drifts into building the thing.
- A box that stays open "one more day" for two weeks.
- Merging spike code because "it works".
- Results with no numbers, so the decision is argued by feel.
- Production data in a throwaway environment.
- A spike used to dodge an estimate instead of informing it.

## Done checklist

- [ ] Question and success bar written before the timer.
- [ ] Time-box set and honoured.
- [ ] Numbers recorded for the result.
- [ ] Verdict written, including "no" and "unknown".
- [ ] No spike code merged.

## Sources

- http://www.extremeprogramming.org/rules/spike.html
