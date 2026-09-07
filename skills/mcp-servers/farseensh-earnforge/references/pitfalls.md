# LI.FI Earn API Pitfalls

25 pitfalls, all verified against the live API on Sep 7, 2026 across 744 vaults.
The SDK handles every one by default.

**Two have inverted since they were first written** and one is obsolete. The API
changed underneath them. Six exist because LI.FI's documentation contradicts
LI.FI's API.

| # | Pitfall | Impact | Handled by |
|---|---------|--------|-----------|
| 1 | Earn Data lives at `earn.li.fi`, Composer at `li.quest` | 404 on every endpoint | Two typed clients with correct defaults |
| 2 | **Earn Data API requires auth** (inverted Apr 2026) | 401 on every call | `x-lifi-api-key` header; `MissingApiKeyError` at construction |
| 3 | Key goes in the `x-lifi-api-key` header, not a query param | 401 with a valid key | Header set by the client |
| 4 | Composer quote is GET, not POST | 405 | Hard-coded `GET /v1/quote` |
| 5 | `toToken` must be the vault address, not the underlying | Wrong asset or failure | `buildDepositQuote()` wires `vault.address` |
| 6 | Pagination is cursor-based, and the cursor is **absent** on the last page | Missing vaults, or an infinite loop | Async iterator treating null and undefined alike |
| 7 | `apy1d` / `apy7d` / `apy30d` can be null | `NaN` in comparisons | Nullable types + `getBestApy()` fallback chain |
| 8 | **`tvl.usd` is a number** (was a string; spec still says string) | Type error or `NaN` | `TvlSchema` accepts both; `parseTvl()` normalises |
| 9 | Amounts need per-token decimals | 10^n too much or too little | `toSmallestUnit()` / `fromSmallestUnit()` |
| 10 | Quotes go stale | Reverted transaction | Quotes are never cached |
| 11 | No gas token on the target chain | Transaction fails | `preflight()` balance check |
| 12 | Wallet on the wrong chain | Transaction fails | `preflight()` chain comparison |
| 13 | Vault is not transactional | Quote fails | `isTransactional` guard |
| 14 | Rate limit is 100 req/min | 429 | Token bucket with async backpressure |
| 15 | Empty `underlyingTokens`: **obsolete**, 0 of 744 vaults | Crash on `[0]` | Guard retained against a synthesised case |
| 16 | `description` is optional (~23% of vaults have it) | undefined access | `.optional()` |
| 17 | **`apy.reward` is three-valued**: null, 0, or positive | Lost signal if collapsed | null preserved; `getRewardApy()` coerces on request |
| 18 | `apy.base` can also be null | Type error | Nullable |
| 19 | **Stale protocol slugs return 200 with zero results** | Silent empty result set | Unversioned ids; existence checked against the live list |
| 20 | **Unknown query params are silently dropped** | Filter fails open: returns everything | Correct param names pinned by test |
| 21 | **`verificationStatus` is undocumented** but flags ~10% of vaults | Recommending a suspect vault | First-class risk dimension; excluded from `suggest` |
| 22 | **The docs contradict the API** in six places | 100x APY error if you follow the spec | Schemas generated from live responses |
| 23 | **Slug format changed** to `protocol:chainId:_:address` | Mis-parsed slugs and cursors | `parseVaultSlug()` accepts both forms |
| 24 | **`underlyingTokens` entries can be partial**: address only, no `symbol`/`decimals` | One vault aborts the whole fleet walk | Both fields optional on the token schema |
| 25 | **New route flags fail by exclusion, not error** (`gasless`, Smart Deposits) | An unserved flag looks identical to a dead pair | `earnforge probe` runs the request both ways |

## The ones that will bite hardest

**APY is a percentage.** `4.63` means 4.63%. LI.FI's OpenAPI spec says these are
decimals and the quickstart multiplies by 100: following the official example
overstates every yield **100×**. A 29% vault renders as 2919%.

**A stale protocol slug fails silently.** `?protocol=morpho-v1` returns HTTP 200
with `total: 0`. There is no error to catch, so it looks identical to a protocol
that genuinely has no vaults. Never hardcode a slug: resolve via
`earnforge protocols`.

**An unknown query param is dropped, not rejected.** Sending `minTvl` instead of
`minTvlUsd` returned all 744 vaults instead of 48: a "$100M+ TVL" filter that
silently returns sub-$20k dust.

**`verificationStatus` is documented nowhere** and flagged 71 of 744 vaults on
7 Sep 2026, all for `zero_apy` (the `apy_outlier` reason has appeared and gone
before, so do not assume the set is fixed). Sort by APY without checking it and a
flagged vault lands at the top of the list.

## A flag that is not served looks exactly like a dead route

LI.FI added `gasless` and Smart Deposits (`destinationActionKind` +
`destinationActionVault`, which bridge and then deposit into an ERC-4626 vault in
one route) in Aug/Sep 2026. Both are accepted by the API. Neither errors when it
cannot be honoured: the route is dropped instead.

    GET  /v1/quote            -> 404 "No available quotes for the requested transfer"
    POST /v1/advanced/routes  -> 200 with routes: []

Identical to a pair with no liquidity. **Do not tell the user a vault is
unreachable on the strength of that 404**, and do not quietly retry without the
flag: that succeeds while abandoning what they asked for. Run
`earnforge probe --flag gasless|smart-deposit` instead, which sends the request
both ways and returns `supported`, `flag-excluded`, `route-unavailable`, or
`rejected`. A `flag-excluded` verdict means *not yet*, not *broken*: on
7 Sep 2026 both flags served zero routes everywhere tested.

## Cross-chain is not atomic

Per LI.FI's own limitations page: a bridge can succeed while the destination
deposit fails, leaving the user holding tokens on the destination chain rather
than a vault position. Always poll status and handle the failed case. Simulation
cannot prevent every revert either: state can change between simulate and
execute, including a vault filling up.

Full detail with a regression test for each: `PITFALLS.md` in the repository root.
