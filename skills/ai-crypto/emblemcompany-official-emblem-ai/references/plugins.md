# Custom Plugins

Extend EmblemAI with your own tools and logic.

## Plugin Structure

```typescript
interface Plugin {
  name: string;           // Unique plugin identifier
  version: string;        // Semantic version
  tools: Tool[];          // Tool definitions
  executors: Executors;   // Tool implementations
  hooks?: Hooks;          // Lifecycle hooks (optional)
}
```

## Creating a Plugin

### Basic Plugin

```typescript
const weatherPlugin = {
  name: 'weather',
  version: '1.0.0',
  tools: [{
    name: 'get_weather',
    description: 'Get current weather for a city',
    parameters: {
      type: 'object',
      properties: {
        city: {
          type: 'string',
          description: 'City name'
        },
        units: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          default: 'celsius'
        }
      },
      required: ['city']
    }
  }],
  executors: {
    get_weather: async ({ city, units }) => {
      const data = await fetchWeatherAPI(city);
      const temp = units === 'fahrenheit'
        ? data.temp * 9/5 + 32
        : data.temp;

      return {
        city: data.city,
        temperature: temp,
        units,
        conditions: data.conditions,
        humidity: data.humidity
      };
    }
  }
};
```

### Registering Plugins

**With hustle-incognito (legacy package name):**

```typescript
import { HustleIncognito } from 'hustle-incognito';

const client = new HustleIncognito({
  getAuthHeaders: async () => buildTrustedBackendHeaders()
});
client.use(weatherPlugin);

// Now EmblemAI can use get_weather
const response = await client.chat([
  { role: 'user', content: 'What is the weather in Tokyo?' }
]);
```

**With hustle-react (legacy package name):**

```tsx
import { useHustle } from '@emblemvault/hustle-react';

function MyComponent() {
  const { registerPlugin } = useHustle();

  useEffect(() => {
    registerPlugin(weatherPlugin);
  }, []);
}
```

## Tool Definition Schema

```typescript
interface Tool {
  name: string;           // Tool function name
  description: string;    // What the tool does (shown to AI)
  parameters: {
    type: 'object';
    properties: {
      [key: string]: {
        type: 'string' | 'number' | 'boolean' | 'array' | 'object';
        description?: string;
        enum?: string[];          // Allowed values
        default?: any;            // Default value
        items?: object;           // For arrays
        properties?: object;      // For nested objects
      };
    };
    required?: string[];  // Required parameters
  };
}
```

## Executor Functions

Executors receive EmblemAI's parameters and return results:

```typescript
executors: {
  tool_name: async (params) => {
    // params contains all arguments from EmblemAI

    // Do your logic
    const result = await someOperation(params);

    // Return data for EmblemAI
    return {
      success: true,
      data: result
    };
  }
}
```

### Error Handling

```typescript
executors: {
  risky_operation: async (params) => {
    try {
      const result = await dangerousOperation(params);
      return { success: true, data: result };
    } catch (error) {
      // Return error info to EmblemAI
      return {
        success: false,
        error: error.message,
        code: error.code
      };
    }
  }
}
```

### Async Operations

```typescript
executors: {
  slow_operation: async (params) => {
    // Long-running operations are fine
    const result = await longRunningTask(params);
    return result;
  }
}
```

## Lifecycle Hooks

Intercept and modify requests/responses:

```typescript
const loggingPlugin = {
  name: 'logging',
  version: '1.0.0',
  tools: [],
  executors: {},
  hooks: {
    // Before request is sent
    beforeRequest: async (messages) => {
      console.log('Sending:', messages.length, 'messages');
      return messages;  // Return (possibly modified) messages
    },

    // After response received
    afterResponse: async (response) => {
      console.log('Received:', response.content.length, 'chars');
      return response;  // Return (possibly modified) response
    },

    // On any error
    onError: async (error) => {
      console.error('Error:', error);
      // Optionally return recovery value
      return null;
    }
  }
};
```

### Hook Use Cases

**PII Protection:**

```typescript
hooks: {
  beforeRequest: async (messages) => {
    return messages.map(m => ({
      ...m,
      content: redactPII(m.content)
    }));
  }
}
```

**Response Caching:**

```typescript
hooks: {
  beforeRequest: async (messages) => {
    const cached = await cache.get(hash(messages));
    if (cached) throw { cached };  // Skip API call
    return messages;
  },
  afterResponse: async (response, messages) => {
    await cache.set(hash(messages), response);
    return response;
  }
}
```

**Analytics:**

```typescript
hooks: {
  afterResponse: async (response) => {
    await analytics.track('ai_response', {
      tokens: response.usage?.totalTokens,
      tools: response.toolCalls?.length
    });
    return response;
  }
}
```

## Multiple Plugins

```typescript
// Register multiple plugins
client.use(weatherPlugin);
client.use(stockPlugin);
client.use(newsPlugin);

// They can all be used in the same conversation
const response = await client.chat([
  { role: 'user', content: 'Weather in NYC, AAPL stock, and tech news' }
]);
// AI may call get_weather, get_stock_price, and get_news
```

## Plugin Priority

Plugins are processed in registration order. If multiple plugins define the same tool name, the first registered wins.

```typescript
client.use(pluginA);  // pluginA.get_data will be used
client.use(pluginB);  // pluginB.get_data is ignored (duplicate)
```

## Unregistering Plugins

**hustle-incognito (legacy package name):**

```typescript
client.unuse('weather');  // Remove by name
```

**hustle-react (legacy package name):**

```tsx
const { unregisterPlugin } = useHustle();
unregisterPlugin('weather');
```

## Example: NFT Plugin

```typescript
const nftPlugin = {
  name: 'custom-nft',
  version: '1.0.0',
  tools: [
    {
      name: 'get_collection_stats',
      description: 'Get detailed stats for an NFT collection',
      parameters: {
        type: 'object',
        properties: {
          collection: {
            type: 'string',
            description: 'Collection name or contract address'
          },
          chain: {
            type: 'string',
            enum: ['ethereum', 'base', 'polygon'],
            default: 'ethereum'
          }
        },
        required: ['collection']
      }
    },
    {
      name: 'find_rare_nfts',
      description: 'Find rare NFTs below floor price',
      parameters: {
        type: 'object',
        properties: {
          collection: { type: 'string' },
          maxPrice: { type: 'number', description: 'Max price in ETH' },
          minRarity: { type: 'number', description: 'Min rarity rank' }
        },
        required: ['collection']
      }
    }
  ],
  executors: {
    get_collection_stats: async ({ collection, chain }) => {
      const stats = await nftAPI.getStats(collection, chain);
      return {
        name: stats.name,
        floor: stats.floorPrice,
        volume24h: stats.volume24h,
        holders: stats.numOwners,
        listed: stats.listedCount,
        avgPrice: stats.avgPrice7d
      };
    },
    find_rare_nfts: async ({ collection, maxPrice, minRarity }) => {
      const listings = await nftAPI.getListings(collection, {
        maxPrice,
        minRarity
      });
      return {
        found: listings.length,
        items: listings.slice(0, 5).map(l => ({
          tokenId: l.tokenId,
          price: l.price,
          rarity: l.rarityRank
        }))
      };
    }
  }
};
```

## TypeScript Types

```typescript
import type {
  Plugin,
  Tool,
  Executors,
  Hooks,
  ToolResult
} from 'hustle-incognito';

// Type-safe executor
const executors: Executors = {
  my_tool: async (params: { city: string }): Promise<ToolResult> => {
    return { success: true, data: {} };
  }
};
```
