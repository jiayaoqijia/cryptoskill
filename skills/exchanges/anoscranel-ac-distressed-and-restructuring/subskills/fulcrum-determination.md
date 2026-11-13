---
name: fulcrum-determination
domain: investing/fulcrum-determination
trigger: "Finding which security becomes the equity of the reorganized company."
anti_trigger: "Not for predicting the court's valuation, and not for ordinary credit analysis."
scope: "Locating the security that becomes the equity of the reorganized company."
status: seedling
---

# Fulcrum determination

## Standard

The fulcrum security is the layer that converts into the reorganized equity: it is the most junior claim that still receives value, and everything above it is paid in cash or reinstated while everything below it is generally wiped out. Finding it is the central exercise in distressed investing, because the fulcrum's holders negotiate the plan and the instruments above and below have entirely different payoff shapes.

The determination is a valuation exercise with a range, not a point. At the low end of enterprise value the fulcrum sits higher in the queue; at the high end it sits lower. A capital structure can have a fulcrum that shifts between two layers across a plausible valuation range, and in that case both layers carry optionality — the junior one on a recovery that may not materialise, the senior one on a cushion that may disappear.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.uscourts.gov/>.

## Decision rules

- Record enterprise value at low, mid, and high, with the method and date for each.
- Apply each value down the waterfall and record which layer is exhausted.
- Identify the fulcrum at each end and state whether it shifts.
- Record the instruments above the fulcrum as money-good, and verify their trading level.
- Record the instruments below as out-of-the-money, and state what would have to change.
- Record the fulcrum's own recovery range and the assumptions that drive it.

## Procedure

1. Fix the claim schedule and the valuation range.
2. Run the waterfall at three valuation points.
3. Record the exhausted layer at each point.
4. Note whether the fulcrum is stable across the range.
5. Compute recovery per fulcrum instrument at each point.
6. Write the determination with the valuation sensitivity shown.

## Anti-patterns

- Naming a fulcrum from a single valuation point.
- Assuming the fulcrum is the largest claim by face amount.
- Ignoring that a valuation dispute is itself the negotiation.
- Treating a senior claim as money-good without checking its trading level.
- Forgetting that new money in the plan can shift the fulcrum.

## Done checklist

- [ ] Valuation range recorded with methods and dates.
- [ ] Waterfall run at three points.
- [ ] Fulcrum identified at each point.
- [ ] Stability across the range stated.
- [ ] Recovery per fulcrum instrument computed.
- [ ] Sensitivity written.

## Sources

- Filing search for disclosure statements and valuations: <https://www.sec.gov/edgar/search/>
- Court process information: <https://www.uscourts.gov/>
- Statutory reference: <https://www.law.cornell.edu/>
