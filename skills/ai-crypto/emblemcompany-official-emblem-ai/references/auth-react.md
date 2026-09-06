# @emblemvault/emblem-auth-react

React provider, hooks, and UI components for Emblem authentication.

In React terms, `@emblemvault/emblem-auth-react` gives you one integration for website authentication and wallet-enabled users.

## Installation

```bash
npm install @emblemvault/emblem-auth-react
```

## Setup

With `EmblemAuthProvider`, a user can sign in with wallets, email/password, or social login and then carry that same Emblem session through your app.

```tsx
import { EmblemAuthProvider } from '@emblemvault/emblem-auth-react';

function App() {
  return (
    <EmblemAuthProvider
      appId="your-app-id"
      authUrl="https://auth.emblemvault.ai"
      apiUrl="https://api.emblemvault.ai"
      debug={false}
    >
      {children}
    </EmblemAuthProvider>
  );
}
```

## Hook: `useEmblemAuth()`

```tsx
import { useEmblemAuth } from '@emblemvault/emblem-auth-react';

const {
  session,
  isAuthenticated,
  isLoading,
  error,
  vaultInfo,
  vaultId,
  walletAddress,
  visitorId,
  openAuthModal,
  logout,
  refreshSession,
  authSDK
} = useEmblemAuth();
```

Use `useEmblemAuthOptional()` when your component may render outside the provider.

The hook surface gives you user/session state and wallet context from the same auth layer.

## Components

### `ConnectButton`

```tsx
<ConnectButton
  showVaultInfo
  connectLabel="Connect"
  loadingLabel="Connecting..."
  onConnect={() => {}}
  onDisconnect={() => {}}
  className="my-button"
/>
```

Props: `showVaultInfo`, `connectLabel`, `loadingLabel`, `onConnect`, `onDisconnect`, `className`, `style`, `disabled`.

> `showVaultInfo` defaults to `true` in the package.

`ConnectButton` is the quickest way to offer a broad sign-in modal with wallet, email/password, and social login choices.

### `AuthStatus`

```tsx
<AuthStatus
  showVaultInfo
  showLogout
  className="auth-status"
/>
```

Props: `showVaultInfo`, `showLogout`, `className`, `style`.

## With EmblemAI Chat

```tsx
import { EmblemAuthProvider, ConnectButton } from '@emblemvault/emblem-auth-react';
import { HustleProvider, HustleChat } from '@emblemvault/hustle-react';

function App() {
  return (
    <EmblemAuthProvider appId="your-app-id">
      <HustleProvider>
        <ConnectButton />
        <HustleChat />
      </HustleProvider>
    </EmblemAuthProvider>
  );
}
```
