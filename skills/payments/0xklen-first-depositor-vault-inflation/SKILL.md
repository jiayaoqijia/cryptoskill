---
name: first-depositor-vault-inflation
description: Use when reviewing an ERC-4626 or share-based vault with a totalAssets/totalSupply price. Checks the first-depositor donation attack and whether virtual shares or a minimum deposit defeat it.
---

# First-depositor vault inflation attack

A fresh vault with `totalSupply == 0` lets the first depositor set the price by donating assets, so the next depositor's shares round down to zero — the fix is virtual shares or a dead minimum stake.

## Procedure

1. Confirm the share-price formula `assets * totalSupply / totalAssets` (OpenZeppelin `_convertToShares`) and note the truncation to zero when `totalAssets` is large relative to the deposit.
2. Reproduce the attack in a test:

```solidity
function testInflationAttack() public {
    attacker.deposit(1);                     // 1 wei -> 1 share
    token.mint(address(attacker), 1e18);
    attacker.donate(1e18);                   // totalAssets = 1e18+1, totalSupply = 1
    assertEq(vault.previewDeposit(1e18), 0); // victim gets 0 shares
}
```

3. Check for defences: OpenZeppelin ERC-4626 uses virtual `+1` shares and `+1` assets; confirm the vault overrides `_decimalsOffset()` to a non-zero value (e.g. `6`).
4. Or verify a dead-shares bootstrap: mint `10 ** decimals` to `address(0)` in the constructor so the price cannot be set by the first user.
5. Check `previewDeposit(dust) > 0` for all dust after the seed with a fuzz test:

```solidity
function testFuzz_noZeroShares(uint96 a) public {
    a = uint96(bound(a, 1, 1e30));
    assertGt(vault.previewDeposit(a), 0);
}
```

6. Confirm the deposit function reverts when `shares == 0` rather than silently accepting (`require(shares != 0)`).
7. Check `convertToShares` and `previewDeposit` rounding agree (Floor both) so integrators cannot exploit a mismatch.
8. Test with `_decimalsOffset` set to 0 (unprotected) — the fuzz test must fail, proving the test has teeth.
9. Verify `totalAssets()` excludes an externally-donated amount or the donation path is closed (no permissionless `skim`).
10. Run `forge test --match-test "Inflation|noZeroShares" -vvv` and read the share counts.

## Pitfalls

- A vault that overrides `totalAssets()` to `token.balanceOf(address(this))` while `totalSupply` is 0 is directly donatable.
- Virtual shares with `_decimalsOffset = 0` do nothing — the offset must be > 0 for the attacker to take a loss on the donation.
- Seeding with `address(0)` shares and a mint that can later be recovered; ensure the seed is unrecoverable.
- Fee-on-transfer deposit token: `previewDeposit` uses `amount` but the vault received less, so shares over-mint.
- An arbitrarily large donation cost is still profitable if the victim's deposit is larger; the attack scales with the victim, so "expensive" is not "safe".

## Verification

    forge test --match-test "Inflation|noZeroShares" -vvv

Pass: `previewDeposit(1e18) > 0` after the attacker's donation, and the noZeroShares fuzz test reports no counterexample. The unprotected variant fails, proving detection.

Report the share formula, `_decimalsOffset`, and whether the attack extracts value.
