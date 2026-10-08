---
name: verify-address-on-hardware-wallet-screen
description: Use when sending funds to an address generated on a hardware wallet. Confirms the device screen shows the same address and amount the host shows, before anything is signed.
---

# Verify the address on the hardware wallet screen

A hardware wallet is only trustworthy if its screen is the source of truth; host malware can rewrite a destination in the unsigned transaction and the device will happily sign it. This skill makes the device display the address and the amount independently and refuses any mismatch.

## Procedure

1. Have the device itself display the receive address, not the host app. For a Trezor:
   `trezorctl get-address -n "m/44'/60'/0'/0/0" -c Ethereum --show-display`
2. Read the full address off the physical screen and compare character by character against the host. Do not compare a truncated `0x1234…abcd` form — check all 40 hex characters, ideally the first four, last six, and a middle chunk.
3. On first use of a derivation path, confirm the device treats it as new. A path that "already knows" an address you never funded means the device is not fresh or is not the device you think it is.
4. For a spend, confirm destination and amount on the device screen, not in the wallet UI. Enable full transaction display so the device shows `to`, `value`, and chain id in one review.
5. Verify the chain id the device reports matches the network you intend. A device signing a mainnet-shaped transfer under the wrong chain id is a substitution attack, not a typo.
6. Sign only after the screen matches. If the host and device disagree on any field, reject on the device and treat the host as compromised.

## Pitfalls

- Blindly approving a device that shows a hash rather than the fields — that is exactly the flow malware needs.
- Copying the address from the wallet UI before the device confirms it inverts the trust direction; the device screen is the anchor.
- A firmware update prompt mid-signing can be malware or a downgrade attack; install firmware only from the vendor app while idle.
- Reusing a single hardware device as the only key for a treasury recreates a single point of failure — pair it with a second signer.
- Never type a seed phrase into the host to "restore" a device seen over chat: keys come from the device or a restricted file, never a command line or message.
- USB or Bluetooth interception can rewrite what the host sends but not what the screen shows; the screen is the last word.
- A device bought second-hand may carry a pre-set seed the seller knows; generate on-device or verify the seed fingerprint.
- Clear-signing support varies by app and chain; older apps show only the hash and must be treated as blind.
- A device that never asks for a PIN on a spend may be in a no-verification mode set by a compromised host.
- Passphrase (BIP-39 25th word) wallets derive a different address set; keep the passphrase recorded separately and securely.
- Two devices of the same model with different seeds look identical; label them and verify the address, never the label.

## Verification

    trezorctl get-address -n "m/44'/60'/0'/0/0" -c Ethereum --show-display
    # expect the screen address to equal the one the host will receive at; compare all 40 hex chars

Report the address, the derivation path, and that the device screen matched, quoting the command.
