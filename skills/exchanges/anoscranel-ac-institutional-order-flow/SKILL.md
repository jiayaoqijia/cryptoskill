---
name: ac-institutional-order-flow
description: "Detecting institutional execution from the tape itself: block prints and off-book crossings, trade-size clustering and iceberg detection, order-book imbalance and spoofing tells, volume profile and the footprints of algorithmic execution, relative volume against a baseline, closing-auction and rebalance flows, and the written footprint record. It reads execution evidence in the data; it never infers who traded or recommends a position. Use when asking \"unusual volume\", \"iceberg order\", \"block print\", \"order book imbalance\", \"is someone accumulating\", \"footprint\", \"VWAP execution\", \"who is buying\". Not for disclosed positions (ac-institutional-positioning), not for operations and settlement plumbing (ac-institutional-operations), not for placing a single order (ac-order-execution)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Institutional order flow

## Overview

An institution executing a large order leaves a footprint even when the order is never displayed. The footprint is statistical rather than individual: trade sizes clustering at round lots, volume arriving in a pattern that repeats, the book thinning on one side and refilling, a print that crosses away from the displayed market. None of it names the participant, and all of it is evidence about how the order was executed.

This skill is about reading that evidence honestly. Each technique here produces a probability statement, not an identification: repeated 5,000-share prints suggest algorithmic execution, and they do not say who ran it or why. The distinctions that matter are between accumulation and distribution, between an order that is being worked patiently and one that is urgent, and between a real imbalance and a displayed one that will be pulled.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## When to use

- When unusual volume or trade patterns need explaining.
- When an order-book imbalance is being read as a signal.
- When a block print or an off-book crossing appears.
- When accumulation or distribution is being inferred from the tape.

## When NOT to use

- For filed positions and ownership data (use ac-institutional-positioning).
- For settlement, clearing and custody mechanics (use ac-institutional-operations).
- For order types, slicing and slippage on your own order (use ac-order-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/block-prints-and-crossings.md` | `investing/block-prints-and-crossings` | Off-book trades, dark pool prints, and what the price concession says. |
| `subskills/trade-size-clustering.md` | `investing/trade-size-clustering` | Round lots, repeated sizes, and the signature of algorithmic working. |
| `subskills/order-book-imbalance.md` | `investing/order-book-imbalance` | Depth imbalance, spoofing tells, and why displayed liquidity is not real liquidity. |
| `subskills/volume-profile-and-vwap.md` | `investing/volume-profile-and-vwap` | Where volume traded, VWAP bands, and the footprint of a benchmarked order. |
| `subskills/relative-volume.md` | `investing/relative-volume` | Volume against a time-of-day baseline rather than against yesterday. |
| `subskills/auction-and-rebalance-flows.md` | `investing/auction-and-rebalance-flows` | Closing auctions, index events, and the flows that arrive on a schedule. |
| `subskills/footprint-record.md` | `investing/footprint-record` | The written record: observation, method, confidence, and the alternative explanation. |

## Status and honest limits

Everything in this skill is inference from aggregated data, and the same tape pattern can be produced by opposite intentions. A cluster of large prints can be one institution accumulating or one liquidating into demand; a book that thins on the bid can precede a rally or a collapse. Every observation therefore needs an alternative explanation recorded beside it, and any conclusion stronger than "consistent with accumulation" is a conclusion the data does not support.
