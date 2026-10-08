---
name: mainnet-fork-testing
description: Use when a test must run against real deployed contracts, liquidity or oracle state. Configures Foundry fork tests with pinned blocks, realistic funding via whale impersonation, and reproducible RPC.
---

# Mainnet fork testing

Fork tests are only evidence when the block number and the fork source are pinned — an unpinned fork silently changes every run and can make a passing test meaningless.

## Procedure

1. Set a pinning block and RPC in `foundry.toml`:

```toml
[rpc_endpoints]
mainnet = "${ETH_RPC_URL}"
```

and in the test:

```solidity
uint256 constant BLOCK = 21_000_000;
function setUp() public {
    vm.createSelectFork(vm.envString("ETH_RPC_URL"), BLOCK);
}
```

2. Fund an account by impersonating a whale, not by `deal` of a rebasing token:

```solidity
address whale = 0x...; // top holder from Etherscan
vm.startPrank(whale);
IERC20(USDC).transfer(address(this), 5_000_000e6);
vm.stopPrank();
```

3. Prefer `deal(address(token), addr, amount)` for standard tokens; use whale impersonation when the token's share accounting must stay consistent (stETH).
4. Verify the fork is live before acting: assert a known balance, e.g. `assertGt(IERC20(USDC).balanceOf(whale), 0)`.
5. Use `vm.createSelectFork` (not `vm.createFork` unless juggling multiple) so `selectFork` can switch chains mid-test.
6. Set `--fork-block-number` explicitly in the CLI too: `forge test --fork-url $ETH_RPC_URL --fork-block-number 21000000`.
7. Cache the fork locally to avoid RPC rate limits: `anvil --fork-url $ETH_RPC_URL --fork-block-number 21000000` then point tests at `http://127.0.0.1:8545`.
8. For multi-chain tests, pick L2 RPCs and pin each block separately.
9. Silence noise: use `vm.recordLogs()`/`vm.getRecordedLogs()` to assert events rather than scraping traces.
10. Never assert on a value that changes every block (e.g. `block.timestamp`-derived rewards) without pinning or tolerance.

## Pitfalls

- Unpinned forks make CI non-reproducible; a test that passed last month fails after a live upgrade.
- Free RPC endpoints rate-limit and fail mid-suite; use a paid key or a local Anvil cache.
- `deal` on a rebasing token breaks its internal share accounting and gives fake balances; use impersonation.
- Forgetting that a proxy address's *implementation* may be upgraded at the pinned block, so slot reads differ from today.
- Assuming the fork includes pending mempool state — it reflects only mined blocks at the pinned height.

## Verification

    forge test --match-test "Fork" --fork-url $ETH_RPC_URL --fork-block-number 21000000 -vv

Pass: every fork test reports against the pinned block and the same block hash; running twice gives identical results.

Report the fork block, the contracts under test, and the outcome.
