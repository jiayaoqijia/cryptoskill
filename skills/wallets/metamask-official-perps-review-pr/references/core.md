# core review rules

<a id="public-controller-contracts-must-be-versioned-and-migration-aware"></a>

## Public Controller Contracts Must Be Versioned and Migration-Aware

A change to controller state shape, method signatures, event names or payloads, or package exports ships with a client migration plan and package-level consumer-style tests.

- [ ] **State shape changes without client migration** — Mobile/Extension selectors and hooks may break.
- [ ] **Method signature changes without compatibility plan** — exported controller methods need backward compatibility or coordinated client changes.
- [ ] **Event name/payload drift** — clients and metrics rely on stable events.
- [ ] **Package export changes without package-level tests** — changing exports must include consumer-style assertions.

<a id="package-release-metadata-must-match-contract-impact"></a>

## Package Release Metadata Must Match Contract Impact

The changelog entry and the semver bump match the contract impact, and a bump PR names the package version and the consumers it was checked against.

- [ ] **Public API/state change without changelog** — clients need migration context.
- [ ] **Breaking change released as minor/patch** — semver must match impact.
- [ ] **Controller package and client integration out of sync** — sync/bump PRs should state package version and consumer compatibility.

<a id="hyperliquid-multi-sig-account-handling-in-hyperliquidprovider"></a>

## HyperLiquid Multi-Sig Account Handling in HyperLiquidProvider

Every user-scoped exchange write in `HyperLiquidProvider` needs both a proactive info probe placed right before the write and a message classifier in its `catch`; HyperLiquid rejects every single-signer write for a multi-sig account, and neither guard alone is sufficient.

- [ ] **Catch-path classifier without proactive probe** — burns a doomed write on every entry
  for a multi-sig account. The error is caught, but the round-trip and any side-effects
  (recording premature state, logging) have already occurred.
- [ ] **Proactive probe without catch-path classifier** — can race the multi-sig conversion
  window and fails open: the probe returns normal, the write fires during the transition,
  and the error is unhandled.
- [ ] **Probe placed too early** — placing the probe immediately after `userAbstraction` (rather
  than immediately before the write) means already-unified multi-sig accounts are probed on
  every call, and the probe result can cause the account to be recorded as `enabled: false`
  before the unified path has had a chance to short-circuit. The correct placement is
  **after** the already-compatible short-circuit, the defer branch, and the unknown-mode
  bail — right before the write that would otherwise fail.

<a id="ensureunifiedaccountenabled-retry-vs-permanent-failure-cache-semantics"></a>

## `#ensureUnifiedAccountEnabled` — Retry vs Permanent-Failure Cache Semantics

An attempted unified-account setup that fails either sets the retry flag (`#unifiedAccountSetupNeedsRetry`, transient) or caches `{ attempted: true, enabled: false }` in `TradingReadinessCache` (permanent), never both; the deferred-signing, feature-disabled, and unknown-mode paths intentionally return without touching either.

- [ ] **Permanent account-shape condition cached as retryable** — if a condition that can never
  resolve (e.g. the account is already a confirmed multi-sig) sets the retry flag instead
  of caching `{ attempted: true, enabled: false }`, the client re-runs the failing path on
  every Perps tab entry indefinitely. This is the root cause of the recurring Perps-tab
  error: set the retry flag only for transient failures that a subsequent attempt might
  recover from; cache permanent failures as final without setting the retry flag.
- [ ] **Retryable flag + permanent condition** — verify that each attempted-setup path through
  `#ensureUnifiedAccountEnabled` that returns without enabling the account either (a) sets
  the retry flag and returns without caching, or (b) caches `{ attempted: true, enabled:
  false }` and does *not* set the retry flag. Both flags active on the same path is a loop.
- [ ] **Deferred or skipped path treated as a failure** — the defer-until-action, feature-disabled,
  and unknown-mode returns leave the cache untouched on purpose so the next entry re-evaluates;
  caching them as attempted suppresses the migration when the user later trades.

<a id="metered-benefits-need-a-strict-improvement"></a>

## Metered Benefits Need a Strict Improvement

A winning fee source and an actual reduction in the charged fee are separate
conditions. Do not spend a metered allowance on a tie. Check the resolver and
every downstream consumption marker against the same economic predicate, with
explicit equality and quantization-boundary cases.

<a id="read-only-account-guards-cover-every-write"></a>

## Read-only Account Guards Cover Every Write

Inventory exchange calls, transfers, cancellation, withdrawals and registered
venue-key paths before claiming an account is read-only. Guard the narrow shared
write boundary before local side effects; preserve setup needed for authenticated
reads. A missing public export is a contract defect even when internal tests pass.

<a id="evidence-expected-before-core-perps-review"></a>

## Evidence Expected Before Core Perps Review

The PR carries a contract impact matrix (state, methods, events, exports, constants), a Mobile/Extension compatibility note or paired PR links, provider abstraction and fallback tests, and grep evidence that no client import or environment global entered the package.
