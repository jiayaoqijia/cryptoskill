---
name: verify-contract-address-matches-project
description: Use when someone gives you a contract address and claims it is the real project (token, router, vault) and you must confirm or reject it before interacting.
---

# Verify a contract address is the project

A wrong address is indistinguishable from a right one by eye, and one changed hex character
sends funds to a lookalike. Prove the address is canonical from at least two independent
sources before any approval, transfer or integration.

## Procedure

1. Confirm the chain and that bytecode exists. `0x` output means EOA or nothing deployed.

       cast code 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --rpc-url $ETH_RPC | head -c 4

   Any result other than `0x` is a contract; capture the full code hash:

       cast code $ADDR --rpc-url $ETH_RPC | cast keccak

2. Read on-chain identity fields and record them verbatim.

       cast call $ADDR "name()(string)"    --rpc-url $ETH_RPC
       cast call $ADDR "symbol()(string)"  --rpc-url $ETH_RPC
       cast call $ADDR "decimals()(uint8)" --rpc-url $ETH_RPC
       cast call $ADDR "totalSupply()(uint256)" --rpc-url $ETH_RPC

3. Find the deployer and creation transaction. A contract creation tx has `to: null`; the
   `from` is the deployer. Check the deployer against the project's known deployer/treasury.

       cast tx $CREATION_TX --rpc-url $ETH_RPC --json | jq -r '.from, .to, .blockNumber'

   If the project ran a CREATE2 factory, the deployer will be that factory (e.g.
   0x4e59b44847b379578588920cA78FbF26c0B4956C) — not proof by itself.

4. Cross-check the address in the project's own primary sources: official docs URL, the
   GitHub repo's `deployments/` or `broadcast/` artifacts, and the block explorer's
   verified contract label. Ignore addresses pasted in DMs, tweets, or token-list sites.
5. Compare the checksummed form. `cast` prints EIP-55; a mismatched checksum in a UI is a
   red flag for a copy-pasted mutant address. Normalise with:

       cast to-check-sum-address $ADDR

6. If the contract advertises a proxy, resolve the implementation before trusting getters —
   see `read-proxy-implementation-slot`.

## Pitfalls

- Vanity lookalikes: `0x...dead` vs `0x...deAd`, or the same first 4 and last 4 characters.
  Always compare the full 42-character string, not a truncated display.
- A block-explorer search result labelled with the right token *name* is not the right token;
  anyone can deploy a contract with `symbol() == "USDC"`.
- The "same address on every chain" assumption is false unless the project used CREATE2 with
  identical initcode. Check `cast code` on each chain separately.
- Token-list aggregators and price sites are lagging and get poisoned; treat them as hints,
  not evidence.
- An address that is verified and correct today can still be a proxy whose implementation was
  swapped to something malicious yesterday.

## Verification

    cast code $ADDR --rpc-url $ETH_RPC | head -c 4        # not 0x
    cast call $ADDR "symbol()(string)" --rpc-url $ETH_RPC
    cast tx $CREATION_TX --json | jq -r '.from'

Report the symbol, deployer, creation tx and the two independent sources that agree, e.g.
"0xA0b8…eB48: symbol USDC, deployed by 0x… at block 6082465, matches Etherscan label and the
Circle docs address page."
