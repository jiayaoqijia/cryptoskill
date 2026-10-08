---
name: model-flash-loan-attacks
description: Use when assessing whether a protocol's invariants can be broken with capital that is borrowed and repaid in one transaction. Enumerates atomic-profit paths and writes a Foundry PoC using a fork.
---

# Model flash-loan attacks

Any exploit whose profit is realised within a single transaction needs no attacker capital — so every state transition must be checked against an atomic borrow-attack, not a funded one.

## Procedure

1. Identify primitives an attacker can move atomically: AMM swaps, liquidations, oracle reads, governance vote snapshots, reward claims.
2. For each, ask: can the attacker borrow X, move price/state, extract Y, repay X, with Y > fee? If yes it is a flash-loan candidate.
3. List the flows that reference block-scoped state: `grep -nE 'block.timestamp|totalSupply\(\)|getReserves|balanceOf' -r src/`.
4. Verify the attack is *atomic*: no step may depend on a prior block.
5. Write a PoC against `--fork-url $ETH_RPC_URL` using an existing lender:

```solidity
function testFlashLoanLiquidate() public {
    uint256[] memory amounts = new uint256[](1);
    amounts[0] = 30_000_000e6;
    address[] memory tokens = new address[](1);
    tokens[0] = USDC;
    aave.flashLoan(address(this), tokens, amounts, "");
}
```

6. In `executeOperation`, run the attack steps; in `_repay`, verify `profitAfterRepay > 0` with `assertGt`.
7. Fund nothing: any `deal()` in the PoC is a smell — the whole point is looped capital.
8. Check reentrancy coupling: the flash-loan callback is itself an external call the victim must survive.
9. Verify the max single-block borrow on the mainnet pool (`cast call <aavePool> "getReserveData(address)"` or the pool TVL); if borrowable >= attack size the attack is live.
10. Report the path, the borrowed amount, the extracted profit, and the test.

## Pitfalls

- Modelling only single-pool flash loans and missing the flash-mint (ERC-3156) or Balancer zero-fee variant that removes the fee constraint entirely.
- Missing that the victim's own accounting can be the profit source (inflating share price) rather than an external pool.
- Forgetting repayment: a PoC that "works" because it never repays is not an exploit.
- Governance flash-loans: a snapshot taken mid-transaction (delegate + propose + vote in one block) can pass a proposal without holding tokens.

## Verification

    forge test --match-test testFlashLoan -vvv --fork-url $ETH_RPC_URL

Pass: the final assertion `profit > borrowed` holds and the trace shows repayment. A run that reverts at the lender's `_repay` means no atomic profit exists.

Report the borrowed size, profit, and the flow that leaked the value.
