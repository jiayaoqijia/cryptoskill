# Using bundled LLM docs from `@mysten/*` packages

Source: https://sdk.mystenlabs.com/sui/llm-docs

Every `@mysten/*` npm package ships markdown documentation alongside its compiled code, designed for AI coding agents to read at runtime. These docs live in `node_modules` and match the installed version exactly — no staleness, no hallucination about a newer or older API than what's actually installed.

## The convention

When you install `@mysten/sui`, the package contains:

```
node_modules/@mysten/sui/
├── docs/
│   ├── llms-index.md       # routing index with page descriptions
│   ├── transactions.md     # topic-specific references
│   ├── client.md
│   └── ...
├── dist/                   # compiled code
└── package.json
```

From the official docs: *"When you install an SDK package, you automatically get accurate, up-to-date documentation that coding agents (Claude Code, Cursor, Copilot, and others) can read directly."*

## How to use them

**Step 1: Check for the index.**

Before answering a TypeScript API question, check whether the project has `@mysten/sui` (or other `@mysten/*` packages) installed:

```bash
ls node_modules/@mysten/
cat node_modules/@mysten/sui/docs/llms-index.md
```

**Step 2: Read the index, then the targeted page.**

`llms-index.md` is a routing guide — it tells you which page covers which topic. Read that first, then load only the specific page(s) you need.

**Step 3: Cite the local path if referring to docs.**

When recommending a pattern, mention you verified it against `node_modules/@mysten/sui/docs/<page>.md` so the user knows the answer is version-matched.

## Which packages ship docs

All modern `@mysten/*` packages, including:
- `@mysten/sui` — core SDK
- `@mysten/dapp-kit-react` — React wallet integration (`@mysten/dapp-kit-core` for non-React)
- `@mysten/kiosk`
- `@mysten/suins`
- `@mysten/deepbook-v3`
- `@mysten/walrus`
- `@mysten/seal`
- `@mysten/zksend`
- `@mysten/enoki`

Check each package's `node_modules/@mysten/<name>/docs/` for its `llms-index.md`.

## Wiring it into a project's agent config

The official recommendation is to add a guidance snippet to `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` in the project root:

```markdown
When working with @mysten/* packages, find relevant docs by looking for
`docs/llms-index.md` files inside `node_modules/@mysten/*/`. Read the index
first to find the page you need, then read that page for details.
```

This way, any agent opened in the project will know to consult the bundled docs before answering.

## Why this matters

- **Version accuracy.** SDK APIs evolve. A file on `sdk.mystenlabs.com/sui` shows the latest; the project's `node_modules` shows what's installed. If the user is on `@mysten/sui@2.3`, the web docs may describe `@mysten/sui@2.5` features that don't exist in their install.
- **No round trip.** No need to `WebFetch` — faster, and works offline.
- **Canonical source.** The bundled docs are the docs the SDK authors ship; they won't conflict with the code.

## When to use the web docs instead

- The user isn't in a project with `@mysten/sui` installed (e.g., they're designing a new app and asking general questions).
- The project has an old `@mysten/sui.js` and you need the new v2 API for a migration answer.
- The bundled docs don't cover the specific topic (rare).

## Fallback: the public URL

If bundled docs aren't available, the authoritative web source is:
- https://sdk.mystenlabs.com/sui — v2 API reference
- https://sdk.mystenlabs.com/sui/llms.txt — aggregated LLM-friendly text file
- https://sdk.mystenlabs.com/sui/migrations/sui-2.0/llms.txt — full v1→v2 migration

Prefer the bundled docs when they exist.
