---
name: dexe-create-dao
description: |
  Deploy a new DeXe DAO with the one-call `dexe_dao_create` composite. Use SIMPLE
  mode (symbol + totalSupply) and let the tool synthesize a coherent, governance-
  safe config — it previews the resolved config + a safety proof and only
  broadcasts on confirm. Covers the quorum turnout rule (quorum ≤ 0.8 × votable
  share) and the ≥50% floor, the implicit-treasury pattern, and the deploy
  gotchas. Use when the user
  says "create/deploy a DAO".
---

# dexe-create-dao

Deploy a DeXe governance DAO in **one tool call**. `dexe_dao_create` handles
avatar → DAO IPFS metadata → `PoolFactory.deployGovPool` (predicted-address
wiring, 1→5 settings auto-expand, executorDescription upload) → **pre-sign
eth_call simulation** → broadcast.

Since v0.24.0 the deploy path is guarded end-to-end: offline coherence checks,
a calldata round-trip self-check (decoded == intended params), a name-collision
pre-check, and a live simulation of the exact calldata from the deployer right
before signing. **A provable revert is refused before any gas is spent** and
comes back with a classified cause + fix. If a tool error arrives with a
`Fix:` line — apply that fix verbatim and re-run; do not improvise
alternative parameters.

**Do NOT hand-fabricate token splits or quorum numbers.** That is exactly how you
ship a broken DAO. Use SIMPLE mode and let the tool synthesize + verify a coherent
config, or read the two rules below and satisfy them.

## The two rules that make a DAO usable (the tool enforces both)

A DeXe DAO holds two kinds of tokens: **votable** (distributed to real wallets)
and **treasury** (held by the DAO/govPool — these **cannot vote**).

1. **Quorum must pass on realistic turnout:** `quorum% ≤ 0.8 × (100 − treasury%)`
   under the default LINEAR vote model. A quorum equal to the votable share is
   reachable on paper and frozen in practice — it demands 100% turnout, so one
   holder asleep, sold out or key-lost and **no proposal ever passes again**,
   including the one that would fix the quorum. Over the ceiling the call comes
   back `mode:"blocked-risky"` with `maxQuorumPercentForThisDistribution` and
   `minVotablePercentForThisQuorum`; `confirmRisky: true` overrides it.
2. **Quorum floor ≥ 50%** (51% recommended). Below 50%, a small group can pass
   proposals and even drain the treasury. Advisory, surfaced in the preview.

Together these cap **treasury% at 37.5%** of supply. The tool's own defaults are
**treasury 30% / quorum 51%** — 72.86% required turnout, inside the 80% ceiling.
Omit both fields and `dexe_dao_create` synthesizes that split for you.

**Want the DAO to control most of the supply?** It cannot sit in the deploy-time
treasury (cap ~37.5%) — and moving supply into the GovPool *after* deploy
re-creates the same dead DAO, because quorum is a % of **total** supply. Put the
reserve in a DAO-controlled wallet/Safe listed in `recipients[]`: those tokens
stay votable, so they count toward quorum and can vote.

## Golden rule: validate on testnet first

Deploy to **BSC testnet (chain 97)** first (`chainId: 97`) — free faucet BNB.
**Mainnet (chain 56) works** (the frontend ships there daily) and is supported,
but it spends real BNB, so `dexe_dao_create` requires `confirm: true` for any
mainnet broadcast. Never confirm a mainnet deploy without the user explicitly
asking.

## Recipe — SIMPLE mode (recommended)

0. **Orient:** `dexe_context` — shows signer, active chain, env readiness, and
   DAOs you already deployed.
1. **Env:** ensure the target chain is 97 and `DEXE_PINATA_JWT` is set (metadata).
2. **(Optional) avatar:** `dexe_dao_generate_avatar` / `dexe_ipfs_upload_avatar`
   → pass the `cid` as `avatarCID`. Since v0.20.0 both enforce real raster
   bytes (generate renders a true JPEG; upload rejects SVG/HTML by magic-byte
   check), so any CID they return is safe to use.
3. **Preview:** call `dexe_dao_create` with just the essentials:

```jsonc
dexe_dao_create({
  chainId: 97,
  daoName: "Aurora Collective",
  symbol: "AUR",
  totalSupply: "1000000",     // whole tokens
  // optional — OMIT BOTH to let the tool pick a governable split (30 / 51):
  treasuryPercent: 30,        // implicit remainder held by the DAO (can't vote)
  quorumPercent: 51,          // must be ≥50 AND ≤ 0.8 × (100 − treasuryPercent)
  voteModel: "LINEAR",        // 1 token = 1 vote (default); or "POLYNOMIAL"
  durationSeconds: 86400,     // 1 day
  minVotesTokens: "1",        // min balance to vote AND create, whole tokens (≤ largest holder)
  earlyCompletion: true,      // end voting as soon as quorum is reached
  daoDescription: "A community treasury DAO.",
  avatarCID: "bafy…"          // optional; or avatarPath: local image path the server uploads
})
```

This returns `mode: "preview"` with the **resolved config** (who holds what) and a
**safety proof** (votable %, quorum %, reachable?, floor OK?). Show it to the user.

4. **Confirm:** re-call with the **same arguments plus `confirm: true`** to broadcast.
   The deployer holds the entire distributed portion; the treasury is an **implicit
   remainder** (the govPool address is never a token recipient).
   When the user has **already approved** the deploy up front, pass
   `confirm: true` on the **first** call — preview and broadcast collapse into
   one call.
5. **Simulation verdict:** on broadcast, the tool simulates the exact calldata
   (eth_call from the deployer) first. Three outcomes:
   - `✓ simulated OK` in the note → the tx was proven against live state before signing.
   - **refused with `WOULD REVERT` + cause + fix** → no gas was spent; apply
     the fix verbatim and re-run.
   - `⚠️ simulation unavailable` → the RPC failed, the deploy proceeded
     unverified (offline guards still ran). Not an error.
6. **After success:** the result includes `readiness.govPoolLive` (the pool's
   code was verified on-chain) and `nextSteps` — follow it for the first
   proposal (deposit-first; fresh pools reject the bundled multicall pattern).

## Recipe — ADVANCED mode (full control)

Pass a full `params` struct (same shape as `dexe_dao_build_deploy`) instead of the
SIMPLE fields. The coherence guards still run. Key rules for hand-built params:

- **Treasury is an implicit remainder.** `tokenParams.users`/`amounts` list only
  external wallets; `sum(amounts)` is **less than** `mintedTotal` (the contract
  mints the remainder to the DAO). **Never** put the predicted govPool in `users[]`.
- Pass **one** `proposalSettings` entry → auto-expands to 5.
- `votePowerParams.voteType: "LINEAR_VOTES"` — `initData` is auto-encoded; don't pass it.

## Deploy gotchas (the tool pre-flights these — heed the errors)

1. **Un-passable quorum** — clearing it would need more than 80% of the votable
   supply to turn out (`quorum% > 0.8 × (100 − treasury%)`). Lower quorum,
   distribute more to voters, or shrink the treasury. (`blocked-risky`;
   `confirmRisky: true` overrides). A quorum above the votable share outright is
   a hard block.
2. **min-votes above every holder** — `minVotesForVoting/Creating` must be ≤ the
   largest single recipient. (hard block)
3. **cap** — must be `> 0` AND `≥ mintedTotal`. There is **no uncapped mode**
   (`cap = 0` reverts `ERC20Capped: cap is 0`); `cap == mintedTotal` is a valid
   fixed supply; `cap < mintedTotal` reverts. SIMPLE mode sets `cap = totalSupply`. (hard block)
4. **LINEAR initData** — auto-encoded (`__LinearPower_init()` = `0x892aea1f`). Never
   pass `initData` for LINEAR/POLYNOMIAL; only CUSTOM_VOTES takes a manual one.
5. **Non-zero governance asset** — if not creating a token, set
   `userKeeperParams.tokenAddress` or `.nftAddress`.
6. **Over-distribution** — `sum(amounts)` must be ≤ `mintedTotal`. (An implicit
   treasury remainder is correct and expected — do NOT force them equal.)
7. **Name collision** — a deployer can use each DAO name once per chain
   (create2 salt = deployer + name). The tool pre-checks and tells you to pick
   a different name. (hard block, v0.24)
8. **Validators** — no duplicates, no zero balances, validator quorum
   0 < q ≤ 1e27, duration > 0. (hard block, v0.24)

## Decimal conventions (must match the frontend)

- `quorum`, `quorumValidators`, `voteRewardsCoefficient`: **25-dec** wei (50% = `5e26`, 100% = `1e27`).
- `minVotes*`, `cap`, `mintedTotal`, `amounts`, `individualPower`, rewards: **18-dec** wei.
- `duration*`, `executionDelay`: plain **seconds** as string.
- `delegatedVotingAllowed` is **inverted**: `true` DISABLES delegation, `false` ALLOWS it.

## Pre-submit self-check (before `confirm: true`)

- [ ] `quorumPercent ≤ 0.8 × (100 − treasuryPercent)` (passes on realistic turnout) and `≥ 50` (floor)?
- [ ] treasury is an implicit remainder — govPool NOT in `users[]`?
- [ ] `sum(amounts) ≤ mintedTotal`, and `cap ≥ mintedTotal > 0` (never cap=0)?
- [ ] validating on testnet (97) first, or the user explicitly asked for mainnet?

## After deploy

The result includes `predictedGovPool` — the DAO's GovPool address once the tx
confirms. Use it for `dexe_proposal_create` / `dexe_proposal_vote_and_execute`.

DAOs deployed by `dexe_dao_create` have the **TokenSale + Distribution
executors and all 5 settings groups auto-wired** (since v0.19) — the OTC
journey ([[dexe-otc]]) works immediately after deploy, no extra settings
proposal needed.

Related: [[dexe-create-proposal]], [[dexe-vote-execute]].

## Canonical recipe (generated from src/knowledge/ — edit there, then `npm run gen:knowledge`)

<!-- BEGIN GENERATED: flow-recipe -->
### Create (deploy) a DAO (`create_dao`)

Deploy a new DeXe governance DAO with its gov token in one composite call (preview → confirm → broadcast).
- **chain 56:** MAINNET — the deploy spends real BNB (cents, ~0.1 gwei). Confirm the user accepts mainnet before broadcasting.
- **chain 97:** Testnet rehearsal: free faucet BNB (https://www.bnbchain.org/en/testnet-faucet). Staking, subgraph reads and off-chain proposals do NOT exist on 97.

**Ask the user:**
- `daoName` — What should the DAO be called? (public, permanent; also the on-chain pool name) · constraint: Non-empty; this deployer must not have used the same name on this chain before.
- `symbol` — Gov token symbol? (e.g. 'GENA')
- `totalSupply` — Total token supply, in whole tokens? (e.g. '1000000') · constraint: > 0. Cap is set equal to minted supply (fixed supply) unless ADVANCED params say otherwise.
- `treasuryPercent` (optional) — What % of supply should the DAO treasury hold? (the rest goes to your deployer wallet as votable supply) · default `30` · constraint: 0 ≤ treasury ≤ 100 − quorumPercent/0.8 (LINEAR; ≤ 37.5 at the 50% floor; lower under POLYNOMIAL). · ⚠ Treasury tokens CANNOT vote. Clearing a Q% quorum needs Q ÷ votable share of every votable token to turn out, and dexe_dao_create refuses above an 80% turnout ceiling — under LINEAR that caps the treasury at 37.5% of supply, and a too-high treasury alone is a HARD error. Treasury 0% means proposals have nothing to spend. Omit this AND quorumPercent for the synthesized 30/51 split.
- `quorumPercent` (optional) — Quorum % required to pass proposals? · default `51` · constraint: 50 ≤ quorum ≤ 0.8 × (100 − treasuryPercent)  (LINEAR power; lower under POLYNOMIAL) · ⚠ Below 50% a small holder group can drain the treasury (blocked-risky without confirmRisky). Above 0.8 × (100 − treasuryPercent) clearing quorum needs >80% turnout of the votable supply and the DAO freezes — the tool refuses and quotes the two numeric ways out.
- `voteModel` (optional) — Vote power model — LINEAR (1 token = 1 vote, recommended) or POLYNOMIAL (meritocratic curve)? · default `LINEAR` · ⚠ POLYNOMIAL caps effective vote power near 56% of supply, so no split supports the ≥50% floor and the tool refuses it. Pick LINEAR unless the user accepts a sub-50% quorum with confirmRisky:true.
- `durationSeconds` (optional) — Voting duration per proposal, in seconds? (86400 = 1 day) · default `86400` · ⚠ Very short durations can end voting before holders react; very long ones stall governance.
- `chainId` (optional) — Which chain — 97 (BSC testnet rehearsal, free) or 56 (BSC mainnet, real BNB)? · default `97`
- `daoDescription` (optional) — One-paragraph DAO description for the public profile? (markdown ok; optional)

**Steps:**
1. `dexe_dao_create` — Preview the resolved config + safety proof (turnout margin, treasury floor). No broadcast. Pass treasuryPercent/quorumPercent ONLY if the user named them — omit both for the governable 30/51 split.
2. `dexe_dao_create` — Broadcast the deploy (same arguments + confirm:true). Signs via hot key or WalletConnect QR.

**Pitfalls (danger first):**
- 🔴 Quorum must be REACHABLE **with margin**: treasury/undistributed tokens cannot vote, so a quorum that only just fits the votable supply is frozen in practice — one holder asleep and nothing passes again, including the fix. dexe_dao_create enforces the margin on all five settings slots — see quorum-turnout-margin.
- 🔴 The tool's own defaults, treasury 30% / quorum 51%, need 72.86% turnout. The ceiling is 80% turnout OF THE VOTABLE POWER: under LINEAR the 50% quorum floor caps the treasury at 37.5% of supply; under POLYNOMIAL vote power follows a curve, not the token share, and no split holds a ≥50% quorum. Over it dexe_dao_create returns mode:"blocked-risky" with maxQuorumPercentForThisDistribution / minVotablePercentForThisQuorum — use either, or omit both fields. confirmRisky:true overrides (DEXE_TREASURY_GUARD=block refuses outright); a DAO cannot repair its own quorum. DEPLOY-TIME only — change_voting_settings is NOT margin-checked.
- 🔴 Quorum below ~50% opens treasury-drain territory: a small token holder group can pass proposals that move the whole treasury. The safe floor is 50% (override via DEXE_MIN_SAFE_QUORUM_PCT); builds that lower quorum below it return mode:"blocked-risky" and need an explicit confirmRisky:true re-run. Warn the user before they choose a low quorum.
- 🔴 Every EXECUTED proposal with rewards configured pays a ~30% DeXe protocol commission on the reward total (voteAmount × voteRewardsCoefficient + fixed rewards) from the DAO treasury at execute time. If the treasury can't cover it, the protocol MINTS new gov tokens (supply inflation — the quorum denominator grows). claimRewards on an empty treasury succeeds but silently pays 0. Keep voteRewardsCoefficient ≤ 1e23 (×0.01) or 0 unless the user explicitly budgets for it.
- ⚠ Token cap rule: cap ≥ mintedTotal > 0. cap:0 reverts 'ERC20Capped: cap is 0' (there is no uncapped mode); cap < mintedTotal reverts; cap == mintedTotal is valid and means fixed supply (no future minting headroom).
- ⚠ A fresh dexe_dao_create deploy auto-expands FIVE proposal-settings ids: 0 default, 1 internal, 2 validators, 3 distribution, 4 tokenSale. Any later rewards/settings change must edit EVERY id whose executor matters — proposals routed through untouched executors keep the old values.
- ⚠ The settings flag `delegatedVotingAllowed` is INVERTED versus its name: false = delegation IS allowed (the default), true = delegated votes are DISABLED for that proposal type. Do not "enable delegation" by setting it to true.
- ⚠ minVotesForVoting and minVotesForCreating must be ≤ the largest single recipient's token allocation, or no holder can ever create/vote. dexe_dao_create's synthesized configs keep this coherent; check it when the user supplies explicit settings.
- ℹ The DAO treasury is the IMPLICIT REMAINDER of the initial distribution: sum(recipient amounts) < mintedTotal, and the contract mints the difference to the DAO itself. Never list the govPool address as a distribution recipient. To give the user's address list X% of supply, put those addresses+amounts in the deploy-time distribution and leave the rest as treasury.
- ℹ The DAO deploy create2 salt is deployer+name: the same deployer reusing a daoName on the same chain reverts 'pool name is already taken'. Pick a fresh name; a different deployer can reuse it.
- ℹ votePower initData is auto-encoded (LINEAR → __LinearPower_init selector 0x892aea1f, POLYNOMIAL → 3 coeffs). Do not override it; empty initData reverts 'power init failed'. Only CUSTOM presets take hand-made initData.
- ℹ Amount strings: digits-only = RAW smallest units (wei); a decimal point ("12.5") = human units scaled by the token's REAL on-chain decimals (never assumed 18). Durations and delays are SECONDS (86400 = 1 day). Composite quorum/percent params are plain percent numbers (51).
- ℹ Chains: 56 = BSC mainnet, 97 = BSC testnet. Rehearse on 97 first (free faucet BNB) except for features that don't exist there (staking, subgraph, off-chain backend). Mainnet gas is cents per tx (~0.1 gwei) — never size budgets from Ethereum L1 intuition.

_For the machine-readable plan (interview questions with risk notes, step templates with `flowContext` chaining), call the `dexe_guide` tool with `flow:"create_dao"`._
<!-- END GENERATED: flow-recipe -->
