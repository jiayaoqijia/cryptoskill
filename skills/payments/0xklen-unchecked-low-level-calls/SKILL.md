---
name: unchecked-low-level-calls
description: Use when a contract uses .call/.delegatecall/.send and does not check success, or uses transfer/send assumptions. Ensures every low-level call's return is handled and reverts on failure.
---

# Unchecked low-level call returns

A `.call` returns `(bool ok, bytes data)` and never reverts on failure — ignoring `ok` (or the bool from `send`) turns a failed transfer into a silent state divergence.

## Procedure

1. Find all low-level calls: `grep -nE '\.call\(|\.delegatecall\(|\.staticcall\(|\.send\(|address\(.*\)\.transfer' -r src/`.
2. For each, require the success flag to be checked and revert:

```solidity
(bool ok, bytes memory ret) = target.call(data);
require(ok, "call failed");
if (ret.length > 0) { /* decode */ }
```

3. Replace `address(x).transfer(y)` and `.send(y)` with `.call{value: y}("")` + a success check, or `payable(x).transfer` only for trusted EOAs; `transfer`/`send` forward 2300 gas and can fail silently on contracts.
4. For `.delegatecall`, verify the target is a trusted, immutable address — a user-supplied delegatecall target executes arbitrary code in your storage.
5. Check ERC-20 `transfer`/`transferFrom` returns the same way: use `SafeERC20.safeTransfer` (`grep -c 'safeTransfer' src/` should cover all token moves).
6. Confirm decode of returned data is length-checked: `abi.decode(ret, (uint256))` reverts on a short return; a manual `ret.length < 32` guard is explicit.
7. Check multicall/loop patterns: one failing leg in a `for` loop must revert the whole batch, not continue.
8. Verify `try/catch` usage: `catch` must not swallow the error without state rollback where the caller assumes success.
9. Test the failure branch: point the call at a contract that returns `false` or reverts, and assert the tx reverts.
10. Re-grep after fixes: `grep -nE '\.call\(' src/` should show every site with a `require(ok`.

## Pitfalls

- `token.transfer(a, b);` with the return ignored — a token that returns `false` (some proxies) leaves accounting updated but funds unmoved.
- `require(token.transfer(...))` reverting on USDT because the call has no return data; use `safeTransfer`.
- `payable(to).send(amount)` returning false and the code proceeding, so the ETH stays in the contract but the ledger says paid.
- `delegatecall` in a loop over user-supplied targets — one entry can `selfdestruct` the implementation.
- `try target.f() { } catch { }` with an empty catch: the outer function returns success while the inner action failed.

## Verification

    forge test --match-test "testCallFailure|testSafeTransfer" -vvvv

Pass: pointing the call at a failing target reverts the whole transaction, and `grep -nE '\.(call|send)\(' src/` shows no site lacking a success check.

Report each low-level call, whether the return is checked, and the delegatecall target trust level.
