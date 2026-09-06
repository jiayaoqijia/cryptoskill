# Neo dApp Starter

**A production-ready Neo N3 dApp starter template** with Next.js 15, wallet integration (NeoLine/OneGate), NEP-17 token operations, multi-chain support, and edge deployment.

| Property       | Value                                  |
| -------------- | -------------------------------------- |
| **Skill Name** | `neo-dapp-starter`                     |
| **Track**      | Web3 Core Operations                   |
| **Chain**      | Neo N3 (Mainnet + Testnet)             |
| **Type**       | Full-stack dApp template               |
| **Framework**  | Next.js 15 + React 19 + TypeScript 5.7 |
| **Status**     | Production-ready                       |

## Features

### Neo N3 Integration

- ✅ **Multi-wallet support** — NeoLine and OneGate with abstract Connector pattern
- ✅ **Multi-chain** — Seamless Mainnet/Testnet switching
- ✅ **NEP-17 tokens** — Balance, symbol, decimals, transfer operations
- ✅ **Smart contract invocation** — Single and batch, read and write
- ✅ **Transaction waiting** — Polling with exponential backoff
- ✅ **Dual API layer** — Direct RPC + NeoFura advanced queries

### Frontend Architecture

- ✅ **Next.js 15 App Router** — Server components, edge runtime
- ✅ **React 19** — Latest features, concurrent rendering
- ✅ **TypeScript 5.7** — Strict mode, full type coverage
- ✅ **Tailwind CSS + shadcn/ui** — Beautiful, accessible components
- ✅ **Jotai state management** — Atomic, SSR-safe, localStorage-persisted
- ✅ **React Query** — Caching, refetching, optimistic updates
- ✅ **Zod validation** — Runtime schema validation for atoms

### Developer Experience

- ✅ **Storybook 8.5** — Isolated component development
- ✅ **Vitest 3.0** — Fast unit testing
- ✅ **ESLint 9 + Prettier** — Zero-warnings code quality policy
- ✅ **Husky + lint-staged** — Pre-commit hooks
- ✅ **Dark/light theme** — System-aware theme switching

### Deployment

- ✅ **Cloudflare Pages** — Global edge deployment
- ✅ **Vercel** — Zero-config Next.js hosting
- ✅ **Edge Runtime** — Low-latency API routes

### Error Handling

- ✅ **13 Neo-specific error types** — Comprehensive wallet error mapping
- ✅ **4 request error types** — HTTP, API, RPC, timeout handling
- ✅ **Global error capture** — Unhandled error/rejection catching
- ✅ **Toast notifications** — User-friendly error display with deduplication
- ✅ **Error chain walking** — Root cause analysis via `.walk()` method

## Quick Start

```bash
# Install dependencies (requires pnpm 10.5+, Node 22.x)
pnpm install

# Start development server
pnpm dev

# Open in browser
open http://localhost:3000
```

### Environment Setup

| File               | Variable                  | Value         |
| ------------------ | ------------------------- | ------------- |
| `.env`             | `NEXT_PUBLIC_ENVIRONMENT` | `production`  |
| `.env.development` | `NEXT_PUBLIC_ENVIRONMENT` | `development` |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    UI Components Layer                        │
│  Connect Wallet · Switch Chain · Switch Theme · Error Toast  │
├─────────────────────────────────────────────────────────────┤
│                    State Management Layer                     │
│  Jotai Atoms (chain, account, connector) + React Query       │
├─────────────────────────────────────────────────────────────┤
│                    Actions Layer                             │
│  connect · disconnect · invoke · rpcRequest · furaRequest    │
├─────────────────────────────────────────────────────────────┤
│                    Connector Layer                            │
│  Abstract Connector → NeoLine / OneGate / Custom             │
├─────────────────────────────────────────────────────────────┤
│                    Neo N3 Blockchain                          │
│  Mainnet · Testnet · NeoFura API                             │
└─────────────────────────────────────────────────────────────┘
```

## Wallet Integration

### Supported Wallets

| Wallet      | Connector ID | Features                       | Chain Switch    |
| ----------- | ------------ | ------------------------------ | --------------- |
| **NeoLine** | `neo-line`   | Full dAPI, event-driven        | ✅ Programmatic |
| **OneGate** | `one-gate`   | Standard dAPI, persistent auth | ❌ Manual only  |

### Connection Flow

1. User clicks "Connect wallet" → modal lists available wallets
2. If wallet not installed → redirects to download page
3. Wallet version check → rejects incompatible versions
4. Request authorization → wallet prompts user
5. Chain verification → auto-switch if mismatched
6. State update → Jotai atoms reflect connected state
7. UI reactive update → address displayed with avatar

### Adding a New Connector

Implement the abstract `Connector` class from `src/lib/utils/neo/connectors/types.ts`:

```typescript
export class MyWalletConnector extends Connector {
  async init(): Promise<void> {
    /* ... */
  }
  async destroy(): Promise<void> {
    /* ... */
  }
  async isIntalled(): Promise<boolean> {
    /* ... */
  }
  async getVersion(): Promise<string | null> {
    /* ... */
  }
  async getData(): Promise<ConnectorData> {
    /* ... */
  }
  async isAuthorized(): Promise<boolean> {
    /* ... */
  }
  async connect(params?: ConnectParams): Promise<void> {
    /* ... */
  }
  async disconnect(): Promise<void> {
    /* ... */
  }
  async switchChain(params: SwitchChainParams): Promise<void> {
    /* ... */
  }
  async invoke(params: InvokeParams): Promise<InvokeResult> {
    /* ... */
  }
  async invokeMultiple(
    params: InvokeMultipleParams,
  ): Promise<InvokeMultipleResult> {
    /* ... */
  }
}
```

Register in `src/configs/chains.ts` and `src/lib/utils/neo/connectors/index.ts`.

## Token Operations

### Available APIs

| Function        | Description          | Input                                                    | Output            |
| --------------- | -------------------- | -------------------------------------------------------- | ----------------- |
| `getDecimals()` | Token decimal places | `{ chainId, scriptHash }`                                | `number`          |
| `getSymbol()`   | Token symbol         | `{ chainId, scriptHash }`                                | `string`          |
| `getBalance()`  | Account balance      | `{ chainId, scriptHash, account, decimals }`             | `string`          |
| `transfer()`    | Send tokens          | `{ chainId, scriptHash, account, decimals, to, amount }` | `string` (txHash) |

### React Hooks

| Hook            | Query Key              | Stale Time | Purpose                        |
| --------------- | ---------------------- | ---------- | ------------------------------ |
| `useDecimals()` | `['decimals', params]` | `Infinity` | Token decimals (immutable)     |
| `useSymbol()`   | `['symbol', params]`   | `Infinity` | Token symbol (immutable)       |
| `useBalance()`  | `['balance', params]`  | Default    | Account balance (auto-refresh) |
| `useTransfer()` | Mutation               | N/A        | Transfer + wait + invalidate   |

### Amount Precision

All token amounts use `BigNumber.js` for precision:

```typescript
// Human-readable "1.5" → Raw 150000000n (8 decimals)
amountToRawAmount("1.5", 8); // → 150000000n

// Raw 150000000n → Human-readable "1.5"
rawAmountToAmount(150000000n, 8); // → "1.5"
```

## Smart Contract Interaction

### Read Operations (No Wallet Required)

```typescript
import { invokeRead } from "@/lib/utils/neo/actions";

const result = await invokeRead({
  chainId: ChainId.Mainnet,
  scriptHash: "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5",
  operation: "totalSupply",
});
```

### Write Operations (Wallet Required)

```typescript
import { invoke, waitForTransaction } from "@/lib/utils/neo/actions";

const { transactionHash } = await invoke({
  chainId: ChainId.Mainnet,
  account: connectedAddress,
  scriptHash: "0xd2a4cff31913016155e38e474a2c06d08be276cf",
  operation: "transfer",
  args: [
    { type: "Hash160", value: fromScriptHash },
    { type: "Hash160", value: toScriptHash },
    { type: "Integer", value: "100000000" },
    { type: "Any", value: null },
  ],
  signers: [{ account: fromScriptHash, scopes: "CalledByEntry" }],
});

await waitForTransaction({ chainId: ChainId.Mainnet, hash: transactionHash });
```

## Error Handling

### Error Types

| Category     | Error                               | Default Message                         | needFix |
| ------------ | ----------------------------------- | --------------------------------------- | ------- |
| **Wallet**   | `ConnectorNotInstalledError`        | Wallet not installed.                   | `false` |
| **Wallet**   | `ConnectorNotConnectedError`        | Wallet not connected.                   | `false` |
| **Wallet**   | `ConnectorCommunicationError`       | Communicate failed with wallet.         | `true`  |
| **Wallet**   | `ConnectorVersionIncompatibleError` | Version not compatible, please upgrade. | `false` |
| **Wallet**   | `ConnectorChainMismatchError`       | Network does not match, please switch.  | `false` |
| **Wallet**   | `ConnectorAccountNotFoundError`     | Wallet does not have an account.        | `false` |
| **Wallet**   | `ConnectorAccountMismatchError`     | Account does not match, please switch.  | `false` |
| **Params**   | `InvalidParamsError`                | Invalid params.                         | `true`  |
| **Balance**  | `InsufficientFundsError`            | Insufficient funds.                     | `false` |
| **RPC**      | `InternalRpcError`                  | Internal RPC error.                     | `true`  |
| **User**     | `UserRejectedRequestError`          | User rejected request.                  | `false` |
| **Chain**    | `SwitchChainNotSupportedError`      | Switching not supported, use wallet.    | `false` |
| **Contract** | `ContractInvocationError`           | Contract invocation failed.             | `true`  |
| **Unknown**  | `UnknownNeoError`                   | Unknown Neo error.                      | `true`  |
| **Network**  | `TimeoutError`                      | Request timeout.                        | `true`  |
| **Network**  | `HttpRequestError`                  | HTTP request failed.                    | `true`  |
| **Network**  | `ApiRequestError`                   | API request failed.                     | `true`  |
| **Network**  | `RpcRequestError`                   | RPC request failed.                     | `true`  |

### Global Error Handling

Unhandled errors are captured by `lastErrorAtom` (via `window.addEventListener('error')` and `window.addEventListener('unhandledrejection')`) and displayed as toast notifications by the `ErrorHandler` component.

## Deployment

### Vercel

```bash
# Deploy to Vercel (auto-detects Next.js)
vercel

# Set environment variables in Vercel dashboard
# NEXT_PUBLIC_ENVIRONMENT=production
```

### Cloudflare Pages

```bash
# Build for Cloudflare
pnpm build

# Preview locally
pnpm start

# Deploy
wrangler pages deploy .vercel/output/static
```

### Available Scripts

| Script           | Command                     | Purpose                       |
| ---------------- | --------------------------- | ----------------------------- |
| `pnpm dev`       | `next dev`                  | Development server            |
| `pnpm build`     | `next-on-pages`             | Production build (Cloudflare) |
| `pnpm start`     | `wrangler pages dev`        | Preview production build      |
| `pnpm lint`      | `eslint --max-warnings 0 .` | Lint with zero warnings       |
| `pnpm test`      | `vitest run`                | Run tests                     |
| `pnpm typecheck` | `tsc`                       | Type checking                 |
| `pnpm storybook` | `storybook dev -p 6006`     | Component development         |

## Configuration Files

| File                 | Purpose                                 |
| -------------------- | --------------------------------------- |
| `next.config.ts`     | Next.js + Cloudflare dev platform setup |
| `tailwind.config.ts` | Tailwind CSS theme customization        |
| `tsconfig.json`      | TypeScript compiler options             |
| `eslint.config.js`   | ESLint 9 flat configuration             |
| `prettier.config.js` | Prettier formatting rules               |
| `vitest.config.ts`   | Vitest test configuration               |
| `components.json`    | shadcn/ui component settings            |
| `wrangler.toml`      | Cloudflare Workers configuration        |
| `vercel.json`        | Vercel deployment settings              |
| `.node-version`      | Required Node.js version (22.x)         |

## Key Dependencies

### Production

| Package                 | Version | Purpose                                |
| ----------------------- | ------- | -------------------------------------- |
| `@cityofzion/neon-core` | ^5.7.0  | Neo N3 core (address, script building) |
| `@neongd/neo-dapi`      | ^2.0.2  | Neo dAPI standard wallet communication |
| `@neongd/json-rpc`      | ^2.0.2  | JSON-RPC transport for Neo nodes       |
| `next`                  | 15.1.9  | React full-stack framework             |
| `react`                 | ^19.0.0 | UI library                             |
| `jotai`                 | ^2.11.0 | Atomic state management                |
| `@tanstack/react-query` | ^5.64.2 | Async data fetching and caching        |
| `zod`                   | ^3.24.1 | Schema validation                      |
| `bignumber.js`          | ^9.1.2  | Precision token arithmetic             |
| `ky`                    | ^1.7.4  | HTTP client                            |
| `catchee`               | ^1.0.2  | @Catch error decorator                 |
| `eventemitter3`         | ^5.0.1  | Event system for connectors            |
| `next-themes`           | ^0.4.4  | Theme switching                        |
| `sonner`                | ^1.7.2  | Toast notifications                    |

### Development

| Package                     | Version  | Purpose                  |
| --------------------------- | -------- | ------------------------ |
| `@cloudflare/next-on-pages` | ^1.13.8  | Cloudflare Pages adapter |
| `vitest`                    | ^3.0.3   | Unit testing             |
| `storybook`                 | ^8.5.0   | Component development    |
| `eslint`                    | ^9.18.0  | Code linting             |
| `prettier`                  | ^3.4.2   | Code formatting          |
| `husky`                     | ^9.1.7   | Git hooks                |
| `wrangler`                  | ^3.109.3 | Cloudflare CLI           |
| `typescript`                | ^5.7.3   | Type checking            |

## Use with SpoonOS

### As Claude Code Skill (Vibe Coding)

```bash
# Copy skill to your workspace
mkdir -p .claude/skills
cp -r web3-core-operations/neo-dapp-starter/ .claude/skills/

# Then describe what you want:
# "Build a Neo N3 dApp with token transfer and NFT gallery"
```

### As SpoonReactSkill Agent Tool

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="neo_dapp_builder",
    skill_paths=["./web3-core-operations"],
    scripts_enabled=True
)

await agent.activate_skill("neo-dapp-starter")
response = await agent.run(
    "Create a new page that displays NEP-17 token balances for the connected wallet"
)
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for submission guidelines.

**PR Title Format:**

```
[web3-core-operations] Add neo-dapp-starter skill
```

## License

MIT License
