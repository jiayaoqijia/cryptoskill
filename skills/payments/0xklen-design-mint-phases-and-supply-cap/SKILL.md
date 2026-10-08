---
name: design-mint-phases-and-supply-cap
description: Use when designing or reviewing an NFT mint with phases, caps, or per-wallet limits. Checks supply arithmetic, phase gating, and oversell protection before mainnet.
---

# Design mint phases and supply caps

A mint that can oversell, miscount allowlist spots, or open a phase early is how collections end with more tokens than promised or none sold at all.

## Procedure

1. Enumerate the phases and their caps — allowlist, public, team, reserve — and write the invariant down: `sum(phaseCaps) <= maxSupply`.

2. Read the live constants:

   ```
   cast call $NFT "maxSupply()(uint256)" --rpc-url $RPC
   cast call $NFT "totalSupply()(uint256)" --rpc-url $RPC
   cast call $NFT "mintPrice()(uint256)" --rpc-url $RPC
   ```

3. Confirm the per-wallet cap is enforced in the contract before minting, not in the front end:

   ```
   cast call $NFT "minted(address)(uint256)" $BUYER --rpc-url $RPC
   ```

4. Verify phase gating uses block time and the window is closed on both ends:

   ```
   grep -nE 'block.timestamp|startTime|endTime|currentPhase' src/*.sol
   ```

   Require a `require(block.timestamp >= start && block.timestamp <= end)` pair; a missing upper bound lets a phase run forever.

5. Confirm the team/reserve allocation cannot exceed its cap and does not also count against the public cap.

6. Test oversell: `forge test --match-test testMintBeyondSupply -vvvv` — the last successful mint must leave `totalSupply() == maxSupply`, and the next must revert.

7. Simulate a full mint on a fork before launch:

   ```
   forge script script/MintSim.s.sol --fork-url $RPC --sender $WHALE
   ```

8. Check refunds: if a mint can fail mid-transaction, the ETH must revert with it, never remain stuck in the contract.

## Pitfalls

- Incrementing `totalSupply` after `_safeMint` lets a reentrant receiver callback double-mint.
- Per-phase caps that do not sum to cover the public cap let reserve tokens silently oversell.
- A `startTime` set in local time or left at a testnet value opens the wrong phase on mainnet.
- A `mintPrice` mutable by owner after allowlist signups re-prices users who signed up in good faith.
- Setting the reveal timestamp equal to the mint timestamp leaks metadata before the mint ends.

## Verification

    forge test --match-test "testMintBeyondSupply|testPhaseWindow" -vvvv

Pass: oversell reverts, the last mint fills exactly `maxSupply`, and the phase windows are disjoint. Report the phase table, the caps, and the oversell test result.
