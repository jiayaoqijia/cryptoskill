# Frontend Architecture

## UI Components

### Connect Wallet Dialog

The `Connect` component provides:

- "Connect wallet" button when disconnected
- Truncated address display with avatar when connected
- Hover-to-reveal "Disconnect" button
- Modal dialog listing all supported wallets
- Auto-redirect to download page if wallet not installed

### Switch Chain Dropdown

The `SwitchChain` component provides:

- Current network name display
- Dropdown with all supported chains (Mainnet/Testnet)
- "Wrong network" destructive button when wallet chain doesn't match app chain
- Triggers wallet-level chain switch when possible

### Switch Theme Toggle

The `SwitchTheme` component provides:

- Sun/Moon icon toggle button
- Dropdown with Light, Dark, System options
- Powered by `next-themes` with `attribute="class"`

### Global Error Handler

The `ErrorHandler` component provides:

- Global capture of unhandled errors and promise rejections via `lastErrorAtom`
- Toast notifications via `sonner` for user-facing errors
- Message deduplication (1-second cooldown per unique message)
- Differentiated logging: `console.error` for fixable bugs, `console.log` for expected errors
- Asynchronous processing to avoid blocking the error event

### Providers Wrapper

The `Providers` component composes all required React context providers:

```
JotaiProvider (store)
  └─ QueryClientProvider (queryClient)
       └─ ReactQueryDevtools
            └─ NextThemesProvider (dark/light/system)
                 └─ Toaster (sonner)
                 └─ ErrorHandler
                 └─ {children}
```

## State Management

### Jotai Atoms Overview

| Atom                           | Type                                 | Storage      | Description                                        |
| ------------------------------ | ------------------------------------ | ------------ | -------------------------------------------------- |
| `lastConnectedConnectorIdAtom` | `ConnectorId \| null`                | localStorage | Last connected wallet ID                           |
| `connectorDatasAtom`           | `Record<ConnectorId, ConnectorData>` | Memory       | All connector states (installed, chainId, account) |
| `connectedConnectorDataAtom`   | `ConnectorData \| null`              | Derived      | Connected connector data (null if disconnected)    |
| `connectorChainIdAtom`         | `ChainId \| undefined`               | Derived      | Connected wallet's chain ID                        |
| `connectorAccountAtom`         | `string \| undefined`                | Derived      | Connected wallet's address                         |
| `storageChainIdAtom`           | `ChainId \| null`                    | localStorage | User-selected chain ID                             |
| `chainIdAtom`                  | `ChainId`                            | Derived      | Active chain ID (wallet > storage > default)       |
| `accountAtom`                  | `string \| undefined`                | Derived      | Active account address                             |
| `lastErrorAtom`                | `Error \| null`                      | Memory       | Global error state for toast display               |

### Chain ID Resolution Priority

```
1. connectorChainId (wallet-reported) → if connected and valid
2. storageChainId (user selection)    → if previously set
3. supportedChainIds[0] (default)     → Mainnet
```

### atomWithStorage Pattern

The template uses a custom `atomWithStorage` that combines Jotai persistence with Zod schema validation:

```typescript
// Persisted to localStorage with Zod validation
export const lastConnectedConnectorIdAtom = atomWithStorage(
  "lastConnectedConnectorId", // localStorage key
  z.nativeEnum(ConnectorId).nullable(), // Zod schema
  null, // Default value
);
```

### Connection Flow

```
User clicks "Connect" → handleConnectClick(connectorId)
  ↓
Check if connector is installed → if not, open download URL
  ↓
connect({ connectorId, chainId })
  ↓
connector.getVersion() → check minimum version
  ↓
connector.connect() → request wallet authorization
  ↓
connector.getData() → get chainId + account
  ↓
If chain mismatch → connector.switchChain()
  ↓
Update connectorDatasAtom + lastConnectedConnectorIdAtom
  ↓
UI reactively updates (Connect button shows address)
```

## Error Handling System

### Error Hierarchy

```
Error (JavaScript built-in)
  └─ BaseError (abstract)
       ├─ InternalError                    # Generic internal error
       ├─ Neo Errors:
       │   ├─ ConnectorNotInstalledError   # Wallet not installed
       │   ├─ ConnectorNotConnectedError   # Wallet not connected
       │   ├─ ConnectorCommunicationError  # Communication failure
       │   ├─ ConnectorVersionIncompatibleError  # Wallet version too old
       │   ├─ ConnectorChainMismatchError  # Wrong network
       │   ├─ ConnectorAccountNotFoundError  # No account in wallet
       │   ├─ ConnectorAccountMismatchError  # Wrong account
       │   ├─ InvalidParamsError           # Bad parameters
       │   ├─ InsufficientFundsError       # Not enough balance
       │   ├─ InternalRpcError             # RPC node error
       │   ├─ UserRejectedRequestError     # User clicked cancel
       │   ├─ SwitchChainNotSupportedError # Connector can't switch
       │   ├─ ContractInvocationError      # Contract execution failed
       │   └─ UnknownNeoError              # Uncategorized wallet error
       └─ Request Errors:
           ├─ TimeoutError                 # Request timeout
           ├─ HttpRequestError             # HTTP error (status, json)
           ├─ ApiRequestError              # API error (name, data)
           └─ RpcRequestError              # RPC error (code, data)
```

### BaseError Properties

| Property  | Type            | Description                                                       |
| --------- | --------------- | ----------------------------------------------------------------- |
| `name`    | `string`        | Error class name                                                  |
| `message` | `string`        | Human-readable message                                            |
| `data`    | `unknown`       | Additional error data                                             |
| `cause`   | `Error \| null` | Original cause (error chain)                                      |
| `needFix` | `boolean`       | `true` = unexpected bug (500), `false` = expected condition (400) |
| `handled` | `boolean`       | Prevents duplicate toast display                                  |

### Error Flow

```
Connector throws wallet-specific error
  ↓
@Catch('handleError') decorator intercepts
  ↓
handleError() maps to domain-specific BaseError subclass
  ↓
Error propagates to component or global handler
  ↓
lastErrorAtom captures unhandled errors
  ↓
ErrorHandler component shows toast notification
  ↓
Error marked as handled (prevented duplicate display)
```

## API Routes

### Edge Runtime

```typescript
// src/app/api/time/route.ts
import { withResponse } from "@/lib/utils/next";

export const runtime = "edge"; // Runs at the edge (Cloudflare Workers / Vercel Edge)

export const GET = withResponse(() => {
  return Date.now();
});
```

### withResponse Wrapper

The `withResponse` utility wraps API handlers with:

- Automatic `NextResponse.json()` serialization
- Error catching and structured error responses
- Status code mapping: `needFix=true` → 500, `needFix=false` → 400
- Consistent error response format: `{ name, message, data }`

### Adding a New API Route

```typescript
// src/app/api/my-endpoint/route.ts
import { withResponse } from "@/lib/utils/next";

export const runtime = "edge";

export const GET = withResponse(async (request) => {
  const url = new URL(request.url);
  const param = url.searchParams.get("param");
  // Your logic here
  return { result: "data" };
});

export const POST = withResponse(async (request) => {
  const body = await request.json();
  // Your logic here
  return { success: true };
});
```
