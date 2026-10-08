---
name: hardware-wallet-signing-workflow
description: Use when signing a transaction or message with a Ledger or Trezor. Covers address verification on-device, clear-signing, derivation-path checks, and refusing blind signatures.
---

# Hardware wallet signing workflow

The device's whole value is that the human confirms what is being signed on a screen the host cannot touch. This skill makes you verify the address and the payload on the device and refuse any signature the device cannot render legibly.

## Procedure

1. Confirm the account address on the device screen matches what your tooling prints, before sending anything:
   `cast wallet address --ledger`
   Approve on-device; the address shown on the device must equal the printed address, character for character.
2. Pin the derivation path explicitly. Default is `m/44'/60'/0'/0/0`; pass it so you cannot silently sign from the wrong account:
   `cast wallet address --ledger --mnemonic-derivation-path "m/44'/60'/0'/0/0"`
3. Enable clear signing. On a Ledger, install the matching app (Ethereum, or the token's own app) and update firmware; blind signing shows only a hash and should be treated as a red flag.
4. Simulate first and keep the simulation summary next to the device:
   `cast run <txhash> --fork-url $RPC`
5. Send with the device:
   `cast send $TO "transfer(address,uint256)" $RECIPIENT 1000000 --ledger --rpc-url $RPC`
6. Read the device screen: verify recipient address, amount, token, chain, and selector against your simulation.
7. If any field is missing or unreadable, reject the signature.
8. Record the firmware version and app version you signed with.

## Pitfalls

- An unverified device can swap the address it displays; confirm a known receive address on-device before trusting anything else.
- Changing the derivation path silently switches accounts; two paths can produce two funded addresses under one phrase.
- A malicious host can present a benign simulation and a different payload to the device. Trust the device screen, not the host UI.
- Trezor `--trezor` and Ledger `--ledger` cannot be combined; and a device left in an "always approve" mode defeats the entire control.
- A firmware downgrade is a real attack vector; a wallet that suddenly asks to install old firmware should be refused.
- Signing on a device shared with other users means the PIN is not unique to your key material.

## Verification

    cast wallet address --ledger && cast chain-id --rpc-url $RPC
    # expect the on-device address to equal the printed address and the chain id to match your target

Report the address confirmed on-device, the derivation path, and the chain id, quoting the commands.
