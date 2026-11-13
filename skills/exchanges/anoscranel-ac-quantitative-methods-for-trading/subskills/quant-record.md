---
name: quant-record
domain: crypto-trading/quant-record
trigger: "Writing the record of a quantitative method or position."
anti_trigger: "Not for recommending a method, and not for the backtest report itself."
scope: "The written record: method, assumptions, decay, costs, and falsifiers."
status: seedling
---

# Quant record

## Standard

The quant record states the method, its assumptions, its measured decay, its costs, and the conditions under which it is retired. Its purpose is the same as every record in this pack: to make a later disagreement about the method an argument about stated assumptions rather than about memory. A quantitative method that is not recorded this way degrades into folklore — a rule that has always been traded, with nobody able to say what its edge was measured to be.

The second function is enforcement of the falsifier. A method whose retirement threshold is written before the trade can be retired honestly when the threshold arrives; a method without one gets defended at the moment the evidence says otherwise. The record is where the half-life, the cost line, and the falsifier wait for the review, and the review triggers are part of the record with dates.

Primary sources: <https://osf.io/prereg/> and <https://quant.stackexchange.com/>.

## Decision rules

- Record the method's exact form and parameters, with the estimation windows.
- Record each assumption the method leans on, and what its failure would look like.
- Record the measured decay and the half-life, with the windows they came from.
- Record costs at the intended size and the persistence-versus-cost margin.
- Record the falsifier and the retirement threshold before the first trade.
- Date every review and record the comparison against the prior one.

## Procedure

1. Write the method form, parameters, and windows.
2. List the assumptions with their failure appearances.
3. Record decay, half-life, cost, and margin.
4. Write the falsifier and the retirement threshold.
5. Set the review triggers with dates.
6. Review on the dates and record the drift, appended without rewriting.

## Anti-patterns

- Recording the backtest's result without its cost line.
- Leaving the falsifier implicit.
- Rewriting the entry record as the edge decays.
- Reporting a fresh backtest as if it were out-of-sample evidence.
- No review cadence, so the drift is never measured.

## Done checklist

- [ ] Method, parameters, and windows recorded.
- [ ] Assumptions with failure appearances listed.
- [ ] Decay and cost margin recorded.
- [ ] Falsifier and threshold written.
- [ ] Review triggers dated.
- [ ] Reviews appended, not rewritten.

The record should also carry the method's provenance: whether the parameters were estimated by the desk, inherited from a published paper, or supplied by a vendor, since each source carries a different decay expectation and a different duty to re-estimate.

## Sources

- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Quantitative method discussion: <https://quant.stackexchange.com/>
- Investor education on risk: <https://www.investor.gov/introduction-investing>
