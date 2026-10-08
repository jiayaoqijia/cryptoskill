---
name: verify-metadata-uri-permanence
description: Use when reviewing an NFT's tokenURI or baseURI to decide whether the artwork survives the loss of a server. Classifies the URI scheme and finds any owner control over the metadata.
---

# Verify token URI permanence

`tokenURI` can be `http`, `ipfs`, `ar`, or `data:` — only some survive the loss of a server, and a mutable `baseURI` behind an owner setter keeps every token hostage.

## Procedure

1. Read the raw URI and the base construction:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC
   cast call $NFT "baseURI()(string)" --rpc-url $RPC
   ```

2. Classify the scheme. `data:application/json;base64,` is fully on-chain; `ipfs://`/`ar://` is content-addressed; `https://` depends on a domain that can lapse or be seized.

3. For an `https://` URI, resolve DNS and record registrar expiry:

   ```
   dig +short example.com
   whois example.com | grep -iE 'expiry|expiration'
   ```

4. Find the setter and its access control:

   ```
   cast call $NFT "owner()(address)" --rpc-url $RPC
   grep -nE 'function setBaseURI|function setTokenURI|function updateBaseURI|function freezeMetadata' src/*.sol
   ```

   An `onlyOwner` `setBaseURI` means the owner can swap all metadata; a one-way `freezeMetadata()` with an event is the durable pattern.

5. For `data:` URIs, decode and confirm the media is embedded, not linked:

   ```
   cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC \
     | sed 's/^data:application\/json;base64,//' | base64 -d | jq -r '.image' | head -c 80
   ```

6. Check whether the URI is stored per token or computed from `tokenId`. A computed URI is compact but still depends on whatever the derivation reads on-chain.

## Pitfalls

- `ipfs://ipfs/Qm...` (double scheme) resolves in some wallets and silently fails in others.
- A `baseURI` with no trailing `/` concatenates wrongly and 404s every token.
- `renounceOwnership()` does not freeze an already-mutable URI if the store sits behind a proxy admin with upgrade rights.
- A `data:` JSON that references an external font or image URL is not actually on-chain.
- Explorers show a cached metadata image; always read `tokenURI` from the contract, never from the marketplace page.

## Verification

    cast call $NFT "tokenURI(uint256)(string)" 1 --rpc-url $RPC
    cast call $NFT "baseURI()(string)" --rpc-url $RPC

Pass: the scheme is `data:`, `ipfs:` or `ar:` AND no reachable setter can change it, or the setter is one-way and already called. Report the scheme, the storage model (per-token vs computed), and who holds the change key.
