---
name: verify-token-trait-rarity
description: Use when marketplaces advertise trait rarity for an NFT collection and you need the underlying counts. Recomputes rarity from the metadata and catches duplicates and null traits that falsify it.
---

# Verify trait rarity against the metadata

Marketplaces show rarity derived from the metadata; if the metadata is wrong or duplicated, the advertised rarity is wrong and the floor prices built around "rare" traits evaporate.

## Procedure

1. Fetch metadata for a revealed collection straight from a content address:

   ```
   for i in $(seq 1 $N); do curl -sL "https://ipfs.io/ipfs/$CID/$i.json" -o "meta/$i.json"; done
   ```

2. Count each trait and value:

   ```
   jq -r '.attributes[] | "\(.trait_type)|\(.value)"' meta/*.json | sort | uniq -c | sort -rn > trait-counts.txt
   ```

3. Divide each count by the total tokens for the trait percentage; write it next to the marketplace's claimed rarity.

4. Look for duplicated metadata or images that inflate counts:

   ```
   sha256sum meta/*.json | sort | uniq -d
   ```

5. If traits are generated on-chain, read the token's seed and reproduce the pick yourself rather than trusting the served JSON.

6. Spot-check that `tokenURI` returns the file you counted:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 42 --rpc-url $RPC
   ```

7. Flag any value with count 1 not advertised as a 1/1, and any empty or null attribute value that rarity tools silently drop.

## Pitfalls

- Counting only revealed metadata misses placeholder rows if the reveal is partial.
- An attribute value of `""` or `null` is counted by some tools as a real trait, inflating rarity.
- Case mismatches ("Blue" vs "blue") split one value into two, doubling its apparent rarity.
- Marketplace rarity is a snapshot and drifts from the live metadata as collections burn or migrate.
- Duplicate CIDs for different token ids are a generator bug, not a rarity feature.

## Verification

    jq -r '.attributes[] | "\(.trait_type)|\(.value)"' meta/*.json | sort | uniq -c | sort -rn | head

Pass: the counts sum to `totalSupply` for each trait type, and no unexpected duplicate metadata hashes appear. Report the top traits, any duplicate metadata, and the ids spot-checked against `tokenURI`.
