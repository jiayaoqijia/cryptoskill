# EmblemAI developer tools

EmblemAI developer tools for one-shot user management, multi-chain wallet authentication, AI chat surfaces, and developer observability workflows.

With Emblem, you get the easiest way to add user management for wallet-native apps without juggling separate auth and wallet stacks. Users can sign in with wallets, email/password, or social login, then continue into chat, plugin, or Reflexive experiences. Wallet/CLI-first workflows are documented in the dedicated agent-wallet skill so this core skill can stay focused on auth, UI, and introspection.

Legacy package names such as `@emblemvault/hustle-react` and `hustle-incognito` are preserved below until the underlying npm surfaces are renamed.

## Features

- **One-shot User Management**: create website users who also have wallet-enabled profiles
- **Flexible Login Options**: wallets, email/password, Google, Twitter/X
- **Wallet Authentication**: Ethereum, Solana, Bitcoin, Hedera
- **AI Chat & Plugins**: Embed EmblemAI chat surfaces and connect your own tools with approval prompts
- **React Components**: Pre-built UI for rapid development
- **Reflexive Observability**: AI-powered app introspection for debugging and operations

## Quick Start

See [SKILL.md](./SKILL.md) for full documentation.

### React App

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

If you want to integrate EmblemAI into your own React app, see the dedicated [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) skill for the React-specific examples and references.

### Need CLI or wallet-first automations?

Use [../emblem-ai-agent-wallet/SKILL.md](../emblem-ai-agent-wallet/SKILL.md) plus [skills/emblem-ai/references/agentwallet.md](./references/agentwallet.md) whenever the user needs the Agent Wallet CLI, credential bootstrap guidance, or automation recipes.

## Documentation

- [SKILL.md](./SKILL.md) - Main documentation
- [references/](./references/) - Detailed API references
  - [agentwallet.md](./references/agentwallet.md) - CLI for AI agents
  - [auth-sdk.md](./references/auth-sdk.md) - Authentication SDK
  - [auth-react.md](./references/auth-react.md) - React auth hooks
  - [emblem-ai-react.md](./references/emblem-ai-react.md) - React EmblemAI chat
  - [emblem-ai-incognito.md](./references/emblem-ai-incognito.md) - EmblemAI SDK
  - [plugins.md](./references/plugins.md) - Plugin integrations
  - [react-components.md](./references/react-components.md) - Component reference
  - [react-skill-proposal.md](./references/react-skill-proposal.md) - Proposed React scope adjustments
  - [reflexive.md](./references/reflexive.md) - AI app introspection
- [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md) - React-only view with migrate.fun hooks
- [../emblem-ai-agent-wallet/SKILL.md](../emblem-ai-agent-wallet/SKILL.md) - Dedicated Agent Wallet CLI skill
- [../emblem-ai-prompt-examples/SKILL.md](../emblem-ai-prompt-examples/SKILL.md) - Standalone EmblemAI prompt catalog shared across skills

For a React-only install surface, use [../emblem-ai-react/SKILL.md](../emblem-ai-react/SKILL.md).

## Packages

| Package | Description |
|---------|-------------|
| `@emblemvault/agentwallet` | CLI for AI agent wallet management (see ../emblem-ai-agent-wallet/SKILL.md) |
| `@emblemvault/auth-sdk` | Core authentication SDK |
| `@emblemvault/emblem-auth-react` | React hooks and components for auth |
| `@emblemvault/hustle-react` | React EmblemAI chat components |
| `@emblemvault/migratefun-react` | React migrate.fun hooks (see ../emblem-ai-react/SKILL.md) |
| `hustle-incognito` | Low-level EmblemAI SDK |
| `reflexive` | AI app introspection and debugging |
