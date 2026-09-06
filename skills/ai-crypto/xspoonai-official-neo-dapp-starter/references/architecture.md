# Architecture & Overview

## Project Overview

| Property         | Value                                                |
| ---------------- | ---------------------------------------------------- |
| **Template**     | Production-ready Neo N3 dApp starter                 |
| **Framework**    | Next.js 15.1.9 (App Router)                          |
| **Language**     | TypeScript 5.7 (strict mode)                         |
| **UI**           | React 19 + Tailwind CSS 3.4 + shadcn/ui              |
| **State**        | Jotai 2.11 (atomic) + Zod 3.24 (validation)          |
| **Data**         | TanStack React Query 5.64                            |
| **Neo SDK**      | @cityofzion/neon-core 5.7 + @neongd/neo-dapi 2.0     |
| **Wallets**      | NeoLine, OneGate (extensible via abstract Connector) |
| **Networks**     | Neo N3 Mainnet, Neo N3 Testnet                       |
| **Deployment**   | Cloudflare Pages, Vercel                             |
| **Testing**      | Vitest 3.0 + Storybook 8.5                           |
| **Code Quality** | ESLint 9 + Prettier 3.4 + Husky 9                    |

## Tech Stack

| Technology                | Role                       | Why Chosen                                |
| ------------------------- | -------------------------- | ----------------------------------------- |
| **Next.js 15**            | Full-stack React framework | App Router, RSC, Edge Runtime, API Routes |
| **React 19**              | UI library                 | Latest features, concurrent rendering     |
| **TypeScript 5.7**        | Type safety                | Strict typing, better DX                  |
| **Tailwind CSS 3.4**      | Utility-first CSS          | Rapid styling, JIT compilation            |
| **shadcn/ui**             | Component library          | Accessible, customizable, copy-paste      |
| **Jotai 2.11**            | Atomic state management    | Fine-grained, no boilerplate, SSR-safe    |
| **React Query 5**         | Server state management    | Caching, refetching, mutations            |
| **Zod 3.24**              | Schema validation          | Runtime type checking, atom validation    |
| **@cityofzion/neon-core** | Neo N3 core library        | Address validation, script building       |
| **@neongd/neo-dapi**      | Neo dAPI standard          | Wallet communication protocol             |
| **@neongd/json-rpc**      | JSON-RPC client            | RPC node communication                    |
| **BigNumber.js**          | Precision arithmetic       | Token amount calculations                 |
| **ky**                    | HTTP client                | Lightweight, retry logic                  |
| **catchee**               | Error decoration           | @Catch decorator for connectors           |
| **EventEmitter3**         | Event system               | Wallet state change events                |
| **next-themes**           | Theme switching            | Dark/light mode                           |
| **Storybook 8.5**         | Component development      | Isolated UI development                   |
| **Vitest 3.0**            | Unit testing               | Fast, Vite-native                         |
| **Cloudflare Pages**      | Edge deployment            | Global CDN, Workers                       |
| **Vercel**                | Deployment platform        | Zero-config Next.js hosting               |

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           neo-dapp-starter                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                        UI Layer (React 19)                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────────┐      │ │
│  │  │ Connect  │  │ Switch   │  │ Switch    │  │ Error        │      │ │
│  │  │ Wallet   │  │ Chain    │  │ Theme     │  │ Handler      │      │ │
│  │  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └──────┬───────┘      │ │
│  │       │              │              │               │              │ │
│  │  ┌────┴──────────────┴──────────────┴───────────────┴──────────┐   │ │
│  │  │                    shadcn/ui Components                      │   │ │
│  │  │  Button, Dialog, DropdownMenu, Input, Sonner                │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                     State Layer (Jotai + React Query)               │ │
│  │  ┌────────────────────────┐  ┌──────────────────────────────────┐  │ │
│  │  │ Jotai Atoms            │  │ React Query Hooks                │  │ │
│  │  │ • chainIdAtom          │  │ • useBalance(scriptHash, acct)   │  │ │
│  │  │ • accountAtom          │  │ • useSymbol(scriptHash)          │  │ │
│  │  │ • connectorDatasAtom   │  │ • useDecimals(scriptHash)        │  │ │
│  │  │ • lastConnectedIdAtom  │  │ • useTransfer()                  │  │ │
│  │  │ • lastErrorAtom        │  │ • useServerTime()                │  │ │
│  │  │  └────────────┬───────────┘  └──────────┬───────────────────────┘  │ │
│  └───────────────┼─────────────────────────┼──────────────────────────┘ │
│                  │                         │                            │
│  ┌───────────────┼─────────────────────────┼──────────────────────────┐ │
│  │               │   Neo Actions Layer     │                          │ │
│  │  ┌────────────┴───────────┐  ┌──────────┴───────────────────────┐  │ │
│  │  │ Wallet Actions         │  │ Contract Actions                 │  │ │
│  │  │ • connect()            │  │ • invoke()                       │  │ │
│  │  │ • disconnect()         │  │ • invokeMultiple()               │  │ │
│  │  │ • switchChain()        │  │ • invokeRead()                   │  │ │
│  │  │ • ensureConnector()    │  │ • invokeReadMultiple()           │  │ │
│  │  └────────────┬───────────┘  │ • rpcRequest()                   │  │ │
│  │               │              │ • furaRequest()                   │  │ │
│  │               │              │ • waitForTransaction()            │  │ │
│  │               │              └──────────┬───────────────────────┘  │ │
│  └───────────────┼─────────────────────────┼──────────────────────────┘ │
│                  │                         │                            │
│  ┌───────────────┼─────────────────────────┼──────────────────────────┐ │
│  │               │  Connector Layer        │                          │ │
│  │  ┌────────────┴───────────┐  ┌──────────┴───────────────────────┐  │ │
│  │  │ Abstract Connector     │  │ RPC / NeoFura Transport          │  │ │
│  │  │ (EventEmitter3)        │  │ (@neongd/json-rpc)               │  │ │
│  │  ├────────────────────────┤  └──────────────────────────────────┘  │ │
│  │  │ NeoLineConnector       │                                       │ │
│  │  │ OneGateConnector       │                                       │ │
│  │  │ (+ custom connectors)  │                                       │ │
│  │  └────────────────────────┘                                       │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                     Neo N3 Blockchain                               │ │
│  │  Mainnet: https://n3seed2.ngd.network:10332                        │ │
│  │  Testnet: https://n3seed2.ngd.network:40332                        │ │
│  │  NeoFura: https://neofura.ngd.network                              │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
neo-dapp-starter/
├── src/
│   ├── app/                              # Next.js App Router
│   │   ├── layout.tsx                    # Root layout (Providers, Header)
│   │   ├── error.tsx                     # Error boundary
│   │   ├── not-found.tsx                 # 404 page
│   │   ├── (home)/page.tsx              # Home page with example links
│   │   ├── examples/
│   │   │   ├── transfer/page.tsx        # NEP-17 transfer example
│   │   │   └── server-time/page.tsx     # Edge API example
│   │   └── api/
│   │       └── time/route.ts            # Edge runtime API endpoint
│   │
│   ├── configs/                          # Application configuration
│   │   ├── app.ts                       # App name and global settings
│   │   ├── chains.ts                    # Chain IDs, RPC URLs, connector config
│   │   ├── environments.ts             # Environment enum with validation
│   │   └── tokens.ts                   # Token script hashes per chain
│   │
│   ├── lib/                             # Core business logic
│   │   ├── apis/                        # API layer
│   │   │   ├── time.ts                 # Server time API
│   │   │   └── tokens.ts              # NEP-17 token APIs (balance, symbol, decimals, transfer)
│   │   ├── errors/                     # Error hierarchy
│   │   │   ├── base.ts                # BaseError abstract class
│   │   │   ├── common.ts             # InternalError
│   │   │   ├── neo.ts                # 13 Neo-specific error types
│   │   │   └── request.ts            # HTTP/RPC/API request errors
│   │   ├── hooks/                     # React Query hooks
│   │   │   ├── time.ts              # useServerTime()
│   │   │   └── tokens.ts           # useBalance(), useSymbol(), useDecimals(), useTransfer()
│   │   ├── states/                   # Jotai state atoms
│   │   │   ├── errors.ts           # lastErrorAtom (global error capture)
│   │   │   └── neo.ts              # All Neo connection/chain/account atoms
│   │   └── utils/                   # Utility functions
│   │       ├── fonts.ts            # Font configuration
│   │       ├── formatters.ts       # Number, text, time formatters
│   │       ├── jotai.ts           # atomWithStorage, atomWithSchema, atomWithHashParam
│   │       ├── json.ts            # JSON serialize/deserialize
│   │       ├── ky.ts              # HTTP client (httpRequest, apiRequest)
│   │       ├── misc.ts            # rawAmountToAmount, isAddress, isScriptHash
│   │       ├── next.ts            # withResponse API wrapper
│   │       ├── react-query.ts     # QueryClient configuration
│   │       ├── shadcn.ts          # cn() utility
│   │       └── neo/               # Neo-specific utilities
│   │           ├── actions.ts     # connect, disconnect, invoke, rpcRequest, etc.
│   │           └── connectors/
│   │               ├── index.ts      # Connector registry
│   │               ├── types.ts      # Abstract Connector class & types
│   │               ├── neo-line.ts   # NeoLine wallet connector
│   │               └── one-gate.ts   # OneGate wallet connector
│   │
│   ├── ui/                           # UI components
│   │   ├── app/                     # App-level components
│   │   │   ├── account-icon.tsx    # Wallet address avatar
│   │   │   ├── connect.tsx         # Connect wallet dialog
│   │   │   ├── error-handler.tsx   # Global error toast handler
│   │   │   ├── header.tsx          # App header bar
│   │   │   ├── providers.tsx       # Jotai + React Query + Themes
│   │   │   ├── switch-chain.tsx    # Network switching dropdown
│   │   │   ├── switch-theme.tsx    # Dark/light theme toggle
│   │   ├── examples/               # Example page components
│   │   │   ├── server-time.tsx    # Server time display
│   │   │   └── transfer.tsx       # Token transfer form
│   │   ├── shadcn/                 # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── input.tsx
│   │   │   └── sonner.tsx         # Toast notifications
│   │   └── svgs/
│   │       └── loader.tsx         # Loading spinner SVG
│   │
│   ├── styles/                     # Global styles
│   │   ├── index.css              # Main CSS entry
│   │   └── shadcn.css             # shadcn/ui theme variables
│   │
│   ├── assets/images/             # Static images
│   │   └── connectors/           # Wallet connector icons
│   │       ├── neo-line.png
│   │       └── one-gate.png
│   │
│   └── types/                     # TypeScript type definitions
│       ├── global.d.ts
│       └── react-env.d.ts
│
├── .github/                       # GitHub Actions workflows
├── .husky/                        # Git hooks (pre-commit)
├── .storybook/                    # Storybook configuration
├── .vscode/                       # VS Code settings
├── .env                           # Production environment
├── .env.development               # Development environment
├── components.json                # shadcn/ui configuration
├── eslint.config.js               # ESLint flat config
├── lint-staged.config.js          # lint-staged configuration
├── next.config.ts                 # Next.js + Cloudflare config
├── package.json                   # Dependencies and scripts
├── postcss.config.js              # PostCSS (Tailwind)
├── prettier.config.js             # Prettier formatting rules
├── tailwind.config.ts             # Tailwind CSS configuration
├── tsconfig.json                  # TypeScript configuration
├── vercel.json                    # Vercel deployment config
├── vitest.config.ts               # Vitest test configuration
└── wrangler.toml                  # Cloudflare Workers config
```
