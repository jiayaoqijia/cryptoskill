---
name: earnforge
description: >
  Discovers, compares, risk-scores, and builds unsigned deposit and withdrawal
  quotes for DeFi yield vaults across every chain indexed by the LI.FI Earn API.
  Surfaces LI.FI's undocumented verificationStatus signal, which flags roughly
  10% of vaults as suspect. Includes ERC-20 allowance checking, a 0-10 composite
  risk score, yield strategy presets, portfolio allocation, and 25 documented
  API pitfalls handled by default. Use when working with DeFi yield, vault APY,
  lending deposits, or the LI.FI Earn API.
license: Apache-2.0
compatibility: >
  Requires the earnforge CLI (npm i -g @earnforge/cli), Node.js 20+, network
  access, and a LI.FI API key in LIFI_API_KEY.
allowed-tools: Bash(earnforge:*) Read
metadata:
  openclaw:
    primaryEnv: LIFI_API_KEY
    homepage: https://github.com/FarseenSh/earnforge
    emoji: 🌾
    requires:
      env:
        - LIFI_API_KEY
      bins:
        - earnforge
    envVars:
      - name: LIFI_API_KEY
        required: true
        description: >
          LI.FI API key from https://portal.li.fi. Mandatory. The Earn Data API
          returns 401 without it.
---

# EarnForge Agent Skill

## Setup

The Earn Data API requires an API key. Every command fails with a clear error
without one:

```bash
npm i -g @earnforge/cli
export LIFI_API_KEY=...   # https://portal.li.fi
```

## Commands

All commands accept `--json` for machine-readable output.

### Vault Discovery

- `earnforge list [--asset USDC] [--chain 8453] [--min-tvl 1000000] [--strategy conservative] [--json]`
  List vaults with optional filters. Supports pagination.

- `earnforge top --asset USDC [--chain 8453] [--limit 10] [--json]`
  Top vaults sorted by APY descending.

- `earnforge vault <slug> [--json]`
  Fetch a single vault by its slug.

### Comparison & Analysis

- `earnforge risk <slug> [--json]`
  Full risk score breakdown (0-10 scale) across seven dimensions: TVL magnitude,
  APY stability, protocol maturity, redeemability, asset type, LI.FI's
  verification status, and reward dependency. Also returns a `flags` array of
  plain-language concerns: always relay these, not just the number.

- `earnforge apy-history <slug> [--json]`
  30-day APY history from DeFiLlama yields API.

- `earnforge compare <slugA> <slugB> [...] [--json]`
  Side-by-side APY, TVL, risk score and verification status for two or more
  vaults. Prefer this over calling `vault` repeatedly when the user is choosing
  between options: it puts the risk score next to the yield, which is the
  comparison they actually need to make.

### Portfolio & Suggestions

- `earnforge suggest --amount 10000 --asset USDC [--max-chains 3] [--strategy diversified] [--json]`
  Risk-adjusted portfolio allocation. Returns vault list with amounts and percentages.

- `earnforge portfolio <wallet> [--json]`
  Current positions for a wallet address.

### Deposit & Withdraw

- `earnforge quote --vault <slug> --amount 100 --wallet 0x... [--from-chain 1] [--optimize-gas] [--json]`
  Build an unsigned deposit quote. Validates all pitfalls before quoting.
  **Check allowance before executing**. The response includes `approvalAddress`.

- `earnforge withdraw --vault <slug> --amount 100 --wallet 0x... [--to-token 0x...] [--json]`
  Build an unsigned redeem/withdraw quote. Checks `isRedeemable` first.

- `earnforge allowance --token 0x... --owner 0x... --spender 0x... --amount 1000000 --chain 8453 [--rpc <url>] [--json]`
  Check ERC-20 token allowance. Returns whether approval is sufficient and
  builds an unsigned approval tx if not. Use `approvalAddress` from the
  deposit quote as the `--spender`.

- `earnforge approve --token 0x... --spender 0x... --chain 8453 (--amount 1000000 | --unlimited) [--json]`
  Build an unsigned ERC-20 approval transaction.

### Safety & Monitoring

- `earnforge preflight --vault <slug> --wallet 0x... [--amount 100] [--cross-chain] [--json]`
  Run all preflight checks: isTransactional, chain match, gas balance,
  token balance, redeemability.

- `earnforge doctor --vault <slug> [--env] [--json]`
  Run 22 checks on a vault: 18 pitfall guards plus 4 environment checks.

- `earnforge watch --vault <slug> [--apy-drop 20] [--tvl-drop 30] [--json]`
  Monitor a vault for APY/TVL drops. Streams events.

- `earnforge simulate --vault <slug> --amount 100 --wallet 0x... [--from-token 0x...] [--slippage-bps 100] [--allow-revert] [--json]`
  Simulate a deposit against the current chain head using Composer's own
  simulator, which sees allowances, balances and protocol state. Runs preflight
  first. Exits non-zero and returns revert diagnostics if it would fail. Report
  that to the user rather than presenting the transaction as ready.

- `earnforge probe --flag gasless|smart-deposit --from-chain <id> --from-token 0x... --wallet 0x... [--vault <slug>] [--to-chain <id>] [--to-token 0x...] [--json]`
  Check whether one of LI.FI's newer route flags is actually served for a pair.
  `gasless` and Smart Deposits (bridge and deposit into a vault in one route) are
  both accepted by the API and both fail by **exclusion**: an unsupported flag
  drops the route and returns the same 404 as a pair with no liquidity. This runs
  the request with and without the flag and returns `supported`,
  `flag-excluded`, `route-unavailable`, or `rejected`. Use it before telling a
  user a vault is unreachable. Never retry without the flag to "make it work":
  that succeeds while silently dropping what they asked for.

### Reference Data

- `earnforge chains [--json]`: chains with at least one indexed vault
- `earnforge protocols [--json]`: protocols with unversioned ids and URLs
- `earnforge init <name>`: Scaffold a new project with EarnForge wired up

## Rules

1. **Never submit transactions.** Only build unsigned quotes. The user signs.

2. **Check ERC-20 allowance before depositing.** Use `earnforge allowance`
   with the quote's `approvalAddress` as spender. If insufficient, have the
   user sign the approval tx from `earnforge approve` first, then the deposit.

3. **Always check `isTransactional` before quoting deposits.** Use `doctor`
   or `preflight` to verify.

4. **Check `isRedeemable` before quoting withdrawals.** Non-redeemable vaults
   have locked liquidity.

5. **Use `vault.address` as `toToken` for deposits, not the underlying.**
   This is Pitfall #5. The SDK handles it automatically.

6. **Filter stablecoins by the `stablecoin` tag, not by token symbol.**

7. **Risk score thresholds:** >= 8 is low risk, 6-7.9 is medium, < 6 is high
   risk. Always show the score and its flags alongside APY.

8. **Never recommend a verification-flagged vault without saying so.** LI.FI
   flags roughly 10% of vaults: usually `zero_apy`, sometimes `apy_outlier`.
   `earnforge risk` reports it. A flagged vault can never score >= 8, so it can
   never be low risk, and `suggest` excludes them by default.

9. **APY values are already percentages** (3.84 = 3.84%). Do NOT multiply by 100.
   LI.FI's own OpenAPI spec and quickstart say to, and they are wrong; doing so
   overstates every yield 100x. `apy1d/apy7d/apy30d` can be null, and so can
   `apy.base` and `apy.reward`: use the fallback chain.

10. **Never hardcode a protocol slug.** Ids are unversioned (`morpho`, not
    `morpho-v1`) and a stale slug returns HTTP 200 with zero results rather than
    an error, so the failure is silent. Resolve via `earnforge protocols`.

11. **Cross-chain deposits require explicit `--from-token`.** The vault's
    underlying token address is on the vault's chain, not the source chain. And
    cross-chain flows are not atomic: a bridge can succeed while the destination
    deposit fails, so always poll status and handle the failed case.

12. **Use chainId (number), not chain name, in all API paths.**

## References

- [references/pitfalls.md](references/pitfalls.md). All 25 API pitfalls
- [references/protocols.md](references/protocols.md): protocols with risk tiers
- [references/chains.md](references/chains.md): chains with chainIds
- [references/examples.md](references/examples.md): Worked examples
- [references/strategies.md](references/strategies.md): 4 yield strategy presets
