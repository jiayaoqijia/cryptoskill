---
name: spot-drainer-signature-phishing
description: Use when a wallet, site or dapp asks you to sign a message or transaction and you must decide whether it is a legitimate request or a drainer trying to take assets.
---

# Spot drainer and signature-phishing requests

The most common wallet drain is not a contract exploit: it is a signature the user is talked
into giving. Decode what is actually being requested before approving anything, and refuse
blind-signing outright.

## Procedure

1. Classify the request before signing:

   - `eth_sign` / `personal_sign` over opaque bytes: the wallet shows only a hex blob. This is
     the highest-risk class — refuse unless you can decode the payload to plain, non-authorising
     text. A legitimate login (SIWE) shows a readable message with a `Nonce` and `domain`.
   - `eth_signTypedData_v4` (EIP-712): decode the domain and message; check `domain.chainId`,
     `domain.verifyingContract`, and every field for an approval.
   - A transaction: decode with `cast calldata-decode` (see `decode-calldata-and-events`).

2. For EIP-712, inspect the spender/operator and amount. An approval-style message names a
   `spender` you have never seen, or grants `uint256` max, or has a far-future `deadline`.

       # In a wallet, read the "spender"/"operator"/"amount"/"deadline" fields directly.
       # Permit2 (0x000000000022D473030F116dDEE9F6B43aC78BA3) requests can move any approved token.

3. For a transaction, print the target and decoded call:

       cast tx $HASH --rpc-url $RPC --json | jq -r '.to, .input' | head
       cast calldata-decode "setApprovalForAll(address,bool)" 0xa22cb465...

   `setApprovalForAll(0xATTACKER, true)` hands over your entire NFT collection.

4. Check existing allowances before signing more. Revoke unknown operators from a wallet you
   trust, not from the site that asked.

       curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokennfttx\
&address=$YOU&apikey=$ETHERSCAN_API_KEY" | jq -r '.result[0]'

5. Hard refuses: `eth_sign` on raw hashes, any signature over a message you cannot read, approvals
   to addresses not in the project's verified docs, and any request from a link in a DM.

## Pitfalls

- EIP-712 payloads look legitimate — the domain name can be spoofed to mimic a real project, and
  the `verifyingContract` may be an attacker's contract that merely shares the name.
- "Sign to verify you are human / to claim an airdrop" is the standard drainer pretext; signing
  a permit grants spend rights, it does not prove identity.
- Permit vs Permit2 have different structures; a Permit2 `permitTransferFrom` lets the attacker
  move tokens you previously approved to the Permit2 contract.
- Revoke sites can themselves be malicious. Verify the revoke contract address before interacting.
- A signature that grants a session key (e.g. a 4337 session) can be replayed for its whole
  validity window; treat validity windows as spend limits.
- Hardware wallets show the message verbatim — if the text is a blob, that is the sign to stop.

## Verification

    cast calldata-decode "setApprovalForAll(address,bool)" $INPUT
    # prints (operator, approved); approved==true for an unknown operator is a drainer

Report the request type (personal_sign / EIP-712 / transaction), the spender or operator address,
the amount and expiry, and whether you decoded it to a readable intent. If it is `eth_sign` or an
unknown spender, report "refuse" with the reason.
