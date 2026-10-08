---
name: verify-a-payment-request-before-sending
description: Use when acting on a payment request that arrived by invoice, email, or API. Verifies the address, amount, chain, and token against the authoritative source before an irreversible send.
---

# Verify a payment request before sending

Payment requests arrive through channels an attacker can edit: an emailed invoice, a chat link, a QR code. Verify the amount, asset, chain, and especially the destination against the authoritative source before the send becomes irreversible.

## Procedure

1. Extract every field independently: chain id, token contract, amount in base units, destination address. Read them from the raw request, not a rendered summary.
2. Confirm the chain id matches the network you will broadcast on:
   `cast chain-id --rpc-url $RPC` — compare to the request's chain id. A wrong chain sends funds to a same-address stranger.
3. Validate the address format and checksum:
   `cast to-check-sum-address $ADDR` and confirm it round-trips; an all-lowercase address skips the checksum and hides a typo.
4. Confirm the token contract against a canonical list:
   `cast call $TOKEN "symbol()(string)" --rpc-url $RPC` — symbols are spoofable, so verify the contract address too.
5. Compare the destination against a previously used address for that counterparty. A changed address is the single strongest signal of invoice fraud — confirm out of band before sending.
6. Re-derive the amount from the fiat figure and the agreed rate; a request that quietly adds zeros or drops decimals is common.
7. For a first-time or large payment, send a small test transfer first, confirm receipt out of band, then send the balance.

## Pitfalls

- Acting on an address shown in a rendered PDF or image; extract from the source data instead.
- A same-address-different-chain send: on EVM chains most addresses exist on every chain, so a chain-id mismatch is a live loss.
- Trusting the token symbol; a fake contract can use the real symbol and name.
- Skipping out-of-band confirmation because the request "looks routine"; invoice fraud targets routine payments.
- Copy-paste from a clipboard a malware swapped; verify the first and last characters.
- A request modified in transit between the sender and you is invisible if you trust the rendered document.
- HD wallets show the same address on multiple accounts; confirming the address but not the account is a partial check.

## Verification

    cast chain-id --rpc-url $RPC && cast to-check-sum-address $ADDR
    # chain matches the request; checksummed address matches the intended destination character for character

Report the verified chain id, token contract, amount in base units, and destination, plus how the address was confirmed out of band.
