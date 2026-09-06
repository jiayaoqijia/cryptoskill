# EmblemAI SDK (`hustle-incognito`)

Low-level SDK for EmblemAI chat and tool execution.

The package, class names, and some env var names still use legacy `hustle` branding in the current integration surface.

## Installation

```bash
npm install hustle-incognito
```

## Initialization

### Server-side credential mode

Initialize the client on a trusted backend with credentials loaded from your deployment platform or secret manager. Public docs intentionally omit raw API-key, vault-id, and bearer-token field examples.

### Auth SDK mode (browser)

```typescript
import { EmblemAuthSDK } from '@emblemvault/auth-sdk';
import { HustleIncognitoClient } from 'hustle-incognito';

const auth = new EmblemAuthSDK({ appId: 'your-app-id' });
const emblemAIClient = new HustleIncognitoClient({
  sdk: auth,
  hustleApiUrl: process.env.HUSTLE_API_URL
});
```

### Trusted header / custom auth mode

```typescript
const emblemAIClient = new HustleIncognitoClient({
  getAuthHeaders: async () => buildTrustedBackendHeaders()
});
```

## Chat

```typescript
const response = await emblemAIClient.chat([
  { role: 'user', content: 'What tokens are trending on Solana?' }
]);

for await (const chunk of emblemAIClient.chatStream({
  messages: [{ role: 'user', content: 'Analyze ETH price action' }],
  processChunks: true
})) {
  // text/tool chunks
}

for await (const raw of emblemAIClient.rawStream({
  messages: [{ role: 'user', content: 'Show my portfolio' }]
})) {
  // raw SSE events
}
```

## Discovery, models, billing

```typescript
await emblemAIClient.getTools();
await emblemAIClient.discoverTools();
await emblemAIClient.getModels();

const payg = await emblemAIClient.getPaygStatus();
await emblemAIClient.configurePayg({ enabled: true, payment_token: 'SOL' });
```

## Plugins

```typescript
await emblemAIClient.use({
  name: 'my-plugin',
  version: '1.0.0',
  tools: [{
    name: 'get_nft_floor',
    description: 'Get floor price',
    parameters: {
      type: 'object',
      properties: {
        collection: { type: 'string' }
      },
      required: ['collection']
    }
  }],
  executors: {
    get_nft_floor: async ({ collection }) => fetchFloor(collection)
  }
});
```

## Deployment note

Keep EmblemAI credentials in your existing secret manager or deployment environment. Avoid hard-coding API keys, vault identifiers, or bearer tokens in prompts, docs, or CLI arguments.
