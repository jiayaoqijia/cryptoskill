# Data Flow & State

- **Old context remains actionable**: On account, provider or network change, clear or re-key committed display/action state immediately. A generation guard against late writes does not invalidate data already shown. Test with the next request held open.
- **Unknown balance treated as usable balance**: Keep unresolved distinct from zero; never substitute a balance from another account. Verify the committing CTA remains disabled until the selected account/token inputs are valid.
- **Late defaults overwrite a user choice**: Typing, percent and MAX controls must all mark a value as user-edited. Hold metadata resolution until after each interaction and confirm the chosen value remains. Apply authoritative limit changes explicitly; a delayed persistence acknowledgment is not a new limit.

Controller → Redux → Hooks → Components. Standalone mode for lightweight queries without full init.

- **Direct controller call from component** — components calling `PerpsController.method()` directly instead of going through hooks (`usePerpsTrading`, `usePerpsAccount`, etc.).
- **Missing `accountState` check** — accessing positions/orders/balances without verifying accountState is loaded. Causes undefined errors on first load or account switch.
- **Derived flag promoted to structural state without its own lifecycle** — define initialization, every set condition, and every clear condition independently of the old string or transient value that first produced the flag. Test both set and clear paths.
- **Unknown async value treated as an absent blocker** — an alert may correctly stay hidden while balance or market data is unresolved, but the CTA must remain disabled through a separate unresolved-state check. Missing alert copy is not permission to submit.
- **Async flow loses ownership of cleanup** — fire-and-forget timers and navigation listeners need a generation guard plus `dispose()` on retry, unmount, and failure. Treat nested confirmation routes as part of the same flow so cleanup does not fire while the user is still inside it.
- **One in-flight mutation lock replaces earlier accepted outcomes** — serialize active requests separately from post-success reconciliation. Keep each accepted result keyed by provider and stable entity ID until an authoritative read or stream confirms it; clear the set when account, provider, network, or connection generation changes. Test sequential successes followed by a partial terminal update.
- **Stale position after close** — position in UI after close because local state not cleared or WS update not processed. Must refresh via `PerpsCacheInvalidator`.
- **Preload data not seeded** — new hook not using `getPreloadedData()` lazy initializer. First render shows skeleton instead of cached data from the 5-minute preload cycle.
- **Order state race** — submitting order and immediately reading order state. WS confirmation hasn't arrived. Use transaction receipt or poll with backoff.
- **Leverage/validation bypass** — allowing values outside market's `maxLeverage` or skipping pre-trade checks (balance, market open, position limit).
