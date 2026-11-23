# Launchpad-native token valuation (the platform's own coin)

Companion to `fee-token-valuation-ceiling.md` (fee/revenue token → run-rate × multiple vs the sector
leader). This file is the **launchpad-flagship** variant: the token is not a coin launched *on* the
platform, it *is* the platform's token. Then the platform's launch survival rate and its fee revenue are the
whole valuation, and the launchpad's own public API is the primary evidence.

Worked example: **HOURS / hours.fun, 1 Oct 2026**, token age 24,5 h (all figures pulled live that day).

## Get the platform's own numbers first

| Endpoint | Returns |
|---|---|
| `https://hours.fun/api/coins` | `coins[]{mint, pool, creator, symbol, name, windows, mcapSol, quoteReserveSol, volumeSol, createdAt, feePct, creatorSharePct, featured, graduated}` |

Keyless, no login, and it beats the marketing page. Look for the equivalent list/stats endpoint on any
launchpad (pump.fun-family, StonkFun `/api/public/v1/stats`, Moonshot, LetsBonk…) — the class of data is
always "how many launched, how many graduated, what volume, what fee".

## The eight measurements, in order

1. **Launch survival rate.** 45 coins launched in 24,5 h → **1 graduated**, and it is the flagship itself;
   **41/45 under 100 SOL mcap** (~$12k) and **23 with volume < 5 SOL**. A launchpad whose only survivor is
   its own token is a product demo, not a business. This single ratio decides more than any narrative check.
2. **Volume concentration.** 912 of 2.550 SOL of platform volume (**36%**) sat in the flagship token — the
   platform's "traction" is one coin deep.
3. **Fee math against mcap.** Flagship fee 1%, creator share 0% (fees accrue to the platform): lifetime fees
   on 912 SOL ≈ 9 SOL (~$1,1k) against a **$458k mcap ≈ 75× lifetime revenue**. Narrative-priced, not
   earnings-priced. Say the multiple.
4. **`windows` is the discriminator.** `[[0, 604800]]` = trades 24/7, while sibling coins carry scheduled
   trading windows (the product: Token-2022 transfer hook + Meteora Dynamic Bonding Curve). The 24/7 coin in
   the list is the platform token.
5. **Age disqualifies a thesis on its own.** 1-day-old token, −30% from ATH, 73,5% of supply in the top-100
   wallets, 241 bundler wallets (18,8% of volume), 1.002 bot-degen wallets, 1.865 holders, and 49 of the
   top-100 traders already fully exited while the top realized winners all sold 100%. Quote counts, not vibes.
6. **An unexplained whale is a finding.** One wallet held 7,3% ($32k) with zero buys and zero sells since
   pool creation — plausibly a vault/lock, but unverifiable from the available data. Report the overhang and
   say plainly the source is unknown; do not silently launder it into "team tokens are locked".
7. **Dev history ≠ project-account history.** The dev wallet had launched exactly 1 token and held a 0
   balance (clean), while the project's X account was 2 days old (188 followers) and had promoted 29 tokens.
   Both facts belong in the report, separately labelled.
8. **Cross-check the smart-money screen against the token.** 12 of the 43 wallets screened by
   `onchain-trader-screening` bought this launch in the first 10 minutes (entry mcap $52k–$180k) and most had
   flipped back out by mcap $120k–$250k — that is exit liquidity, not conviction. Only 1 of 4 KOL holders was
   still in. Check `gmgn-cli token holders/traders` and count the fully-exited among the top 100.

## Deliverable

Platform-traction numbers next to the user's own verified position (see
`wallet-position-pnl-reconstruction.md`), then the exit ladder — partial sell into the ATH re-test, stop at
the user's own average entry so the trade cannot become a loss. Never let "the product is real" stand in for
"the price is supported": the fee-vs-mcap multiple is what settles it, and the dead-launch ratio is what says
whether the platform can ever grow into the narrative.
