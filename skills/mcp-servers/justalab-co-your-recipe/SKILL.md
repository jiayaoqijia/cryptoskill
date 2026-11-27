---
name: your-recipe
description: One or two sentences an agent reads to decide whether this recipe fits. Say what it does, on which protocol and chain, and end with a sentence that starts "Use when the owner wants to".
metadata:
  version: "1"
  author: recipes.jaw.eth
  chains: "8453"
---

# What the recipe does, in a few words

One short paragraph: the calls the owner approves and what they get.

## When to use

- The intents this recipe covers, in the owner's words.
- The intents it does not cover, and which recipe or tool covers them instead.

## Network

Base only (chain id 8453). Name every chain the recipe runs on, since a host's skill list does not filter by chain. On any other chain, tell the owner this recipe does not apply and stop.

## Addresses (Base, chain id 8453)

| Label | Address |
| --- | --- |
| TOKEN (what it is) | 0x0000000000000000000000000000000000000000 |
| PROTOCOL_CONTRACT (what it is) | 0x0000000000000000000000000000000000000000 |

Use only these addresses. Each one comes from the protocol's published deployments page, linked in the pull request.

## Before you start

1. Get the owner's account address from the `account` field of `jaw_session_status`.
2. Read the balance with `jaw_get_assets` for the chain. When it fails, leaves the chain out, or returns no entry for TOKEN, read `balanceOf(account)` on TOKEN with one `jaw_read_contracts` call.
3. Anything else to check before building calls, such as a position, an allowance or a health factor.

## Steps

1. Ask the owner for anything the recipe needs, unless they already said, and convert amounts to base units.
2. Call `jaw_prepare_calls` with the actions in order, naming each address by its label above.
3. Call `jaw_simulate_calls` with the chain id and the returned calls.
4. Call `jaw_send_calls` with the chain id, the calls exactly as `jaw_prepare_calls` returned them, and `recipes` set to ["your-recipe@1"].
5. Follow the request as "After the link" says.

## Stop when

Each stop ends the recipe before anything is sent: no link opens, of any kind, not even one to add funds. Tell the owner, in one message, what is missing and the one thing they can do next:

- The balance is below the amount: "You have X TOKEN on Base and asked for Y. Add Z TOKEN or choose a smaller amount."
- A read in "Before you start" fails: "I could not read your TOKEN balance on Base, so I stopped before building anything."
- The simulation fails: show its reason and stop.

## After the link

1. Show the owner the link on its own line, with one sentence of what it does.
2. Call `jaw_get_request` with the request's `id` and `waitSeconds` 30, right away. Do not wait for the owner to say they approved, and stay in this turn while you follow it.
3. While its `status` is `pending_approval`, `pending_signature` or `pending_confirmation`, call it again with `waitSeconds` 30. `pending_confirmation` is never final: the transaction may still land. Never send these calls again while you follow it. Read its `summary` each time: when it tells you to read `jaw_get_calls_history` or check the account before sending these calls again, as it does for a send the wallet page lost or one not seen on chain in time, stop reading. Tell the owner it is not confirmed, that it must not be sent again, and that the wallet's activity will show whether it went through.
4. When the status is final, tell the owner how it ended:
   - `success`: what the owner has now. Give the transaction hash or link from the summary.
   - `denied`: the owner declined or let the link expire. Nothing moved.
   - `error`: the transaction reverted. Nothing moved, and the owner paid the network fee. When the summary says nothing was sent, the wallet refused the request before sending it: nothing moved and no fee was paid.
5. If you cannot keep reading in this turn while it is still pending, say where it stands, waiting for approval or not confirmed yet, and that it must not be sent again, then end the turn. On the owner's next message, call `jaw_get_request` again with the same `id`.
