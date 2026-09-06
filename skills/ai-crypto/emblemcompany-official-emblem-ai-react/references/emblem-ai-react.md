# EmblemAI React Chat (`@emblemvault/hustle-react`)

React provider, hooks, and UI components for EmblemAI chat.

The package and exported symbol names still use legacy `hustle` branding in the current integration surface.

## Installation

```bash
npm install @emblemvault/hustle-react @emblemvault/emblem-auth-react
```

## Setup

```tsx
import { EmblemAuthProvider } from '@emblemvault/emblem-auth-react';
import { HustleProvider } from '@emblemvault/hustle-react';

function App() {
  return (
    <EmblemAuthProvider appId="your-app-id">
      <HustleProvider
        hustleApiUrl={import.meta.env.VITE_HUSTLE_API_URL}
        debug={false}
        instanceId="main"
      >
        {children}
      </HustleProvider>
    </EmblemAuthProvider>
  );
}
```

Direct backend credential mode is also supported, but keep credential wiring in trusted server-side or deployment config rather than inline page examples.
Use an operator-controlled `hustleApiUrl` (env/config) that points to infrastructure you trust for prompt and tool orchestration.

## Hook: `useHustle()` (legacy hook name)

```tsx
const {
  instanceId,
  isApiKeyMode,
  isReady,
  isLoading,
  error,
  models,
  client,
  chat,
  chatStream,
  uploadFile,
  loadModels,
  selectedModel,
  setSelectedModel,
} = useHustle();
```

Prompt policy and backend defaults should be managed inside trusted app/server configuration rather than inline examples on public docs pages.

## Hook: `usePlugins()`

Plugin registration is managed by `usePlugins`, not `useHustle`.

```tsx
import { usePlugins } from '@emblemvault/hustle-react';

const { plugins, enabledPlugins, registerPlugin, unregisterPlugin, enablePlugin, disablePlugin } = usePlugins();
```

## `HustleChat` props

```tsx
<HustleChat
  placeholder="Ask about crypto..."
  showSettings
  showDebug
  hideHeader={false}
  enableSpeechToText
  onMessage={(message) => {}}
  onToolCall={(toolCall) => {}}
  onResponse={(content) => {}}
/>
```

Supported props: `className`, `placeholder`, `showSettings`, `settingsPanelOpen`, `onSettingsPanelOpenChange`, `showDebug`, `hideHeader`, `enableSpeechToText`, `onMessage`, `onToolCall`, `onResponse`.

## `HustleChatWidget`

```tsx
<HustleChatWidget showSettings placeholder="How can I help?" />
```

Widget accepts a `config` object (position/size/title/offset, etc.) and passes through `HustleChat` props.
