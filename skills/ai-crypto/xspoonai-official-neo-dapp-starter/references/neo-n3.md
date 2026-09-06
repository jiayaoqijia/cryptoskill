# Neo N3 Integration

## Neo N3 Network Configuration

### RPC Endpoints

| Network     | RPC URL                             | Purpose                 |
| ----------- | ----------------------------------- | ----------------------- |
| **Mainnet** | `https://n3seed2.ngd.network:10332` | Production transactions |
| **Testnet** | `https://n3seed2.ngd.network:40332` | Development and testing |

### NeoFura API Endpoints

| Network     | NeoFura URL                      | Purpose                     |
| ----------- | -------------------------------- | --------------------------- |
| **Mainnet** | `https://neofura.ngd.network`    | Advanced blockchain queries |
| **Testnet** | `https://testmagnet.ngd.network` | Test environment queries    |

### Chain Configuration

```typescript
// src/configs/chains.ts

export enum ChainId {
  Mainnet = "mainnet",
  Testnet = "testnet",
}

export const supportedChainIds = [ChainId.Mainnet, ChainId.Testnet];

export const rpcUrls: Record<ChainId, string> = {
  [ChainId.Mainnet]: "https://n3seed2.ngd.network:10332",
  [ChainId.Testnet]: "https://n3seed2.ngd.network:40332",
};
```

### Native Token Configuration

| Token   | Script Hash                                  | Decimals |
| ------- | -------------------------------------------- | -------- |
| **GAS** | `0xd2a4cff31913016155e38e474a2c06d08be276cf` | 8        |
| **NEO** | `0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5` | 0        |

## Wallet Connector System

### Abstract Connector Interface

The template uses an abstract `Connector` class (extending `EventEmitter3`) that defines a standardized wallet integration interface. This enables seamless addition of new wallet providers.

```typescript
// Core abstract class - src/lib/utils/neo/connectors/types.ts

export abstract class Connector extends EventEmitter<ConnectorEvents> {
  // Lifecycle
  abstract init(): Promise<void>;
  abstract destroy(): Promise<void>;

  // Status
  abstract isIntalled(): Promise<boolean>;
  abstract getVersion(): Promise<string | null>;
  abstract getData(): Promise<ConnectorData>;
  abstract isAuthorized(): Promise<boolean>;

  // Connection
  abstract connect(params?: ConnectParams): Promise<void>;
  abstract disconnect(): Promise<void>;
  abstract switchChain(params: SwitchChainParams): Promise<void>;

  // Contract Interaction
  abstract invoke(params: InvokeParams): Promise<InvokeResult>;
  abstract invokeMultiple(
    params: InvokeMultipleParams,
  ): Promise<InvokeMultipleResult>;

  // Events
  protected emitChange = async (): Promise<void> => {
    this.emit("change", await this.getData());
  };
}
```

### Connector Data Types

```typescript
export type ConnectorData = {
  chainId: ChainId | null;
  account: string | null;
};

export type InvokeParams = {
  scriptHash: string;
  operation: string;
  args?: Argument[];
  signers?: Signer[];
  broadcastOverride?: boolean;
};

export type InvokeResult = {
  transactionHash: string;
  signedTransaction?: string;
};
```

### Supported Wallet Connectors

| Connector   | ID         | Auth Storage     | Chain Switch   | Download                                                                                               |
| ----------- | ---------- | ---------------- | -------------- | ------------------------------------------------------------------------------------------------------ |
| **NeoLine** | `neo-line` | `sessionStorage` | ✅ Supported   | [Chrome Web Store](https://chrome.google.com/webstore/detail/neoline/cphhlgmgameodnhkjdmkpanlelnlohao) |
| **OneGate** | `one-gate` | `localStorage`   | ❌ Manual only | [onegate.space](https://onegate.space)                                                                 |

### NeoLine Connector

Uses `window.NEOLine` and `window.NEOLineN3` browser globals. Maps internal chain IDs:

```typescript
const neoChainIds: Partial<Record<number, ChainId>> = {
  3: ChainId.Mainnet,
  6: ChainId.Testnet,
};
```

Key implementation details:

- Initialization waits for `NEOLine.NEO.EVENT.READY` and `NEOLine.N3.EVENT.READY` events
- Falls back after 3-second timeout via `whenDomReady`
- Subscribes to `NETWORK_CHANGED` and `ACCOUNT_CHANGED` events
- Uses `@Catch('handleError')` decorator for unified error mapping

### OneGate Connector

Uses `window.OneGate` provider with standard Neo dAPI:

```typescript
const neoChainIds: Partial<Record<string, ChainId>> = {
  MainNet: ChainId.Mainnet,
  TestNet: ChainId.Testnet,
};
```

Key implementation details:

- Uses `BaseDapi` from `@neongd/neo-dapi` for standards-compliant communication
- Subscribes to `networkChanged` and `accountChanged` events
- Does NOT support programmatic chain switching (throws `SwitchChainNotSupportedError`)
- Maps `JsonRpcError` codes to domain-specific errors

### Adding a Custom Connector

To add a new wallet connector, implement the abstract `Connector` class:

```typescript
// src/lib/utils/neo/connectors/my-wallet.ts
import {
  Connector,
  ConnectorData,
  ConnectParams,
  InvokeParams,
  InvokeResult,
} from "./types";

export class MyWalletConnector extends Connector {
  async init(): Promise<void> {
    // Initialize wallet provider (e.g., window.MyWallet)
    // Subscribe to change events
  }

  async destroy(): Promise<void> {
    // Cleanup event listeners
  }

  async isIntalled(): Promise<boolean> {
    return window.MyWallet != null;
  }

  async getVersion(): Promise<string | null> {
    return (await window.MyWallet.getProvider()).version;
  }

  async getData(): Promise<ConnectorData> {
    // Return current chain and account
  }

  async isAuthorized(): Promise<boolean> {
    return localStorage.getItem("myWalletAuthorized") === "true";
  }

  async connect(params?: ConnectParams): Promise<void> {
    // Request account access
  }

  async disconnect(): Promise<void> {
    localStorage.removeItem("myWalletAuthorized");
  }

  async switchChain(params: SwitchChainParams): Promise<void> {
    // Switch network or throw SwitchChainNotSupportedError
  }

  async invoke(params: InvokeParams): Promise<InvokeResult> {
    // Execute contract invocation
  }

  async invokeMultiple(
    params: InvokeMultipleParams,
  ): Promise<InvokeMultipleResult> {
    // Execute batch invocations
  }
}
```

Then register it:

```typescript
// src/configs/chains.ts
export enum ConnectorId {
  NeoLine = "neo-line",
  OneGate = "one-gate",
  MyWallet = "my-wallet", // Add new ID
}

// src/lib/utils/neo/connectors/index.ts
import { MyWalletConnector } from "./my-wallet";

export const connectors: Record<ConnectorId, Connector> = {
  [ConnectorId.NeoLine]: new NeoLineConnector(),
  [ConnectorId.OneGate]: new OneGateConnector(),
  [ConnectorId.MyWallet]: new MyWalletConnector(),
};
```

## NEP-17 Token Operations

### Token API Layer

```typescript
// src/lib/apis/tokens.ts

// Get token decimals via invokeRead('decimals')
async function getDecimals(params: { chainId; scriptHash }): Promise<number>;

// Get token symbol via invokeRead('symbol') + base64 decode
async function getSymbol(params: { chainId; scriptHash }): Promise<string>;

// Get token balance via invokeRead('balanceOf') + rawAmountToAmount conversion
async function getBalance(params: {
  chainId;
  scriptHash;
  account;
  decimals;
}): Promise<string>;

// Transfer tokens via invoke('transfer') with proper NEP-17 arguments
async function transfer(params: {
  chainId;
  scriptHash;
  account;
  decimals;
  to;
  amount;
}): Promise<string>;
```

### Transfer Arguments (NEP-17 Standard)

```typescript
args: [
  { type: 'Hash160', value: addressToScriptHash(from) },    // sender
  { type: 'Hash160', value: addressToScriptHash(to) },      // recipient
  { type: 'Integer', value: amountToRawAmount(amount, decimals).toString() }, // raw amount
  { type: 'Any', value: null },                              // data (optional)
],
signers: [
  { account: addressToScriptHash(from), scopes: 'CalledByEntry' }
]
```

### React Query Hooks

```typescript
// src/lib/hooks/tokens.ts

// Query token decimals (staleTime: Infinity - never refetch)
function useDecimals(params: { chainId; scriptHash } | SkipToken);

// Query token symbol (staleTime: Infinity - never refetch)
function useSymbol(params: { chainId; scriptHash } | SkipToken);

// Query token balance (auto-resolves decimals dependency)
function useBalance(params: { chainId; scriptHash; account } | SkipToken);

// Transfer mutation (auto-waits for confirmation, invalidates balance cache)
function useTransfer(): UseMutationResult;
```

### Token Amount Utilities

```typescript
// src/lib/utils/misc.ts

// Convert raw blockchain amount to human-readable (e.g., 100000000 → "1" for 8 decimals)
function rawAmountToAmount(rawAmount: bigint, decimals: number): string;

// Convert human-readable to raw (e.g., "1" → 100000000n for 8 decimals)
function amountToRawAmount(amount: string, decimals: number): bigint;

// Validate Neo N3 address format (starts with "N")
function isAddress(address: string): boolean;

// Validate script hash format (starts with "0x")
function isScriptHash(scriptHash: string): boolean;
```

## Smart Contract Interaction

### Read-Only Invocations

```typescript
// Single contract read via RPC invokefunction
async function invokeRead<T>(params: {
  chainId?: ChainId;
  scriptHash: string;
  operation: string;
  args?: Argument[];
  signers?: Signer[];
}): Promise<T>;

// Multiple contract reads via RPC invokescript (batched)
async function invokeReadMultiple<T>(params: {
  chainId?: ChainId;
  invocations: Invocation[];
  signers?: Signer[];
}): Promise<T>;
```

### State-Changing Invocations

```typescript
// Single contract invoke via wallet connector
async function invoke(params: {
  chainId?: ChainId;
  account?: string;
  scriptHash: string;
  operation: string;
  args?: Argument[];
  signers?: Signer[];
}): Promise<InvokeResult>;

// Multiple contract invokes via wallet connector
async function invokeMultiple(params: {
  chainId?: ChainId;
  account?: string;
  invocations: Invocation[];
  signers?: Signer[];
}): Promise<InvokeMultipleResult>;
```

### Transaction Waiting

```typescript
// Wait for transaction confirmation via polling getapplicationlog
async function waitForTransaction(params: {
  chainId?: ChainId;
  hash: string;
}): Promise<ApplicationLogJson>;
// Retries with exponential backoff (5s * 1.2^retryCount)
```

### Direct RPC Requests

```typescript
// Direct Neo N3 RPC call
async function rpcRequest<T>(params: {
  chainId?: ChainId;
  method: string;
  params: unknown[];
}): Promise<T>;

// NeoFura advanced query
async function furaRequest<T>(params: {
  chainId?: ChainId;
  method: string;
  params: unknown[];
}): Promise<T>;
```

### Common RPC Methods

| Method               | Description          | Example                                                                  |
| -------------------- | -------------------- | ------------------------------------------------------------------------ |
| `getblockcount`      | Current block height | `rpcRequest({ method: 'getblockcount', params: [] })`                    |
| `getbestblockhash`   | Latest block hash    | `rpcRequest({ method: 'getbestblockhash', params: [] })`                 |
| `getnep17balances`   | NEP-17 balances      | `rpcRequest({ method: 'getnep17balances', params: [address] })`          |
| `getnep17transfers`  | Transfer history     | `rpcRequest({ method: 'getnep17transfers', params: [address] })`         |
| `invokefunction`     | Contract read call   | `rpcRequest({ method: 'invokefunction', params: [hash, method, args] })` |
| `invokescript`       | Script execution     | `rpcRequest({ method: 'invokescript', params: [base64Script] })`         |
| `getapplicationlog`  | Transaction log      | `rpcRequest({ method: 'getapplicationlog', params: [txHash] })`          |
| `sendrawtransaction` | Broadcast TX         | `rpcRequest({ method: 'sendrawtransaction', params: [base64TX] })`       |
