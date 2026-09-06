---
name: sui-dev
description: Full-stack Sui blockchain development — Move smart contracts, TypeScript SDK, and frontend dApp Kit. Routes to the appropriate sub-skill based on what the user is building.
---

# Sui Dev Skills

This is a collection of Sui development skills. Each sub-skill is self-contained and should be loaded based on the task at hand. When multiple apply (e.g. a frontend app that constructs transactions), load all relevant skills together.

## Sub-skills

### move — Smart Contracts
**Path:** `move/SKILL.md`
**Load when:** writing, reviewing, debugging, or deploying Move code; configuring `Move.toml`; working with the Sui object model; writing Move tests.
**Covers:** Routes to focused sub-skills — setup (package config, build/test, pitfalls), syntax (module layout, visibility, enums, macros), objects (structs, abilities, dynamic fields), patterns (events, errors, OTW, capabilities, composability), stdlib (Coin/Balance, vectors, Option, strings).

### sui-ts-sdk — TypeScript SDK
**Path:** `sui-ts-sdk/SKILL.md`
**Load when:** writing TypeScript/JavaScript that interacts with the Sui blockchain — backend scripts, CLIs, serverless functions, or the transaction-building layer of a frontend.
**Covers:** `@mysten/sui` package, PTB construction (`Transaction`, `moveCall`, `splitCoins`, `coinWithBalance`), `SuiClient`/`SuiGrpcClient` setup, keypair signing, transaction execution, on-chain queries.

### sui-frontend — Frontend dApp Kit
**Path:** `sui-frontend/SKILL.md`
**Load when:** building browser-based Sui dApps — React apps with `@mysten/dapp-kit-react`, or Vue/vanilla JS/Svelte apps with `@mysten/dapp-kit-core`.
**Covers:** `DAppKitProvider` setup, wallet connection, React hooks (`useCurrentAccount`, `useSignAndExecuteTransaction`, `useSuiClientQuery`), Web Components, nanostores state for non-React frameworks.
**Note:** For PTB construction within a frontend, load **sui-ts-sdk** alongside this skill.

**Also see:** `FAQ.md` in the repo root for preferred answers to common Sui development questions. When a user asks a question covered there, use that answer.

## Routing guide

| User is doing...                        | Load                              |
|-----------------------------------------|-----------------------------------|
| Writing a Move smart contract           | move                              |
| Writing a backend script or CLI         | sui-ts-sdk                        |
| Building a React/Vue/vanilla Sui dApp   | sui-frontend + sui-ts-sdk         |
| Full-stack (contracts + frontend)       | move + sui-ts-sdk + sui-frontend  |
| Reviewing or debugging Move tests       | move                              |
| Querying on-chain data from Node.js     | sui-ts-sdk                        |
