---
name: signal-decay
domain: investing/signal-decay
trigger: "Assessing what happens to an edge once a dataset is widely sold."
anti_trigger: "Not for predicting returns, and not for backtest validation."
scope: "What happens to an edge once the dataset is widely sold."
status: seedling
---

# Signal decay

## Standard

A dataset that is sold to many participants stops being informative in the way it was when it was exclusive. The mechanism is straightforward: if the data predicts a return, buyers act on it, the price moves earlier, and the predictable window shrinks. The signal does not necessarily disappear, but its magnitude falls and its timing moves toward the publication date rather than the underlying event.

Decay can be measured if the dataset has a long history: split the sample at the point the data became widely available and compare the signal's strength before and after. A signal that halves is still usable at a lower capacity; one that vanishes was a description of a period rather than a persistent effect. The record should state the decay estimate and the capacity it implies.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record when the dataset became available and to how many participants.
- Split the sample at the availability date where the history permits.
- Compare the signal's strength in the two periods.
- Record the decay estimate and its uncertainty.
- Record the capacity implied by the post-publication strength.
- Record whether the signal's timing moved toward publication.

## Procedure

1. Establish the availability date.
2. Split the sample.
3. Measure the signal in each period.
4. Compute the decay and its range.
5. Derive capacity from the post-period strength.
6. Write the decay assessment.

## Anti-patterns

- Measuring the signal only over the period before it was sold.
- Assuming decay is linear rather than a step at publication.
- Ignoring the timing shift, which changes implementation.
- Treating a decayed signal as unusable rather than as lower capacity.
- Failing to record the availability date on which everything depends.

## Done checklist

- [ ] Availability date recorded.
- [ ] Sample split.
- [ ] Signal measured in both periods.
- [ ] Decay estimated with range.
- [ ] Capacity derived.
- [ ] Timing shift recorded.

A useful companion measure is how much of the signal's return accrues in the first day after the data becomes available: if the entire effect is captured at the release, the strategy is a race rather than an analysis, and its capacity is bounded by execution speed rather than by idea quality.


## Sources

- Research on return predictability and decay: <https://www.nber.org/>
- Investor education on data-driven strategies: <https://www.investor.gov/introduction-investing>
- Market data for sample construction: <https://fred.stlouisfed.org/>
