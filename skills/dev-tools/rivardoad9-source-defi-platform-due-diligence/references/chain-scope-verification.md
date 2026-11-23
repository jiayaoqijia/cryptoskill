# Chain-scope questions ("does <protocol> have <chain>?") — verify, don't recall

Triggered by *"di meteora ada robinhood chain ga?"* (16 Sep 2026). The answer was **no**, and the
premise came from a *tool's* feature list — a classic layer mix-up worth its own recipe because the
user asks this shape of question whenever a new chain or product trends.

## Three keyless checks (all of them, in this order)

**1. The protocol's own docs index** — count chain names in the official `llms.txt`:

```bash
curl -s https://docs.<protocol-host>/llms.txt | python3 -c "
import sys; t=sys.stdin.read()
for kw in ['Solana','EVM','Ethereum','Arbitrum','Base','Robinhood','multi-chain']:
    print(f'{kw:12} {t.count(kw)}')"
```

Worked case: 61.477 chars, `Solana 4`, everything else **0**. A 60k-char official index with zero
mentions of a chain is stronger evidence than any marketing page. The tagline ("…on Solana") is a
second free confirmation.

**2. DefiLlama** — `https://api.llama.fi/protocol/<slug>`:

- `chains: ['Solana']` on `protocol/meteora-dlmm`.
- On `protocol/meteora`, `chains` came back **empty** while `currentChainTvls {"Solana": 295883700}`
  named the chain anyway → read both fields, an empty `chains` array is not "no chain".

**3. The GitHub org** — if every program/SDK in it targets one chain, there is no other deployment to
look for. `MeteoraAg`: damm-v2, dlmm-sdk, dynamic-bonding-curve, presale, zap, vault — all Solana
programs (+2 Go SDKs), zero EVM contracts.

## Then attribute the chain to the right layer

A tool can legitimately support a chain its data source does not. Prove it from the bundle instead of
inferring from a tweet: grep the page chunk for the chain name + the protocol the tool actually talks to.

Worked case: `metina.id`'s PnL card chunk contained a chain selector `AUTO / ROBINHOOD / BASE / BNB`
with **protocol = Uniswap** (version derived from `uniswapVersion`/`payload.binStep`, v2/v3/v4),
explorer `robinhoodchain.blockscout.com`, and an `EVM` label in its event guard — while the same site's
pool/portfolio pages read `dlmm.datapi.meteora.ag`. So: **Robinhood Chain support = Uniswap positions on
an EVM L2 (Arbitrum Orbit, chain ID 4663, ETH gas)**, not Meteora moving chains.

Facts to carry for that comparison: Robinhood Chain launched 1 Jul 2026; ~$1B TVL and $1,88B/day DEX
volume (13 Sep 2026); **≈95% of its DEX volume is Uniswap** v2/v3/v4.

## How to phrase the consequence

- Protocol-side answer first, with the three proofs.
- Then the layer correction ("yang punya fitur itu tool-nya, dan protokol LP-nya Uniswap").
- Then the engine implication: Meteora DLMM = Solana programs; LP on an EVM L2 means a different stack
  end-to-end (viem/ethers, position-manager NFT, fee tiers 0,05/0,3/1%, no bins) → **an engine port,
  not a config change.** Saying that plainly stops the user from expecting a settings toggle.
