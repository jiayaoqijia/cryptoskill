# React Components Reference

Current component map for `@emblemvault/emblem-auth-react` and the EmblemAI chat package `@emblemvault/hustle-react`.

## Authentication Components

### `ConnectButton` (`@emblemvault/emblem-auth-react`)

```tsx
<ConnectButton
  showVaultInfo
  connectLabel="Connect"
  loadingLabel="Connecting..."
  onConnect={() => {}}
  onDisconnect={() => {}}
/>
```

Props: `showVaultInfo` (default `true`), `connectLabel`, `loadingLabel`, `className`, `style`, `disabled`, `onConnect`, `onDisconnect`.

### `AuthStatus` (`@emblemvault/emblem-auth-react`)

```tsx
<AuthStatus showVaultInfo showLogout />
```

Props: `showVaultInfo`, `showLogout`, `className`, `style`.

## AI Chat Components

### `HustleChat` (`@emblemvault/hustle-react`)

```tsx
<HustleChat
  placeholder="Ask anything..."
  showSettings
  showDebug
  hideHeader
  initialSystemPrompt="You are a helpful crypto assistant."
  enableSpeechToText
  onMessage={(msg) => {}}
  onToolCall={(call) => {}}
  onResponse={(content) => {}}
/>
```

Props: `className`, `placeholder`, `showSettings`, `settingsPanelOpen`, `onSettingsPanelOpenChange`, `showDebug`, `hideHeader`, `initialSystemPrompt`, `enableSpeechToText`, `onMessage`, `onToolCall`, `onResponse`.

### `HustleChatWidget` (`@emblemvault/hustle-react`)

```tsx
<HustleChatWidget
  config={{ position: 'bottom-right', size: 'md', defaultOpen: false }}
  showSettings
/>
```

`HustleChatWidget` accepts widget `config` plus `HustleChat` props for the EmblemAI chat UI.

## Provider Components

### `EmblemAuthProvider`

```tsx
<EmblemAuthProvider
  appId="your-app-id"
  authUrl="https://auth.emblemvault.ai"
  apiUrl="https://api.emblemvault.ai"
  debug={false}
>
  {children}
</EmblemAuthProvider>
```

### `HustleProvider` (legacy provider name)

```tsx
<HustleProvider
  hustleApiUrl={import.meta.env.VITE_HUSTLE_API_URL}
  debug={false}
  instanceId="main"
>
  {children}
</HustleProvider>
```

Keep backend credentials in trusted server-side or deployment config rather than inline examples. Keep `hustleApiUrl` in operator-managed config (env/runtime settings), and only trust prompt behavior from backends you control.
