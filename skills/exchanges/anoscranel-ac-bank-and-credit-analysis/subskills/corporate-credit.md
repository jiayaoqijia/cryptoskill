---
name: corporate-credit
domain: investing/corporate-credit
trigger: "Assessing whether a non-bank borrower can service its debt."
anti_trigger: "Not for equity valuation, and not for predicting default timing."
scope: "Coverage, leverage, and covenants for a non-bank borrower: the lender's view of repayment."
status: seedling
---

# Corporate credit

## Standard

Credit analysis of a non-bank borrower asks one question: will the cash flow cover the obligations, in bad years as well as good. The tools are coverage ratios, leverage ratios, and the covenant package, each read against the borrower's history and its industry's cycle. Unlike equity analysis, the upside is capped by the promise; the work is about the downside.

Cash flow is the anchor, not earnings. A borrower that reports profit but generates no cash will service debt from reserves or new borrowing, both of which end. The analysis therefore starts with funds from operations, subtracts maintenance capital expenditure, and compares what remains with the debt service due in the next twelve months and over the maturity profile.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.federalreserve.gov/>.

## Decision rules

- Compute debt service coverage from cash flow, not from EBITDA alone.
- Leverage is measured net of cash and against a stated metric: debt to EBITDA, or debt to capital.
- Read the covenant package: which ratios are tested, at what levels, and with what headroom.
- The maturity profile is recorded, because a refinancing wall is a credit event even when coverage is adequate.
- Industry cyclicality is stated; coverage that is adequate at the peak may not be at the trough.
- Where the borrower is private and disclosure is thin, cap the confidence.

## Procedure

1. Pull the financial statements and the debt note.
2. Compute funds from operations and free cash flow after maintenance capex.
3. Compute coverage and leverage ratios with definitions stated.
4. Build the maturity profile and record the refinancing requirement.
5. Read the covenants and compute headroom.
6. Write the assessment with the cycle assumption and confidence.

## Anti-patterns

- Using EBITDA as a proxy for cash flow without the adjustments.
- Ignoring the maturity wall because coverage is comfortable.
- Reading covenants without computing headroom.
- Assuming the current cycle continues.
- Treating a rating as the analysis.

## Done checklist

- [ ] Cash flow and free cash flow computed.
- [ ] Coverage and leverage ratios computed with definitions.
- [ ] Maturity profile built.
- [ ] Covenant headroom computed.
- [ ] Cycle assumption stated.
- [ ] Confidence recorded.

## Sources

- Full-text filing search for borrower financials: <https://www.sec.gov/edgar/search/>
- Credit-market context from the Federal Reserve: <https://www.federalreserve.gov/>
- Investor education on credit risk: <https://www.investor.gov/introduction-investing>

The lender's question is not whether the business is good but whether the promise survives its worst plausible year. That framing changes which numbers matter: coverage at the trough, covenant headroom under stress, and the maturity wall are more informative than this year's growth, and the record should say so explicitly.
