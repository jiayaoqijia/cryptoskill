---
name: publish-a-governance-transparency-report
description: Use when a DAO or delegate needs to publish a periodic governance report. Defines the metrics, pulls them from chain and subgraph, and keeps each figure reproducible.
---

# Publish a governance transparency report

A report whose numbers cannot be reproduced is marketing. Define each metric, cite the block range, and pull every figure from a query a reader can rerun.

## Procedure

1. Freeze the reporting window and its boundary blocks (first and last block of the quarter), then state them in the report.
2. Compute the proposal metrics from `ProposalCreated` and state transitions:
   - proposals submitted, executed, defeated, cancelled
   - median voting-period turnout as a fraction of quorum
   - time from propose to execute
   One `cast logs` pull per governor plus a group-by in Python.
3. Compute delegation metrics at the window's end snapshot: total delegated weight, top-5 share, number of active delegates (voted at least once in the window). Reuse the concentration method — do not eyeball the leaderboard.
4. Compute treasury flows: total inflow, total outflow, and ending balance per asset, from token `Transfer` logs involving the treasury address. Denominate in the asset and note the price source if you also quote USD.
5. For each metric, write the query or command that produced it and the block range directly beneath the figure.
6. Flag the limitations: off-chain Snapshot votes not reflected on-chain, proposals still pending, and any data source that failed.

7. Snapshot the exact query results to a file and commit it, so the report's numbers have a reproducible artefact.
8. Publish the methodology appendix even when short; a figure without a method invites dispute.
9. Diff the report against the previous one and explain every large change rather than presenting each in isolation.

## Pitfalls

- Quoting token-holder numbers from a dashboard without stating the snapshot block; the reader cannot reproduce it.
- Reporting "participation up" without a denominator; participation is a fraction, and the base changes with supply.
- Mixing on-chain and off-chain governance counts in one table so the totals double-count or contradict.
- Presenting treasury USD values without the price and timestamp used.
- Publishing a top-delegate leaderboard that merges the same actor's addresses; cluster before ranking.

- Averaging turnout across proposals of different sizes hides that a few huge votes carry the figure.
- Quoting one quarter's treasury outflow without the inflow makes net flow look like a haemorrhage.
- Counting a Snapshot signal and its on-chain execution as two governance events inflates the activity metric.

## Verification

    python3 report.py --from $START --to $END > report.md && grep -c "block" report.md
    # every figure should sit next to its block range and the command that produced it

Report the window blocks, each metric with its source query, and the stated limitations, all in the published file.
