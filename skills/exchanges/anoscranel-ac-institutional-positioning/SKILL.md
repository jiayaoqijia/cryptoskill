---
name: ac-institutional-positioning
description: "Reading what institutions must disclose about their positions and what it cannot tell you: 13F filings and their lag, Form 4 insider transactions, short interest and failure-to-deliver, CFTC Commitments of Traders, block trades and 13D activist stakes, institutional ownership data and its reconstruction, and the written positioning record. It reads disclosed positions as evidence with dates; it never infers intent or recommends a trade. Use when asking \"13F\", \"follow the institutions\", \"Commitments of Traders\", \"who holds this stock\", \"insider buying\", \"short interest report\", \"13D activist\", \"smart money holdings\". Not for reading the tape institutions leave (ac-institutional-order-flow), not for operations and settlement mechanics (ac-institutional-operations), not for single-name due diligence (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Institutional positioning

## Overview

Large positions are disclosed on schedules, and the schedules are the only public window into who holds what. Each has its own filing trigger, its own lag, and its own blind spots: a quarterly holdings report that arrives six weeks after the quarter ends, an insider form due two business days after a transaction, a weekly aggregate of futures positions by trader category, and a short interest figure that is published twice a month without naming who is short.

Reading them well means treating each as evidence with a timestamp and a coverage limit, not as a signal without one. The craft is knowing which disclosure answers which question, how stale the answer is, and what fraction of the market it actually covers. This skill is about those disclosures; the execution footprints institutions leave in the tape are a separate skill, and so is the operations plumbing.

Primary sources: <https://www.sec.gov/investor> and <https://www.cftc.gov/>.

## When to use

- When a position is being attributed to institutions and the disclosure needs checking.
- When insider transactions, short interest, or futures positioning are cited as evidence.
- When a 13F or 13D filing is being read for what it implies.
- When the ownership data on a security need reconstructing from filings.

## When NOT to use

- For inferring accumulation from order flow and tape (use ac-institutional-order-flow).
- For settlement, custody and clearing mechanics (use ac-institutional-operations).
- For the investment case on a company (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/holdings-disclosures.md` | `investing/holdings-disclosures` | 13F scope, the 45-day lag, and what a long-only snapshot misses. |
| `subskills/insider-transactions.md` | `investing/insider-transactions` | Form 4 timing, codes, and distinguishing signal from compensation. |
| `subskills/short-interest-and-fails.md` | `investing/short-interest-and-fails` | Twice-monthly short interest, days to cover, and fail-to-deliver data. |
| `subskills/commitments-of-traders.md` | `investing/commitments-of-traders` | CFTC categories, net positioning, and the commercial-versus-fund split. |
| `subskills/blocks-and-activist-stakes.md` | `investing/blocks-and-activist-stakes` | Block prints, 13D and 13G thresholds, and what an activist filing announces. |
| `subskills/ownership-reconstruction.md` | `investing/ownership-reconstruction` | Combining filings into a holding picture, and the double-counting that breaks it. |
| `subskills/positioning-record.md` | `investing/positioning-record` | The written record: which disclosure, which date, which coverage limit. |

## Status and honest limits

Every disclosure in this skill is late, partial, or both. A 13F says what a manager held at a quarter end and was filed weeks later; short interest is a snapshot that can be a month old when it is quoted; Commitments of Traders aggregates categories that contain heterogeneous participants. Any conclusion drawn from these sources inherits their lag and their coverage, and the record must state both. Nothing here infers intent, and a position attributed to "institutions" without naming the filing and its date has not been attributed at all.
