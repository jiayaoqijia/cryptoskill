---
name: cost-record
domain: investing/cost-record
trigger: "Writing the record of what trading costs and how it was measured."
anti_trigger: "Not for recommending a broker, and not for the execution blotter."
scope: "The written cost record: benchmark, decomposition, and review triggers."
status: seedling
---

# Cost record

## Standard

The cost record states the benchmark used, the decomposition into components, the sample and period, and the conclusion about what the cost implies. It is written so that a later reader can tell whether the figure is comparable with another: a cost of twelve basis points measured against arrival price over one quarter is not the same claim as one measured against VWAP over three years.

The record also carries the decision it informs. Cost measurement exists to change behaviour — slicing differently, choosing a venue, giving an order more time — and a record that reports a number without the change it produced is a report rather than a control. Stating the action taken, and re-measuring after it, is what closes the loop.

Primary sources: <https://www.cfainstitute.org/> and <https://osf.io/prereg/>.

## Decision rules

- Record the benchmark, its definition, and the window.
- Record the decomposition and the largest component.
- Record the sample size, period, and instruments covered.
- Record the conclusion and the action it implies.
- Record the re-measurement date and what would count as improvement.
- Record any comparison with a prior period on the same basis.

## Procedure

1. Record the benchmark and its definition.
2. Record the components and their shares.
3. Record the sample and period.
4. Record the conclusion and the intended action.
5. Set the re-measurement date and the success threshold.
6. File and reference from the execution policy.

## Anti-patterns

- Reporting a cost without the benchmark.
- Comparing periods measured on different bases.
- Recording a number with no action attached.
- Omitting the sample size.
- Treating a favourable quarter as an improvement without re-measurement.

## Done checklist

- [ ] Benchmark and definition recorded.
- [ ] Decomposition recorded.
- [ ] Sample and period recorded.
- [ ] Action recorded.
- [ ] Re-measurement date set.
- [ ] Prior comparison on the same basis.

The threshold matters as much as the date: a re-measurement that is not tied to a size of change the reader would act on produces a monthly report nobody changes anything for, and setting the threshold in advance is what makes the next quarter's number mean something.

Keeping the record alongside the execution policy, rather than in a reporting folder, is what makes it operative: the policy states how orders should be worked and the record states what that produced, and a reader who has both can see whether the policy is being followed rather than whether it exists.

## Sources

- Trading and performance standards: <https://www.cfainstitute.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Execution quality guidance: <https://www.finra.org/>
