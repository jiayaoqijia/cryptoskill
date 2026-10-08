---
name: seed-phrase-backup-safety
description: Use when generating or storing a BIP-39 seed phrase for a wallet. Covers offline generation, durable backup, restore testing, and the rule that a mnemonic never enters a chat, a website, or a shell command.
---

# Seed phrase backup safety

A seed phrase is the account itself; anything that can read it can empty the wallet on every chain at once. This skill generates it offline, backs it up physically, and proves the backup restores before a single unit of value is deposited.

## Procedure

1. Generate on an air-gapped machine, never on a shared or cloud-synced host:
   `python3 -c "from mnemonic import Mnemonic; print(Mnemonic('english').generate(strength=256))"`
   Strength 256 gives 24 words (256 bits of entropy + 8-bit checksum).
2. Write the words by hand onto two durable media (stamped steel, or paper in two sealed envelopes) and store them in two separate physical locations, neither being the home of the device.
3. Take the first derived address and record it next to nothing that identifies the chain:
   ```python
   from eth_account import Account
   print(Account.from_mnemonic(open("/mnt/offline/m.mn").read().strip()).address)
   ```
4. Before funding, test the backup: enter the words from the *backup medium* into a fresh offline device and confirm it derives the same first address. A backup that was never restored is a hypothesis, not a backup.
5. If the amount is material, split custody with SLIP-39 or a 2-of-3 multisig across independent devices so no single location holds a complete phrase.
6. Destroy the generation workspace: wipe the temp file, clear the clipboard, and power off the air-gapped machine.

## Pitfalls

- Photographing the phrase puts it in the camera roll and possibly the cloud. Don't.
- Typing it into a "wallet validator", a browser extension, or a support chat is the single most common theft path. Reject any request to do so.
- A passphrase (the optional 25th word) is not stored with the phrase; losing it loses the wallet even with 24 words intact.
- Splitting words across two envelopes is *not* multisig: whoever finds both halves has the whole phrase. Use a real m-of-n scheme instead.

## Verification

    # On the air-gapped host, using the backup medium's words:
    python3 -c "from eth_account import Account; import sys; print(Account.from_mnemonic(open('m.mn').read().strip()).address)"
    # expect it to equal the address recorded at generation time

Report the restored address matching the generation-time address, quoting both commands.
