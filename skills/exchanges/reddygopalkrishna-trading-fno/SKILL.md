---
name: trading-fno
description: Futures and options (F&O) analysis for India (NSE) and US - Black-Scholes price and Greeks (delta, gamma, theta, vega), implied volatility from a price, multi-leg payoff with breakevens and max profit/loss (long/short calls and puts, spreads, straddles, strangles, iron condor, butterfly), and option-chain reading - open interest, put/call ratio, max pain, OI walls, ATM straddle and implied move. Chains come from a US ticker (Cboe delayed data), an NSE option-chain CSV you download, or Kite instruments and quotes when Kite is set up. Analysis only, never places an order. Use when the user says "option chain", "PCR", "max pain", "what are the Greeks", "implied volatility", "payoff of an iron condor", "breakeven on this spread", "NIFTY options", "F&O", or before sizing an options trade.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# F&O Analysis (`trading-fno`)

Reads an option chain and prices option positions. **It never places an order.** Anything you decide to
trade still goes: trading-risk approval -> trading-broker preview -> the user's explicit confirm -> submit.

```bash
python3 scripts/fno.py greeks --spot 24500 --strike 24600 --kind call --days 7 --iv 14 --lot-size 75
python3 scripts/fno.py iv --price 120 --spot 24500 --strike 24600 --kind call --days 7
python3 scripts/fno.py payoff --kind put --side short --strike 24400 --premium 95 --lot-size 75 --spot 24500 --chart
python3 scripts/fno.py strategies                                    # the named shapes
python3 scripts/fno.py strategy --name iron-condor --strikes 24000,24200,24800,25000 \
    --premiums 20,60,55,18 --lot-size 75 --spot 24500 --chart
python3 scripts/fno.py strategy --legs +1C24600@120 -1C24800@60 --lot-size 75   # custom legs
python3 scripts/fno.py chain AAPL                                    # US chain, nearest expiry
python3 scripts/fno.py chain SPY --expiry 2026-12-18
python3 scripts/fno.py chain --file ~/Downloads/option-chain.csv --spot 24512 --expiry 2026-11-27 NIFTY
python3 scripts/fno.py chain NIFTY --kite                            # needs Kite with market data
```

Add `--json` to any command for machine-readable output.

## Data sources (be plain about what is available)

| Market | Source | Notes |
|---|---|---|
| US | Cboe delayed-quotes JSON (`cdn-api.cboe.com`) | Plain GET, no key, about 15 min delayed. An unofficial public endpoint that can change. Yahoo's options endpoint needs a cookie and crumb session, so it is **not** used, and nothing here imitates a browser. |
| India (NSE) | The option-chain CSV the user downloads from nseindia.com (Option Chain page -> Download) | nseindia.com blocks programs, and this skill does not try to get around that. The CSV has no spot or expiry, so pass `--spot` and `--expiry`. Columns are read by header name. |
| India (NSE) | Kite Connect: `--kite` | Instruments (strikes, expiries, **lot size**) plus quotes (OI, volume, depth). Quotes need Kite's paid market-data plan; with a free plan or no login the command says so and points to the CSV. Index spot keys are mapped (NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY); pass `--spot` if the spot is missing. |

If a source is not available, tell the user which one and what to do instead. Never invent chain data.
Cboe's own IV is used for US; the NSE CSV's IV column is used for India; Kite quotes carry no IV, so use
the `iv` command on a price when you need one.

## Rules

1. **Lot sizes come from the user or Kite's instruments**, never from memory (they are revised by the
   exchange). Without `--lot-size`, results are per unit and the output says so.
2. **Black-Scholes is an estimate.** It is European-style with constant volatility and a flat rate
   (`--rate`, default 5%, set it to the local risk-free rate). Index options (NIFTY, SPX) are European;
   stock options are not, so Greeks there are approximations. Units: theta per calendar day, vega per 1
   volatility point.
3. **Payoff is at expiry**, before brokerage, taxes, STT/fees and margin. Short strangles, naked calls and
   naked puts show their real risk; say "unlimited" when the tool does.
4. **Read the chain honestly.** PCR, OI walls and max pain describe positioning; they are not forecasts.
   Max pain is where option buyers lose most at expiry, a level people watch. Stale last-traded prices on
   illiquid strikes mislead: prefer the bid/ask midpoint, and note the data is delayed.
5. Price a leg you have no quote for with `--spot --iv --days` (marked "Black-Scholes" in the output), and
   say that premium is modelled, not quoted.

## Steps

1. Pick the source for the market (above). Get the chain; if US and it fails, report the HTTP reason.
2. `chain`: report spot, expiry, PCR, max pain, the biggest call/put OI strikes, the ATM straddle and the
   implied move. Say the data's age and source.
3. For a view the user has, build the position with `strategy` (use the chain's quotes as premiums), show
   max profit, max loss, breakevens, and the net debit/credit. Compare breakevens with the implied move.
4. `greeks` for the position's legs when theta, delta or vega matter (earnings, expiry week).
5. To trade it: hand the legs to trading-risk, then trading-broker preview, then the user's explicit
   confirm. Check trading-earnings first: IV usually falls after the event, whatever the stock does.

Options can lose the whole premium, and short options can lose far more than the account. This is
analysis, not advice.
