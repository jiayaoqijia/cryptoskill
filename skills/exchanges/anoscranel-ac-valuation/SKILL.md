---
name: ac-valuation
description: "Estimating what a business is worth and stating the assumptions that carry the answer: choosing a method, constructing a discounted cash-flow model, using multiples honestly, terminal value and growth discipline, cost of capital, scenarios and sensitivity, and the written valuation record with its falsifiers. It produces ranges and assumptions, never a price target recommendation. Use when asking \"what is this worth\", \"run a DCF\", \"which multiple\", \"discount rate\", \"terminal value\", \"valuation model\". Not for gathering the underlying facts (ac-equity-research), not for allocation policy (ac-investment-policy-statement), not for trade sizing (ac-crypto-trading-discipline)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Valuation

## Overview

A valuation is an argument whose conclusion is a number. The number is the least important part; the assumptions that move it are the analysis. Two analysts can agree on every fact and disagree by a factor of three because they assume different growth, margins, or discount rates — and the useful output is not a point estimate but a range tied to named assumptions.

This skill builds valuations that can be checked and falsified. It does not produce recommendations, and it does not pretend that precision is accuracy: a model that reports a value to the cent has hidden its assumptions behind arithmetic.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## When to use

- After research has established that the reported numbers are trustworthy.
- When comparing two businesses as candidates for capital.
- When a held position's price implies assumptions worth testing.
- Before writing any purchase or sale memo.

## When NOT to use

- Before the financial statements and red flags have been examined (use ac-equity-research).
- For deciding how much of the portfolio a position may occupy (use ac-investment-policy-statement).
- For pricing a crypto token's supply schedule (use ac-token-diligence).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/valuation-methods.md` | `investing/valuation-methods` | Discounted cash flow, multiples, asset-based, and sum-of-parts, and when each is the honest choice. |
| `subskills/dcf-construction.md` | `investing/dcf-construction` | Forecast horizon, cash-flow definition, discount rate, and terminal value, built with assumption discipline. |
| `subskills/multiples.md` | `investing/multiples` | Peer selection, multiple choice, and why every multiple embeds a set of assumptions. |
| `subskills/terminal-value-and-growth.md` | `investing/terminal-value-and-growth` | Why terminal assumptions dominate the answer, and the sanity checks that keep them honest. |
| `subskills/discount-rate.md` | `investing/discount-rate` | Cost of capital, risk-free rate, equity premium, and the sensitivity that follows from beta. |
| `subskills/scenarios-and-sensitivity.md` | `investing/scenarios-and-sensitivity` | Bull, base, and bear cases as driver tables, and the sensitivity that shows what actually moves the value. |
| `subskills/valuation-record.md` | `investing/valuation-record` | The written valuation: assumptions, outputs, ranges, and the facts that would falsify it. |

## Status and honest limits

Every valuation is wrong, and the useful ones are wrong in a stated direction with stated bounds. Discounted cash flow rewards precision it does not have; multiples are shortcuts that hide their assumptions; and a terminal value that grows faster than the economy forever is a modelling error, not an assumption. Record the range, name the drivers, and treat the output as a hypothesis about the future rather than a fact about the present.
