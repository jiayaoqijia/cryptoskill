---
name: cash-conversion-forensics
domain: investing/cash-conversion-forensics
trigger: "Finding which accounts absorb the gap between earnings and cash."
anti_trigger: "Not for alleging manipulation, and not for valuation."
scope: "Which accounts absorb the gap between earnings and cash."
status: seedling
---

# Cash conversion forensics

## Standard

When earnings and operating cash flow diverge, the difference sits in a working-capital account or in a non-cash charge, and the identity is arithmetically exact: every gap has a home. The forensic exercise is to locate that home rather than to describe the gap, because the account that absorbs it tells you what kind of divergence it is.

Receivables absorbing the gap means revenue is being recognised ahead of collection. Inventory absorbing it means production is ahead of sale. Payables absorbing it means the company is paying suppliers later, which is a one-time benefit that reverses. A non-cash charge absorbing it means earnings are below cash rather than above, which is a different story entirely. Each has a different implication and a different persistence.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## Decision rules

- Record earnings and operating cash flow for each period.
- Compute the gap and identify the accounts that close it.
- Record each absorbing account's change as a share of the gap.
- Record whether the absorption is a one-time reversal or a trend.
- Record the direction: earnings above cash, or cash above earnings.
- Record the accounts that have absorbed the gap for several consecutive periods.

## Procedure

1. Record earnings and cash flow by period.
2. Compute the gap.
3. Walk the working-capital accounts and non-cash charges.
4. Attribute the gap and record each attribution's share.
5. Record persistence across periods.
6. Write the attribution with the dominant account named.

## Anti-patterns

- Describing a gap without locating it.
- Treating a payables extension as a permanent improvement.
- Ignoring the direction of the divergence.
- Looking at one period rather than a run of them.
- Assuming a non-cash charge is a quality problem rather than an economic event.

## Done checklist

- [ ] Earnings and cash flow recorded.
- [ ] Gap computed.
- [ ] Accounts walked.
- [ ] Attribution recorded with shares.
- [ ] Persistence recorded.
- [ ] Dominant account named.

The most informative single check is whether the same account has absorbed the gap for three periods running: a one-period absorption is usually a timing difference that reverses, while a persistent one is a structural feature of how the company recognises revenue or manages its balance sheet, and the distinction changes what a reader should expect in the next period.

## Sources

- Cash flow statement disclosure: <https://www.sec.gov/investor>
- Research on earnings and cash: <https://www.nber.org/>
- Investor education on financial statements: <https://www.investor.gov/introduction-investing>
