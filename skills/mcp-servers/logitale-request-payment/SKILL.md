---
name: request-payment
description: "Create a Toreador payment request (a hosted payment page for an amount in USD or EUR, paid in stablecoins) and give its link to the user. Use when the user wants to charge, bill, invoice or be paid in crypto or stablecoins with Toreador."
---

# Ask for a payment with Toreador

Toreador is non-custodial software. A payment request is a page: the payer opens it, picks a
stablecoin and a network, and pays from their own wallet straight to the user's wallet. Toreador
never receives the funds. Use the Toreador MCP tools (their names end with `toreador_…`).

## Steps

1. **Amount and currency.** You need an amount and a currency, `USD` or `EUR` only. If either is
   missing, ask. Do not guess a currency.
2. **Receiving wallet.** Call `toreador_list_wallets`.
   - No wallet: stop. Tell the user to add a receiving wallet in their Toreador dashboard (Wallets).
     You cannot add one, and no address typed in the conversation can be used.
   - One wallet: use its address.
   - Several: ask which one, showing each label and a shortened address, unless the user already
     named it.
3. **Create.** Call `toreador_create_checkout` with `amount`, `currency`, `recipientAddress`, and:
   - `reference`: the user's own order or invoice number, when they gave one;
   - `description`: a few words shown to the payer, when useful.
   Leave `conversion` and `acceptNative` off unless the user asks. If they ask: `conversion` also
   offers stablecoins of the other currency, at an indicative reference rate (Toreador converts
   nothing); `acceptNative` also offers coins such as ETH, whose price moves, so the user bears
   the difference.
4. **Hand over.** Give the user:
   - the `url` field exactly as returned. Never rebuild, shorten or edit it: its domain is not the
     API's domain;
   - the checkout id (`co_…`), which they will need to check the payment later.

## What to say, and what never to say

- If the key is a test key (the account or the response says `test`), say clearly that this is a
  test payment request on test networks: no real funds will move.
- A created request is not a payment. Never say or imply the user has been paid. Only
  `toreador_get_payment` returning the status `completed` means that.
- Toreador cannot refund, reverse, hold or forward a payment. A refund is a transfer the user
  makes from their own wallet.
- Never ask the user to paste their API key in the conversation. The key is set with
  `/plugin configure toreador`.

## When a call fails

- `402`: the monthly quota of tracked payments is reached. Call `toreador_get_account` and report
  what is used and the limit. Direct QR codes (the `direct-qr-code` skill) are not counted.
- `429`: too many requests. Wait a moment, then retry once.
- `401`: the key is invalid or revoked. The user creates a new one in the dashboard, API section,
  then runs `/plugin configure toreador`.
- `address_not_registered`: the address is not one of the account's wallets. Go back to step 2.
