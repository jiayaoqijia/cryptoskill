---
name: buyback-execution
domain: investing/buyback-execution
trigger: "Reading how a buyback programme is executed and whether it is executed well."
anti_trigger: "Not for predicting the share price, and not for the dividend policy."
scope: "Open-market programmes, 10b5-1 plans, and what execution quality looks like."
status: seedling
---

# Buyback execution

## Standard

An authorisation is not a buyback. A company announces a programme, and then buys — or does not — subject to blackout periods, liquidity constraints, and the discretion of management. The disclosure of what was actually purchased, at what average price, and over what period is the evidence of execution, and it arrives quarterly at best.

Execution quality has two tests. The first is whether the shares were bought when they were cheap relative to the company's own cash flows, which is testable after the fact against the price history. The second is whether the programme was completed at all: a recurring pattern of announcing large authorisations while purchasing a small fraction is a signal about intent, and it is visible in the share count over several years rather than in any single filing.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the authorised amount, the announced period, and any stated conditions.
- Record the shares actually repurchased and the average price paid, by period.
- Track the diluted share count over several years to test whether the programme netted out.
- Record the buyback's interaction with issuance: options, stock compensation, and convertibles can offset repurchases.
- Record the blackout and trading-plan arrangements where disclosed.
- Compare the average purchase price with the price range over the same period.

## Procedure

1. Collect the authorisation and each period's actual repurchases.
2. Compute the proportion of the authorisation used.
3. Track the diluted share count across years.
4. Compute net reduction after issuance.
5. Compare average purchase prices with the period's range.
6. Write the execution assessment.

## Anti-patterns

- Treating an announcement as a completed buyback.
- Measuring repurchases gross while ignoring share issuance.
- Concluding on execution from one quarter.
- Ignoring the blackout windows that constrain purchases.
- Assuming a repurchase at any price is a return of capital.

## Done checklist

- [ ] Authorisation and period recorded.
- [ ] Actual repurchases and average prices recorded.
- [ ] Diluted share count tracked.
- [ ] Net reduction after issuance computed.
- [ ] Blackout arrangements recorded.
- [ ] Execution assessment written.

The cost of a repurchase is also the opportunity cost of the price paid, which is not visible in the disclosure: a company that repurchased at a high multiple and later traded lower has transferred value to sellers, and the only way to see it is to record the price paid beside the price range and the valuation at the time.

## Sources

- Share repurchase disclosure: <https://www.sec.gov/investor>
- Investment analysis standards: <https://www.cfainstitute.org/>
- Market data for price comparison: <https://fred.stlouisfed.org/>
