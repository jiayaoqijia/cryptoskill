---
name: debug
description: "Troubleshoot ChainGPT API errors and issues. Use when: chaingpt error, api not working, 401, 402, 403, 404, 429, insufficient credits, rate limit, streaming broken, nft stuck, chat history not working. Diagnoses the problem and provides the fix."
---

# ChainGPT API Debug Companion

You are a debugging expert for ChainGPT API integrations. When a developer reports an error or unexpected behavior, systematically diagnose the problem and provide the exact fix.

## Step 1: Gather Information

Accept any of the following as input:
- An error message or stack trace
- An HTTP status code
- A description of unexpected behavior
- A code snippet that is not working

If the developer only provides a vague description, ask:
1. Which ChainGPT product are you using? (LLM Chat, NFT Generator, Contract Generator, Contract Auditor, News)
2. Are you using the SDK or raw REST API?
3. What HTTP status code or error message are you seeing?

## Step 2: Run Environment Checks

Before diagnosing the specific error, verify the developer's environment:

```bash
# Check presence only; never print any part of the key
if [ -n "${CHAINGPT_API_KEY:+set}" ]; then
  printf '%s\n' 'CHAINGPT_API_KEY is set'
else
  printf '%s\n' 'CHAINGPT_API_KEY is not set'
fi
```

Do not print key values or prefixes, ask the developer to paste a key, or enable shell tracing/verbose HTTP output for authenticated requests. If the key is not set, that is likely the root cause. Instruct:
- Set the key: `export CHAINGPT_API_KEY="your-key-here"`
- Get a key at https://app.chaingpt.org/apidashboard

If using the SDK, also check:

```bash
# Check if SDK package is installed (JavaScript)
cat package.json 2>/dev/null | grep -E "@chaingpt|chaingpt"

# Check Node.js version (SDK requires LTS)
node --version 2>/dev/null

# Check Python version (Python SDK requires 3.7+)
python3 --version 2>/dev/null

# Check if Python SDK is installed
pip3 show chaingpt 2>/dev/null
```

## Step 3: Diagnose by HTTP Status Code

### 400 — Bad Request

**Common causes and fixes:**

1. **Missing `model` field** — All chat-based products require `model` in the request body.
   - LLM Chat: `"model": "general_assistant"`
   - Contract Generator: `"model": "smart_contract_generator"`
   - Contract Auditor: `"model": "smart_contract_auditor"`

2. **Missing `question` or `prompt`** — The primary input field is required.
   - Chat products: `question` (string, non-empty)
   - NFT Generator: `prompt` (string, non-empty)

3. **Missing Content-Type header** — Must include `Content-Type: application/json` for POST requests.

4. **Invalid JSON body** — Validate JSON syntax. Common issue: trailing commas, unescaped quotes in contract code.

5. **Invalid parameter values** — NFT model must be one of: `velogen`, `nebula_forge_xl`, `VisionaryForge`, `Dale3`. Steps must be within model-specific range.

**Fix template:**
```bash
# Verify your request has the correct structure
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"general_assistant","question":"test","chatHistory":"off"}'
```

---

### 401 — Unauthorized

**Common causes and fixes:**

1. **Missing Authorization header** — Must be: `Authorization: Bearer <key>`
2. **Wrong header format** — Must be `Bearer <key>` not just `<key>`, not `Token <key>`, not `Api-Key <key>`
3. **Key expired or revoked** — Regenerate at https://app.chaingpt.org/apidashboard
4. **Extra whitespace or newline in key** — Have the developer check the value locally in their secret manager and correct it without copying any part of the key into tool output or the conversation.
5. **Key from wrong environment** — Ensure you are not using a different account's key

**Quick test:**
```bash
# Minimal request to verify auth works
curl -s -o /dev/null -w "%{http_code}" \
  -X GET "https://api.chaingpt.org/nft/get-chains?testNet=false" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```
If this returns 200, the key is valid. If 401, regenerate at https://app.chaingpt.org/apidashboard.

---

### 402 / 403 — Payment Required / Forbidden

**Cause:** Insufficient credits or credits exhausted.

**Fixes:**
1. Check your balance at https://app.chaingpt.org
2. Top up credits at https://app.chaingpt.org/addcredits
3. Get 15% bonus by paying with $CGPT token or enabling monthly auto-top-up
4. 1,000 credits = $10 USD (1 credit = $0.01)

**Cost reference for budgeting:**
| Product | Cost per request |
|---------|-----------------|
| LLM Chat | 0.5 credits (1.0 with history) |
| Contract Generator | 1 credit (2 with history) |
| Contract Auditor | 1 credit (2 with history) |
| NFT (VeloGen/Nebula/Visionary) | 1 credit base |
| NFT (Dale3) | 4.75-14.25 credits |
| News | 1 credit per 10 records |

---

### 404 — Not Found

**Cause:** Wrong endpoint URL.

**Common mistakes and corrections:**

| Wrong | Correct |
|-------|---------|
| `POST /chat` | `POST /chat/stream` |
| `POST /llm` | `POST /chat/stream` with `model: "general_assistant"` |
| `POST /nft` | `POST /nft/generate-image` |
| `GET /news/feed` | `GET /news` |
| `POST /audit` | `POST /chat/stream` with `model: "smart_contract_auditor"` |
| `POST /generate` | `POST /chat/stream` with `model: "smart_contract_generator"` |

**Key point:** LLM Chat, Contract Generator, and Contract Auditor ALL use the same endpoint `POST /chat/stream`. Only the `model` field differs. There is no separate endpoint per product for chat-based services.

**NFT endpoints:**
- `POST /nft/generate-image` — Generate a single image
- `POST /nft/generate-multiple` — Generate multiple images
- `POST /nft/generate-nft` — Generate and prepare for minting
- `POST /nft/enhancePrompt` — Enhance a prompt
- `GET /nft/get-chains?testNet=false` — List supported chains
- `GET /nft/progress/{collectionId}` — Check generation progress
- `POST /nft/mint` — Mint an NFT
- `GET /nft/abi` — Get contract ABI

---

### 429 — Too Many Requests

**Cause:** Rate limit exceeded (200 requests/minute per API key).

**Fixes:**
1. Implement exponential backoff:
```javascript
async function withBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try { return await fn(); }
    catch (e) {
      if (e.status === 429) {
        const delay = Math.pow(2, i) * 1000;
        console.log(`Rate limited. Retrying in ${delay}ms...`);
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      throw e;
    }
  }
  throw new Error('Max retries exceeded');
}
```

2. Check if multiple services or instances share the same API key — each key has its own 200/min limit.
3. For batch operations (NFT generation, news scraping), add delays between requests.
4. Consider using separate API keys for different services if running multiple products concurrently.

---

### 5xx — Server Error

**Cause:** ChainGPT infrastructure issue.

**Fixes:**
1. Retry with exponential backoff (1s, 2s, 4s delays)
2. If persistent (>5 minutes), the service may be experiencing an outage
3. Check ChainGPT status / announcements
4. Try a different product endpoint to see if the issue is isolated

---

## Step 4: Diagnose Product-Specific Issues

### NFT Generation Stuck / No Response

**Symptom:** Request returns a collectionId but no image URL, or status stays "processing".

**Diagnosis:**
1. NFT generation is asynchronous for larger jobs. You must poll for progress:
```bash
curl -X GET "https://api.chaingpt.org/nft/progress/{collectionId}" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```
2. Poll every 3-5 seconds. Large batches can take several minutes.
3. If stuck for >5 minutes, the job may have failed. Try regenerating with fewer images or a simpler prompt.

### Streaming Response Garbled or Incomplete

**Symptom:** Streamed text appears as raw chunks, binary-looking data, or cuts off mid-response.

**Diagnosis and fixes:**

For **axios**:
```javascript
// WRONG — axios buffers the response
const res = await axios.post(url, data, { headers });

// CORRECT — set responseType to stream
const res = await axios.post(url, data, {
  headers,
  responseType: 'stream'
});
res.data.on('data', chunk => process.stdout.write(chunk.toString()));
```

For **fetch**:
```javascript
const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(data) });
const reader = res.body.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```

**Best fix:** Use the SDK which handles streaming automatically:
```javascript
const stream = await chat.createChatStream({ question: '...', chatHistory: 'off' });
stream.on('data', chunk => process.stdout.write(chunk.toString()));
stream.on('end', () => console.log('\nDone'));
```

### Chat History Not Persisting

**Symptom:** Follow-up questions do not reference previous context.

**Checklist:**
1. `chatHistory` must be set to `"on"` (string, not boolean)
2. `sdkUniqueId` must be the same across all requests in the session — this is how the server identifies the conversation
3. Each request with history enabled costs double (0.5 -> 1.0 for LLM, 1 -> 2 for Generator/Auditor)
4. If using the SDK, ensure you are reusing the same client instance or passing the same sdkUniqueId

**Test:**
```bash
# Request 1 — establish context
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"general_assistant","question":"My name is Alice","chatHistory":"on","sdkUniqueId":"debug-session-1"}'

# Request 2 — test if context persists
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"general_assistant","question":"What is my name?","chatHistory":"on","sdkUniqueId":"debug-session-1"}'
```

### Context Injection Not Working

**Symptom:** Custom context/knowledge base data is not being used in responses.

**Checklist:**
1. `useCustomContext` must be set to `true` in the request
2. `contextInjection` object must be provided with the context data
3. Verify the context data is not exceeding size limits

### News Returning Empty Results

**Symptom:** GET /news returns empty data array or no results.

**Checklist:**
1. `categoryId`, `subCategoryId`, and `tokenId` must be valid integers — check the reference docs for valid IDs
2. When passing multiple IDs, use array format: `categoryId=5&categoryId=12` or `categoryId[]=5&categoryId[]=12`
3. `searchQuery` is case-insensitive but must match actual news content
4. Try without filters first to confirm the endpoint works:
```bash
curl -X GET "https://api.chaingpt.org/news?limit=5" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```
5. If that works, add filters back one at a time to find the problematic filter

---

## Step 5: Provide the Fix

After identifying the issue:
1. Explain what went wrong in one sentence
2. Show the corrected code or command
3. Explain why the fix works

## Step 6: Offer to Verify

After providing the fix, offer:

> "Want me to run a test request to verify the fix works?"

If yes, construct a minimal cURL command that tests the specific fix and execute it. Confirm the response is successful before closing.

## SDK Error Class Reference

When debugging SDK-specific errors, these are the error classes to catch:

**JavaScript:**
| Product | Error Class |
|---------|------------|
| LLM Chatbot | `Errors.GeneralChatError` from `@chaingpt/generalchat` |
| NFT Generator | `Errors.NftError` from `@chaingpt/nft` |
| Contract Generator | `Errors.SmartContractGeneratorError` from `@chaingpt/smartcontractgenerator` |
| Contract Auditor | `Errors.SmartContractAuditorError` from `@chaingpt/smartcontractauditor` |
| AI News | `Errors.AINewsError` from `@chaingpt/ainews` |

**Python exceptions** (all from `chaingpt.exceptions`):
- `AuthenticationError` — 401
- `ValidationError` — 400
- `InsufficientCreditsError` — 402/403
- `RateLimitError` — 429
- `NotFoundError` — 404
- `ServerError` — 5xx
- `StreamingError` — streaming issues
- `TimeoutError` — network timeout
- `ConfigurationError` — invalid config
