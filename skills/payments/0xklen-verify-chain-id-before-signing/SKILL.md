---
name: verify-chain-id-before-signing
description: Use when signing a transaction or typed message, or after switching RPC endpoints. Reads chainId from the endpoint, compares it to the expected constant, and refuses to sign against a mismatched or lying RPC.
---

# Verify chain id before signing

An RPC can claim to be mainnet and serve testnet state, or a mis-set endpoint can send your valid signature into the void or onto the wrong chain. This skill pins the expected chain id and checks the live endpoint before the signature.

## Procedure

1. Write the expected chain id as a constant where the signing code can read it: 1 mainnet, 10 Optimism, 42161 Arbitrum One, 8453 Base, 137 Polygon, 11155111 Sepolia.
2. Read the endpoint's chain id at runtime and compare:
   `cast chain-id --rpc-url $RPC`
   `cast rpc eth_chainId --rpc-url $RPC` → returns the same value as hex.
3. Gate the sign call on the comparison. In viem:
   ```javascript
   const id = await client.getChainId();
   if (id !== 1) throw new Error(`refusing to sign on chain ${id}`);
   ```
4. Confirm the endpoint is the one you think: print the host, and reject any provider whose chain id disagrees with the expected for the URL you configured.
5. When multi-chain operations run in one process, carry the chain id alongside every account and payload; never rely on an ambient default.
6. Re-verify immediately after any RPC failover, because a backup endpoint may point at a different network.
7. Log the chain id with every signature so a later audit can prove which network each signature was meant for.

## Pitfalls

- A single endpoint is a single point of truth. A compromised or misconfigured RPC can report 1 while serving testnet state; cross-check with a second provider before a large signing.
- Chain id and network id (now removed from the spec) are not interchangeable; some tools still expose the old `net_version` and it can differ.
- Hardcoded chain ids in tests let a mainnet signing path pass CI; use the same constant the production path uses.
- Chain id 0 in a signing tool means "unspecified" and disables EIP-155; treat it as an error, not a default.
- A testnet chain id can be reused by a later testnet reset; a persisted signature aimed at the old chain id may collide.

## Verification

    cast chain-id --rpc-url $RPC && cast rpc eth_chainId --rpc-url $RPC
    # expect both to resolve to the same decimal chain id equal to your expected constant

Report the observed chain id from both calls and the expected constant, with the commands behind them.
