---
name: buy-cycles
description: "Buy cycles with a credit card for the CLI's own identity with `icp cycles buy`, through CyclePay's on-chain gateway, then continue deploying. Use when a mainnet deploy or canister creation fails for lack of cycles, the user has no ICP, no wallet or no exchange account, or asks to pay for cycles by card, Stripe, fiat or USD. Do NOT use for converting ICP you already hold (cycles-management: `icp cycles mint`), for topping up a canister from an existing balance, or for Internet Identity sign-in (agent-web-identity)."
license: Apache-2.0
compatibility: "icp-cli with `icp cycles buy` (dfinity/icp-cli#815; `icp cycles --help` lists `buy`), or any icp-cli >= 1.0 for the `icp canister call` fallback. Mainnet (`-n ic`). A human with a browser on any device to pay."
metadata:
  title: Buy Cycles With a Card
  category: Infrastructure
---

# Buy Cycles With a Card

## What This Is

A cycles gateway is a canister that takes an order for cycles, has the buyer pay for it
by card on a hosted Stripe page, and delivers the cycles on-chain. `icp cycles buy` makes
the **CLI identity the buyer**: the identity that will run `icp deploy` creates the order
itself, so the cycles land on that identity's own cycles-ledger account and nothing has
to be linked, signed in or transferred afterwards. The agent's job is to create the
order, hand the payment link to the human, wait for delivery, and carry on deploying.

The default gateway is [CyclePay](https://www.cyclepay.org), run by the DFINITY
Foundation: backend canister `2bwus-iiaaa-aaaac-bee3a-cai`, **mainnet only**, USD only.
Everything the command quotes with is read from the gateway at run time (`get_card_terms`,
`get_xdr_rate_status`): the per-order range (USD 1 to 200 at the time of writing), the
card fee (2.9 % + 0.30 USD), the cycles-ledger delivery fee (200 M cycles) and the USD
per XDR rate (1 XDR = 1 T cycles). Do not hardcode any of them. Card details never touch
the canister or the CLI.

## Prerequisites

- `icp` CLI installed (https://cli.internetcomputer.org); load the `icp-cli` skill for
  general usage and the `-n` / `-e` flag rule. `icp cycles --help` must list `buy`;
  otherwise use the fallback below.
- A **named** `icp` identity for the project. The anonymous identity is refused, and the
  identity that buys must be the one that deploys.
- A human who can open a URL on **some** device (laptop, phone). The agent's machine
  needs no browser.

## The Flow

```bash
# 1. Who is buying, and what they hold now
icp identity principal --identity "$ID"
icp cycles balance -n ic --identity "$ID"

# 2. Buy (spend 10 USD; or `--cycles 5t` to pay the least that buys 5 T cycles)
icp cycles buy --amount 10 -n ic --identity "$ID" --no-open --yes --json
#  stdout, line 1, as soon as the order exists:
#  {"order_id":"co-12-…","checkout_url":"https://buy.stripe.com/…","amount":{"currency":"USD","value":"10.00"},
#   "net":{"currency":"USD","value":"9.41"},"fee":{"currency":"USD","value":"0.59"},
#   "estimated_cycles":"6959859171597","expires_at":"2026-10-15T18:03:12Z"}
#  → show checkout_url to the user VERBATIM and ask them to pay on it (any device).
#  The command polls every 3 s for up to an hour, then prints line 2 and exits 0 only on delivery:
#  {"order_id":"co-12-…","status":"delivered","cycles_delivered":"6938000000000",
#   "paid":{"currency":"USD","value":"10.00"},"refunded":null,"detail":null,"balance":"6938000000000"}

# 3. Continue as the same identity
icp cycles balance -n ic --identity "$ID"
icp deploy -e ic --identity "$ID"
```

Without `--yes` the command shows the quote and asks for confirmation, which needs a
terminal; without one it prints the quote and refuses (`Use --yes to proceed`), creating
nothing — a usable dry run when the user wants to see the figures first:

```
Identity: dev
Buyer:    7k7px-dcypq-wulnh-byzgd-6sib2-udn6c-lfo6e-6oujd-veifp-62woo-5ae
Gateway:  2bwus-iiaaa-aaaac-bee3a-cai (CyclePay)
Price:    10.00 USD (9.41 USD after a 0.59 USD card fee)
Estimate: about 6.959T cycles, at 1.3520 USD per 1T cycles
```

Flags that matter to an agent: `--no-open` (never let the CLI try a browser), `--json`
(two objects on stdout, one per line, never an array; progress and prompts go to stderr),
`-q` (stdout is the link, then the final status tag), `--no-wait` (print the link and
return; the order needs nothing more from the CLI), `--gateway <canister-id>` /
`ICP_CYCLES_GATEWAY_CANISTER_ID` (another canister serving the same interface, on any
network).

### Fallback: the same order with `icp canister call`

Only when the installed CLI has no `cycles buy`. Same canister, same identity rules. The
argument and reply shapes are those of
[`cycles_gateway.did`](https://github.com/dfinity/icp-cli/blob/main/crates/icp-cli/src/cyclepay/cycles_gateway.did),
which icp-cli holds against CyclePay's backend interface; this sequence was run against
icp-cli's stand-in gateway and mainnet's public queries on 2026-10-14.

```bash
GW=2bwus-iiaaa-aaaac-bee3a-cai
icp canister call "$GW" get_card_terms '()' -n ic --query        # deliveries_paused, min/max_order_usd_cents, fee_bps, fee_fixed_usd_cents, ledger_delivery_fee_cycles
icp canister call "$GW" get_xdr_rate_status '()' -n ic --query   # xdr_usd_x10000, stale

# Create: USD cents, destination = the caller's own cycles-ledger account.
icp canister call "$GW" create_order \
  '(record { destination = variant { Ledger }; beneficiary = null; project_id = null;
             amount_usd_cents = 1000 : nat64; confirm_system_canister = null })' \
  -n ic --identity "$ID"
# Ok = record { order_id = "co-…"; payment_url = "https://…"; net_usd_cents; expires_at }
# Err = record { code = "AMOUNT_OUT_OF_RANGE"; message = "…" }   (nothing was created)

# Wait: poll until the status is Delivered, or one of the end states in Pitfall 6.
icp canister call "$GW" order_status '("'"$ORDER_ID"'")' -n ic --query --identity "$ID" \
  | grep -oE 'status = variant \{ [A-Za-z]+'
```

To extract the link from the Candid text, take the quoted string after `payment_url =`
**unchanged**: `grep -oE 'payment_url = "[^"]+"' | sed -E 's/.*"(.*)"/\1/'` (Pitfall 2).
Cycles to expect, before the ledger fee: `net_usd_cents / 100 / (xdr_usd_x10000 / 10000)`
trillion, where `net = amount − (amount × fee_bps / 10000 + fee_fixed_usd_cents)`, rounded
to the cent.

## Common Pitfalls

1. **The cycles go to the buyer's own cycles-ledger account, nowhere else.** The CLI has no
   "send to my canister" option. From there, `icp deploy -e ic` creates canisters out of
   the balance and `icp canister top-up <canister> --amount <N> -e ic` funds one.
   `icp cycles transfer` to a canister principal credits that principal's *ledger*
   balance, not the canister's execution balance (see `cycles-management`).

2. **Never "clean up" the Candid text a link arrives in.** Candid prints numbers with
   underscore separators (`6_938_000_000_000`), and a regex that strips underscores
   turns `client_reference_id=o_co-12-…` into a link to the wrong order. Prefer `--json`;
   in the fallback, extract the quoted URL exactly and strip underscores only from values
   that are all digits.

3. **The agent cannot pay, and usually cannot open a browser.** Print the link and ask the
   human to open it; they may use another device. Never ask for or type card details.
   `--yes` is fine for an amount the user asked for: creating an order charges nothing,
   and the human sees the price again on the payment page before paying.

4. **`-n ic` is required, `-e ic` is not accepted here.** CyclePay sells on mainnet only.
   Run outside a project or against a local network and the command fails with
   `this network is not mainnet` or `is not running`, each ending in
   ``CyclePay sells cycles on mainnet: use `-n ic` ``. The deploy that follows takes `-e ic`
   as usual (`icp-cli` Pitfall 2).

5. **Buy and deploy as the same, named identity.** The command refuses the anonymous
   identity, and `icp deploy` spends the *default* identity's balance unless `--identity`
   is passed. A purchase as one identity and a deploy as another fails with insufficient
   cycles while the balance sits one identity over. Pass `--identity "$ID"` everywhere,
   or check `icp identity default` first.

6. **Stopping the command does not stop the order, and there is no resume.** Ctrl-C (or a
   killed process) leaves the order payable; once paid, the cycles land anyway and
   `icp cycles balance -n ic` shows them. Do not create a second order for the same
   purchase; the gateway caps open orders per principal (`TOO_MANY_OPEN_ORDERS`). To watch
   the first one again, poll `order_status` as in the fallback. An unpaid order expires
   (the `expires_at` in the JSON, about a day) with nothing charged; start a new one then.

7. **Read the final status before deciding anything.** The command exits 0 only for
   `delivered`; the JSON `status` (or the human message) says why otherwise:
   - `processing` / `payment_pending`: the card was charged and delivery is under way.
     Keep waiting or poll; never re-order.
   - `needs_review`: charged, and a CyclePay operator settles it by hand. Report the order
     id and the charge to the user and stop.
   - `refunding` / `refunded`: not delivered, the money comes back (`refunded` says how
     much). A new order is fine once the user agrees.
   - `refund_owed`: not delivered, an operator refunds by hand. Keep the order id.
   - `unknown` (`--json`) / "a state this version of icp does not know": a status newer
     than the CLI; poll `order_status` to read it.

8. **The quote is an estimate; delivery is net of a ledger fee.** The cycles are minted
   at the rate in force when the payment lands, so `cycles_delivered` can differ slightly
   from `estimated_cycles`, and the gateway's `ledger_delivery_fee_cycles` (200 M) comes off
   a ledger delivery. That is not a short delivery. A stale-rate warning on stderr means
   CyclePay has not refreshed its rate for longer than it tolerates; tell the user before
   they pay. With `--cycles N` the command pays the smallest amount, to the cent, that
   buys at least `N` at the quoted rate.

9. **A refusal is `CyclePay refused the order: <CODE>: <message>`, and nothing was
   created.** `AMOUNT_OUT_OF_RANGE`: the terms set the range (USD 1 to 200), pick an amount
   in it. `CARDS_UNAVAILABLE` / `PAUSED`: the gateway is not taking card orders, try later.
   `RATE_LIMITED` / `TOO_MANY_OPEN_ORDERS`: wait, or pay the open order (Pitfall 6). Do not
   loop on any of them.

10. **`failed to read the card terms`** means the canister does not serve the gateway
    interface: a `--gateway` that is not a cycles gateway, or an old CyclePay deployment.
    Check the canister id; do not fall back to guessing a Payment Link.

## Verify It Works

```bash
icp cycles balance -n ic --identity "$ID"   # ≈ estimated_cycles − 200_000_000 after a first purchase
icp canister call 2bwus-iiaaa-aaaac-bee3a-cai order_status '("'"$ORDER_ID"'")' -n ic --query --identity "$ID" \
  | grep -E 'status|cycles_delivered|paid_usd_cents'   # status = variant { Delivered }; cycles_delivered = opt (6_938_000_000_000 : nat64)
```

`order_status` answers only the identity that created the order (`null` for anyone
else, and for an unpaid order after it expired). Purchases also appear under "My
purchases" on www.cyclepay.org when the user signs in there with the same identity:
`icp identity link web cyclepay --app 4w3yu-fyaaa-aaaac-beeoa-cai.icp0.io` makes one.

## Security Rules for Agents

- Create orders only for an amount the user named, as the identity they will deploy
  with, and relay the `amount`, `fee` and `estimated_cycles` the command prints.
- Hand over the payment link and stop. Do not attempt to automate the payment page.
- Never collect, store or echo card details; the hosted Stripe page is the only place
  they are entered.
- Treat the order id as a reference, not a secret: it travels in the payment link.
- When a purchase ends in `needs_review` or `refund_owed`, report the order id and the
  charge to the user and do not retry.
