---
name: send-usdt
description: Send USDT or another TRC20 token on TRON safely with the GoTRON MCP tools. Checks the network, token contract, recipient, balance and energy cost, then builds the transfer and signs it only after explicit confirmation. Use when the user asks to send, transfer or pay USDT (or any TRC20 token) on TRON.
---

# Send USDT on TRON

A TRC20 transfer can't be reversed. Every step below exists to stop a wrong
network, contract, address or amount before anything is signed.

## 1. Pin down the request

You need four things from the user: sender, recipient, amount, and token.
Never guess or complete an address, and never take one from an earlier,
unrelated message without asking.

- **Network:** call `get_network`. Say which network you are on (mainnet,
  nile or shasta) before going further.
- **Token contract:** on mainnet, USDT is `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`.
  On a testnet, or for any other token, ask the user for the contract
  address. Call `get_trc20_token_info` with `contract_address` and confirm the
  symbol and decimals match what the user means. If the symbol isn't what
  they expect, stop and ask.
- **Recipient:** call `validate_address` with `address`. If it fails, stop. An
  address given in hex (`41...`) or EVM (`0x...`) form converts to base58;
  show the user the base58 form you will use.

## 2. Check the sender can pay

- `get_trc20_balance` with `address` (the sender) and `contract_address`.
  Stop if the balance is below the amount.
- `analyze_transfer_cost` with `from`, `to`, `amount` and `contract_address`.
  It returns `energy_required`, the sender's available energy and bandwidth,
  and `total_estimated_cost_trx`: the TRX that will be burned when staked
  resources don't cover the transfer.
- `get_account` for the sender's TRX balance. Stop if it can't cover
  `total_estimated_cost_trx`: a transfer without enough TRX for energy fails
  and still burns what it used.

Sending USDT to an address that has never held it needs roughly twice the
energy of a transfer to an existing holder. The estimate already includes
this; mention it when the cost looks high.

If the result has a `warning` that energy estimation is unavailable, tell the
user the cost is unknown and give the typical range from the warning. Don't
present a guess as the estimate.

### Choose the Energy fee limit

Set `fee_limit` from the full Energy requirement and current price returned
by `analyze_transfer_cost`, including Energy covered by staking:

```text
fee_limit = ceil(energy_required * energy_price_sun * 1.5 / 1_000_000)
```

This adds 50% headroom and rounds up to whole TRX, as required by the tool.
Do not subtract staked Energy or use `total_estimated_cost_trx` for this
calculation: `fee_limit` caps the caller's Energy budget even when staking
covers it. Bandwidth burn is separate from this Energy ceiling.

For example, 65,000 Energy at 100 SUN per Energy needs a `fee_limit` of
10 TRX with headroom, even if available staked Energy makes the estimated
TRX burn zero. The same Energy demand and price give the same limit whether
staking covers all, some or none of the Energy.

Use a positive integer no greater than the tool's 15,000 TRX maximum. If the
calculated limit exceeds that maximum, stop and explain that the requested
headroom cannot be provided; do not silently clamp it or build the transfer.
If the Energy estimate or a positive Energy price is unavailable, leave the
100 TRX default and explain that its sufficiency is unverified, rather than
calculating a zero limit from missing data. Include the chosen ceiling in
the confirmation summary; a change to it needs a new confirmation.

`fee_limit` is a ceiling, not a charge: unused budget is not charged.

## 3. Confirm with the user

Show one summary and wait for an explicit yes:

- network
- sender address, and on the local path the wallet that will sign (name
  and address)
- token symbol and contract
- amount
- full recipient address (not shortened)
- estimated TRX burn, or that staked energy covers it
- chosen Energy fee ceiling (`fee_limit` in TRX)

Any change to these after confirmation needs a new confirmation.

## 4. Build the transaction

Call `transfer_trc20` with `from`, `to`, `contract_address`, `amount`, and
`fee_limit`. Pass `amount` in token units (for example `"25.5"`, not the raw
integer), and explicitly pass the confirmed `fee_limit` as whole TRX. Do not
omit `fee_limit` and let the tool substitute its default ceiling.

The result is an unsigned `transaction_hex` and its `txid`.

## 5. Sign and broadcast

Which path applies depends on how the server runs:

- **Local server with a keystore** (`sign_and_confirm` is available): call
  `sign_and_confirm` with `transaction_hex`, `wallet` (name or address) and a
  short `reason`. A wallet policy can refuse the transfer or ask for approval;
  report that to the user as it is, and don't retry another way. If the user
  wants a limit raised and a policy is configured, `request_limit_override`
  asks for a one-time override.
- **Hosted server** (`mcp.gotron.sh`, no signing tools): give the user the
  `transaction_hex` and `txid`, and tell them to sign and broadcast it with
  their own wallet, such as tronctl. A transaction expires shortly after it
  is built (about a minute by default), so if they take longer, build it
  again.

### If signing or confirmation fails

An error from `sign_and_confirm` doesn't always mean nothing was sent. A
confirmation timeout, a cancelled wait, or a "broadcast failed" network error
can come after the transaction reached the network. Never build or sign the
transfer again until you know the first one isn't on chain:

1. Look it up: `get_transaction` and `is_transaction_pending`, each with
   `transaction_id` set to the txid in the error. When the error has none,
   use the `txid` from `transfer_trc20`, unless an approval rebuilt the
   transaction (its txid then differs); in that case check the sender's
   recent transfers with `get_trc20_transfers` (`address` set to the sender).
2. If it's on chain or pending, report it and stop. Only send again once the
   first transaction is not found, not pending, and past its expiry.

A "broadcast rejected" error means the node refused it, so nothing was sent;
fix the cause it names before trying again. If the rejection says the
transaction is a duplicate, it was already sent: look it up as above.

## 6. Verify

Call `get_transaction` with `transaction_id` set to the final txid, and report
the result. On the local path that is the txid `sign_and_confirm` returns: when
an approval was needed, the transaction is rebuilt and its txid differs from
the one `transfer_trc20` gave. On the hosted path it is the `txid` from step 4.

Judge success by the `result` field (`SUCCESS` or `FAILED`), or by `success`
from `sign_and_confirm`. Don't read `contract_result`: USDT on TRON is
reported to return `false` from `transfer` even when the tokens moved, so
decoding it would make a successful send look failed and invite a second one.
To show the user the transfer itself, `get_trc20_transfers` with `address`
set to the recipient lists it. A transaction
that is found but failed (for example out of energy) did not move the tokens;
say so plainly.
