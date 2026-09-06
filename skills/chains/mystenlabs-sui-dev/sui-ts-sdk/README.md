# Sui TypeScript SDK Skill

A Claude skill for idiomatic Sui TypeScript SDK usage — PTB construction, client setup, transaction execution, and on-chain queries. These patterns apply in both backend scripts and frontend apps. Fixes common AI coding mistakes like using deprecated `@mysten/sui.js` imports, the old `TransactionBlock` class, manual BCS when helpers exist, and not checking transaction status.

## What's covered

- Client setup (`SuiGrpcClient` vs legacy `SuiJsonRpcClient` / `SuiClient`)
- Transaction construction (`Transaction` class, commands, inputs)
- Pure value encoding (`tx.pure.u64()`, `tx.pure.address()`, vectors, options)
- Object references and auto-resolution (`tx.object()`, system object shortcuts)
- Built-in commands (`splitCoins`, `mergeCoins`, `transferObjects`, `moveCall`, `makeMoveVec`, `publish`)
- Command result chaining across PTB steps
- Gas coin usage and configuration
- Transaction intents (`coinWithBalance` for automatic coin selection)
- Execution, status checking (`result.$kind === 'FailedTransaction'`), and `waitForTransaction`
- Keypairs, KMS signers, and signing flows
- Offline building with `Inputs.ObjectRef` / `SharedObjectRef`
- Common query patterns (objects, coins, balances, pagination)
- Sponsored transactions
- Anti-patterns to avoid (old class names, deprecated APIs, missing status checks)

## Relationship with sui-frontend skill

The PTB and client patterns in this skill work the same way in frontend apps. The **sui-frontend** skill covers the additional setup needed to get there — dApp Kit, wallet adapters, React hooks (`useSignAndExecuteTransaction`, etc.), and `@mysten/wallet-standard`. Use the frontend skill first or alongside this one when building a UI.

## Usage

Copy or reference `SKILL.md` in your project's `CLAUDE.md`:

```bash
cp SKILL.md ~/my-sui-project/CLAUDE.md
```

Or via the monorepo path — see the [root README](../README.md).

## Evals

The PTB construction benchmark in `evals/evals.json` tests whether the skill produces correct, modern SDK code for a multi-step transaction. See the [root README](../README.md) for how to run it.