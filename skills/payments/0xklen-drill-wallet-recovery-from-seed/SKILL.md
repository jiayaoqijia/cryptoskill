---
name: drill-wallet-recovery-from-seed
description: Use when a wallet holds real funds and no one has proven its backup restores. Runs a fire-drill restore from the backup on an isolated machine and proves the recovered address matches before any real loss is at stake.
---

# Drill wallet recovery from seed

A backup that has never been restored is a hope, not a control. This skill restores from the recorded backup on a fresh offline machine and proves the recovered address matches the funded one — without moving funds.

## Procedure

1. Pick a wallet whose backup you have but have never tested. Do the drill on a machine that has never touched the real key and is offline.
2. Restore from the backup exactly as a real recovery would happen — the same medium, the same passphrase, the same order of words or share reconstruction:
   ```bash
   cast wallet import recovered --interactive --keystore-dir /tmp/drill
   ```
   Enter the mnemonic at the prompt; never pass it as an argument.
3. Derive the address at the recorded path and compare it to the funded address, all 40 hex characters:
   `cast wallet address --account recovered --keystore-dir /tmp/drill`
4. For a threshold wallet, restore `t` of the `n` shares and confirm the group address matches. Then repeat with a different `t`-subset to prove more than one combination works.
5. Check the passphrase is the one recorded, not a remembered variant; a wrong BIP-39 passphrase silently derives a different, empty address.
6. Time the drill and write down the actual duration next to the recovery runbook. A recovery nobody can complete inside the incident window is not a recovery.
7. Wipe the drill keystore and the machine: `shred -u /tmp/drill/recovered`.

## Pitfalls

- A mnemonic that restores to a different address means a wrong passphrase, a different derivation path, or a transcribed word — do not "fix" it by transferring funds into the wrong address.
- Testing on a machine that already holds the live key proves nothing about the backup; use a clean host.
- Never paste a seed phrase into a chat, a shell command, or a log; type it at the tool's interactive prompt or read it from a restricted 0600 file.
- Backups split across too many places get lost; split across too few fail together. Record which pieces exist and where.
- A drill that only checks the word count skips the derivation; the address is the assertion that matters.

## Verification

    cast wallet address --account recovered --keystore-dir /tmp/drill | tr 'A-F' 'a-f'
    # expect an exact match to the funded address; any difference means the backup is wrong

Report the drill machine, the recovered address, the measured duration, and the wipe confirmation, quoting the commands.
