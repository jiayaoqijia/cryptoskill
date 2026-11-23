# Exchange exit → self-custody

Triggered by: *"gw mau stop pakai exchange"*, *"pindahin semua ke hardware wallet"*, *"biar nggak gatel trading"*.
Deliverable: a migration sequence with real balances, real network fees, and a behaviour plan — not a pep talk
about self-custody.

## 1. Read the actual book first

The plan is sized by what is really there, not by what the user remembers. Before advising anything, pull the
live account: spot balances, Simple Earn (flexible + locked), open orders, futures wallet and positions.
`binance_porto.py` already prints this card; the `--json` dump is the machine-readable version.

What this changes: a user talking about "my whole portfolio" may hold one stablecoin in Earn with a zero spot
balance. Saying that plainly resets the plan from "migrate a portfolio" to "move $500 and stop the habit".

## 2. Free the funds before planning a withdrawal

Flexible Earn must be redeemed to spot (instant, no fee); locked Earn has an end date and cannot be moved early.
Check `canRedeem` / locked rows, and state the date instead of discovering it during the transfer.

## 3. Get the exact withdrawal cost from the API, not from memory

Fees and minimums change per network and per coin, and the cheapest network is often the one the destination
wallet does not support. Read the live table (signed, read-only, no side effect):

```python
# GET /sapi/v1/capital/config/getall  (HMAC-SHA256, timestamp + recvWindow, X-MBX-APIKEY)
for c in data:
    if c["coin"] == "USDT":
        for n in c["networkList"]:
            print(n["network"], n["withdrawEnable"], n["withdrawFee"],
                  n["withdrawMin"], n.get("busy"), n.get("name"))
```

Report the table for the networks that matter (BSC, ETH, TRX, SOL, Polygon, Arbitrum, Base) rather than the
single cheapest one; `withdrawEnable=False` or `busy=True` is a hard stop that no amount of fee arithmetic fixes.

## 4. Sequence that survives contact with reality

1. Device in hand, set up, and a receive address generated on it. Never send to an address you have not seen
   the wallet produce.
2. Send a **test amount** (for stables, ~$20). Confirm it lands and the address string matches end to end.
3. Send the remainder only after the test confirms.
4. **Fund gas.** On BSC, moving USDT later costs BNB; on Ethereum it costs ETH. Send a small gas top-up to the
   same address, or the balance is stranded until the user buys gas on an exchange again.
5. After the balance reaches zero, enable an address whitelist on the exchange. It converts a future panic
   transfer into something that cannot leave the book.
6. Record the withdrawal hashes and export the trade history for cost basis.

## 5. Hardware wallet caveats to state before purchase

- **Seedless backup is not "no backup".** The cards are copies of one key: losing every card loses the funds.
  A backup card that is lost generally cannot be re-linked to the same wallet, so a 3-card pack is the honest
  recommendation when the setup is meant to last.
- **No screen = the phone is the verification surface.** Address substitution by clipboard malware is the live
  risk; verify first and last characters on the device app, not from a copied string.
- **Closed firmware and no independent display** are real trade-offs, not disqualifiers — say them once, then
  move on.
- **Cost against balance.** At a few hundred dollars, the device costs a double-digit percentage of the assets;
  call it behaviour tooling rather than security, and say at what balance it starts paying for itself.

## 6. The habit, not the wallet

A cold wallet adds friction; it does not remove the impulse. Pair the move with levers that actually bind:
kill futures access on the account (not a promise), remove the exchange app from the daily phone, and set a
72-hour wait between deciding to send funds back and sending them. Review after a month: if nothing was moved
back, the friction worked.

## 7. Pause the monitors you are about to orphan

Cron jobs that read the exchange balance will keep reporting `$0` or erroring every 30 minutes once the account
is empty. Pause them as part of the migration and say which ones, so the user does not read it as a broken job.
Public-data collectors can stay.

## Boundaries

- Never execute a withdrawal, redemption, or trade on the user's behalf. Withdrawals need 2FA/email codes and the
  user's own approval; the deliverable is the numbered sequence, the amounts, and the fees.
- Moving between the user's own wallets is not a taxable sale; selling on a registered exchange is, and the tax is
  withheld at source. Keep the records either way.
