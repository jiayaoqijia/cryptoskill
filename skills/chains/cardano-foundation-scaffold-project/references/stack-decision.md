# Stack Decision Aid

Short flowchart for picking one of the four v1 stacks. For a broader tour of the ecosystem, hand off to `suggest-tooling`.

## The four v1 stacks

| # | On-chain | Off-chain | Primary language |
|---|---|---|---|
| 1 | Aiken | Evolution SDK | TypeScript |
| 2 | Aiken | Mesh SDK | TypeScript |
| 3 | Aiken | PyCardano | Python |
| 4 | Aiken | cardano-client-lib | Java / Kotlin |

On-chain is fixed at Aiken across all four. Aiken has the strongest tooling for new projects: fast compiler, native CIP-57 `plutus.json` emitter, built-in test framework, and the largest stdlib coverage of any current option. The decision is entirely about the off-chain language.

## Three questions, in order

### 1. What language is your team strongest in?

This is the dominant factor. Off-chain code is where most of the application logic lives; pick the language your team already writes well.

- **TypeScript / JavaScript** → stack 1 or 2
- **Python** → stack 3
- **Java / Kotlin / Scala / JVM** → stack 4

If the team is multi-language, pick the language the off-chain service will be deployed in, not the language the team explores on weekends.

### 2. Do you need browser wallet integration?

Browser wallet integration (CIP-30) only works from a browser. That means TypeScript on the off-chain side — there is no in-browser PyCardano or in-browser cardano-client-lib.

- **Yes, browser dApp with wallet connect** → stack 1 or 2
- **No, backend service or CLI tool** → any stack works; pick by language

A common shape: backend in Python or Java, plus a small TypeScript frontend that handles wallet connect and builds user-facing transactions directly against Blockfrost. The backend is its own concern. The scaffold supports this split — see the frontend section of the layout references and hand off to `connect-wallet` for the CIP-30 details.

### 3. Stack 1 vs Stack 2 (only if TypeScript)

If the answer to question 1 is TypeScript, you still need to pick between Evolution SDK and Mesh SDK. Factual differences:

- **Evolution SDK** — pure JavaScript runtime (no WASM dependency at the build step); composable transaction builder; ships TypeScript types throughout. Wraps the Effect library internally — the public API hides most of it, but Effect types may surface in advanced usage. See https://effect.website/ if you want to go deeper.
- **Mesh SDK** — broader tutorial coverage and the largest TypeScript-side community; ships React components for wallet connect out of the box; high-level transaction builder; relies on a WASM core (`@meshsdk/core-csl`) for serialization.

Both stacks consume the same `plutus.json`, so switching later is moderate-cost — your validator and datum design carry across; the off-chain code is rewritten. There is no editorial preference here; both are actively maintained and production-used.

## Enterprise / JVM constraints

If the organisation mandates JVM for backend services (common in fintech, government, or established enterprises), stack 4 is the only option. cardano-client-lib is mature, has Spring Boot integration, and fits naturally into existing JVM CI/CD. Trade-off: smaller community than the TypeScript options, fewer end-to-end tutorials. Start from `../../skills/build-transaction/references/cclib-quicktx.md` for the QuickTx API, and read a complete worked program under `../../docs/sources/cardano-use-case-templates/<use-case>/offchain/ccl-java/`. The mirrored upstream docs at `../../docs/sources/cardano-client-lib/` are the API reference.

## Python data and scripting

Stack 3 (PyCardano) is the natural fit when:

- The team writes data pipelines, analytics, or ML services in Python
- The dApp's off-chain logic is a backend service, not a browser app
- You want to integrate with existing Python infrastructure (FastAPI, Celery, Airflow)

PyCardano is lighter-weight than the TypeScript SDKs but covers the full transaction-building surface for Plutus V3. Bundled docs at `../../docs/sources/pycardano/`.

## Deferred stacks: why they are not v1 defaults

These languages and SDKs exist and are used in production by specific teams. They are not in the v1 default set for one of three reasons: changing fast (still maturing), niche (small audience), or experimental (production use limited). A future version of this skill may add them as their tooling stabilises.

- **Scalus** — Scala 3 on-chain and off-chain. Powerful for Scala teams but still evolving; small developer base. Use directly if your team is already deep in Scala.
- **OpShin** — Python that compiles to UPLC. Works, but tooling and ecosystem are smaller than Aiken's. Pick if a Python-on-chain story is a hard requirement.
- **Plutarch** — typed Haskell eDSL for highly optimised UPLC. Best raw performance, but steepest learning curve and a Haskell-only team requirement.
- **Pebble** — Harmonic Labs' TypeScript-family on-chain language (successor of Plu-ts; same repo, renamed). Interesting for keeping one language across the stack, but smaller community than Aiken + Evolution/Mesh.
- **Plutus (original Haskell)** — the historical on-chain language. Functional and production-proven, but Aiken has surpassed it in developer experience for new projects. Pick Plutus only if maintaining an existing Plutus codebase.
- **Helios** — DSL with browser-side compilation. Niche; smaller ecosystem than Aiken.
- **Marlowe** — domain-specific language for financial contracts. Use only if you are building a structured financial contract that fits Marlowe's model.
- **Blaze** — TypeScript transaction builder. Lightweight alternative to Mesh and Evolution; smaller community. Sometimes paired with storage-style use cases where many small UTxOs need indexing.
- **Atlas** — Haskell PAB. Mature within the Haskell ecosystem; outside scope for a multi-language v1.

If a developer insists on a deferred stack, hand off to `suggest-tooling` for a deeper conversation rather than improvising a layout here. This skill's scope is the four confirmed-active v1 stacks.

## Decision summary

```
Is the team's primary language TypeScript?
  Yes -> Stack 1 (Aiken + Evolution SDK) or Stack 2 (Aiken + Mesh SDK)
         — both consume the same plutus.json; pick on team preference.
  No  -> Is it Python?
           Yes -> Stack 3 (Aiken + PyCardano)
           No  -> Is it JVM (Java/Kotlin)?
                    Yes -> Stack 4 (Aiken + cardano-client-lib)
                    No  -> Hand off to suggest-tooling for a non-v1 stack.
```
