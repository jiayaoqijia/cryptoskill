---
name: pre-deposit-safety-check
description: >
  Use this when the user is about to deposit, supply, or loop and wants a
  pre-deposit safety check. Includes check_loop_venue for collateral/debt
  loops. Cite only identifiers and figures the Philidor tools return.
---

# Pre-deposit safety check

Use this before a deposit into a vault or a collateral/debt loop. Philidor underwrites the venue. It does not compute health factor and it does not prepare transactions. Quote only figures and ids returned in this turn. Never invent a risk number.

The hosted server is `https://mcp.philidor.io/api/mcp`.

## Vault deposit

1. Call `search_vaults` with the asset, chain, and protocol the user named. Set `depositable` to `true` when they need a vault that can still take deposits. `riskTier` is `Prime`, `Core`, or `Edge`. `limit` defaults to 10 and caps at 50. Say so when the list is a sample.
2. Read the deposit line on each row. `closed` means `maxDeposit` is zero. `unknown` means on-chain status was not probed. When `depositable` is true, vaults whose depositability is not yet indexed can still appear. Do not treat `unknown` or an unindexed row as open.
3. For the chosen row, call `get_vault` and `get_vault_risk_breakdown` with the returned `network` and `address` (or `get_vault` by returned `id`).
4. Call `explain_risk_score` with the returned composite score. Read `philidor://methodology` if you explain vectors.
5. Check events on `get_vault`. `list_vaults_with_incidents` is a separate global list of critical incidents in the last 365 days. Absence from that list is not proof of a clean history. Say which call you made.
6. `find_safest_vaults` returns at most 10 audited vaults sorted by score (higher means lower assessed risk). It is a screen, not the full market, and not a safety guarantee.

Report the vault id, network, address, score, tier, TVL, APR labels, and deposit status from those results. Stop if the user asked you to send a transaction.

## Loop (collateral posted, debt borrowed)

1. If the user did not give a market id, call `list_markets` first. Aave V4 is `protocol=aave` and `version=v4` (`aave-v4` is an accepted alias). Vault search uses `protocolVersion`; this tool uses `version`. Chain is an integer id (`1`, `8453`) or a slug (`ethereum`, `solana`).
2. Call `check_loop_venue` with the `marketId` from that list plus the collateral and debt symbols the user named (`weETH`, `USDC`, and so on). Required arguments are `marketId`, `collateral`, and `debt`.
3. Report, from that result only: score, tier, utilization, borrow APR, deposit status, and recent incidents for both legs. Also report whether both reserves exist. Closed or unknown deposits are not executable. Headline APR alone is not a venue choice.
4. Philidor stops there. For wallet health factor, `preview_action`, or `prepare_action`, hand off to the protocol MCP (Aave is `https://mcp.aave.com`). Do not invent those figures here.
5. If the client exposes MCP prompts, `review_loop_venue` takes the same `marketId`, `collateral`, and `debt`.

Spoke ids look like `aave-v4-1-main`. Composed hub ids look like `aave-v4-1-hub-global-dollar`. Pass the id `list_markets` returned. Do not construct an id by hand.
