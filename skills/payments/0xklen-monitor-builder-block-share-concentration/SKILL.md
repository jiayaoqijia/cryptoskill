---
name: monitor-builder-block-share-concentration
description: Use when assessing censorship or builder-centralisation risk: computing per-builder block share over a rolling window from relay bid traces, and flagging when one builder exceeds a concentration threshold.
---

# Monitor builder block share concentration

Block production concentrated in one or two builders is a liveness and censorship risk even when every individual bid is valid, so the metric that matters is the share of blocks each builder wins over a rolling window.

## Procedure

1. Pull the builder attribution for a window of blocks. Flashbots exposes received blocks and their builder pubkeys:

   ```bash
   curl -s "https://relay.flashbots.net/relay/v1/data/bidtraces/builder_blocks_received?limit=500" | \
     jq '[.[].builder_pubkey] | group_by(.) | map({builder:.[0], blocks:length}) | sort_by(-.blocks)'
   ```

2. Normalise the pubkeys to names using the community builder-label list; an unlabelled pubkey with a large share is worth investigating rather than ignoring.

3. Compute share per builder over 24 h and 7 d. A single builder above 40% of blocks, or the top two above 60%, is the concentration threshold used in most MEV dashboards — flag it.

4. Check the exclusion set: for a suspect builder, look at whether it ever includes transactions touching a known filtered address. A 45% builder that filters is a system-wide risk; a 45% builder that does not is only a diversity concern.

5. Compare the share to the relay mix. If one builder's share rose because a competing relay dropped out, the concentration is an artifact of relay availability, not builder behaviour.

6. Trend it: a builder rising 10 points over a week is the actionable signal. Plot share by day and look at the slope, not the level.

7. Tie it to your own transactions. Cross-reference your stuck transactions' missed blocks against the winning builder pubkeys to see whether concentration is already affecting you.

## Pitfalls

- Using a short window. A single block produced by an unlabelled builder is not concentration; you need hundreds of blocks.
- Double-counting: some relays report the same block twice with different metadata. Deduplicate by block number before counting.
- Attributing every unlabelled block to a single unknown builder; many small builders share the absence of a label.
- Ignoring that share is measured on received blocks, not all blocks; a builder that never submits to the relay is invisible here.
- Treating concentration as inherently bad without checking inclusion behaviour; diversity is a proxy, censorship is the harm.

## Verification

    curl -s "https://relay.flashbots.net/relay/v1/data/bidtraces/builder_blocks_received?limit=500" | jq '[.[].builder_pubkey] | group_by(.) | map({builder:.[0], blocks:length}) | sort_by(-.blocks) | .[0:5]'

Top builder share above 40% over the window confirms concentration. Report the top five builders, their shares, the window, and whether any filters.
