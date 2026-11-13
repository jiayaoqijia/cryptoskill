---
name: ac-corporate-treasury
description: "The issuer's side of capital management: liquidity policy and the cash buffer, money market and deposit counterparty limits, interest rate and FX hedging programme design, hedge accounting and why it constrains the programme, the debt maturity ladder and refinancing risk, bank facility covenants, and the written treasury policy record. It explains how a company manages its own balance-sheet risk; it never recommends a security and never gives tax or legal advice. Use when asking \"corporate treasury\", \"cash investment policy\", \"hedge accounting\", \"FX hedging programme\", \"interest rate hedge\", \"maturity ladder\", \"counterparty limits\", \"why does my company hedge\", \"minimum cash balance\". Not for the investor's portfolio policy (ac-investment-policy-statement), not for the company's credit analysis (ac-bank-and-credit-analysis), not for the capital return programme (ac-capital-return-policy)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Corporate treasury

## Overview

Treasury is where a company manages the risks its business creates but does not want to keep: the cash it must hold, the rates it pays, the currencies it earns, and the maturity of its debt. The decisions look like investment decisions and are not, because their purpose is to protect the operating business rather than to earn a return, and a treasury that forgets this becomes a proprietary trading desk with the company's balance sheet.

This skill covers the policy and the mechanics: how much liquidity to hold and in what, how to set counterparty limits for deposits, how to design an interest rate and currency hedging programme, how hedge accounting constrains that design, how to read a maturity ladder, and what a covenant package permits. The investor-side policy and the credit analysis belong to other skills.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## When to use

- When reading a company's treasury policy and its disclosed hedges.
- When assessing whether a cash buffer is adequate for the business.
- When a hedging programme's accounting treatment affects reported results.
- When a maturity ladder or a covenant package needs evaluating.

## When NOT to use

- For the investor's own portfolio policy (use ac-investment-policy-statement).
- For assessing the company's credit quality (use ac-bank-and-credit-analysis).
- For the buyback and dividend programme (use ac-capital-return-policy).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/liquidity-policy.md` | `investing/liquidity-policy` | The cash buffer, its size relative to the business, and what it may be invested in. |
| `subskills/counterparty-limits.md` | `investing/counterparty-limits` | Deposit and derivative counterparty limits, and concentration in a stress. |
| `subskills/hedging-programme-design.md` | `investing/hedging-programme-design` | What to hedge, how much, over what horizon, and with which instruments. |
| `subskills/hedge-accounting.md` | `investing/hedge-accounting` | Designation, effectiveness testing, and why accounting constrains the hedge. |
| `subskills/maturity-ladder.md` | `investing/maturity-ladder` | The debt profile, refinancing walls, and the cost of extending. |
| `subskills/facility-covenants.md` | `investing/facility-covenants` | Maintenance and incurrence tests, and the headroom they leave. |
| `subskills/treasury-policy-record.md` | `investing/treasury-policy-record` | The written policy: limits, authority, instruments, and review triggers. |

## Status and honest limits

Treasury disclosure is partial: companies report the hedges they have, less often the policy that governs them, and rarely the sensitivity that would show how much is unhedged. Hedge accounting depends on documentation and testing that is not public, so the reported effect may differ from the economic one. Nothing here recommends a security, and a cash buffer judged adequate on a stable business may be far too small for a cyclical one, which is why the policy and the business have to be read together.
