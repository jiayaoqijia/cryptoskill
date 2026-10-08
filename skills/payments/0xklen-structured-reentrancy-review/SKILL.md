---
name: structured-reentrancy-review
description: Use when reviewing a Solidity contract that makes external calls before finishing state updates, or when triaging a reported reentrancy finding. Walks every external call site, classifies single vs cross-function reentrancy, and proves the guard by test.
---

# Structured reentrancy review

Reentrancy is only dismissed when every external call site has been enumerated and the state it can observe has been shown safe — not when a `nonReentrant` modifier is present.

## Procedure

1. List every external call: `grep -nE '\.(call|delegatecall|transfer|send)\(|\.(mint|burn|transferFrom|onERC721Received|flashLoan)\(' -r src/`.
2. For each call site, record in a table: function, state written AFTER the call, and whether the callee can re-enter with attacker-controlled value.
3. Apply checks-effects-interactions: all balance/accounting writes must precede the call. A store after a `call` is the bug, even if guarded elsewhere.
4. Classify each site: single-function (guarded), cross-function (modifier on the wrong function only), or read-only (a view returning stale mid-state).
5. Find every public entry that mutates the same state and confirm the guard covers all of them: `grep -rn "nonReentrant\|ReentrancyGuard" src/`.
6. Write a malicious receiver and a Foundry test that re-enters:

```solidity
contract Attacker is IERC721Receiver {
    function onERC721Received(address, address, uint256, bytes calldata) external returns (bytes4) {
        if (address(target).balance > 0) target.withdraw(); // re-enter
        return this.onERC721Received.selector;
    }
}
```

7. Run `forge test --match-test testReentrancy -vvvv` and confirm the guarded build reverts with `ReentrancyGuard: reentrant call` and an unguarded build drains.
8. Check ETH-sending paths: `transfer`/`send` forward 2300 gas (safe-ish), `call{value:}` forwards all (unsafe to a contract).
9. Re-scan for state read by a *later* call in the same transaction that an earlier call could have corrupted (the cross-contract variant).
10. Record the finding with the exact call-site line, the state variable, and the test that demonstrates loss.

## Pitfalls

- `nonReentrant` on `withdraw` but not on `emergencyWithdraw` — a second copy of the same transfer bypasses the guard.
- A guard that protects state but not a view used as an oracle: the reentrant frame reads the half-updated price and a borrower over-borrows.
- Assuming `transfer()` is safe: post-Istanbul it forwards 2300 gas, enough for an attacker `receive()` to re-enter a cheap SSTORE-light path.
- Deciding "no reentrancy" from the modifier alone; the modifier uses one shared slot and two entry points can sit in different guards.

## Verification

    forge test --match-contract ReentrancyAttack -vvvv

Pass: the run reverts with the guard's message; the unguarded variant (guard commented out) shows the attacker's balance rising in the trace.

Report the call site, the re-entered function, and the test name that shows the loss.
