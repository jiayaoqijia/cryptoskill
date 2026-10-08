---
name: verify-builder-censorship-of-a-transaction
description: Use when a valid transaction fails to be included across many blocks and you suspect builder-level censorship. Covers retrying across relays, checking builder diversity, and neutralizing censorship with an OFAC-safe relay.
---

# Verify builder censorship of a transaction

High tips do not force inclusion when the builder constructing the block is filtering your transaction for policy or a private agreement; the only proof is a valid transaction that overpays and still misses block after block.

## Procedure

1. Rule out the boring causes first. Confirm the transaction is valid, funded, correctly nonced, and above the current base fee. A stuck nonce, not censorship, explains most stalls.

   ```bash
   cast nonce $ADDR --rpc-url $RPC && cast balance $ADDR --rpc-url $RPC
   ```

2. Track inclusion attempts across at least 20 blocks. Record the tip offered versus the block's median clearing tip. If your tip is in the top decile and you still miss 20 blocks, filter for something structural rather than fee-related.

3. Check which builder produced each block. If the same builder dominates the range where you are missing, the failure is concentrated, not random:

   ```bash
   curl -s https://relay.flashbots.net/relay/v1/data/bidtraces/builder_blocks_received?limit=20
   ```

4. Retarget through a relay that does not share the suspected builder's policy. Submit the same signed transaction as a bundle to a neutral relay and to a censorship-resistant relay; if it lands only via the second, that isolates the filtering builder.

5. Compare with a control: send an identical transaction that is trivially includable (no blacklisted addresses, no sanctioned interactors). If the control lands with a lower tip, the filter is on the content of yours, not the market.

6. Look at whether the filtering correlates with a read of a specific list. A transaction that touches a mixer or a sanctioned address and stalls while otherwise-identical flow lands is policy filtering, not congestion.

7. Record blocks-missed, builders-seen, and the relay that first includes it. That triple is the evidence; a single miss is not.

## Pitfalls

- Calling it censorship because your tip was high. A high tip loses to a higher bid inside a bundle; ordering is not fee-only.
- Testing during a burst of organic MEV where the block is full of profitable bundles; you will miss for market reasons, not filtering.
- Assuming a builder censors everything from an address. Filters are often per-interaction, not per-sender.
- Forgetting that a relay can censor by dropping your submission before any builder sees it; check the sendFor result, not just inclusion.
- Concluding from one block. Censorship is a pattern across many blocks by a concentrated builder set.

## Verification

    curl -s "https://relay.flashbots.net/relay/v1/data/bidtraces/builder_blocks_received?limit=20" | jq '[.[].builder_pubkey] | group_by(.) | map({b:.[0], n:length})'

A single builder responsible for the misses, confirmed by the same tx landing through a neutral relay, is censorship. Report missed blocks, dominant builder, and the relay that included it.
