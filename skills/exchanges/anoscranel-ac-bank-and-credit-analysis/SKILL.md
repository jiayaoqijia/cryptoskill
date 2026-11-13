---
name: ac-bank-and-credit-analysis
description: "Analysing banks and credit: a bank's balance sheet and why it differs from a company's, net interest margin and funding cost, credit quality through the cycle, capital and liquidity ratios, bank valuation through return on equity and price to book, corporate credit analysis for non-bank borrowers, and the written record. It analyses balance sheets and credit quality; it never recommends a security or predicts a default. Use when asking \"analyse this bank\", \"bank balance sheet\", \"NPL ratio\", \"CET1\", \"credit analysis\", \"will this borrower repay\", \"net interest margin\". Not for general equity research (ac-equity-research), not for valuation of a non-financial business (ac-valuation), not for fixed-income instrument mechanics (ac-fixed-income-and-rates)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Bank and credit analysis

## Overview

A bank is a leveraged intermediary: it borrows short and lends long, earns the spread, and absorbs the difference between promises it has made and promises it holds. That structure makes its financial statements read differently from an industrial company's — deposits are funding rather than a liability in the ordinary sense, loans are the inventory, and equity is a thin buffer whose adequacy is the central question.

Credit analysis asks the same question from the borrower's side: given this borrower's cash flows and obligations, what is the probability and the loss if the promise breaks. Both halves share a discipline — you are underwriting promises, not buying stories — and both end in a written record with stated confidence.

Primary sources: <https://www.federalreserve.gov/> and <https://www.fdic.gov/>.

## When to use

- Before taking equity or credit exposure to a bank or financial institution.
- When assessing a corporate borrower's ability to service debt.
- When a bank reports results and the loan book or capital position has changed.
- When a credit spread or a rating is being questioned.

## When NOT to use

- For non-financial equity research (use ac-equity-research).
- For valuing an ordinary business (use ac-valuation).
- For bond price and duration arithmetic (use ac-fixed-income-and-rates).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/bank-balance-sheet.md` | `investing/bank-balance-sheet` | Loans, deposits, equity, and the leverage that makes a bank's balance sheet a different object. |
| `subskills/net-interest-margin.md` | `investing/net-interest-margin` | Spread, funding cost, and the rate sensitivity of a banking book. |
| `subskills/credit-quality.md` | `investing/credit-quality` | Non-performing loans, provisions, coverage, and charge-offs through the credit cycle. |
| `subskills/capital-and-liquidity.md` | `investing/capital-and-liquidity` | CET1, leverage ratios, and liquidity coverage, and what the minimums actually constrain. |
| `subskills/bank-valuation.md` | `investing/bank-valuation` | Return on equity, price to book, and why earnings multiples mislead for a leveraged lender. |
| `subskills/corporate-credit.md` | `investing/corporate-credit` | Coverage, leverage, and covenants for a non-bank borrower: the lender's view of repayment. |
| `subskills/bank-credit-record.md` | `investing/bank-credit-record` | The written record: exposure, ratios, cycle position, assumptions, and review triggers. |

## Status and honest limits

Bank accounting is judgement-heavy: provisioning is an estimate, loan classifications vary by regime, and regulatory ratios are computed under rules that change. A capital ratio that looks comfortable today can be restated by a supervisory exercise. Credit analysis likewise produces probabilities, not certainties, and a record that says "cannot assess" is more useful than a confident score built on missing data.
