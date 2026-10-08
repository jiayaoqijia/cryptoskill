---
name: foundry-fuzz-testing
description: Use when writing or reviewing Foundry fuzz tests to find edge cases in arithmetic and state transitions. Sets runs, bound, and asserts properties that must hold for all inputs.
---

# Foundry fuzz testing

A fuzz test states a property and lets Foundry search inputs for a counterexample; the value is in the property chosen, not the number of runs.

## Procedure

1. Write stateless fuzz tests with one named property per test:

```solidity
function testFuzz_depositThenWithdraw(uint96 amount) public {
    amount = uint96(bound(amount, 1, 1e30));
    token.mint(address(this), amount);
    vault.deposit(amount);
    vault.withdraw(vault.balanceOf(address(this)));
    assertGe(token.balanceOf(address(this)), amount - 1); // rounding
}
```

2. Constrain inputs with `bound(x, lo, hi)` or `vm.assume`; unbounded uints mostly revert and waste runs.
3. Configure runs in `foundry.toml`:

```toml
[fuzz]
runs = 1000
max_test_rejects = 100000
fail_on_revert = true
```

4. Use `fail_on_revert = true` so a revert is a counterexample, not a skip — but only once inputs are bound.
5. Add `/// forge-config: default.fuzz.runs = 10000` for hot properties in CI.
6. Assert *relations*, not exact values: monotonicity (`f(a) <= f(b)` when `a <= b`), conservation (`sum(balances) == totalSupply`), idempotence of views.
7. Reproduce a failure deterministically with the emitted seed: `forge test --match-test testFuzz_x --fuzz-seed 0x1234`.
8. Check stateful interplay by moving invariants to an invariant test rather than a fuzz test.
9. Run under the optimiser and without (`forge test --no-optimize`) to catch different overflow paths.
10. Keep a corpus: Foundry writes failing inputs to `cache/fuzz/`; commit them so the fix is regression-tested.

## Pitfalls

- `vm.assume` on a narrow condition rejects most inputs and slows the run to a crawl; use `bound`.
- Fuzzing a getter that cannot fail gives false confidence — fuzz state-changing paths.
- `fail_on_revert = false` (the default) hides reverts, so an assertion after a revert is never reached.
- Testing exact equality on a value that legitimately rounds; use `assertApproxEqAbs(..., 1)`.
- Addresses from the fuzzer can be `address(0)`; `assume(addr != address(0))` before using them.

## Verification

    forge test --match-test "testFuzz" -vv

Pass: all fuzz tests report the configured run count with no counterexample; a shrink report shows the minimal failing input when one exists.

Report the properties fuzzed, the run count, and any counterexample with its seed.
