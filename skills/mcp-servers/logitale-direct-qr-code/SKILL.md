---
name: direct-qr-code
description: "Show a direct crypto QR code (BTC, ETH, SOL, POL or USDC on Solana) that pays one of the user's Toreador wallets, including as text in a terminal. Use when the user asks for a quick QR code or wallet-to-wallet payment without a payment page. Not tracked: for a payment Toreador confirms, use request-payment."
---

# Show a direct QR code with Toreador

A direct QR code encodes a payment from the payer's wallet to the user's wallet, and nothing
else. It is free and unlimited, and it is **not tracked**: Toreador cannot tell whether it was
paid. If the user needs to know that the money arrived, use the `request-payment` skill instead
and say why. Use the Toreador MCP tools (their names end with `toreador_…`).

## Steps

1. **What to ask for.** You need a token, a network and an amount in the token's own unit
   (for example `0.001` BTC), as a decimal string. If the user gives an amount in dollars or
   euros, do not convert it yourself: propose `request-payment`, which takes an amount in USD or
   EUR.
2. **Valid pair.** If you are not sure the token exists on that network, call
   `toreador_list_tokens` and use a pair it lists.
3. **Receiving wallet.** Call `toreador_list_wallets` and use a wallet of the right family (EVM,
   Solana or Bitcoin) for that network. If several fit, ask which one. If none fits, stop and tell
   the user to add one in their dashboard.
4. **Generate.** Call `toreador_generate_qr` with `token`, `chainId`, `amount`,
   `recipientAddress`.
   - In a terminal or any text-only interface, pass `format: "text"`. Pass `textBackground:
     "light"` if the user's terminal has a light background; the default is dark.
   - Otherwise leave the default format.
5. **Show.** For a text QR code, show the block exactly as returned, in a code block, without
   changing a character. If the user's phone cannot read it, the background is probably the
   opposite: generate it again with the other `textBackground`.

## What to say

- State that this QR code is not tracked: the user checks their own wallet to see the payment.
- With a test key, say that the QR code targets a test network.
- Never present the QR code as a confirmation or a receipt.
