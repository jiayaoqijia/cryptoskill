---
name: transition-management
domain: investing/transition-management
trigger: "Moving a portfolio between managers and controlling the cost of the move."
anti_trigger: "Not for selecting the new manager, and not for predicting markets."
scope: "Moving a portfolio between managers, and where the cost and risk sit."
status: seedling
---

# Transition management

## Standard

A transition moves a portfolio from one set of holdings to another, usually when a mandate changes hands. The cost is not only the commission on the trades: it is the market exposure carried during the transition, the impact of liquidating and rebuilding positions that overlap, and the risk that the portfolio is out of the market during a move. A transition that takes weeks carries weeks of tracking error against the target.

The specialist's job is to manage that exposure, and the conflict is that the specialist is also paid for the trades it executes. Crossing positions internally between the outgoing and incoming portfolios reduces both cost and impact, but the price at which the cross happens is a negotiation, and the incentive to trade rather than cross is real. The record should state the crossing policy and the exposure budget before the transition begins.

Primary sources: <https://www.cfainstitute.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the target portfolio and the starting portfolio.
- Record the overlap and what can be crossed rather than traded.
- Record the exposure budget: how much tracking error is acceptable during the move.
- Record the crossing policy and how the cross price is determined.
- Record the fee structure: per trade, per basis point, or asset-based.
- Record the risk controls during the transition and who monitors them.

## Procedure

1. Record the starting and target portfolios.
2. Identify overlapping positions suitable for crossing.
3. Set the exposure budget and the time limit.
4. Record the crossing policy and pricing method.
5. Record the fee structure and its incentive.
6. Write the transition plan with its risk limits.

## Anti-patterns

- Rewarding the transition manager per trade rather than per outcome.
- Setting no exposure budget, so the transition drifts.
- Crossing at a price that favours one side of the transition.
- Ignoring the tax consequence of liquidating positions.
- Treating the transition as a back-office task.

## Done checklist

- [ ] Starting and target portfolios recorded.
- [ ] Overlap identified.
- [ ] Exposure budget set.
- [ ] Crossing policy recorded.
- [ ] Fee structure recorded.
- [ ] Risk controls recorded.

The measure of a transition is the tracking error against the target after the move, not the commission paid: a transition that trades cheaply and takes six weeks can cost more in foregone exposure than one that pays twice the commission and finishes in three days, and the exposure budget is the number that makes the comparison possible.

## Sources

- Investment management and trading standards: <https://www.cfainstitute.org/>
- Market structure and disclosure: <https://www.sec.gov/investor>
- Execution quality guidance: <https://www.finra.org/>
