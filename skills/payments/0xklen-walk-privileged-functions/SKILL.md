---
name: walk-privileged-functions
description: Use when a contract has owner/admin/role modifiers and you must prove every privileged function is actually reachable only by the intended address. Enumerates each modifier-gated entry and tests the negative case.
---

# Walk every privileged function

Access control is verified by calling each protected function from an unauthorised account and watching it revert — reading the modifier is not evidence.

## Procedure

1. Enumerate role checks: `grep -nE 'onlyOwner|onlyRole|onlyAdmin|require\(msg.sender ==|hasRole\(|_checkRole' -r src/`.
2. Map auth-related state: `cast storage <addr> <slot>` for the owner slot, and `forge inspect <Contract> storage-layout` to place role hashes.
3. Build an inventory: for each gated function — selector, modifier, intended caller, and the effect if called by an attacker.
4. Compute selectors to confirm nothing is mislabeled: `cast sig "setFee(uint256)"` and `forge inspect MyContract methods`.
5. For every function, write a negative test from a fresh account:

```solidity
address mallory = address(0xBEEF);
vm.prank(mallory);
vm.expectRevert(bytes4(keccak256("OwnableUnauthorizedAccount(address)")));
target.setFee(9999);
```

6. Run the negative suite: `forge test --match-test testOnlyOwner -vv`.
7. Check initialisation: is `owner` set in the constructor, or in an `initialize()` anyone can call? Call `initialize` twice and confirm the second reverts.
8. Hunt privilege escalation: any function that can set owner/admin/role, or that `delegatecall`s into a mutable target.
9. Check renounce/admin-transfer paths leave no orphan: `transferOwnership(address(0))` must be explicitly forbidden or documented.
10. Confirm two-step ownership: `transferOwnership` sets `pendingOwner` and `acceptOwnership` finalises (guards against a typo'd address).

## Pitfalls

- An `onlyOwner` function that calls an unguarded internal function which is itself `public`.
- A role granted in `initialize` to the deployer, and the deployer is a fresh EOA whose key later leaks.
- `tx.origin` used as the check — phishable via any intermediate contract.
- A modifier present but `_checkRole` uses the wrong role constant, copy-pasted from another role.
- Missing negative test: a green suite that never calls a privileged function as a non-admin cannot detect the hole.

## Verification

    forge test --match-test "testAccessControl" -vvv | grep -c PASS

Pass: one PASS per gated function plus one PASS per `expectRevert` negative. A gated function with no negative test is reported as unverified.

Report the count of gated functions, the selectors, and any that revert for the wrong reason.
