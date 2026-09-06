# Frontend limitations — what dApps can't or shouldn't do

The browser is a hostile environment for some things that look tempting. This page is the "are you sure?" list.

## Things the browser should never hold

- **Private keys.** dApps sign via wallets. Never ask a user to paste a mnemonic or keypair into a form field. If your flow seems to require this, you're designing a wallet, not a dApp.
- **API secrets that authorize signing.** RPC keys for paid endpoints are okay (they're rate-limited). Signing keys, sponsor keys, validator keys, admin keys — all backend-only.
- **Gas station coins.** A gas station service sits server-side. The browser asks it for sponsored signatures via an authenticated endpoint.
- **Indexer database credentials.** Queries go through a backend or a public GraphQL / gRPC endpoint.

## Things that need a backend

Any of these require a server component — a dApp alone cannot do them safely:

- **Sponsored transaction gas selection** (the sponsor signs on a backend; the frontend only signs the user side with `signTransaction`).
- **Rate-limited writes** (preventing one user from spamming a mint).
- **Server-signed allowlists / merkle proofs** (generated server-side, verified on-chain).
- **Signed-message nonces** for authentication (nonces issued + invalidated server-side; never client-issued).
- **Webhooks / polling from external sources** (e.g., cross-chain bridges) that trigger on-chain actions.
- **Operating a custom indexer** or querying an internal DB.

If a user asks for a pure-frontend version of any of these, explain the constraint: a malicious browser client can lie about allowlist membership, replay nonces, or spam an endpoint.

## Things the current dApp Kit does not support

The new v2 dApp Kit is built around `SuiGrpcClient`. Some older JSON-RPC-only features don't have gRPC equivalents yet — or the mapping is still shifting. If a user asks for something specific and you can't find it in the v2 docs:

- Check whether it's a JSON-RPC-only method and the user wants to stay on gRPC → may need to fall back to `SuiJsonRpcClient` alongside the dApp Kit client (deprecated, but still available as a migration surface).
- Check the `@mysten/dapp-kit-core` changelog for breaking changes.
- If genuinely missing, document the gap to the user rather than fabricating an API.

## Non-recommended patterns

### Auto-connect without UX for reconnecting state

`autoConnect: true` (default) restores the last wallet on page load. During that restore, `useWalletConnection().status === 'reconnecting'`. If your app shows `ConnectButton` whenever `account === null`, the user sees a connect button flash on every reload.

Fix: branch on `status`, not just on `account`:

```tsx
const { status } = useWalletConnection();
if (status === 'reconnecting') return <Spinner />;
if (status === 'disconnected') return <ConnectButton />;
```

### Calling `tx.build()` in app code before `signAndExecuteTransaction`

The wallet needs the raw `Transaction` so it can select gas coins and set budget. Pre-building locks those in and often breaks sponsored flows. Always pass the `Transaction` instance.

Exception: sponsored flows that use `tx.build({ client, onlyTransactionKind: true })` and hand kind-only bytes to a backend sponsor service.

### Hardcoding `setGasBudget`, `setGasPrice`, `setGasPayment` in app code

The wallet computes these better than you can — gas price is network-variable, gas budget is dry-run-derived. Only set them for backend-signed flows.

### Using `tx.gas` in `splitCoins` in a sponsored transaction

Sponsors typically reject PTBs that consume the gas coin for non-gas purposes, because the sponsor's gas coin shouldn't be spent on app logic. Use `tx.coin({ balance, useGasCoin: false })` instead (see `sui-sdks` / `typescript.md`).

### Instantiating `SuiGrpcClient` inside components

```tsx
// ❌ Wrong — loses network switching
function Foo() {
  const client = new SuiGrpcClient({ network: 'mainnet', baseUrl: '...' });
}

// ✅ Right
function Foo() {
  const client = useCurrentClient();
}
```

### Using wallet-standard APIs directly

```tsx
// ❌ Don't
const wallets = window.navigator.wallets;

// ✅ Do
const wallets = useWallets();
```

dApp Kit handles the wallet-standard event loop — reaching past it causes race conditions.

### Querying immediately after execution

Always `waitForTransaction` before the follow-up read / invalidate. Common omission.

### Ignoring `FailedTransaction`

A transaction that validators accepted can still fail at the Move layer (assertion, insufficient budget). `result.$kind === 'FailedTransaction'` is the failure signal. Don't treat a returned digest as proof of success.

### Building infinite queries without `enabled: !!account`

The query fires with `undefined` owner and errors. Always gate queries that require a connected wallet.

### Invalidating with loose query keys

`invalidateQueries({ queryKey: ['balance'] })` invalidates every balance-related query across every account the user has connected. Usually you want `['balance', account.address]`. Be specific.

## SSR / Next.js

- Wallet detection is browser-only. Any component that calls a dApp Kit hook or imports `@mysten/dapp-kit-react`/`-core` must be client-rendered.
- In app-router Next.js: put providers in a `'use client'` file, wallet-aware leaf components in `'use client'` files.
- Don't pre-render wallet UI on the server — it'll hydrate into a mismatch.
- If you need server-side on-chain reads (e.g., for SEO), use a separate `SuiGrpcClient` on the server directly, not via dApp Kit. The server has no wallet concept.

## Mobile webviews and in-app browsers

- Many in-app browsers (Twitter, Discord, etc.) don't support wallet extensions. Detect and show a "Open in your browser" message.
- Mobile wallets typically implement WalletConnect or deeplink flows. The wallet standard handles this via wallet adapters — no special handling in dApp Kit.

## Caveat when adopting new SDK versions

Both `@mysten/sui` and `@mysten/dapp-kit-*` evolve independently but must be compatible. Check the installed versions match the examples in their own `docs/llms-index.md` (see `sui-sdks` skill, `llm-docs.md`) before pulling patterns from web tutorials. Web tutorials go stale within months.
