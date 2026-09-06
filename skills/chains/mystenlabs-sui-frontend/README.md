# Sui Frontend Skill

A Claude skill for building Sui dApps with the modern dApp Kit SDK (`@mysten/dapp-kit-react` for React, `@mysten/dapp-kit-core` for Vue/vanilla JS/other frameworks) — provider setup, wallet connection, on-chain queries, and transaction signing. Fixes common AI coding mistakes like using the deprecated `@mysten/dapp-kit` providers, the wrong client type, and invalidating queries before waiting for indexing.

## What's covered

- Package installation (`@mysten/dapp-kit-react`, `@mysten/dapp-kit-core`, `@mysten/sui`, `@tanstack/react-query`, `@nanostores/vue`)
- DApp Kit instance setup (`createDAppKit`, `SuiGrpcClient`, network configuration)
- **React**: `DAppKitProvider`, hooks (`useCurrentAccount`, `useCurrentWallet`, `useCurrentClient`, `useCurrentNetwork`, `useDAppKit`, `useWallets`, `useWalletConnection`)
- **Non-React** (Vue, vanilla JS, Svelte): nanostores stores (`$connection`, `$currentNetwork`, `$currentClient`, `$wallets`) and Web Components (`mysten-dapp-kit-connect-button`, `mysten-dapp-kit-connect-modal`)
- On-chain queries using React Query + `useCurrentClient` (with `enabled` guards)
- Paginated queries with `useInfiniteQuery`
- Transaction signing and execution (`dAppKit.signAndExecuteTransaction`) with the discriminated union result pattern
- Signing without executing (`dAppKit.signTransaction`) for sponsored flows
- Personal message signing (`dAppKit.signPersonalMessage`) for auth
- Network switching (`useCurrentNetwork` + `dAppKit.switchNetwork()`)
- Cache invalidation after transactions (wait for indexing before invalidating)
- Wallet-gated UI patterns
- Anti-patterns to avoid (deprecated `@mysten/dapp-kit`, wrong client type, old three-provider pattern, missing `declare module` augmentation, stale queries)

## Relationship with sui-ts-sdk skill

The `Transaction` class and PTB construction patterns from **sui-ts-sdk** work identically in the browser. This skill covers the React/dApp Kit layer on top. Use both skills together when building a frontend — the frontend skill for hooks and providers, the SDK skill for building transactions.

## Usage

Copy or reference `SKILL.md` in your project's `CLAUDE.md`:

```bash
cp SKILL.md ~/my-sui-dapp/CLAUDE.md
```

Or via the monorepo path — see the [root README](../README.md).

## Evals

`evals/evals.json` contains five test cases: four React dApp Kit scenarios (provider setup, portfolio queries, transaction execution with cache invalidation, and sign-in + network switching) plus a non-React `@mysten/dapp-kit-core` eval. See the [root README](../README.md) for how to run them.
