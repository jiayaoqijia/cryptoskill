---
name: wagmi
description: Use wagmi React hooks for Celo dApps. Includes wallet connection, transaction hooks, and React integration patterns.
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Wagmi for Celo

Wagmi is a React library for building Ethereum applications with hooks. It uses viem under the hood.

Source: https://wagmi.sh

## When to Use

- Building React dApps on Celo
- Implementing wallet connection flows
- Managing blockchain state in React components
- Using React hooks for contract interactions

## Installation

```bash
npm install wagmi viem@2.x @tanstack/react-query
```

## Configuration

### Basic Setup

```typescript
// config.ts
import { http, createConfig } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";

export const config = createConfig({
  chains: [celo, celoSepolia],
  transports: {
    [celo.id]: http(),
    [celoSepolia.id]: http(),
  },
});
```

### With Connectors

```typescript
import { http, createConfig } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";
import { injected, walletConnect, metaMask } from "wagmi/connectors";

const projectId = process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!;

export const config = createConfig({
  chains: [celo, celoSepolia],
  connectors: [
    injected(),
    walletConnect({ projectId }),
    metaMask(),
  ],
  transports: {
    [celo.id]: http(),
    [celoSepolia.id]: http(),
  },
});
```

Source: https://wagmi.sh/react/guides/connect-wallet

## Provider Setup

```tsx
// app.tsx
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";

const queryClient = new QueryClient();

function App({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## Wallet Connection

### Display Wallet Options

```tsx
import { useConnect, useConnectors } from "wagmi";

function WalletOptions() {
  const { connect } = useConnect();
  const connectors = useConnectors();

  return (
    <div>
      {connectors.map((connector) => (
        <button
          key={connector.uid}
          onClick={() => connect({ connector })}
        >
          {connector.name}
        </button>
      ))}
    </div>
  );
}
```

### Display Connected Account

```tsx
import { useAccount, useDisconnect } from "wagmi";

function Account() {
  const { address, isConnected, chain } = useAccount();
  const { disconnect } = useDisconnect();

  if (!isConnected) return <WalletOptions />;

  return (
    <div>
      <p>Connected: {address}</p>
      <p>Chain: {chain?.name}</p>
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  );
}
```

## Reading Contract Data

```tsx
import { useReadContract } from "wagmi";

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
] as const;

function TokenBalance({ address }: { address: `0x${string}` }) {
  const { data: balance, isLoading } = useReadContract({
    address: "0x765de816845861e75a25fca122bb6898b8b1282a", // USDm
    abi: ERC20_ABI,
    functionName: "balanceOf",
    args: [address],
  });

  if (isLoading) return <div>Loading...</div>;

  return <div>Balance: {balance?.toString()}</div>;
}
```

## Writing to Contracts

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from "wagmi";
import { parseEther } from "viem";

function TransferToken() {
  const { writeContract, data: hash, isPending } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  async function handleTransfer() {
    writeContract({
      address: "0x765de816845861e75a25fca122bb6898b8b1282a",
      abi: ERC20_ABI,
      functionName: "transfer",
      args: ["0x...", parseEther("10")],
    });
  }

  return (
    <div>
      <button onClick={handleTransfer} disabled={isPending}>
        {isPending ? "Confirming..." : "Transfer"}
      </button>
      {isConfirming && <div>Waiting for confirmation...</div>}
      {isSuccess && <div>Transaction confirmed!</div>}
    </div>
  );
}
```

## Sending Transactions

```tsx
import { useSendTransaction, useWaitForTransactionReceipt } from "wagmi";
import { parseEther } from "viem";

function SendCelo() {
  const { sendTransaction, data: hash, isPending } = useSendTransaction();

  const { isSuccess } = useWaitForTransactionReceipt({ hash });

  return (
    <button
      onClick={() =>
        sendTransaction({
          to: "0x...",
          value: parseEther("0.1"),
        })
      }
      disabled={isPending}
    >
      Send 0.1 CELO
    </button>
  );
}
```

## Chain Switching

```tsx
import { useSwitchChain } from "wagmi";
import { celo, celoSepolia } from "wagmi/chains";

function NetworkSwitcher() {
  const { switchChain, isPending } = useSwitchChain();

  return (
    <div>
      <button
        onClick={() => switchChain({ chainId: celo.id })}
        disabled={isPending}
      >
        Switch to Celo Mainnet
      </button>
      <button
        onClick={() => switchChain({ chainId: celoSepolia.id })}
        disabled={isPending}
      >
        Switch to Celo Sepolia
      </button>
    </div>
  );
}
```

## Common Hooks

| Hook | Purpose |
|------|---------|
| useAccount | Get connected account info |
| useConnect | Connect wallet |
| useDisconnect | Disconnect wallet |
| useReadContract | Read contract state |
| useWriteContract | Write to contract |
| useSendTransaction | Send native currency |
| useWaitForTransactionReceipt | Wait for tx confirmation |
| useSwitchChain | Switch networks |
| useBalance | Get account balance |
| useChainId | Get current chain ID |

## Celo Chain IDs

| Network | Chain ID |
|---------|----------|
| Celo Mainnet | 42220 |
| Celo Sepolia | 11142220 |

## Dependencies

```json
{
  "dependencies": {
    "wagmi": "^2.0.0",
    "viem": "^2.0.0",
    "@tanstack/react-query": "^5.0.0"
  }
}
```

## Additional Resources

- [hooks-reference.md](references/hooks-reference.md) - Complete hooks reference
