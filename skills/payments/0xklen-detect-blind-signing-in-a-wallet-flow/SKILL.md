---
name: detect-blind-signing-in-a-wallet-flow
description: Use when a device or service asks a signer to approve a hash or opaque blob. Decodes the payload to a human-readable statement before signing and refuses anything that cannot be described.
---

# Detect and refuse blind signing

Blind signing — approving a hash or an unknown contract call you cannot read — is how drainers and malicious payloads turn a cautious signer into a victim. This skill requires every payload to decode to a statement a person can check, or be rejected.

## Procedure

1. Before signing, decode the calldata to a function and arguments:
   `cast calldata-decode "transfer(address,uint256)" 0x<data>`
   `cast 4byte 0x<selector>` to identify an unknown selector.
2. Classify the request:
   - Reads a function name and arguments you can state in a sentence → signable after review.
   - A raw `eth_sign` or a 32-byte digest with no fields → blind; refuse.
   - A `Permit`, `approve`, or `setApprovalForAll` → check the spender and amount; `uint256.max` to an unknown spender is the classic drain.
3. For typed data, decode and display the EIP-712 struct; if the wallet shows only the hash, treat it as blind signing and decline.
   `cast decode-eip712 --data 0x<data>` or inspect the JSON in the signing request.
4. Confirm `spender` / `to` against the allowlist before approving; an unknown spender is a stop, not a maybe.
5. On the hardware device, enable "full data" display so it shows `to`, `value`, and `data`, not a raw hash. Refuse if the device offers only the hash.
6. When the payload is a familiar pattern with unfamiliar parameters, stop and get a second human review; do not sign "because the last one looked like this".

## Pitfalls

- `eth_sign` (prefix-less personal message) is safe only with a device that displays the message; signing an arbitrary digest is signing whatever the host wants.
- A permit looks like a signature, not a transaction, and can be replayed by anyone who sees it; check the `value` and `spender`.
- A decoded function name can lie: an attacker's contract can name a function `transfer` while it drains; trust the simulation result, not the label.
- Wallets that show a truncated recipient defeat review; compare the full address.
- A signature request from a link is the attack surface; decode locally rather than trusting the dapp's own preview.

## Verification

    cast calldata-decode "transfer(address,uint256)" 0x<data>
    # expect a namespaced function and readable arguments; an undecodable selector fails the check

Report the decoded function and arguments, or the refusal with the raw hash shown, quoting the decode command.
