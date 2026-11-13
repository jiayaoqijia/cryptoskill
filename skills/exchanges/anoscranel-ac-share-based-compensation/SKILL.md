---
name: ac-share-based-compensation
description: "Reading equity compensation from the investor's side: option and restricted stock grants, the expense and the adjusted metric that excludes it, fully diluted share count and the treasury stock method, buyback offset arithmetic, dilution per year and what it costs holders, performance and market-condition vesting, and the written dilution record. It measures what compensation transfers from shareholders; it never recommends a security and never gives tax advice. Use when asking \"stock based compensation\", \"SBC\", \"dilution\", \"fully diluted shares\", \"treasury stock method\", \"buyback offset\", \"is dilution getting worse\", \"restricted stock units\", \"option expense\", \"share count creep\". Not for the buyback programme itself (ac-capital-return-policy), not for the equity research case (ac-equity-research), not for non-GAAP bridge analysis in general (ac-earnings-quality)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Share-based compensation

## Overview

Equity compensation pays employees in shares or in claims on shares, and the cost is borne by existing holders through dilution rather than by the company through cash. That substitution is why the expense line and the share count tell different stories: a company can report a compensation expense that is added back in its preferred metric, while the share count rises year after year and each holder's claim on the business shrinks.

This skill measures that transfer. It covers the grant types and their vesting, the accounting expense and what a non-GAAP add-back does to it, the fully diluted count and the treasury stock method that produces it, the arithmetic of how much buyback is needed to hold the count flat, and the annual dilution rate that results. The buyback programme and the earnings quality questions belong to other skills.

Primary sources: <https://www.sec.gov/investor> and <https://www.fasb.org/>.

## When to use

- When a company's compensation is materially equity-based.
- When comparing a reported per-share figure with the diluted count.
- When a buyback is described as offsetting dilution.
- When vesting schedules and performance conditions affect future share supply.

## When NOT to use

- For the buyback programme's execution and timing (use ac-capital-return-policy).
- For the investment case and management assessment (use ac-equity-research).
- For non-GAAP bridges outside compensation (use ac-earnings-quality).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/grant-types-and-vesting.md` | `investing/grant-types-and-vesting` | Options, restricted stock, and units, and when each becomes shares. |
| `subskills/expense-and-add-back.md` | `investing/expense-and-add-back` | The accounting expense, the cash-flow treatment, and the add-back's effect. |
| `subskills/fully-diluted-count.md` | `investing/fully-diluted-count` | Basic versus diluted shares, and the treasury stock method's mechanics. |
| `subskills/buyback-offset-arithmetic.md` | `investing/buyback-offset-arithmetic` | How much repurchase is needed to hold the count flat. |
| `subskills/dilution-per-year.md` | `investing/dilution-per-year` | The annual transfer to employees and what it costs a holder. |
| `subskills/performance-and-market-conditions.md` | `investing/performance-and-market-conditions` | Vesting that depends on results or on the share price, and its probability. |
| `subskills/dilution-record.md` | `investing/dilution-record` | The written record: count, grants outstanding, dilution rate, and offset. |

## Status and honest limits

Grant terms are disclosed in filings but the aggregate is scattered across several notes, and the fully diluted count is an estimate that depends on the method used. Vesting and performance conditions can be modified, accelerated, or repriced, all of which change the forward supply without changing the past expense. Nothing here recommends a security, and a dilution estimate should carry the method and the filing date it rests on, because the share count in a summary is rarely the count that will exist.
