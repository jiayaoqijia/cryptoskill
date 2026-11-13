---
name: ac-pension-risk-transfer
description: "The endgame of a defined-benefit pension: buy-ins and buy-outs, insurer pricing and what drives the quote, longevity swaps and their residual risk, partial transfers and phased de-risking, member option exercises and their cost, the accounting settlement effects, and the written transfer record. It explains the transaction mechanics and the pricing drivers; it never recommends an insurer and never gives actuarial advice. Use when asking \"pension risk transfer\", \"buy-in versus buy-out\", \"longevity swap\", \"bulk annuity\", \"insurer pricing\", \"pension de-risking transaction\", \"member options exercise\", \"settlement accounting\". Not for funding ratio and glide path policy (ac-liability-driven-investing), not for household annuity purchase (ac-retirement-and-drawdown), not for insurance coverage decisions (ac-insurance-and-risk-transfer)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Pension risk transfer

## Overview

A defined-benefit pension eventually stops being an investment problem and becomes a transaction: the liabilities are transferred to an insurer or hedged with a counterparty, and the plan's exposure ends or changes form. The decision is not whether to transfer — for most closed plans it is a matter of timing — but which instrument, at what price, and with what residual obligations left behind.

This skill covers the mechanics of that transaction: the difference between a buy-in and a buy-out, what an insurer's quote reflects, how a longevity swap transfers the risk without transferring the assets, how partial transfers and phased approaches work, and what member option exercises cost. The funding ratio and glide path belong to the liability-driven investing skill; this one starts where that policy becomes an execution.

Primary sources: <https://www.bis.org/> and <https://www.fca.org.uk/>.

## When to use

- When a plan is approaching a buy-in or buy-out transaction.
- When an insurer's quote needs decomposing into its drivers.
- When a longevity swap is being considered as an alternative.
- When member option exercises are likely to change the liability.

## When NOT to use

- For funding ratio arithmetic and glide path design (use ac-liability-driven-investing).
- For an individual's annuity purchase decision (use ac-retirement-and-drawdown).
- For general insurance coverage analysis (use ac-insurance-and-risk-transfer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/buy-in-versus-buy-out.md` | `investing/buy-in-versus-buy-out` | The insurer holds the assets versus the insurer takes the assets and the liabilities. |
| `subskills/insurer-pricing.md` | `investing/insurer-pricing` | What drives a bulk annuity quote, and which inputs the plan controls. |
| `subskills/longevity-swaps.md` | `investing/longevity-swaps` | Hedging longevity while keeping the assets, and the residual risks. |
| `subskills/partial-and-phased-transfers.md` | `investing/partial-and-phased-transfers` | Tranches, member selection, and phasing across market conditions. |
| `subskills/member-options.md` | `investing/member-options` | Option exercises, take-up assumptions, and their effect on the liability. |
| `subskills/settlement-accounting.md` | `investing/settlement-accounting` | What the transaction does to the sponsor's reported position. |
| `subskills/transfer-record.md` | `investing/transfer-record` | The written record: instrument, price drivers, residuals, and timeline. |

## Status and honest limits

Bulk annuity pricing is quoted rather than published, and the drivers described here are the ones that generally apply rather than the ones in any specific quote. Longevity swap documentation is bespoke and its residual risks are contractual. Nothing here recommends an insurer or a transaction, and every figure in a record should carry the date it was quoted, because a quote is a market statement that expires.
