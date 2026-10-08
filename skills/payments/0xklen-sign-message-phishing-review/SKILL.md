---
name: sign-message-phishing-review
description: Use when asked to sign a plain message or an unknown typed payload. Detects Seaport/OpenSea orders, permit-like permits, and hashed transactions, and refuses eth_sign and anything you cannot render.
---

# Review a message-signing request

Message signatures have no gas cost and no on-chain record, which is why drainers ask for them. This skill classifies the payload, decodes anything structured, and refuses blind signatures.

## Procedure

1. Classify the prefix. `personal_sign` uses `0x19` + `"Ethereum Signed Message:\n"` + length + message; EIP-712 uses `0x1901` + domain separator + struct hash. Decode the first bytes:
   `python3 -c "print(open('payload.hex').read()[:10])"` → `0x19457468...` is personal_sign, `0x1901` is typed data.
2. Refuse `eth_sign` outright. Its `0x19` + raw-hash prefix signs an arbitrary hash, which is equivalent to signing a transaction you never saw.
3. If it is EIP-712, print the domain and the full struct and confirm the wallet shows the same fields. Check for a Seaport `OrderComponents` or an OpenSea order — signing one lets the recipient transfer your listed assets.
4. If it is permit-shaped (`permit`, `Permit`, `PermitSingle`), treat it as an approval: check spender, value, and deadline as you would for an on-chain approval.
5. Compare the signing site's domain to the project's real domain; a signature request from a lookalike host is the phish.
6. Use a dedicated signer address that holds no assets for logins and off-chain proofs, so a leaked signature cannot move funds.
7. If any field is unreadable, do not sign.
8. Record the exact payload hash and the domain you saw, so a disputed signature can be audited later.

## Pitfalls

- A drainer can craft a typed message that grants an approval with a far-future deadline and no visible token; the wallet renders the struct but users skim it.
- `signTypedData` with a domain that omits `verifyingContract` can be replayed on any contract that accepts it.
- Lookalike domains (extra hyphen, different TLD) render identically to a skimming eye; compare the full hostname.
- A message that is actually a serialized transaction hash signed with `eth_sign` is indistinguishable from a harmless login string to a user; only refusing `eth_sign` prevents it.
- Approving a signature on a site you reached from a DM or an ad is the common path; navigate to the project yourself.

- A login that produces a `permit` payload is not a login; the label on the page is not the payload.
- Wallet pop-ups truncate long messages; expand the raw view before deciding.
- A signature requested on a testnet can be replayed on mainnet if the domain lacks a chain id.
- A drainer can ask for two signatures in sequence; the second completes what the first prepared.

## Verification

    python3 -c "print(open('payload.hex').read()[:10])" && cast to-dec <v>
    # expect 0x19457468 or 0x1901 (never a bare 0x19), and a legitimate chain id

Report the payload prefix, the decoded domain, and the exact fields signed, with the commands behind them.
