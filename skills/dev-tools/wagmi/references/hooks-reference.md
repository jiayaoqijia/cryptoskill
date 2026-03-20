# Wagmi Hooks Reference

Source: https://wagmi.sh/react/api/hooks

## Account Hooks

### useAccount

Get information about the connected account.

```tsx
import { useAccount } from "wagmi";

function Component() {
  const { address, isConnected, isConnecting, chain } = useAccount();

  if (!isConnected) return <div>Not connected</div>;
  return <div>Connected to {chain?.name} as {address}</div>;
}
```

### useBalance

Get the balance of an address.

```tsx
import { useBalance } from "wagmi";

function Balance({ address }: { address: `0x${string}` }) {
  const { data, isLoading } = useBalance({ address });

  if (isLoading) return <div>Loading...</div>;
  return <div>{data?.formatted} {data?.symbol}</div>;
}
```

## Connection Hooks

### useConnect

Connect to a wallet.

```tsx
import { useConnect } from "wagmi";
import { injected } from "wagmi/connectors";

function Connect() {
  const { connect, isPending, error } = useConnect();

  return (
    <button onClick={() => connect({ connector: injected() })}>
      {isPending ? "Connecting..." : "Connect"}
    </button>
  );
}
```

### useDisconnect

Disconnect the current wallet.

```tsx
import { useDisconnect } from "wagmi";

function Disconnect() {
  const { disconnect } = useDisconnect();
  return <button onClick={() => disconnect()}>Disconnect</button>;
}
```

### useConnectors

Get available connectors.

```tsx
import { useConnectors } from "wagmi";

function Connectors() {
  const connectors = useConnectors();
  return connectors.map((c) => <div key={c.uid}>{c.name}</div>);
}
```

## Contract Hooks

### useReadContract

Read data from a contract.

```tsx
import { useReadContract } from "wagmi";

function TokenName() {
  const { data, isLoading } = useReadContract({
    address: "0x...",
    abi: erc20Abi,
    functionName: "name",
  });

  return <div>{isLoading ? "Loading..." : data}</div>;
}
```

### useWriteContract

Write to a contract.

```tsx
import { useWriteContract } from "wagmi";

function Approve() {
  const { writeContract, isPending } = useWriteContract();

  return (
    <button
      onClick={() =>
        writeContract({
          address: "0x...",
          abi: erc20Abi,
          functionName: "approve",
          args: [spender, amount],
        })
      }
    >
      {isPending ? "Approving..." : "Approve"}
    </button>
  );
}
```

### useReadContracts

Batch multiple contract reads.

```tsx
import { useReadContracts } from "wagmi";

function MultipleReads() {
  const { data } = useReadContracts({
    contracts: [
      { address: "0x...", abi: erc20Abi, functionName: "name" },
      { address: "0x...", abi: erc20Abi, functionName: "symbol" },
    ],
  });

  return (
    <div>
      {data?.[0].result} ({data?.[1].result})
    </div>
  );
}
```

## Transaction Hooks

### useSendTransaction

Send a transaction.

```tsx
import { useSendTransaction } from "wagmi";
import { parseEther } from "viem";

function Send() {
  const { sendTransaction, isPending } = useSendTransaction();

  return (
    <button
      onClick={() =>
        sendTransaction({
          to: "0x...",
          value: parseEther("0.1"),
        })
      }
    >
      Send
    </button>
  );
}
```

### useWaitForTransactionReceipt

Wait for a transaction to be confirmed.

```tsx
import { useWaitForTransactionReceipt } from "wagmi";

function TxStatus({ hash }: { hash: `0x${string}` }) {
  const { isLoading, isSuccess } = useWaitForTransactionReceipt({ hash });

  if (isLoading) return <div>Confirming...</div>;
  if (isSuccess) return <div>Confirmed!</div>;
  return null;
}
```

## Network Hooks

### useChainId

Get the current chain ID.

```tsx
import { useChainId } from "wagmi";

function ChainId() {
  const chainId = useChainId();
  return <div>Chain ID: {chainId}</div>;
}
```

### useSwitchChain

Switch to a different chain.

```tsx
import { useSwitchChain } from "wagmi";

function SwitchNetwork() {
  const { switchChain, isPending } = useSwitchChain();

  return (
    <button onClick={() => switchChain({ chainId: 42220 })}>
      Switch to Celo
    </button>
  );
}
```

## Celo-Specific Configuration

### Custom RPC Endpoints

```typescript
import { http, createConfig } from "wagmi";
import { celo } from "wagmi/chains";

export const config = createConfig({
  chains: [celo],
  transports: {
    [celo.id]: http("https://forno.celo.org"),
  },
});
```

### Multiple Networks

```typescript
import { celo, celoSepolia } from "wagmi/chains";

export const config = createConfig({
  chains: [celo, celoSepolia],
  transports: {
    [celo.id]: http(),
    [celoSepolia.id]: http(),
  },
});
```
