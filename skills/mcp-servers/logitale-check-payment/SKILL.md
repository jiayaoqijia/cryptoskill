---
name: check-payment
description: "Check whether a Toreador payment request has been paid, or list recent payments with their status. Use when the user asks if an order, invoice, checkout or customer has paid, or asks for their latest crypto payments."
---

# Check a payment with Toreador

Toreador follows each payment request on the blockchain. The status it reports is the only source
of truth: do not infer a payment from anything else. Use the Toreador MCP tools (their names end
with `toreador_…`).

## One payment

Call `toreador_get_payment` with the checkout id (`co_…`) or the session id.

If the user gives an order or invoice number instead of an id, call `toreador_list_payments` and
look for that `reference`. Read further pages with `cursor` while there is a `next_cursor`, and
stop as soon as you find it. If you do not find it, say so; do not pick a similar-looking payment.

## What each status means

| Status | Say to the user |
|---|---|
| `open` | The request exists; nobody has started to pay. |
| `pending` | The payment is waiting for the payer; nothing has been sent yet. |
| `submitted` | The payer has sent a transaction; it is not confirmed. Not paid yet. |
| `confirming` | The transaction has a first confirmation on the blockchain. Not final yet. |
| `completed` | Paid. The funds are in the user's wallet. Give the amount, the token, the network and the transaction hash. |
| `expired` | The request ran out of time without a confirmed payment. A new request is needed. |
| `failed` | No valid payment was confirmed for this request. |

Only `completed` means paid. For every other status, say plainly that the payment is not
confirmed. For `submitted` and `confirming`, suggest checking again in a moment.

## Recent payments

Call `toreador_list_payments` (newest first, `limit` up to 100). Present a short table: date,
reference, amount and token, network, status. Do not add up amounts of different tokens or
currencies into one total.

The list covers the payments created by the whole team, and each one carries its establishment
(`establishmentName`). When the user asks about one shop or point of sale, call
`toreador_list_establishments`, find the establishment by its name, and pass its id as
`establishmentId`. If no name matches, list the establishments and ask which one; do not guess.

## Limits to state honestly

- The list contains tracked payments only. A direct QR code is paid from wallet to wallet without
  tracking: Toreador cannot tell whether it was paid.
- Toreador cannot refund, reverse or hold a payment.
- A rate shown with a payment is an indicative reference rate recorded at the time; Toreador
  converts nothing.
