---
name: venture-debt
domain: investing/venture-debt
trigger: "Evaluating debt as a financing layer on a venture-backed company."
anti_trigger: "Not for recommending financing, and not for credit analysis of banks."
scope: "Debt against venture equity: warrants, covenants, and maturity."
status: seedling
---

# Venture debt

## Standard

Venture debt is a loan to a company whose equity story, not its cash flow, is expected to repay it. Because the lending logic differs from conventional credit, the instrument carries the marks of the difference: a maturity far shorter than the company's plausible timeline to a repayment event, covenants keyed to fund-raising milestones rather than coverage ratios, warrants on the lender's equity to bridge the pricing gap between debt interest and equity returns, and material-adverse-change clauses that can trigger default when the next round fails to arrive on time.

The decision arithmetic weights dilution against rigidity. Debt extends runway and reduces the equity dilution of a round deferred or shrunk; in exchange it fixes a maturity date that the company's own milestones do not respect. The standard failure mode is not the interest rate but the maturity: a company that expected to raise a Series C in eighteen months reaches month sixteen with the raise delayed, and the debt's acceleration provisions convert a timeline problem into a solvency problem.

Primary sources: <https://www.fasb.org/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record the facility amount, draw schedule, interest rate, and — above all — the maturity date.
- Record every covenant and its measurement basis, including raised-capital milestones.
- Record warrant coverage: the percentage of the loan or of the round, the strike, and the vesting on drawdown.
- Read the events of default for material-adverse-change clauses and the remedy (equity cure rights, collateral).
- Compute the runway the facility adds and the milestones it presupposes.
- Record prepayment penalties, which can trap the company in the facility after a raise closes.

## Procedure

1. Extract amount, rate, maturity, and draw mechanics.
2. List covenants and their measurement basis with their test dates.
3. List events of default, with particular attention to MAC clauses.
4. Compute warrant-dilution effects at the strike prices provided.
5. Model the company reaching maturity without the milestone; state the consequence.
6. Write the debt summary beside the equity alternative it defers.

## Anti-patterns

- Sizing the decision by interest rate rather than by maturity risk.
- Treating raised-capital covenants as formalities when they are the real control.
- Ignoring warrant dilution in the round's ownership arithmetic.
- Assuming a bridge facility can itself be bridged.
- Overlooking prepayment penalties that persist after the raise.

## Done checklist

- [ ] Amount, rate, draw schedule recorded.
- [ ] Covenants and test dates listed.
- [ ] MAC and default clauses read.
- [ ] Warrant dilution computed.
- [ ] Milestone-miss scenario stated.
- [ ] Prepayment terms recorded.

## Sources

- Debt and lease accounting classification: <https://www.fasb.org/>
- Secured transaction filings and debt disclosure: <https://www.sec.gov/edgar/search/>
- Statutory reference on secured lending: <https://www.law.cornell.edu/>
