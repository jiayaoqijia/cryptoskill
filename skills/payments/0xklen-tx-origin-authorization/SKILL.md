---
name: tx-origin-authorization
description: Use when auditing authorisation that compares against tx.origin instead of msg.sender, or when a contract passes user addresses to a call. Detects phishing via an intermediate attacker contract.
---

# tx.origin authorization

`tx.origin` is the transaction's EOA, not the immediate caller, so any contract the user is tricked into calling inherits their authority — auth must compare `msg.sender`.

## Procedure

1. Find every use: `grep -nE 'tx\.origin' -r src/`.
2. For each, check whether it gates a value-moving or privileged action. If it gates nothing, it is informational; if it gates a transfer, it is critical.
3. Confirm the phishing path: victim EOA → attacker contract → victim contract; `msg.sender` is the attacker but `tx.origin` is the victim.
4. Write the PoC:

```solidity
contract Phisher {
    function attack(address wallet, bytes calldata data) external {
        (bool ok,) = wallet.call(data);   // tx.origin == victim, msg.sender == this
        require(ok);
    }
}
// test: vm.prank(victim); phisher.attack(address(bank), abi.encodeCall(bank.withdrawAll, ()));
```

5. The fix is `require(msg.sender == owner)`. Verify the fixed build reverts from the Phisher with `vm.expectRevert`.
6. Also flag `tx.origin` used for replay protection or as a nonce source — it is not unique per call.
7. Check forwarded calls: a contract that does `target.call{value:...}` with a user-supplied target lets the user's `tx.origin` leak into `target`.
8. Scan dependencies: `grep -rn 'tx.origin' lib/ node_modules/` for a transitive use behind your call.
9. Check `extcodesize` "is-a-EOA" tricks: a contract in its constructor has no code, so `extcodesize(msg.sender) == 0` passes — do not use it for auth either.
10. Run the suite and confirm no legitimate path relies on the victim's EOA authority directly.

## Pitfalls

- `tx.origin` in an `onlyOwner`-style modifier on a wallet that also accepts arbitrary calls — a single legitimate call drains it.
- `require(tx.origin == msg.sender)` as an anti-contract guard: it blocks legitimate multisig/AA wallets and is bypassable by a constructor call.
- Test harnesses using `vm.prank` set `msg.sender` but not `tx.origin`, hiding the bug; use `vm.prank(victim, victim)` to set both.
- Treating it as low severity because "it needs user interaction" — a malicious dapp front-end is exactly that interaction.
- Confusing `tx.origin` with `msg.sender` inside a `delegatecall`: `msg.sender` is preserved, `tx.origin` is not.

## Verification

    forge test --match-test "testTxOrigin" -vvvv

Pass: the PoC drains the wallet in the vulnerable build and reverts with `vm.expectRevert()` after the `msg.sender` fix; `grep -c 'tx\.origin' src/*.sol` returns 0.

Report each `tx.origin` site, whether it gates value, and the PoC outcome.
