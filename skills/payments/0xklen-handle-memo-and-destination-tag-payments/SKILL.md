---
name: handle-memo-and-destination-tag-payments
description: Use when a payment rail requires a memo or destination tag to route funds. Explains where the tag belongs, what its omission costs, and how to recover a missing tag.
---

# Handle memo and destination-tag payments

Some chains and exchange rails route funds by a memo, destination tag, or comment field rather than a unique address. Omitting it sends the money to a shared pool with no way to attribute it.

## Procedure

1. Determine whether the rail needs a tag: XRP (destination tag), Stellar (memo), Cosmos/ATOM (memo for exchanges), TON (comment). An exchange deposit address without a tag is a shared address.
2. Put the tag in the correct field, not in the amount or a separate one: XRP `DestinationTag` is a uint32, Stellar `memo_text` a string, TON `comment`.
3. Confirm the tag with the recipient's system before sending; a tag that routes to another customer's account is not recoverable by the sender.
4. For exchange deposits, verify the tag scheme on the exchange's current page — providers rotate the requirement and decommission tag-less addresses.
5. If a transfer lands without a tag, contact the receiving exchange's support with the tx hash immediately; recovery is a manual credit, is discretionary, and often carries a fee or a cut-off window.
6. Never reuse a destination tag after the exchange says to stop, and regenerate the tag per deposit if the provider assigns per-transaction tags.
7. Record the tag alongside the tx hash.

## Pitfalls

- Sending to an exchange's shared address with no tag: funds arrive but are unattributable and depend on support goodwill.
- A tag that is numeric on one rail and alphanumeric on another; a type mismatch rejects or misroutes.
- Encoding the tag in a memo on a chain where the exchange ignores memos.
- Treating a tag-less transfer as lost immediately; it is usually recoverable via support within a window.
- Sending a test amount with a tag then a real amount with a typo'd tag.
- A memo that is optional on the sending UI but mandatory for credit leads to a silent unattributed deposit.
- Some exchanges change the required tag when you request a new address; an old tag routes to a decommissioned pool.
- A trailing space or newline copied into the memo string can make it not match and not credit.
- A tag pointing at the wrong customer's deposit account is not recoverable by you even though it is on-chain.
- Moving funds between your own exchange sub-accounts needs the tag too; internal confusion still misroutes.

## Verification

    # after broadcast, open the tx on the chain explorer (XRP/Stellar/TON) and read the tag field
    # tag on-chain == tag on the deposit instruction, character for character

Report the rail, the tag value, the tx hash, and confirmation the tag matches the deposit instruction.
