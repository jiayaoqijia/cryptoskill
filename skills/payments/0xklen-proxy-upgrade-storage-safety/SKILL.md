---
name: proxy-upgrade-storage-safety
description: Use when a contract is behind a proxy (Transparent/UUPS/Beacon/Diamond) or you must upgrade an implementation. Verifies storage layout compatibility, initializer safety, and upgrade authority.
---

# Proxy upgrade safety

Behind a proxy the storage lives in the proxy and the logic in the implementation, so an upgrade that shifts a variable's slot silently corrupts every existing value.

## Procedure

1. Identify the pattern: `grep -nE 'delegatecall|ERC1967|_implementation|Beacon|DiamondCut|Initializable' -r src/`.
2. Dump both layouts and diff them:

```
forge inspect VaultV1 storage-layout --pretty > v1.txt
forge inspect VaultV2 storage-layout --pretty > v2.txt
diff v1.txt v2.txt
```

3. Reject any upgrade that inserts a new variable before existing ones or changes a type. New variables only append.
4. Confirm `__gap` entries: reserve `uint256[50] private __gap;` in base contracts and shrink it by each added variable.
5. Verify initialiser protection: `initializer` modifier on V2's `initialize`, plus `_disableInitializers()` in the implementation constructor.
6. Check upgrade authority: `_authorizeUpgrade` must be `onlyOwner`/`onlyRole(UPGRADER_ROLE)`; a public one is a takeover.
7. Confirm the proxy admin cannot be a contract that itself can be reentered during `upgradeToAndCall`.
8. Run a storage checker: `npx @openzeppelin/upgrades-core validate` or `slither-check-upgradeability`.
9. Upgrade on a fork and assert state survives:

```solidity
vm.selectFork(fork);
(uint256 v,) = readPreUpgradeValue();
proxy.upgradeTo(address(newImpl));
assertEq(readPostUpgradeValue(), v);
```

10. Confirm no `selfdestruct` in the implementation (post-Cancun it no longer removes code but still disrupts assumptions).

## Pitfalls

- Removing a variable in V2 shifts everything after it up one slot — balances read from the wrong slot.
- Adding `initialize()` without `_disableInitializers()` in the implementation constructor lets anyone initialise the implementation and poison the flag.
- UUPS upgrade logic in the implementation: if the implementation is called directly it can `selfdestruct` on older EVMs.
- Diamond: adding a facet whose selector collides with an existing one; run the diamond loupe `facets()` before a cut.
- `upgradeToAndCall` reentering into the new implementation before its initialiser completes.

## Verification

    forge inspect VaultV2 storage-layout --pretty | diff - v1.txt

Pass: only appends (new lines at the end), no line changed, and `__gap` shrank by the number of words added.

Report the pattern, the layout diff, the upgrade authority, and the fork test result.
