---
name: ac-scenario-and-stress-testing
description: "Designing scenarios that test a portfolio rather than flatter it: reverse stress testing from a failure back to its cause, historical versus hypothetical scenarios and what each can and cannot show, correlation and liquidity breakdown under stress, scenario severity calibration, the pass/fail criterion set before the test, and the written scenario record. It designs and reads tests; it never predicts a crisis and never recommends a position. Use when asking \"stress test\", \"reverse stress test\", \"scenario analysis\", \"what would break us\", \"historical scenario\", \"correlation breakdown\", \"severity calibration\". Not for measuring liquidity in isolation (ac-liquidity-risk), not for drawdown budgeting (ac-portfolio-construction), not for validating a backtest (ac-backtest-integrity)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Scenario and stress testing

## Overview

A scenario test answers a question about a specific set of conditions, and the value of the answer depends entirely on whether the question was chosen well. Scenarios designed around historical episodes test whether the portfolio would survive a repeat of events already known; scenarios designed around the portfolio's own vulnerabilities test whether it can survive something new.

The second kind is where the craft lies, and reverse stress testing is its main technique: instead of asking what happens under a given shock, it asks what shock would cause a given failure. That inverts the exercise from describing outcomes to identifying the combinations of moves that matter, which is both more uncomfortable and more useful.

Primary sources: <https://www.bis.org/> and <https://www.investor.gov/introduction-investing>.

## When to use

- When a portfolio's vulnerability needs testing rather than describing.
- When a historical scenario is being reused and its limits matter.
- When correlations or liquidity are assumed to hold under stress.
- When a pass/fail threshold is being set for a risk review.

## When NOT to use

- For building a liquidity ladder (use ac-liquidity-risk).
- For budgeting drawdowns across strategies (use ac-portfolio-construction).
- For judging whether a backtest is trustworthy (use ac-backtest-integrity).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/reverse-stress-testing.md` | `investing/reverse-stress-testing` | Starting from failure and solving for the shock that causes it. |
| `subskills/historical-versus-hypothetical.md` | `investing/historical-versus-hypothetical` | What a repeat of a known episode can and cannot tell you. |
| `subskills/correlation-breakdown.md` | `investing/correlation-breakdown` | Diversification that disappears exactly when it is needed. |
| `subskills/severity-calibration.md` | `investing/severity-calibration` | Choosing how severe a scenario should be, and defending the choice. |
| `subskills/scenario-pass-fail.md` | `investing/scenario-pass-fail` | The criterion set before the test, and what failure triggers. |
| `subskills/scenario-construction.md` | `investing/scenario-construction` | Building a scenario that is coherent across asset classes. |
| `subskills/scenario-record.md` | `investing/scenario-record` | The written record: scenario, assumptions, result, and action. |

## Status and honest limits

Every scenario is a construction, and the portfolio's response is a model output rather than a fact. Correlations estimated from normal periods understate stress dependence, and liquidity assumptions are the ones most likely to be wrong precisely in the scenario being tested. The record therefore states the assumptions explicitly and treats a passing result as evidence about the assumptions as much as about the portfolio.
