---
name: verify-wallet-derivation-paths
description: Use when recovering a wallet or confirming you derived the funded account. Enumerates BIP-32/44 paths, compares addresses to known-funded ones, and checks indices beyond zero.
---

# Verify wallet derivation paths

"I restored the phrase and see nothing" is almost always a path or index problem, not a lost wallet. This skill enumerates the standard paths and indices, matches them against known deposit addresses, and finds the account that actually holds the funds.

## Procedure

1. List the candidate paths before deriving anything. EVM wallets use BIP-44 `m/44'/60'/0'/0/i`; some legacy wallets use `m/44'/60'/0'/i` or `m/44'/60'/0'/0` with no change level.
2. Derive a range of indices per path and print the addresses, reading the mnemonic from a file, never from a command line:
   ```python
   from eth_account import Account
   mn = open("m.mn").read().strip()
   for i in range(0, 5):
       a = Account.from_mnemonic(mn, account_path=f"m/44'/60'/0'/0/{i}")
       print(i, a.address)
   ```
3. Repeat for the legacy path and the no-change path:
   `account_path=f"m/44'/60'/0'/{i}"` and `account_path="m/44'/60'/0'/0"`.
4. Compare every derived address to the deposit address you have on record. The path/index whose address matches is the wallet; the funds are in the first index with a nonzero balance.
5. For a hardware wallet, confirm with the device rather than pure software derivation, since the device is the source of truth for what it will sign from.
6. Record the winning path and index next to the wallet so the next restore is one step.

## Pitfalls

- Scanning only index 0 misses accounts funded at index 1+ created by "add account" in a UI.
- Case and checksum aside, an address must match exactly; a truncated log line that looks close is not a match.
- Some wallets use a passphrase (BIP-39 25th word) that changes *every* address; if nothing matches, the passphrase is the missing variable, not the path.
- Deriving with a mnemonic passed on the command line leaks it into history and `ps`; always read from a 0600 file.

## Verification

    # from a file, never argv
    python3 -c "from eth_account import Account; mn=open('m.mn').read().strip(); print([Account.from_mnemonic(mn, account_path=f\"m/44'/60'/0'/0/{i}\").address for i in range(3)])"
    # expect the recorded deposit address to appear in the printed list

Report which path and index produced the funded address, with the derivation command.
