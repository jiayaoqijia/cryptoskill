# Vault forensics pass (Krystal-style agent vaults) — worked on Robinhood Chain, 20 Sep 2026

Trigger: the user drops a **vault URL** (`.../vaults/<chainId>/<addr>?r=<ref>`) and asks "worth trying?
is it transparent?". A vault is a *fund product with a promoter*: before rating the platform, prove
**whether the user can even enter it**, and **what the money actually did**. Data below verified live
20 Sep 2026; endpoints and field names drift — re-check top-level JSON keys before trusting output.

## 1. Endpoints that worked (keyless, no browser)

| What | URL |
|---|---|
| Vault detail (the JSON the app renders) | `https://api.krystal.app/all/v1/vaults/{chainId}/{vaultAddr}` |
| Vault positions / activities | `.../vaults/{chainId}/{vaultAddr}/positions`, `.../activities` |
| Cohort list (rank by TVL) | `https://api.krystal.app/all/v1/vaults?chainIds=4663&limit=100&page=1&sortBy=tvl` |
| Robinhood Chain 4663 — RPC | `https://rpc.mainnet.chain.robinhood.com` (chainId `0x1237`), fallback `https://robinhood-rpc.publicnode.com` |
| Robinhood Chain — explorer | `https://robinhoodchain.blockscout.com/api/v2/addresses/<addr>` (`/counters`, `/token-balances`) |
| Chain metadata (RPC list per chainId) | `https://chainid.network/chains.json` |
| DeFi platform TVL / hacks | `https://api.llama.fi/protocol/<slug>` |

The Krystal API sits behind a WAF: when a raw `curl` from the shell answers 403, fetch the same URL
through the render/extract proxy path — that returns the JSON (it arrives wrapped with a page header,
so parse the JSON body, and be ready to unescape `\"` artifacts). Docs are GitBook: `<docs>/llms.txt`
index, `.md` suffix for clean markdown.

## 2. Depositability test — do this FIRST

```
allowDeposit == true  AND  totalUser > 1   → other people can join (Community/Shared Vault)
allowDeposit == false AND  totalUser == 1  → private Auto-Farm Vault: ONE owner, nobody can deposit
```

Worked case: the promoted vault was `vaultType: autofarm`, `allowDeposit: false`, `totalUser: 1`,
`totalSupply: 1` share, owner `0x42e71af1f1f59434522308dfbe4a45724612c448`. Sampling the 30
largest autofarm vaults on chain 4663: **30/30 private, 0 depositable**. So the link was a
**showcase of the owner's own book + a referral ad**, not an investable product — lead the report
with that, because it changes the whole question ("nyoba" means *create your own vault*, not *join
this one*).

## 3. Cash-flow reconciliation — the core technique

Panel fields lie in different directions; only the cash flow settles it:

```
net_flow = userPerformance.totalDepositValue − userPerformance.totalWithdrawValue − tvl
```

| Field | Worked case | Meaning |
|---|---|---|
| `userPerformance.totalDepositValue` | $4,515.29 | all deposits, USD at tx time |
| `userPerformance.totalWithdrawValue` | $3,810.95 | all withdrawals |
| `tvl` | $542.31 | value left (confirmed by on-chain balances) |
| → net | **−$162.03 (−23% of the $704 net capital in)** | the number that matters |
| `feeGenerated` | $254.88 (30d $203.08, 24h $8.35) | gross LP fees — *not* profit |
| `pnl` | **+$68.94** | sum of per-strategy `pnl` → contradicts cash flow |

`feeGenerated − net_flow` ≈ what price/IL drag ate ($185 here). Green panel + negative cash flow is
the standard failure mode of these vaults — report both numbers side by side and say they don't
reconcile.

**APR field is unusable for ranking.** Krystal's own FAQ formula is `(earning24h × 365) / liquidity`
= 8.35 × 365 / 542.31 = **562%**, while the vault's `apr`/`feeApr` field said **5.998%** and 30d
fees/TVL said 37%/month. Three numbers, three stories → rank by cash flow and gross fees, cite the
APR field only as *"panel says X, its own docs' formula says Y"*.

## 4. On-chain verification of the vault (claim vs chain)

RPC calls that matched the API exactly: `eth_getBalance` + `balanceOf` for each holding (7/7 exact),
and position-NFT count via `balanceOf(vault)` on the Uniswap V3 NFPM
(`0x73991a…` = 153) and V4 PositionManager (`0x58daec…` = 28) = 181 sub-positions vs 181 asset rows.
Also: `eth_getCode` on the vault returns a **45-byte EIP-1167 minimal proxy** → read the
implementation address out of it (worked case `0x34c1b3f20c83f0d959ea8ff5a6d37960bd2362e3`) before
judging "unverified contract"; `eth_getTransactionCount` + balance on the owner EOA (0 code = EOA,
nonce 196, 0.016 ETH = small operator, not a whale) for the promoter-size question the PnL card
leaves open.

Position sample worth printing: `strategies[].status` (CLOSED vs IN_RANGE), `ageInSecond`
(median 0.64 d → ~2.5 rotations/day proves a live agent), `feeTierPercentage` distribution
(1% tier on 72/110 — fee-tier aggression is the strategy's real risk), `initialDepositValue`, `pnl`,
and per-position `pool` `apr30d` / `volume30d` / `fee30d` / `drawdown24h`.

## 5. Why the fees lose: read the pools, not the vault

The farmed pools were Robinhood Chain meme/stock-token pools — fee APR enormous, price decay bigger:

| Pool | pool TVL | 30d volume | 30d fees | apr30d | drawdown 24h |
|---|---|---|---|---|---|
| WETH–AI 1% | $3.41M | $245M | $2.05M | 1,641% | −13.8% |
| WETH–CHUMP 1% | $1.12M | $79M | $661K | 899% | −16.9% |
| WETH–PONS 0.3% | $5.52M | $571M | $1.43M | 698% | −9.7% |
| CASHCAT–WETH 0.3% | $2.41M | $479M | $1.20M | 596% | −19.6% |

Print `drawdown24h` beside `apr30d` every time — "feral fee APR × 10–20%/day drawdown" is the
one-line explanation of a negative net flow, and it tells the user which pairs to prefer (a
stable leg, e.g. PONS/USDG or WETH/USDG, instead of two memes).

## 6. Cohort sanity check before rating the chain-level opportunity

Aggregate the N largest same-type vaults on that chain from the list endpoint:
30 vaults → deposits $190,557, withdrawals $162,545, remaining TVL $16,563 (= −$11,450 net) while
cumulative `feeGenerated` was $12,434; 17/30 negative `pnl`; TVL median $142; `riskScore: HIGH` 30/30.
One vault can be bad luck; a *cohort* that nets negative while generating fees in the same order of
magnitude is a property of the venue. State it as platform/chain-level evidence.

## 7. Referral & conflict-of-interest check

Resolve `?r=<name>` to the promoter wallet (here `0x42e71…c448`, the same wallet from the X post on
16 Sep) and compare it with the vault's `owner` field. Same wallet ⇒ the poster is promoting **his own
vault**, and the economics stack: referral share of the invitee's yield + copy fee + league ranking
(leaderboards rank by owner fees *and* copier fees — verified in the Robinhood Yield League article:
#1 "RAPTOR_X" $6,508 fees / 81 copiers). Say "anggep iklan, bukan review", then tell them to enter
without the `?r=` param or to make their own referral.

## 8. Honest limits to write down

- `copyCount` (406) and copy-fee totals ($16,796) are **backend accounting** — unverifiable on-chain.
  What you *can* prove: sample the copier addresses and `eth_getCode` them (40/40 live contracts here).
- The app UI (Agent Overview / Chat / Action Logs / Terminal) may be unreachable from the server
  (Cloudflare). Then the transparency claim for *logs* is documentation-only — mark it ⚠️, don't
  claim you saw it.
- A private vault has **no deposit path**, so never present it as something to try; test = own vault.

## 9. Fee ladder to quote (docs, verified 20 Sep 2026)

Auto-Farm Vault **10% of all rewards generated** (zap/rebalance/compound inside the vault free) ·
Community Vault 10% (5% if sharing) **+ owner commission** · zap/manual rebalance 0.05–0.25% ·
auto-rebalance/auto-exit 0.01–0.05% per execution · auto-compound/auto-harvest **2% of LP fee** per
run · swap 0.1% · withdraw 0.01%. Against Meteora (LP keeps 90% of swap fee, zero performance fee):
the agent must beat manual rules by the fee it skims before it breaks even.

Vault note naming for this class: `~/obsidian-vault/DD - <Subject> (<Platform> <Chain>).md`,
linked back from the older platform note under `Lihat juga:`.
