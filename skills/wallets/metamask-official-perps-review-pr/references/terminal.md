# va-mmcx-terminal review rules

<a id="provider-agnostic-perps-code"></a>

## Provider-Agnostic Perps Code

Hyperliquid-specific logic stays behind the `@metamask/perps-controller` provider interface, never in UI or feature code. Provider IDs, capabilities and limits are data, so another provider can use the same flows.

<a id="mobile-parity"></a>

## Mobile Parity

Before implementation, MetaMask Mobile's matching flow, validation, copy and controller use are checked and matched unless the ticket explicitly requires a difference, which the PR explains.

- [ ] **Unexplained Mobile divergence** — a flow, validation or copy that differs from the matching Mobile implementation without a stated reason. Cite the Mobile counterpart you read.
- [ ] **Formatting divergence** — formatting and display precision are never an explained divergence, even when the PR states it; apply the shared *Shared Formatting & Display Precision* check.

<a id="reuse-and-types"></a>

## Reuse and Types

Controller and shared utilities, and Mobile's controller selectors, actions and state shape, are reused with no parallel state or copied logic. Types are narrowed or validated, never silenced.

- [ ] **Parallel controller state** — a Terminal store or cache with its own writes, invalidation or fallback authority (REST snapshots, connection-flag source selection) for controller-owned state. A read-only view cache fed solely by a controller subscription is allowed.
- [ ] **Force casts** — `as unknown as T`, `as any` or non-null `!` used to silence a type.

<a id="legacy-local-formatters"></a>

## Legacy Local Formatters

Terminal's `formatFee`, `formatPercentage`, `formatSize`, `formatTablePrice` and `formatUsd` (`src/features/perpetuals/utils/`) are legacy copies: a PR that uses, extends or calls one migrates that call site. They copy the controller's perps formatters; the shared *Shared Formatting & Display Precision* check applies.

<a id="forced-testnet"></a>

## Forced Testnet

`config.hyperliquid.forceTestnet` (`src/features/perpetuals/config/hyperliquid.config.ts`) is authoritative: code that reads network state respects it (for example `client-factory.ts`, `account-balances.ts`).

- [ ] **Mainnet fallback** — a default, catch or missing-config branch that resolves to mainnet. Never add one.
