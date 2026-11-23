# Worked case: Krystal vs Meteora (16 Sep 2026)

Input: user dropped `https://x.com/bukanpamanmu/status/2100028152252948568` with
*"apakah platform ini layak di coba, rating dan bandingkan dengan meteora"*. No other context.
Output: rating + comparison + vault note `Ide Project - Krystal (LP Agent EVM) vs Meteora.md`.

## What the post actually was

`@bukanpamanmu` ("pamanberuang", blue verified), 16 Sep 2026 01:05 UTC, 4 fav / 2 reply. Text =
filler about a market dump, **zero performance numbers**. The useful content was in
`entities.urls[].expanded_url`: `defi.krystal.app/account/0x42e71…c448/positions?r=paman` → the
**platform is Krystal**, and `?r=paman` marks the post as a **referral ad** (Krystal's referral
program pays the referrer a share of the invitee's *yield*).

Screenshot (transcribed with vision): Krystal portfolio, Sept 2026, `9 vaults · 2 positions`,
**Monthly PnL +$136.70**; daily array had 8 up days (+305.73) vs 7 down days (−169.03) = net
136.70. **No capital, no APR, no TVL, no pool name** ⇒ unratable, which was reported as the first
finding.

## Wallet check (Blockscout, keyless)

Base / Ethereum / Arbitrum / Polygon for `0x42e71af1f1f59434522308dfbe4a45724612c448`:
native ≈ $1–2 per chain, real tokens ≈ **$27 total** (NPC 1,110 ≈ $21.7, AERO 4.64, AWETH
0.000526), plus ~80 dust / scam-airdrop tokens ("Claim: aerodrome.supply",
"NC-Eligible nodepay.promo", "ARB | t.me/s/claimarb", fake USDC/USDT claims,
"🎁 5K$ Airdrop at bit.ly/shibaz"). BSC / Ronin / HyperEVM have no Blockscout instance and
`api.krystal.app` answered `403 Just a moment` ⇒ **size unverified** (principal sits inside vault
contracts) — reported as a gap, not as proof of a scam.

## Platform numbers (api.llama.fi, 16 Sep 2026)

| Krystal | |
|---|---|
| TVL total | **$819,128** (Auto-Farm $584,756 · Community $234,372) |
| per chain | Base $401K · BSC $171K · Robinhood Chain $109K · Arb $60K · ETH $32K · **Solana $21.5K** · Polygon $19K · HyperEVM $5K · Ronin $239 |
| hacks | none recorded |
| funding | $6.6M seed, Aug 2021 (Crypto.com, Hashed, BlockTower, Coin98, Arrington, LD Capital) |
| audit | Code4rena Jun 2024 — 1,137 LOC, 6 researchers, 5 medium + 5 low (3 fixed, 2 accepted w/ mitigation); Admin = **multisig 5-of-6** (roles Admin/Operator/Withdrawer) |
| token | none — Point System live since Mar 2024 (airdrop speculation) |

Krystal fee schedule (docs, `ecosystem/fees`): **Auto-Farm Vault 10% of all generated rewards**;
shared/community vault 10% (5% if sharing on) **+ owner commission**; vault withdrawal 0.01%;
zap 0.05/0.1/0.25% by fee tier; manual rebalance & compound 0.05/0.1/0.25%; auto-rebalance &
auto-exit 0.01/0.03/0.05%; **auto-compound & auto-harvest 2% of LP fees each run**; swap 0.1%.

## Incumbent (api.llama.fi/protocol/meteora + docs.meteora.ag/protocol/protocol-revenues)

TVL **$296.7M** (DLMM $184M) · 30d fees $23.4M (cumulative $1.478B) · 24h volume $234M ·
208,541 active addresses/24h · treasury $14.26M · MET mcap $108M.
Fee split: **DLMM standard pool = protocol 10% / LP 90% of the trading fee**; launch pools 20/80;
limit orders 50/50; DAMM v2 20/80; DAMM v1 20/80 (0% stable). **No performance or management fee.**
One incident: 17 Jan 2026, $1.5M — *social engineering / impersonation*, not a contract bug.

## The comparison line that mattered

Krystal takes **10% of your rewards**; Meteora takes **10% of the swap fee while you keep 90%** —
same "10%", opposite meaning. Plus Krystal stacks 2%/compound + per-rebalance % + EVM gas, and its
Solana side is $21.5K of TVL (i.e. no sample on the chain the user actually farms).

## Ratings handed back (per-use-case, not one score)

- Krystal **6/10** — real product, audited, non-custodial, agent works; minus for $819K TVL, layered
  fees, and the docs' own admission that a Community Vault owner can act against depositors'
  expectations.
- Meteora **8.5/10** for this user — deepest Solana liquidity, LP keeps 90% of swap fee, no perf
  fee, own engine already running; minus the social-engineering incident.
- Verdict: **eksperimen kecil, bukan pengganti** — Auto-Farm Vault (not someone's Community Vault),
  Base, WETH/USDC or WETH/cbBTC, $100–200, 30 days, then compare to the user's own Meteora numbers.
  Solana side: skip until it has real TVL.
- Layer mismatch named explicitly: Krystal = manager/agent layer on top of DEXs; Meteora = the DEX
  protocol itself. Different questions, so "which is better" was split into two ratings.
