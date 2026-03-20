# Frontend Integration (viem + wagmi)

All chain interaction uses viem directly or wagmi hooks.

## Dependencies

```bash
pnpm add viem wagmi @tanstack/react-query
```

## Chain Configuration

### Local devnode

```typescript
import { defineChain } from "viem";

export const arbitrumLocal = defineChain({
  id: 412346,
  name: "Arbitrum Local",
  nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["http://localhost:8547"] },
  },
});
```

### Testnets and mainnet

```typescript
import { arbitrumSepolia, arbitrum } from "viem/chains";
```

viem ships with built-in chain definitions for `arbitrum` (One) and `arbitrumSepolia`.

## wagmi Config

**Important:** Always pass explicit URLs to `http()`. Calling `http()` with no argument does not reliably resolve custom chain RPC URLs from `defineChain` — requests will silently fail.

```typescript
import { http, createConfig } from "wagmi";
import { arbitrum, arbitrumSepolia } from "wagmi/chains";
import { injected, walletConnect } from "wagmi/connectors";

export const config = createConfig({
  chains: [arbitrum, arbitrumSepolia],
  connectors: [
    injected(),
    walletConnect({ projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID! }),
  ],
  transports: {
    [arbitrum.id]: http("https://arb1.arbitrum.io/rpc"),
    [arbitrumSepolia.id]: http("https://sepolia-rollup.arbitrum.io/rpc"),
  },
});
```

For local devnode, use a Next.js API route proxy (see `references/local-devnode.md` CORS section):

```typescript
import { http, createConfig } from "wagmi";
import { arbitrumLocal } from "./chains";

export const config = createConfig({
  chains: [arbitrumLocal],
  transports: {
    [arbitrumLocal.id]: http("/api/rpc"),
  },
});
```

## Provider Setup (Next.js)

```typescript
"use client";

import { useState } from "react";
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## Hydration Safety

Wagmi hooks like `useAccount()` return different values on the server (no wallet) vs the client (potentially connected). This causes Next.js hydration mismatches when components conditionally render based on wallet state (`isConnected`, `address`).

**Fix:** Use a `mounted` guard so wallet-dependent UI only renders after the first client render:

```typescript
"use client";

import { useState, useEffect } from "react";
import { useAccount } from "wagmi";

export function WalletInfo() {
  const { address, isConnected } = useAccount();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  // Render a placeholder until mounted to avoid hydration mismatch
  if (!mounted) return <div className="h-10 w-32" />;

  if (!isConnected) return <button>Connect Wallet</button>;

  return <span>{address}</span>;
}
```

Apply this pattern to **every** client component that branches on `useAccount`, `useConnect`, or other wagmi hooks that depend on browser-only wallet state.

## Reading Contract State

### With wagmi hooks

```typescript
import { useReadContract } from "wagmi";
import { counterAbi } from "./abi";

function CounterDisplay({ address }: { address: `0x${string}` }) {
  const { data: count, isLoading } = useReadContract({
    address,
    abi: counterAbi,
    functionName: "number",
  });

  if (isLoading) return <span>Loading...</span>;
  return <span>{count?.toString()}</span>;
}
```

### With viem directly

```typescript
import { createPublicClient, http } from "viem";
import { arbitrumSepolia } from "viem/chains";

const publicClient = createPublicClient({
  chain: arbitrumSepolia,
  transport: http(),
});

const count = await publicClient.readContract({
  address: "0x...",
  abi: counterAbi,
  functionName: "number",
});
```

## Writing to Contracts

### With wagmi hooks

```typescript
import { useWriteContract, useWaitForTransactionReceipt } from "wagmi";

function IncrementButton({ address }: { address: `0x${string}` }) {
  const { writeContract, data: hash, isPending } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  return (
    <div>
      <button
        disabled={isPending || isConfirming}
        onClick={() =>
          writeContract({
            address,
            abi: counterAbi,
            functionName: "increment",
          })
        }
      >
        {isPending ? "Confirming..." : "Increment"}
      </button>
      {isSuccess && <p>Transaction confirmed.</p>}
    </div>
  );
}
```

### With viem wallet client

```typescript
import { createWalletClient, custom } from "viem";
import { arbitrumSepolia } from "viem/chains";

const walletClient = createWalletClient({
  chain: arbitrumSepolia,
  transport: custom(window.ethereum!),
});

const hash = await walletClient.writeContract({
  address: "0x...",
  abi: counterAbi,
  functionName: "increment",
  account: "0x...",
});
```

## Watching Events

```typescript
import { useWatchContractEvent } from "wagmi";

useWatchContractEvent({
  address: "0x...",
  abi: counterAbi,
  eventName: "NumberSet",
  onLogs(logs) {
    console.log("New event:", logs);
  },
});
```

## ABI Management

Keep ABIs in a shared location both contract workspaces can export to:

```
apps/
├── frontend/src/abi/
│   ├── Counter.ts          # Stylus contract ABI (from cargo stylus export-abi)
│   └── SolidityCounter.ts  # Solidity ABI (from forge inspect)
```

### Typed ABI pattern

```typescript
export const counterAbi = [
  {
    type: "function",
    name: "number",
    inputs: [],
    outputs: [{ type: "uint256" }],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "increment",
    inputs: [],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "setNumber",
    inputs: [{ name: "newNumber", type: "uint256" }],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "event",
    name: "NumberSet",
    inputs: [{ name: "newNumber", type: "uint256", indexed: false }],
  },
] as const;
```

Using `as const` gives you full type inference with wagmi and viem.

## Error Handling

```typescript
import { BaseError, ContractFunctionRevertedError } from "viem";

try {
  await writeContract({ ... });
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName;
      // Handle specific contract errors
    }
  }
}
```
