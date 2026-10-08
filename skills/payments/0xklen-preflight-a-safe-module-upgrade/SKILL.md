---
name: preflight-a-safe-module-upgrade
description: Use when adding, removing, or upgrading a Safe module or guard. Verifies the module's storage, checks it cannot brick the account, and runs the change on a fork before mainnet signers approve.
---

# Preflight a Safe module upgrade

A module can move funds with no further threshold, so a bad upgrade is a permanent backdoor or a permanent lock. This skill inspects the module's code and storage, proves the removal path works, and forktests the change before any mainnet signature.

## Procedure

1. Identify exactly what changes: `enableModule`, `disableModule`, `setGuard`, or upgrading a module's implementation behind a proxy. Each has a different blast radius.
2. Read the module's `execTransaction` / `exec` entrypoints and find what authority it has. A module that can call `execTransactionFromModule` can transfer funds without a threshold — treat it as a full signer.
3. Confirm the Safe can still remove the module: `disableModule(prevModule, module)` must be reachable by the owner set. Test it on a fork, not in production.
4. Check for storage collisions if the module reads/writes Safe storage or your own proxy slots. Compare slot layouts before upgrading an implementation.
5. Verify the module address is the audited one and not a look-alike:
   `cast code $MODULE --rpc-url $RPC | head -c 64`
   compare the bytecode hash against the audited build.
6. Forktest the full path: enable in the fork, run a representative transaction, then disable and confirm funds are still controllable.
   `anvil --fork-url $RPC` then run the enable/execute/disable sequence against the fork.
7. Only after the fork passes do the real signers approve, each recomputing the Safe transaction hash.

## Pitfalls

- A module that cannot be disabled without itself is a brick; verify the disable path on a fork every time.
- `setGuard(0x0)` removes the guard; a proposal to "update the guard" that points at `0x0` silently disables all policy checks.
- Upgrading a module proxy by changing the implementation to an unaudited version is the classic rug; hash the implementation.
- Modules are invisible to the Safe UI's threshold display; a reader who trusts "2-of-3" misses that a module already has full authority.
- Testing only the enable path and not the disable path leaves the escape hatch unproven.
- A module that reads `msg.sender` assumptions not met through `execTransactionFromModule` can behave differently than in tests.
- Upgrading a module behind a proxy can leave stale initialization; call the initializer on the fork, not only in production.
- `enableModule` on an already-enabled address is a no-op or a revert depending on the Safe version; check the version's behavior.
- Keep the disable transaction pre-signed so a compromised module can be removed without a fresh signing round.

## Verification

    cast call $SAFE "getModulesPaginated(address,uint256)(address[],address)" 0x1 10 --rpc-url $RPC
    # expect the module set to match the runbook and the fork disable to have succeeded

Report the module address and code hash, the fork enable/disable result, and the guard state, quoting the outputs.
