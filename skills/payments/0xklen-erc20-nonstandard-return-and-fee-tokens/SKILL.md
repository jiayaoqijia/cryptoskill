---
name: erc20-nonstandard-return-and-fee-tokens
description: Use when a contract interacts with external ERC-20 tokens and assumes transfer/transferFrom return a bool. Handles non-returning tokens (USDT), fee-on-transfer and rebasing tokens safely.
---

# ERC-20 non-standard quirks

Assuming a token returns `true` from `transfer` or that `amount` sent equals `amount` received breaks real integrations — USDT returns nothing, and fee/rebasing tokens change balances underneath you.

## Procedure

1. Find every token interaction: `grep -nE '\.transfer\(|\.transferFrom\(|\.approve\(|safeTransfer|balanceOf\(' -r src/`.
2. Replace raw `.transfer(` with `SafeERC20.safeTransfer` (OpenZeppelin), which tolerates a missing return value and reverts on `false`:

```solidity
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;
token.safeTransfer(to, amount);
```

3. For tokens that deduct a fee on transfer, measure the delta, never the argument:

```solidity
uint256 before = token.balanceOf(address(this));
token.safeTransferFrom(user, address(this), amount);
uint256 received = token.balanceOf(address(this)) - before; // use `received`, not amount
```

4. For rebasing tokens (stETH, aTokens), never store a raw `balanceOf` snapshot as an accounting constant; track shares or use the wrapped variant.
5. Check approvals: set to `type(uint256).max` only for trusted spenders, or reset to 0 first for tokens that require it (USDT reverts on a non-zero-to-non-zero `approve`).
6. Test with real token addresses on a fork: USDT, USDC (a proxy, 6 decimals), and a fee-on-transfer mock.
7. Decode decimals at runtime if the token list is open: `IERC20Metadata(token).decimals()`.
8. Verify the token cannot be reentered: some ERC-20s (ERC-777) call hooks on `transfer`.
9. Check `balanceOf(this) >= sum(accounting)` after every state transition — a fee token silently breaks this invariant.
10. Run the suite against three token mocks: standard, non-returning, fee-on-transfer.

## Pitfalls

- Solidity that stores `amount` while the fee token delivered `amount - fee`, so the contract is insolvent by the fee each time.
- `require(token.transfer(...))` reverting on USDT because the call returns no data — use safeTransfer.
- Assuming `transferFrom` succeeded because it did not revert; Vyper and some proxies return `false` silently.
- Double-counting when a rebase increases `balanceOf` and the contract also credits a reward.
- Approving an external router to `type(uint256).max` on a token whose `approve` is itself malicious.

## Verification

    forge test --match-test "testTokenCompat" -vvv

Pass: the fee-token mock shows the contract's internal accounting equal to its actual `balanceOf` after transfer; the non-returning mock does not revert.

Report every token interaction, whether it uses safeTransfer, and the fee/rebasing handling.
