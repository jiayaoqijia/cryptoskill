---
name: ac-liability-driven-investing
description: "Managing assets against defined liabilities rather than against a market index: funding ratio arithmetic and surplus risk, liability discount curves and their sensitivity, duration and key-rate matching, immunisation and its conditions, de-risking glide paths and trigger design, contribution and benefit policy interaction, and the written LDI record. It explains the arithmetic that connects assets to obligations; it never recommends an allocation and never gives actuarial advice. Use when asking \"funding ratio\", \"surplus risk\", \"liability driven investing\", \"LDI\", \"immunisation\", \"duration matching\", \"glide path\", \"derisking trigger\", \"liability discount rate\", \"key rate duration\". Not for household retirement spending (ac-retirement-and-drawdown), not for bond duration mechanics in isolation (ac-fixed-income-and-rates), not for portfolio policy without liabilities (ac-investment-policy-statement)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Liability-driven investing

## Overview

A liability-driven mandate measures success against a stream of obligations rather than against a market index. That change of benchmark changes everything else: the relevant risk is not volatility of assets but volatility of the surplus between assets and liabilities, the relevant duration is the difference between the two, and a fall in interest rates can improve the funding position even as it reduces asset values.

This skill covers that arithmetic: how a funding ratio is computed and what makes it move, how liabilities are discounted and why the discount basis is a policy choice, how duration and key-rate matching reduce surplus risk, what immunisation actually requires, and how a de-risking glide path converts a funding improvement into a lower-risk portfolio. It is about the link between assets and obligations, not about choosing investments.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## When to use

- When a portfolio exists to fund defined obligations rather than to track a market.
- When a funding ratio or surplus risk is being measured or reported.
- When duration or key-rate matching against liabilities is being designed.
- When a de-risking glide path or trigger framework is being set.

## When NOT to use

- For household retirement spending arithmetic (use ac-retirement-and-drawdown).
- For bond duration and convexity mechanics alone (use ac-fixed-income-and-rates).
- For policy on a portfolio without defined liabilities (use ac-investment-policy-statement).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/funding-ratio-and-surplus.md` | `investing/funding-ratio-and-surplus` | The ratio, its components, and surplus risk as the measure that matters. |
| `subskills/liability-discounting.md` | `investing/liability-discounting` | Discount curves, the choice of basis, and the sensitivity of the liability value. |
| `subskills/duration-and-key-rate-matching.md` | `investing/duration-and-key-rate-matching` | Matching duration and key-rate exposures between assets and liabilities. |
| `subskills/immunisation-conditions.md` | `investing/immunisation-conditions` | What immunisation requires, and the conditions that break it. |
| `subskills/derisking-glide-path.md` | `investing/derisking-glide-path` | Glide-path design, funding triggers, and the cost of de-risking late. |
| `subskills/contribution-and-benefit-policy.md` | `investing/contribution-and-benefit-policy` | How contributions and benefit design change the liability itself. |
| `subskills/ldi-record.md` | `investing/ldi-record` | The written record: funding basis, surplus risk, hedge ratio, and triggers. |

## Status and honest limits

The liability side of the calculation is an estimate built on demographic and financial assumptions, and small changes in those assumptions move the liability value more than a year of asset returns. Nothing here is actuarial advice, and a funding ratio computed on one basis is not comparable with one computed on another. A hedge that matches duration on the stated basis still leaves the risk that the basis itself was wrong.
