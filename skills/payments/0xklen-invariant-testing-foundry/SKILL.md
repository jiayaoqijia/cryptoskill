---
name: invariant-testing-foundry
description: Use when a protocol has a system-wide property (solvency, supply conservation, exchange-rate monotonicity) that must hold across arbitrary call sequences. Writes stateful Foundry invariant tests with handlers.
---

# Invariant testing in Foundry

Invariant testing calls your contract in random sequences and checks a property after every call — it finds bugs that require state built over multiple transactions, which fuzzing cannot.

## Procedure

1. State each invariant as a boolean that must always hold:

```solidity
function invariant_solvent() public {
    assertGe(token.balanceOf(address(vault)), vault.totalDebt());
}
function invariant_supplyBacksShares() public {
    assertEq(vault.totalAssets(), depositToken.balanceOf(address(vault)));
}
```

2. Write a handler that bounds the actions the fuzzer may take, so sequences are realistic:

```solidity
contract Handler is Test {
    function deposit(uint256 amount) public {
        amount = bound(amount, 1, 1e24);
        deal(address(token), address(this), amount);
        vault.deposit(amount, address(this));
    }
}
```

3. Restrict calls to the handler, not the vault directly: `targetContract(address(handler))` in `setUp` — otherwise the fuzzer makes unpayable calls.
4. Configure depth and runs:

```toml
[invariant]
runs = 256
depth = 50
fail_on_revert = false
call_override = false
```

5. Exclude unpayable selectors with `targetSelector(FuzzSelector({addr: addr, selectors: sels}))`.
6. Add tolerance for dust in invariants: `assertApproxEqAbs(..., 2)`.
7. Reproduce failures with the exported sequence: Foundry prints the call sequence; replay with `forge test --match-test invariant_x -vvvv`.
8. Model at least three actors (`address(0x1)..(0x3)`) so multi-user interactions are explored.
9. Run longer in CI: `forge test --match-test invariant --fuzz-runs 5000` overnight.
10. Keep invariants in a dedicated `test/invariant/` dir so they are not confused with unit tests.

## Pitfalls

- `fail_on_revert = true` with a handler that can revert on valid-but-unpayable calls aborts runs; handle the revert inside the handler instead.
- Targeting the vault directly rather than a handler, so the fuzzer passes `type(uint256).max` and everything reverts.
- An invariant that is tautological (`x == x`) or reads only constants — it passes forever and proves nothing.
- Forgetting that `msg.sender` in the invariant test is the test contract; a rule that only the owner may call is never exercised unless the handler pranks.
- Too shallow depth (default 15) to build the state the bug needs.

## Verification

    forge test --match-test invariant -vv

Pass: `invariant_x` runs the configured number of sequences and depth with no counterexample. On failure Foundry prints the exact call sequence to replay.

Report each invariant, its runs/depth, and the sequence when one breaks.
