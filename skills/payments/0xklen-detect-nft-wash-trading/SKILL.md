---
name: detect-nft-wash-trading
description: Use when a collection's volume or ranking looks inflated and you need to know if it is real. Finds closed trading loops between related wallets before trusting volume signals.
---

# Detect NFT wash trading

Volume built by a wallet trading with itself inflates ranking and price signals; find the closed loops before trusting a collection's headline volume.

## Procedure

1. Pull the collection's transfer events into a file:

   ```
   cast logs --address $NFT "Transfer(address,address,uint256)" \
     --from-block $START --to-block $END --json > transfers.json
   ```

2. Build buyer-to-seller pairs and count repeated pairs:

   ```
   jq -r '.[] | [.topics[1],.topics[2],.topics[3]] | @tsv' transfers.json | sort | uniq -c | sort -rn | head
   ```

3. Score wallets by in-degree and out-degree. A ring has wallets that repeatedly sell to and buy from the same counterparties with low net ETH movement.

4. Cross-check the price paid. Two addresses swapping a token for a deliberately high amount, graded the same day with no third party, is the classic pattern.

5. Compute the share of volume from the top counterparty pairs. If more than ~30% comes from self-dealing loops, the headline number is not organic.

6. Trace funding convergence — where the trading wallets got gas:

   ```
   cast receipt $TX --rpc-url $RPC | jq '.from'
   ```

   Follow the first inbound ETH with an explorer trace; a common funder links the ring.

7. Require, before calling it a wash, that the loop is within a short window and on matching token ids.

## Pitfalls

- Blur/OpenSea bid walls generate many transfers that resemble wash trades but are legitimate accepted bids.
- A collector buying back a token they once sold is not a wash trade — look for repeated loops, not one round trip.
- Volume high in token count but flat in ETH is more suspicious than both high, because the ETH fee cost of real wash trading is high.
- Marketplace-custodied transfers show the marketplace as sender, hiding the real parties.
- Self-transfers (`from == to`, e.g. cold to hot) are not wash trades but pollute the pairing.

## Verification

    jq -r '.[] | [.topics[1],.topics[2],.topics[3]] | @tsv' transfers.json | sort | uniq -c | sort -rn | head

Pass: top counterparty pairs account for a plausible share of volume and no single ring exceeds ~10% without an explanation. Report the top pairs, their volume share, and the token ids involved.
