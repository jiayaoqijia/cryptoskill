---
name: read-only-reentrancy
description: Use when a protocol reads another contract's view function (price, virtual price, getReserves) and that contract's state can be mid-update. Detects read-only reentrancy where a stale read passes checks the real state would fail.
---

# Read-only reentrancy

A view function can be read by a third protocol in the middle of a state transition, returning a value that satisfies a check the completed state would reject — no state is re-entered, only a number read.

## Procedure

1. Find view functions other protocols consume as prices or balances: `grep -nE 'function get.*\) .*view|getVirtualPrice|getReserves|pricePerShare|convertToAssets' -r src/`.
2. Check whether the view returns a value derived from `address(this).balance` or `asset.balanceOf(address(this))` — both change *during* an incoming transfer, before the hook returns.
3. Trace: attacker calls the victim's `withdraw` → victim calls the attacker's callback → attacker (as a second protocol) reads `victim.getRate()` → gets a manipulated value → borrows against it.
4. Confirm the vulnerable window: the balance is sent before internal accounting is updated (`grep -n -A3 'safeTransfer' src/Vault.sol`).
5. Reproduce with a mock integrator that reads the victim from its hook:

```solidity
function onERC1155Received(...) external returns (bytes4) {
    uint rate = victim.getRate();        // stale/manipulated
    lending.borrow(rate * 2);            // uses the wrong price
    return this.onERC1155Received.selector;
}
```

6. Verify fix pattern A: a `nonReentrantView` modifier (OpenZeppelin `ReentrancyGuard` exposes `nonReentrantView`) on the price getter.
7. Verify fix pattern B: compute the rate from internally tracked shares, not `balanceOf`, so a transfer cannot move the value.
8. Check that Balancer/Curve-style `getRate` calls used by lending protocols are wrapped in a reentrancy check by the *reader*.
9. Fuzz the ordering: assert `getRate()` is constant across a full deposit/withdraw cycle when called from a hook.
10. Document which integrators read the view and whether they guard it.

## Pitfalls

- Only checking state-mutating reentrancy and missing a view that feeds a *third* protocol.
- Assuming `nonReentrant` on the mutation is enough: the reader is a different contract with a different guard slot.
- `convertToAssets` reading `totalAssets() == balanceOf(this)` — donating mid-callback shifts it.
- ERC-1155/721 hooks firing after a `safeTransferFrom` in the same function that also moves value, exposing the window.
- Reading `block.timestamp`-based rates that change within the reentrant frame.

## Verification

    forge test --match-test "testReadOnlyReentrancy" -vvvv

Pass: the integrator's borrow reverts or uses the correct value after the guard is added; the unguarded build shows the manipulated `getRate()` in the trace.

Report the view function, the integrator, and the manipulated value observed mid-callback.
