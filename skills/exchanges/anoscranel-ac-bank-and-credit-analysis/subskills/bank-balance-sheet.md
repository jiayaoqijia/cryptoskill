---
name: bank-balance-sheet
domain: investing/bank-balance-sheet
trigger: "Reading a bank's balance sheet and understanding what its leverage implies."
anti_trigger: "Not for valuing the bank, and not for non-financial companies."
scope: "Loans, deposits, equity, and the leverage that makes a bank's balance sheet a different object."
status: seedling
---

# Bank balance sheet

## Standard

A bank's balance sheet is mostly loans on one side and deposits on the other, with a thin layer of equity between them. That thinness is the point: a bank operating at ten to twenty times equity means a fall of five to ten percent in asset value can consume half or all of the capital. Reading a bank begins with that arithmetic, because it explains why small changes in credit quality or funding cost matter so much.

The statement also requires translation. Deposits are not debt in the way an industrial company's bonds are — they are the funding base, and their stability is the asset that matters. Loans are not receivables held to be collected in full; they are claims whose value depends on the borrowers' ability to pay, which is why provisions sit against them.

Primary sources: <https://www.federalreserve.gov/> and <https://www.fdic.gov/>.

## Decision rules

- Compute equity as a percentage of assets first; the leverage ratio frames everything else.
- Separate the loan book by category: retail, commercial, real estate, and any concentration.
- Record deposits by type, because stable retail deposits and wholesale funding behave differently in stress.
- Off-balance-sheet commitments and securities holdings are recorded, not ignored.
- Compare the balance sheet with the prior year's to see how the mix has changed.
- Where a category is not disclosed, record the gap.

## Procedure

1. Pull the balance sheet and the loan and deposit composition notes.
2. Compute equity to assets and equity to loans.
3. Build the loan mix by category and the deposit mix by type.
4. Note securities holdings and their duration if disclosed.
5. Compare with the prior year and record changes in mix.
6. Write the summary with the leverage arithmetic shown.

## Anti-patterns

- Reading a bank like an industrial company.
- Treating all deposits as equally stable.
- Ignoring concentration in one loan category.
- Forgetting off-balance-sheet commitments.
- Using a single year's mix as the structural picture.

## Done checklist

- [ ] Equity to assets computed.
- [ ] Loan mix built by category.
- [ ] Deposit mix built by type.
- [ ] Securities and off-balance-sheet items recorded.
- [ ] Year-on-year mix change noted.
- [ ] Undisclosed categories recorded as gaps.

## Sources

- Federal Reserve supervision and bank data: <https://www.federalreserve.gov/>
- Federal Deposit Insurance Corporation bank data: <https://www.fdic.gov/>
- Investor education on financial institutions: <https://www.investor.gov/introduction-investing>
