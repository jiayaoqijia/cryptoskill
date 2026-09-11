---
name: dexe-otc
description: |
  Run a DeXe OTC token sale end-to-end — open a multi-tier TokenSaleProposal,
  vote+execute it, then buyers check status / buy / claim. Covers the five
  dexe_otc_* composites plus the PRECISION-1e25 rate, native-BNB sentinel, and
  claim-timing gotchas. Use when the user mentions "OTC", "token sale", "sell DAO
  tokens", "buy from a tier", "claim vested tokens".
---

# dexe-otc

An OTC DAO sells its own token via on-chain `TokenSaleProposal` tiers. Each step
is one MCP call; calldata auto-broadcasts when `DEXE_PRIVATE_KEY` is set.
Validate on **BSC testnet (chain 97)** first. Full recipe + runnable proof:
`docs/OTC.md` and `scripts/lifecycle-otc.mjs`.

## The five composites

| Tool | Role |
|---|---|
| `dexe_otc_dao_open_sale` | multi-tier `createTiers` envelope + IPFS metadata + deposit + `createProposalAndVote`. `buildOnly:true` returns just the envelope. |
| `dexe_otc_list_sales_for_dao` | list a DAO's tiers (prices, `totalSold`, `isOff`, UTC times). |
| `dexe_otc_buyer_status` | render-ready buyer view: prices, claimable, vesting, auto-merkle proof. |
| `dexe_otc_buyer_buy` | preflight balance/allowance + approve + `buy()`; native path uses the sentinel + `value`. |
| `dexe_otc_buyer_claim_all` | claims tiers with `canClaim && !isClaimed`, withdraws vested; `noop` when nothing pending. |

## Owner flow

1. `dexe_dao_predict_addresses` → get `govPool` / `govToken` / `govTokenSale`.
2. Deploy with treasury pre-seeded (mint to the predicted `govPool` via
   `tokenParams.users[]`) — see [[dexe-create-dao]].
3. `dexe_otc_dao_open_sale` with tiers (schema below).
4. Poll `dexe_proposal_state` until `SucceededFor` (index 4; it briefly sits in
   `Locked`=6), then `dexe_vote_build_execute` → broadcast.

## Buyer flow

`dexe_otc_buyer_status` → `dexe_otc_buyer_buy` → (after the sale window closes)
`dexe_otc_buyer_claim_all`.

## Critical gotchas

- **Buyer amounts accept human units** — a decimal string (`"50.0"`) is scaled
  by the token's real on-chain decimals; digits-only stays raw wei.
  `dexe_otc_buyer_buy` converts the 18-dec-normalized buy amount to the
  **payment token's native decimals** for the balance check and the exact
  approve — no silent under-pay on <18-dec payment tokens.
- **Exchange rate is PRECISION 1e25**, not 1e18. 1:1 = `"10000000000000000000000000"`.
- **Native BNB = `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`** (ETHEREUM_ADDRESS),
  never `0x0…0` — a zero-address purchase token makes the tier unbuyable. Buy
  tools accept `0x0` as an alias but emit the sentinel.
- **`canClaim` needs `block.timestamp ≥ saleEndTime + claimLockDuration`** — buyers
  wait for the window to close even when `claimLockDuration:0`.
- **`maxAllocationPerUser == 0` means unlimited**, not zero — set a real cap.
- **Treasury must hold the sale token before the sale opens** — pre-seed at deploy.
- **`vestingPercentage` is a human percent 0–100** (auto-scaled by 1e25).
- **Merkle tiers** need the whitelist JSON on IPFS; `open_sale` auto-uploads when
  `uri` is empty (needs `DEXE_PINATA_JWT`). Roots via `dexe_merkle_build`.

## Tier schema (abridged)

```jsonc
{
  "name": "Public Tier 1", "description": "",
  "totalTokenProvided": "<wei>",
  "saleStartTime": "<unix sec>", "saleEndTime": "<unix sec>", "claimLockDuration": "0",
  "saleTokenAddress": "0x…",
  "purchaseTokenAddresses": ["0xEeee…EEeE"],   // native, or ERC20 addresses
  "exchangeRates": ["10000000000000000000000000"],
  "minAllocationPerUser": "0", "maxAllocationPerUser": "<wei, non-zero>",
  "vestingSettings": { "vestingPercentage": "0", "vestingDuration": "0", "cliffPeriod": "0", "unlockStep": "0" },
  "participation": []   // AND-list; empty = open tier
}
```

Do not modify OTC tool behavior lightly — the v0.11.x OTC surface is validated
E2E on mainnet. See `docs/OTC.md` for the exhaustive reference.

## Canonical recipe (generated from src/knowledge/ — edit there, then `npm run gen:knowledge`)

<!-- BEGIN GENERATED: flow-recipe -->
### Open an OTC / token sale (`otc_sale`)

Open a multi-tier token sale (proposal → vote → execute → live), then buyers check status / buy / claim via the dexe_otc_* composites.

**Ask the user:**
- `govPool` — Which DAO (govPool address)?
- `saleTokenAmount` — How many DAO tokens to sell in this tier? · ⚠ This amount moves from the treasury into the sale at execute.
- `price` — Price per DAO token, and in which purchase token (address, or native BNB)? · ⚠ Rates are stored ×1e25 on-chain — always pass human units and let the composite scale; a mis-scaled hand-made rate can sell the allocation for pennies.
- `saleWindow` — Sale start and end times? (ask in the user's words — e.g. 'starts tomorrow, runs 7 days' — then compute Unix seconds from the CURRENT time; never guess the date) · ⚠ The window must be in the future at EXECUTE time (add voting-period headroom). A past window creates a dead tier — every buy reverts.
- `vesting` (optional) — Vesting? (RECOMMEND 0 on newly deployed DAOs — vested funds are currently unrecoverable there) · default `0` · ⚠ vestingWithdraw is blocked by SphereX on fresh pools — a non-zero vestingPercentage strands the vested portion (confirmed protocol bug).
- `whitelist` (optional) — Open to everyone, or a whitelist of addresses?

**Steps:**
1. `dexe_otc_dao_open_sale` — Build + create the TokenSaleProposal tiers proposal (auto-uploads merkle whitelist JSON if given).
2. `dexe_proposal_vote_and_execute` — Vote + execute the sale proposal — the tier goes live at execute.
3. `dexe_otc_list_sales_for_dao` — Confirm the tier is live and show its parameters (times are UTC).

**Pitfalls (danger first):**
- 🔴 TokenSaleProposal.vestingWithdraw is blocked ('SphereX error: disallowed tx pattern') in EVERY call shape on fresh pools — the VESTED portion of a purchase CANNOT be withdrawn (confirmed protocol bug, escalated upstream). Until fixed: open tiers with vestingPercentage:"0" on new DAOs. claim (the instant portion) works fine.
- 🔴 NEVER guess dates for sale/staking windows — compute Unix timestamps from the CURRENT time (ask the user or read the latest block; your idea of 'now' may be a stale year). Windows must be in the future AT EXECUTE TIME (add headroom for the voting period). A staking tier with a past deadline is SILENTLY rejected on-chain (the execute succeeds, a StakingRejected event fires, NO tier exists, the reward bounces back); a sale tier with a past window is created dead-on-arrival (every buy reverts 'TSP: token sale is over'). The builders refuse past end-times before any transaction.
- ⚠ Native BNB in sale tiers uses the sentinel address 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE, NOT the zero address (0x0 reverts 'TSP: incorrect token'). A native-currency buy must send msg.value equal to the buy amount. The dexe_otc_* composites canonicalize this.
- ⚠ Tier exchange rates are scaled ×1e25 (PRECISION) on-chain. Pass human units to the dexe_otc_* composites and they scale for you; only ADVANCED raw structs need pre-scaled values. A hand-scaled rate off by 10^2 sells the whole allocation for pennies.
- ℹ Whitelisted tiers use a merkle root; the tier's uri must point to IPFS JSON {"list":[lowercased addresses]} so buyers can regenerate proofs — dexe_otc_dao_open_sale auto-uploads it when uri is empty (needs DEXE_PINATA_JWT). Buyer-side reads need the proof BEFORE getUserViews or canParticipate reads false.
- ℹ Amount strings: digits-only = RAW smallest units (wei); a decimal point ("12.5") = human units scaled by the token's REAL on-chain decimals (never assumed 18). Durations and delays are SECONDS (86400 = 1 day). Composite quorum/percent params are plain percent numbers (51).

_For the machine-readable plan (interview questions with risk notes, step templates with `flowContext` chaining), call the `dexe_guide` tool with `flow:"otc_sale"`._
<!-- END GENERATED: flow-recipe -->
