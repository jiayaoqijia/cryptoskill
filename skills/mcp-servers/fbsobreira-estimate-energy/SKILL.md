---
name: estimate-energy
description: Estimate what a TRON transaction will cost in energy, bandwidth and burned TRX with the GoTRON MCP tools, and explain whether to burn TRX or stake for energy. Use when the user asks how much a USDT or TRC20 transfer, a TRX transfer or a smart contract call will cost, why a fee is high, or whether they have enough energy.
---

# Estimate energy and fees on TRON

On TRON a transaction spends energy (smart contract execution) and bandwidth
(transaction size). What the account's staked resources don't cover is paid
by burning TRX at the network price. The tools below report numbers from the
connected node; quote them, and don't fill gaps with remembered figures.

Start with `get_network` and say which network the numbers come from. Prices
and limits differ between mainnet and testnets.

## Transfers (TRX, USDT and other TRC20)

Call `analyze_transfer_cost` with `from`, `to` and `amount`, plus
`contract_address` for a TRC20 token (USDT on mainnet is
`TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`). It returns:

- `energy_required` and `bandwidth_required`
- `account_energy_available` and `account_bandwidth_available`
- `cost_breakdown`: per resource, whether staked resources cover it
  (`use_staked`) or TRX is burned (`burn_trx`, with `cost_trx` and the deficit)
- `total_estimated_cost_trx`, plus `energy_price_sun` and
  `bandwidth_price_sun` per unit

The sender and recipient matter, not only the amount. A USDT transfer to an
address that has never held USDT needs roughly twice the energy of one to an
existing holder. If the user only wants the energy figure without the cost
breakdown, `estimate_trc20_energy` takes the same `from`, `to`,
`contract_address` and `amount`.

If the result has a `warning` that energy estimation is unavailable on this
node, say the cost is unknown and give the range from the warning as a range,
not an estimate.

## Smart contract calls

Call `estimate_energy` with `from`, `contract_address`, `method` (the
signature, such as `"transfer(address,uint256)"`) and `params` as a JSON array.
If you don't know the signature, `list_contract_methods` with
`contract_address` lists it. To turn the energy into TRX, multiply by the
energy price from `get_energy_prices` (in SUN per unit; 1 TRX = 1,000,000 SUN),
and compare with the account's available energy from `get_account_resources`
(`energy_limit` minus `energy_used`).

## Burn or stake

When the user pays by burning TRX, explain the alternative and let them
choose; don't push either:

- **Burn:** nothing to set up; each transaction costs the TRX shown.
- **Stake for energy:** staking TRX (`freeze_balance` with `resource` set to
  `ENERGY`) gives a share of the network's daily energy, which regenerates
  over 24 hours. It suits regular senders. Staked TRX stays the user's, but
  getting it back takes an unstake and a waiting period (currently 14 days
  on mainnet; it is a network parameter and can change).
  These tools don't report how much energy one staked TRX yields, so don't
  quote a figure for it. After staking, `get_account_resources` shows the
  new `energy_limit`.
- **Delegation:** another account can delegate energy to this one
  (`delegate_resource`, signed by the delegator). `get_delegatable_amount`
  shows how much an account can still delegate.

Staking and delegation build unsigned transactions like any write tool. If the
user goes ahead, follow the same confirm-then-sign steps as a transfer: sign
with the local keystore when signing tools are available, otherwise hand the
user the transaction to sign with their own wallet.

## Reporting

Give the user, in this order: the total TRX they will burn (or that staked
resources cover it), what drives it (energy or bandwidth), and the inputs
behind it (energy required, available, price). Round TRX to two decimals in
prose, and keep the exact figures available if they ask.

For a smart contract call, `estimate_energy` covers energy only. Report that
figure as the energy cost, not the total, and say bandwidth isn't included:
an account without enough bandwidth also burns TRX for it.
