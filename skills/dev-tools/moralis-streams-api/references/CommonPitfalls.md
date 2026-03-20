# Common Pitfalls Reference

Complete reference for common mistakes, bugs, and gotchas when working with Moralis Streams API.

## Table of Contents

- [HTTP Method Confusion](#http-method-confusion)
- [Stream Configuration Gotchas](#stream-configuration-gotchas)
- [Response Structure Variations](#response-structure-variations)
- [Webhook Payload Fields](#webhook-payload-fields)
- [Other Common Issues](#other-common-issues)
- [Error Messages and Causes](#error-messages-and-causes)
- [Debugging Tips](#debugging-tips)
- [Prevention Checklist](#prevention-checklist)

---

## HTTP Method Confusion

The Streams API uses different HTTP methods than typical REST APIs:

### Method Reference Table

| Action | HTTP Method | Endpoint | Example |
|--------|-------------|----------|-----------|
| Create stream | `PUT` | `/streams/evm` | Create a new stream |
| Update stream | `POST` | `/streams/evm/{id}` | Update existing stream |
| Delete stream | `DELETE` | `/streams/evm/{id}` | Delete a stream |
| Get streams | `GET` | `/streams/evm` | List all streams |
| Get stream | `GET` | `/streams/evm/{id}` | Get specific stream |
| Add address | `POST` | `/streams/evm/{id}/address` | Add addresses to stream |
| Delete address | `DELETE` | `/streams/evm/{id}/address/{address}` | Remove address |
| Pause/Resume | `POST` | `/streams/evm/{id}/status` | Update stream status |

### Common Mistake: Using POST to Create Streams

```typescript
// ❌ WRONG - Using POST
const stream = await fetch('/streams/evm', {
  method: 'POST',
  body: JSON.stringify({ webhookUrl: 'https://...' })
});

// ✅ CORRECT - Using PUT
const stream = await fetch('/streams/evm', {
  method: 'PUT',
  body: JSON.stringify({ webhookUrl: 'https://...' })
});
```

**Why PUT for create?**
The Streams API uses RESTful conventions where:
- `PUT` creates a new resource at a specific endpoint
- `POST` updates an existing resource by ID

### Common Implementation Errors

```typescript
// ❌ WRONG - Wrong method for stream creation
const response = await axios.post('/streams/evm', config);

// ❌ WRONG - Wrong method for stream update
const response = await axios.put(`/streams/evm/${streamId}`, config);

// ✅ CORRECT - Using axios with proper methods
import axios from 'axios';

const stream = await axios.put('/streams/evm', config);
const updated = await axios.post(`/streams/evm/${streamId}`, config);
const deleted = await axios.delete(`/streams/evm/${streamId}`);
```

## Stream Configuration Gotchas

When creating streams, always check the rule file for required fields.

### Wrong Base URL

```typescript
// ❌ WRONG - Using Data API base URL
const STREAMS_URL = 'https://deep-index.moralis.io';

// ✅ CORRECT - Using Streams API base URL
const STREAMS_URL = 'https://api.moralis-streams.com';
```

**Impact:** Using wrong base URL causes 404 errors for all endpoints.

### Missing Required Limit Parameter

```typescript
// ❌ WRONG - Missing limit parameter (required for GET /streams/evm)
const streams = await fetch('/streams/evm');

// ✅ CORRECT - Including limit parameter (max 100)
const streams = await fetch('/streams/evm?limit=100');
```

**Error message:** `"limit parameter is required"`

### Wrong Stream ID Format

```typescript
// ❌ WRONG - Using hex format for stream ID
const streamId = '0x1234567890abcdef';
await fetch(`/streams/evm/${streamId}`);

// ✅ CORRECT - Using UUID format
const streamId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
await fetch(`/streams/evm/${streamId}`);
```

**Error message:** `"Invalid stream ID format"`

### Invalid Chain ID Format

```typescript
// ❌ WRONG - Using string names for chain IDs
const config = {
  chainIds: ['eth', 'polygon', 'bsc']  // Wrong!
};

// ✅ CORRECT - Using hex format
const config = {
  chainIds: ['0x1', '0x89', '0x38']  // Correct!
};
```

**Impact:** Streams will not monitor the specified chains.

### Incorrect Topic0 Format

```typescript
// ❌ WRONG - Missing parameter types
const config = {
  topic0: ['Transfer', 'Approval']  // Wrong!
};

// ✅ CORRECT - Full event signature with types
const config = {
  topic0: ['Transfer(address,address,uint256)', 'Approval(address,address,uint256)']
};
```

**Impact:** Stream won't filter for the correct events.

## Response Structure Variations

Different endpoints return different structures. Always check the rule file.

### GetStreams Response

```typescript
// Returns array wrapped in result
{
  result: [
    {
      id: "a1b2c3d4-...",
      webhookUrl: "https://...",
      status: "active"
    },
    // ... more streams
  ]
}

// ❌ WRONG - Assuming direct array
const streams = await fetch('/streams/evm');
streams.forEach(stream => ...); // Error: streams.forEach is not a function

// ✅ CORRECT - Access result array
const { result: streams } = await fetch('/streams/evm');
streams.forEach(stream => ...);
```

### GetStream Response

```typescript
// Returns wrapped object with stream key
{
  stream: {
    id: "a1b2c3d4-...",
    webhookUrl: "https://...",
    description: "...",
    // ... other stream fields
  }
}

// ❌ WRONG - Assuming result wrapper
const { result: stream } = await fetch(`/streams/evm/${id}`);

// ✅ CORRECT - Access stream property
const { stream } = await fetch(`/streams/evm/${id}`);
```

### GetStats Response

```typescript
// Returns flat object with stats
{
  totalStreams: 5,
  activeStreams: 3,
  pausedStreams: 2
}

// ❌ WRONG - Assuming result wrapper
const { result: stats } = await fetch('/streams/evm/stats');

// ✅ CORRECT - Direct access to stats
const stats = await fetch('/streams/evm/stats');
```

### Universal Safe Access Pattern

```typescript
// Safe access function that handles all response types
async function safeFetch<T = any>(endpoint: string): Promise<T> {
  const response = await fetch(endpoint);

  if (response.result && Array.isArray(response.result)) {
    return response.result;
  } else if (response.stream) {
    return response.stream;
  } else if (response.totalStreams) {
    return response;
  }

  return response as unknown as T;
}
```

## Webhook Payload Fields

Webhook payloads have different field names than API responses.

### Field Name Differences

| API Response | Webhook Payload | Example |
| --------------- | ---------------- | --------- |
| `method` | `method_label` | Transaction history webhooks |
| `sync_at` | `synced_at` | NFT metadata webhooks |
| `chain` (decimal) | `chainId` (hex) | Some endpoints |

### Webhook Payload Structure

```typescript
// Example transaction webhook
{
  "txs": [
    {
      "method_label": "erc20transfer",  // Not 'method'!
      "chainId": "0x1",            // Hex string
      "hash": "0x...",
      "from": "0x...",
      "to": "0x...",
      "value": "1000000000000000000"
    }
  ]
}

// ⚠️ Important: Handle method_label, not method
txs.forEach(tx => {
  console.log(tx.method_label);  // Correct!
  // console.log(tx.method);     // Undefined!
});
```

### Webhook Signature Verification

```typescript
// Webhooks include x-signature header
const signature = req.headers['x-signature'];

// Verify signature
const body = JSON.stringify(req.body);
const expectedSignature = web3.utils.sha3(body + secret);

if (signature !== expectedSignature) {
  throw new Error('Invalid webhook signature');
}
```

## Other Common Issues

### All Addresses Resource Usage

```typescript
// ❌ DANGEROUS - Monitors ALL addresses on specified chains
const config = {
  allAddresses: true,
  chainIds: ['0x1', '0x89']  // All addresses on Ethereum and Polygon!
};

// ✅ CORRECT - Monitor only specific addresses
const config = {
  allAddresses: false,
  // Add addresses via AddAddressToStream endpoint
};
```

**Impact:** Can exhaust your compute quota quickly. Only use when you truly need to monitor all addresses.

### Advanced Options Required

Some features require advanced options configuration:

```typescript
// ❌ WRONG - Trying to include native hash directly
const config = {
  includeNativeHash: true  // This field doesn't exist at top level!
};

// ✅ CORRECT - Using advanced options
const config = {
  advancedOptions: [
    {
      topic0: "Transfer(address,address,uint256)",
      includeNativeHash: true  // Correct!
    }
  ]
};
```

### Status Value Case Sensitivity

```typescript
// ❌ WRONG - Using uppercase
const response = await fetch(`/streams/evm/${id}/status`, {
  method: 'POST',
  body: JSON.stringify({ status: 'ACTIVE' })  // Wrong!
});

// ✅ CORRECT - Using lowercase
const response = await fetch(`/streams/evm/${id}/status`, {
  method: 'POST',
  body: JSON.stringify({ status: 'active' })  // Correct!
});
```

**Valid status values:** `active`, `paused`

### Missing Webhook URL

```typescript
// ❌ WRONG - Creating stream without webhook
const config = {
  description: "My stream",
  topic0: ["Transfer(address,address,uint256)"]
};

// ✅ CORRECT - Including webhook URL
const config = {
  description: "My stream",
  webhookUrl: "https://your-server.com/webhook",  // Required!
  topic0: ["Transfer(address,address,uint256)"]
};
```

**Impact:** Stream is created but won't send any webhooks.

### Webhook URL Not Publicly Accessible

```typescript
// ❌ PROBLEM - Webhook URL is localhost or private IP
const config = {
  webhookUrl: "http://localhost:3000/webhook"
};

// ✅ CORRECT - Use publicly accessible HTTPS endpoint
const config = {
  webhookUrl: "https://your-domain.com/webhook"
};
```

**Impact:** Moralis can't deliver webhooks to your server.

## Error Messages and Causes

| Error Message | Likely Cause | Solution |
| ------------- | -------------- | ---------- |
| "limit parameter is required" | Missing limit in GET /streams/evm | Add `?limit=100` to request |
| "Invalid stream ID format" | Using hex instead of UUID | Use UUID format: `a1b2c3d4-...` |
| "Invalid chain ID" | Using string name instead of hex | Use hex: `0x1`, `0x89`, etc. |
| "Invalid topic0 format" | Missing event signature types | Use full signature: `Transfer(address,address,uint256)` |
| "webhookUrl is required" | Missing webhook URL in create stream | Include `webhookUrl` field |
| "Stream not found" | Wrong stream ID or already deleted | Verify stream ID exists |
| "Method not allowed" | Wrong HTTP method | Check method: PUT for create, POST for update |

## Debugging Tips

### Logging Stream Configuration

```typescript
function logStreamConfig(config: any): void {
  console.log('Creating stream with config:', JSON.stringify(config, null, 2));

  // Validate critical fields
  if (!config.webhookUrl) {
    console.error('❌ Missing webhookUrl');
  }
  if (!config.chainIds || config.chainIds.length === 0) {
    console.error('❌ No chain IDs specified');
  }
  if (!config.topic0 || config.topic0.length === 0) {
    console.error('❌ No topic0 events specified');
  }
}
```

### Testing Stream Creation

```typescript
// Test with minimal config first
const testConfig = {
  webhookUrl: 'https://your-server.com/webhook',
  description: 'Test stream',
  tag: 'test',
  topic0: ['Transfer(address,address,uint256)'],
  chainIds: ['0x1'],
  allAddresses: false,
  includeNativeTxs: false
};

// If successful, then add more complex features
const stream = await createStream(testConfig);
console.log('Stream created:', stream.id);
```

### Monitoring Webhook Deliveries

```typescript
// In your webhook handler
function handleWebhook(req: any, res: any): void {
  const startTime = Date.now();

  // Log webhook receipt
  console.log('Webhook received at:', new Date().toISOString());
  console.log('Stream ID:', req.headers['x-stream-id']);
  console.log('Records charged:', req.headers['x-records-charged']);

  // Process webhook
  try {
    await processWebhookData(req.body);
    const processingTime = Date.now() - startTime;
    console.log('Processing time:', processingTime, 'ms');

    // Respond quickly to acknowledge receipt
    res.status(200).json({ status: 'received' });
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
}
```

## Prevention Checklist

Before implementing ANY stream operation:

- [ ] Check the endpoint rule file
- [ ] Verify HTTP method (PUT vs POST vs DELETE vs GET)
- [ ] Use correct base URL: `api.moralis-streams.com`
- [ ] Verify stream ID is UUID format
- [ ] Use hex chain IDs (0x1, 0x89, etc.)
- [ ] Use full event signatures in topic0 (with types)
- [ ] Use lowercase status values ("active", "paused")
- [ ] Include required fields (webhookUrl, chainIds, topic0)
- [ ] Test webhook URL is publicly accessible
- [ ] Verify response structure before accessing data

Skipping any of these steps will result in errors or non-functional streams.
