---
name: sui-sdks
description: >
  Sui SDK landscape — which SDK to pick (TypeScript, Rust, or community-maintained
  Python/Go/Dart/Kotlin/Swift), how they map to each other, and how to install and
  wire each one up. Use when a user is starting a new Sui project in any language,
  migrating between languages, comparing APIs across SDKs, or asking "what SDK
  should I use for X?". For deep patterns inside a single SDK, route to that
  SDK's reference file.
---

# Sui SDKs

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

Most AI agents give confusing, outdated, or cross-wired answers about Sui SDKs. This skill fixes the three most common failure modes:

1. **Recommending a community SDK as if it were official.** Only two SDKs are maintained by Mysten Labs: TypeScript (`@mysten/sui`) and Rust (`sui-rust-sdk` family of crates). Everything else is community-maintained.
2. **Mixing up TypeScript SDK generations.** The old `@mysten/sui.js` package was renamed to `@mysten/sui` at v1.0. The v2 client API (`client.core.*`, `include` instead of `show*`, `SuiGrpcClient` replacing `SuiClient`) is distinct from v1.
3. **Not using the installed LLM docs.** Every `@mysten/*` package ships `docs/llms-index.md` + topic-specific markdown files to `node_modules`. Agents should read those before answering; they are guaranteed to match the installed version.

All patterns in this skill are derived from:
- https://docs.sui.io/references/sui-sdks (canonical SDK inventory)
- https://sdk.mystenlabs.com/sui (TypeScript SDK reference)
- https://sdk.mystenlabs.com/sui/llm-docs (bundled LLM docs convention)
- https://github.com/MystenLabs/sui-rust-sdk (Rust SDK source)
- https://docs.rs/sui-transaction-builder (Rust PTB builder)

If unsure about any specific API in any SDK, fetch from the relevant doc page — do not extrapolate from a different SDK's surface.

---

## Reference files

### typescript — TypeScript SDK (`@mysten/sui` v2)
**Path:** `typescript.md`
**Load when:** writing, reviewing, or migrating TypeScript/JavaScript code that imports `@mysten/sui`, constructing PTBs in TS, choosing between `SuiGrpcClient` / `SuiGraphQLClient`, using the v2 Core API, or migrating from SDK v1 (`@mysten/sui.js`).
**Covers:** install, imports, client classes and when to use each, v2 Core API, PTB construction, pure/object inputs, balance and coin intents, execution & status checking, `waitForTransaction`, keypairs, offline building, sponsored transactions, v1→v2 migration table, `$extend` pattern for kiosk/suins/deepbook/walrus/seal/zksend.

### rust — Rust SDK (`sui-*` crates)
**Path:** `rust.md`
**Load when:** writing Rust code that interacts with Sui — CLI tools, backend services, validators, indexers. Also when choosing between the new modular crates and the legacy in-monorepo `sui-sdk` crate.
**Covers:** the five crates (`sui-sdk-types`, `sui-crypto`, `sui-rpc`, `sui-graphql`, `sui-transaction-builder`), `TransactionBuilder` API with an end-to-end example, signing via `sui-crypto`, gRPC client from `sui-rpc`, relationship to the legacy `sui-sdk` crate, and the "intents" feature flag (high-level `Coin` / `Balance` intents).

### community — Community SDKs (Python, Go, Dart, Kotlin, Swift, Vue)
**Path:** `community.md`
**Load when:** a user asks about or is using a non-TS-non-Rust SDK. Also when assessing risk for a language choice (maintainer responsiveness, feature gaps vs official SDKs).
**Covers:** for each community SDK — repo, maintainer, install, what's supported/not, caveats, and a recommendation on whether to use it or call the Rust/TS SDK from an FFI wrapper instead.

### mapping — Cross-SDK operation mapping
**Path:** `mapping.md`
**Load when:** porting code from one SDK to another, writing a polyglot reference, or answering "how do I do X in SDK Y".
**Covers:** side-by-side tables mapping the 10-or-so core Sui operations (build PTB, split gas, moveCall, transfer, sign & execute, wait, query object / owned objects / balance, dry-run) across the TS and Rust SDKs, with syntactic parallels.

### llm-docs — Using bundled docs from node_modules
**Path:** `llm-docs.md`
**Load when:** the agent needs authoritative, version-matched TypeScript API docs before writing code. Always check `node_modules/@mysten/*/docs/llms-index.md` first if it exists.
**Covers:** the `docs/llms-index.md` convention, which `@mysten/*` packages ship it, how to read the index and target pages, how to wire it into `AGENTS.md` / `CLAUDE.md` for a project.

## Routing guide

| Task | Load |
|------|------|
| "Which SDK should I use?" | (this file) + mapping |
| Writing TS/JS code against Sui | typescript + llm-docs |
| Writing Rust code against Sui | rust |
| Using pysui / ksui / suikit / sui-go / mofalabs/sui | community |
| User mentions Go / Python / Dart / Kotlin / Swift / Vue (even casually, e.g. "my team uses Go") | community (always — language constraint trumps perf recommendations) |
| Porting between languages | mapping + (target SDK file) |
| Migrating from `@mysten/sui.js` / SDK v1 | typescript |
| Frontend / React integration | route to `frontend-apps` skill first (covers React hooks, wallet connection, query patterns), then typescript here for `Transaction` construction |
| PTB semantics deep dive | route to `ptbs` skill, then language-specific file here |
| Data access patterns (gRPC vs GraphQL vs indexer) | route to `accessing-data` skill |
| Full project setup | **all reference files** (or the SDK-specific one + llm-docs) |
| Code review | **all reference files** |

## Skill Content

### Key concepts

- **Two officially-supported SDKs.** TypeScript (`@mysten/sui`) and Rust (`sui-rust-sdk` crates). Both are maintained by Mysten Labs and updated alongside protocol changes. For performance-critical paths in non-Rust languages, `sui-rust-sdk` can be called via FFI (Foreign Function Interface) from Python, Go, Swift, etc., giving those languages access to the official SDK without relying on community wrappers.
- **Everything else is community.** Python (`pysui`), Go (`block-vision/sui-go-sdk`), Dart (`mofalabs/sui`), Kotlin (`mcxross/ksui`), Swift (`opendive/suikit`), Vue (`SuiFansCN/suiue`). They typically lag protocol updates and feature coverage varies. Treat them as best-effort.
- **The TS SDK has two client generations.** v1 used `SuiClient` + `@mysten/sui.js`. v2 uses `SuiGrpcClient` / `SuiJsonRpcClient` / `SuiGraphQLClient` from `@mysten/sui`. JSON-RPC is deprecated; gRPC is the default for new code.
- **The Rust SDK has two generations.** The new modular crates (`sui-sdk-types`, `sui-crypto`, `sui-rpc`, `sui-transaction-builder`) are the recommended surface. The "legacy Rust SDK" is the monolithic `sui-sdk` crate in the sui monorepo; it uses JSON-RPC (deprecated) and is not the recommended target for new code.
- **Every `@mysten/*` package ships LLM-ready docs.** Look for `node_modules/@mysten/sui/docs/llms-index.md` and follow its pointers before asking the user to clarify APIs. Matches the installed version exactly.
- **Frameworks on top of SDKs.** `@mysten/dapp-kit-react` (React wallet integration; `@mysten/dapp-kit-core` for Vue/vanilla/Svelte/Web Components), `@mysten/kiosk`, `@mysten/suins`, `@mysten/deepbook-v3`, `@mysten/walrus`, `@mysten/seal`, `@mysten/zksend`, `@mysten/enoki` — all are thin layers over `@mysten/sui`. The Mysten extensions integrate via the v2 `client.$extend(...)` pattern; dApp Kit does not (it's a React framework, not a client extension — see `frontend-apps` skill). The bare `@mysten/dapp-kit` package name is the deprecated JSON-RPC-only predecessor.

### Rules

1. **Default to TypeScript or Rust, but respect language constraints.** For any new Sui project, recommend TypeScript (`@mysten/sui`) or Rust (`sui-rust-sdk` crates) — unless the user has named a language (Go, Python, Dart, Kotlin, Swift, Vue) or said "my team uses X". Then `community.md` is the load: name the canonical community SDK (`block-vision/sui-go-sdk` for Go, `pysui` for Python, etc.), flag the staleness risk, and offer FFI-to-Rust as a fallback. **Do not recommend TypeScript or Rust as a replacement language** when the user has stated their team's language. For example, if the user says "my team uses Go", do not suggest rewriting in TypeScript — recommend the Go community SDK and/or Rust via FFI.
2. **For TypeScript, always use `@mysten/sui`, never `@mysten/sui.js`.** The `.js`-suffixed package is frozen at v1 and will not receive updates. Legacy code using it should be migrated.
3. **For TypeScript v2, use `SuiGrpcClient` by default.** `SuiJsonRpcClient` exists for legacy compatibility but JSON-RPC is deprecated; `SuiGraphQLClient` is for specialized relational query flows. See `typescript.md` for the decision.
4. **For Rust, prefer `sui-rust-sdk` crates over the legacy monorepo `sui-sdk`.** Import `sui-transaction-builder`, `sui-sdk-types`, `sui-crypto`, `sui-rpc` individually — pay only for what you use.
5. **Check `node_modules/@mysten/*/docs/llms-index.md` before writing TS code.** If the project has `@mysten/sui` installed, those docs are the authoritative, version-matched source. Read the index, then the targeted page.
6. **Do not mix v1 and v2 TS patterns.** Code that uses `SuiClient`, `TransactionBlock`, `getFullnodeUrl`, `options: { showEffects }`, `signAndExecuteTransactionBlock`, or `result.effects?.status?.status` is v1. Migrate wholesale or keep everything on v1 — a half-migrated file is a bug surface.
7. **Community SDK caveat is mandatory.** When recommending or using a community SDK, mention that it's community-maintained and may lag protocol updates. Check the repo's last commit and latest Sui version support before relying on it.
8. **Frameworks integrate via `$extend()` in v2.** `client.$extend(suins(), deepbook({ address }))` is the v2 pattern. Do not instantiate `SuinsClient` or `DeepBookClient` directly — that's the v1 style.
9. **Route frontend questions to the `frontend-apps` skill.** When the user asks about React hooks, wallet connection, or dApp Kit query patterns, explicitly direct them to the `frontend-apps` skill for hook-level details. This skill covers SDK selection and `Transaction` construction only.
9. **Cite the docs when unsure.** Official TS SDK docs live at `sdk.mystenlabs.com`. The inventory list lives at `docs.sui.io/references/sui-sdks`. Rust SDK docs live on `docs.rs` (per-crate) and `mystenlabs.github.io/sui-rust-sdk/<crate_name>/` (e.g., `/sui_transaction_builder/`).

### Common mistakes

- **Calling a community SDK "the Python SDK" or "the Go SDK" as if official.** There is no official Python or Go SDK. Name the specific package (`pysui`, `block-vision/sui-go-sdk`) and flag it as community.
- **Telling users `SuiClient` is the recommended client.** That was v1. v2 uses `SuiGrpcClient` (or `SuiJsonRpcClient` as a deprecated migration stopgap).
- **Recommending `@mysten/sui.js`.** Deprecated package name. Always `@mysten/sui`.
- **Confusing the two Rust SDKs.** The new `sui-rust-sdk` crates (on `crates.io` as separate crates like `sui-sdk-types` / `sui-transaction-builder` / `sui-rpc`) are distinct from the legacy `sui-sdk` crate in the sui monorepo. New code should use the former.
- **Fetching TS docs from the web when they're installed locally.** If the project has `@mysten/sui` installed, read `node_modules/@mysten/sui/docs/llms-index.md` instead — it matches the installed version.
- **Hardcoding a specific SDK version.** SDK APIs evolve. Prefer "install the latest `@mysten/sui`" and then consult the bundled docs, rather than pinning advice to a version.
- **Recommending `@mysten/dapp-kit` for backend code.** dApp Kit is a React-oriented frontend framework. Backend or CLI code should use `@mysten/sui` directly.
- **Providing React hook details instead of routing to the `frontend-apps` skill.** When a user asks about React hooks, wallet connection patterns, or dApp Kit query patterns, do not answer with hook-level code from this skill. Instead, explicitly tell the user: "For React hook details, see the `frontend-apps` skill." This skill covers SDK selection and `Transaction` construction only — the `frontend-apps` skill has the hook-level guidance.
- **Using JSON-RPC as the default for any client.** JSON-RPC is deprecated; Sui Foundation mainnet full nodes will disable it the week of July 27, 2026. Default to gRPC (or GraphQL for relational queries). `SuiJsonRpcClient` still exists for migration but should not be the default.
