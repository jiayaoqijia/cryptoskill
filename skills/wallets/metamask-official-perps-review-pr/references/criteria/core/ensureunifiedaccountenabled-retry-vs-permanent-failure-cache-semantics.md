# `#ensureUnifiedAccountEnabled` — Retry vs Permanent-Failure Cache Semantics

An attempted unified-account setup that fails either sets the retry flag (`#unifiedAccountSetupNeedsRetry`, transient) or caches `{ attempted: true, enabled: false }` in `TradingReadinessCache` (permanent), never both; the deferred-signing, feature-disabled, and unknown-mode paths intentionally return without touching either.

- **Permanent account-shape condition cached as retryable** — if a condition that can never
  resolve (e.g. the account is already a confirmed multi-sig) sets the retry flag instead
  of caching `{ attempted: true, enabled: false }`, the client re-runs the failing path on
  every Perps tab entry indefinitely. This is the root cause of the recurring Perps-tab
  error: set the retry flag only for transient failures that a subsequent attempt might
  recover from; cache permanent failures as final without setting the retry flag.
- **Retryable flag + permanent condition** — verify that each attempted-setup path through
  `#ensureUnifiedAccountEnabled` that returns without enabling the account either (a) sets
  the retry flag and returns without caching, or (b) caches `{ attempted: true, enabled:
  false }` and does *not* set the retry flag. Both flags active on the same path is a loop.
- **Deferred or skipped path treated as a failure** — the defer-until-action, feature-disabled,
  and unknown-mode returns leave the cache untouched on purpose so the next entry re-evaluates;
  caching them as attempted suppresses the migration when the user later trades.
