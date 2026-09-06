# React Hooks & Patterns

Source: https://sdk.mystenlabs.com/dapp-kit/getting-started/react

## Current hook inventory (v2 dApp Kit)

| Hook | Returns | Use for |
|---|---|---|
| `useCurrentAccount()` | `UiWalletAccount \| null` | Connected address; null-check always required |
| `useCurrentWallet()` | `UiWallet \| null` | Connected wallet (name, icon, accounts list) |
| `useWalletConnection()` | `{ status, wallet, account, ... }` | Full connection state incl. `connecting` / `reconnecting` |
| `useCurrentNetwork()` | `string` (e.g. `'testnet'`) — not a tuple | Read current network |
| `useCurrentClient()` | `SuiGrpcClient` for current network | Passing to TanStack Query / imperative calls |
| `useDAppKit()` | the dApp Kit instance | Imperative actions: `signAndExecuteTransaction`, `connectWallet`, `switchNetwork`, etc. |
| `useWallets()` | `UiWallet[]` | List detected wallets (custom wallet menu) |

All of these pick up the typed instance automatically when the `declare module` augmentation is in place.

## Removed hooks (do not use)

| Removed | Replacement |
|---|---|
| `useSuiClient()` | `useCurrentClient()` |
| `useSuiClientContext()` | `useCurrentNetwork()` (read) + `useDAppKit().switchNetwork(n)` (write) |
| `useSuiClientQuery()` | `useCurrentClient()` + `useQuery()` (see `queries.md`) |
| `useSuiClientInfiniteQuery()` | `useCurrentClient()` + `useInfiniteQuery()` |
| `useSignAndExecuteTransaction()` (mutation hook) | `useDAppKit().signAndExecuteTransaction({ transaction })` |
| `useSignTransaction()` (mutation hook) | `useDAppKit().signTransaction({ transaction })` |
| `useSignPersonalMessage()` (mutation hook) | `useDAppKit().signPersonalMessage({ message })` |
| `useConnectWallet()` | `useDAppKit().connectWallet({ wallet })` |
| `useDisconnectWallet()` | `useDAppKit().disconnectWallet()` |

If a tutorial or tool recommends any of the removed hooks, it's out of date.

## `ConnectButton`

**`ConnectButton` is exported from `@mysten/dapp-kit-react/ui`**, not from the main `@mysten/dapp-kit-react` entry point. This is the most common import mistake — using the wrong path causes a silent white screen with no error.

```tsx
// ✅ Correct import
import { ConnectButton } from '@mysten/dapp-kit-react/ui';

// ❌ Wrong — ConnectButton is NOT exported from the main entry
import { ConnectButton } from '@mysten/dapp-kit-react';

<ConnectButton />

// With filtering
<ConnectButton
  modalOptions={{
    filterFn: (wallet) => wallet.name !== 'ExcludedWallet',
    sortFn: (a, b) => a.name.localeCompare(b.name),
  }}
/>
```

`ConnectModal` is also exported from `@mysten/dapp-kit-react/ui`.

Wallet detection is browser-only. In SSR frameworks, ensure this renders client-side (`'use client'` in Next.js).

## Custom wallet menu

```tsx
import { useWallets, useDAppKit, useCurrentWallet } from '@mysten/dapp-kit-react';

function WalletMenu() {
  const wallets = useWallets();
  const dAppKit = useDAppKit();
  const current = useCurrentWallet();

  if (current) {
    return (
      <div>
        <p>Connected: {current.name}</p>
        <button onClick={() => dAppKit.disconnectWallet()}>Disconnect</button>
      </div>
    );
  }

  return (
    <div>
      {wallets.map((wallet) => (
        <button key={wallet.name} onClick={() => dAppKit.connectWallet({ wallet })}>
          {wallet.name}
        </button>
      ))}
    </div>
  );
}
```

## Connection state for UX

`useWalletConnection` exposes the full state machine:

```tsx
import { useWalletConnection } from '@mysten/dapp-kit-react';

function Status() {
  const { status, wallet, account } = useWalletConnection();
  // status: 'disconnected' | 'connecting' | 'reconnecting' | 'connected'

  if (status === 'reconnecting') return <Spinner label="Reconnecting..." />;
  if (status === 'connecting')  return <Spinner label="Connecting..." />;
  if (status === 'connected')   return <p>{wallet?.name}: {account?.address}</p>;
  return <ConnectButton />;
}
```

`reconnecting` fires on page reload when `autoConnect: true` is restoring the last wallet. Design for it — don't treat it as `disconnected`.

## Accessing the client

```tsx
import { useCurrentClient } from '@mysten/dapp-kit-react';

function Component() {
  const client = useCurrentClient();
  // SuiGrpcClient for the current network; auto-updates on switchNetwork
}
```

Never `new SuiGrpcClient(...)` inside a component — you'd lose network switching and duplicate connections.

## Wallet-gated UI

```tsx
import { useCurrentAccount } from '@mysten/dapp-kit-react';
import { ConnectButton } from '@mysten/dapp-kit-react/ui';

function ProtectedFeature() {
  const account = useCurrentAccount();
  if (!account) {
    return (
      <div>
        <p>Connect your wallet to continue.</p>
        <ConnectButton />
      </div>
    );
  }
  return <Feature address={account.address} />;
}
```

Reusable guard:

```tsx
function WalletGuard({ children }: { children: React.ReactNode }) {
  const account = useCurrentAccount();
  if (!account) return <ConnectButton />;
  return <>{children}</>;
}
```

## Network switching

```tsx
import { useCurrentNetwork, useDAppKit } from '@mysten/dapp-kit-react';

function NetworkSwitcher() {
  const network = useCurrentNetwork();
  const dAppKit = useDAppKit();

  return (
    <select value={network} onChange={(e) => dAppKit.switchNetwork(e.target.value)}>
      <option value="mainnet">Mainnet</option>
      <option value="testnet">Testnet</option>
    </select>
  );
}
```

Only networks included in `createDAppKit`'s `networks` array are valid. `switchNetwork` updates the dApp's active client — it does not ask the wallet to switch.

## Account details

```tsx
const account = useCurrentAccount();       // UiWalletAccount | null
// account.address, account.label, account.chains, account.features
```

Always null-check:
```tsx
if (!account) return <ConnectButton />;
```

## Patterns to avoid

- **Nested providers**: one `DAppKitProvider` only.
- **Duplicate `createDAppKit`** calls: create the instance once in a module file, import everywhere.
- **Accessing `window.navigator.wallets` directly**: use `useWallets()`.
- **Reaching into the wallet's internals**: if a feature isn't exposed on the dApp Kit API, open an issue or fall back to `wallet.features['<name>']` — but this is rare.
- **Using any removed hook**.
