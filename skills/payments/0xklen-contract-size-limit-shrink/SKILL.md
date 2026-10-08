---
name: contract-size-limit-shrink
description: Use when a contract fails to deploy with 'max code size exceeded' or runs close to the 24576-byte limit. Measures deployed size and applies concrete shrink techniques.
---

# Contract size limit (EIP-170)

Ethereum caps deployed bytecode at 24,576 bytes, so a contract that compiles but exceeds it cannot be deployed — measure early and shrink deliberately.

## Procedure

1. Measure: `forge build --sizes` lists runtime size per contract; anything over 24,576 fails.
2. Identify the offenders and their margin:

```
forge build --sizes | awk '$2 > 20000'
```

3. Enable the optimiser with runs tuned for size: `optimizer_runs = 200` (lower = smaller) in `foundry.toml`, then `via_ir = true` for deeper optimisation.
4. Convert `require(cond, "long string")` to custom errors — each string costs ~32 bytes:

```solidity
error Unauthorized();
...
if (msg.sender != owner) revert Unauthorized();
```

5. Extract logic into a library with `external` (not `internal`) functions so its code lives separately, or split into facets/modules.
6. Remove unused imports, generated getters for `public` state (use `private` + an explicit getter only where needed), and duplicate constant strings.
7. Turn on the compiler's `revertStrings = "strip"` only for interfaces where revert data is not needed.
8. Consider a linked library (`external` library → delegatecall) or a minimal-proxy factory for many identical instances.
9. Rebuild and diff: `forge build --sizes | grep MyContract` before and after each change.
10. Verify the final deployed bytecode size on-chain after deploy: `cast code $ADDR --rpc-url $RPC | wc -c`.

## Pitfalls

- Optimiser `runs` at 1,000,000 minimises gas at the cost of size — the default 200 is usually the right trade for a big contract.
- `via_ir = true` can increase size for small contracts; measure rather than assume.
- Using `--via-ir` locally but not in the deploy config, so CI passes and the deploy script fails.
- Splitting into a library but marking functions `internal` — the code is then inlined back into every caller and nothing shrinks.
- Forgetting initcode: constructor + runtime is capped at 49,152 bytes (EIP-3860), separate from the runtime limit.

## Verification

    forge build --sizes | awk '$2 > 24576 {print "OVER", $0}'

Pass: empty output (no contract over 24,576). Confirm the deployed instance: `cast code $ADDR --rpc-url $RPC | wc -c` is `2 * size` hex characters.

Report each contract's size, the techniques applied, and the final number.
