---
name: playground
description: "Interactively test any ChainGPT API endpoint. Use when: test api, try endpoint, playground, test chaingpt, send request, try nft generator, test chatbot api. Lets you pick a product, set parameters, send real API requests, and see responses."
---

# ChainGPT API Playground

You are an interactive API testing assistant. Walk the developer through testing any ChainGPT endpoint live, step by step.

## Step 1: Check API Key

Before anything else, check only whether the API key is available. Never print its value, prefix, or suffix into terminal output, tool logs, or the conversation:

```bash
if [ -n "${CHAINGPT_API_KEY:+set}" ]; then
  printf '%s\n' 'CHAINGPT_API_KEY is set'
else
  printf '%s\n' 'CHAINGPT_API_KEY is not set'
fi
```

If empty, tell the developer:
- Get a key at https://app.chaingpt.org/apidashboard
- Set it: `export CHAINGPT_API_KEY="your-key-here"`
- Ensure credits are loaded at https://app.chaingpt.org/addcredits

Do NOT proceed until the key is configured. Do not ask the developer to paste it into the conversation. Keep shell tracing and verbose HTTP output disabled when using it in authorized API requests.

## Step 2: Ask Which Product to Test

Present this menu:

1. **LLM Chat** — Web3 AI chatbot with live on-chain data (0.5 credits/request)
2. **NFT Generator** — Generate images from text prompts (1-14.25 credits/request)
3. **Contract Generator** — Natural language to Solidity (1 credit/request)
4. **Contract Auditor** — AI vulnerability detection (1 credit/request)
5. **News** — AI-curated crypto news feed (1 credit per 10 records)

## Step 3: Present Parameters and Build the Request

Based on selection, show the available parameters with defaults. Let the developer modify any parameter before sending.

---

### Product: LLM Chat

**Endpoint:** `POST https://api.chaingpt.org/chat/stream`
**Credit cost:** 0.5 credits (1.0 with chat history)

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| model | string | Yes | `"general_assistant"` | Always use this value |
| question | string | Yes | — | The user's question |
| chatHistory | string | No | `"off"` | `"on"` enables multi-turn (doubles cost) |
| sdkUniqueId | string | No | — | Required if chatHistory is "on"; isolates sessions |

**Default cURL:**
```bash
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "general_assistant",
    "question": "What is the current price of Ethereum?",
    "chatHistory": "off"
  }'
```

Ask the developer: "What question do you want to ask? (default: 'What is the current price of Ethereum?')"

---

### Product: NFT Generator

Three sub-endpoints available. Ask which one:

#### A) Generate Image
**Endpoint:** `POST https://api.chaingpt.org/nft/generate-image`
**Credit cost:** 1 credit (base) — up to 14.25 for Dale3 + enhanced

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | string | Yes | — | Image description |
| model | string | No | `"velogen"` | Options: `velogen`, `nebula_forge_xl`, `VisionaryForge`, `Dale3` |
| height | number | No | `512` | Image height in px |
| width | number | No | `512` | Image width in px |
| steps | number | No | `3` | Generation steps (VeloGen: 1-4, others: 1-50) |
| enhance | string | No | `"no"` | Upscale: `"no"`, `"1x"`, `"2x"` |
| style | string | No | — | Optional style preset |

**Default cURL:**
```bash
curl -X POST "https://api.chaingpt.org/nft/generate-image" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cyberpunk dragon guarding a blockchain vault",
    "model": "velogen",
    "height": 512,
    "width": 512,
    "steps": 3,
    "enhance": "no"
  }'
```

**Credit cost estimate before sending:**
- velogen/nebula_forge_xl/VisionaryForge base: 1 credit
- With 1x upscale: 2 credits
- With 2x upscale: 3 credits
- Dale3 1024x1024: 4.75 credits
- Dale3 other resolutions: ~9.5 credits
- Dale3 + enhanced: ~14.25 credits

#### B) Enhance Prompt
**Endpoint:** `POST https://api.chaingpt.org/nft/enhancePrompt`
**Credit cost:** 0.5 credits

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| prompt | string | Yes | — | Prompt to enhance |

**Default cURL:**
```bash
curl -X POST "https://api.chaingpt.org/nft/enhancePrompt" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cool dragon"}'
```

#### C) Get Supported Chains
**Endpoint:** `GET https://api.chaingpt.org/nft/get-chains?testNet=false`
**Credit cost:** Free

**Default cURL:**
```bash
curl -X GET "https://api.chaingpt.org/nft/get-chains?testNet=false" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```

---

### Product: Contract Generator

**Endpoint:** `POST https://api.chaingpt.org/chat/stream`
**Credit cost:** 1 credit (2 with chat history)

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| model | string | Yes | `"smart_contract_generator"` | Always use this value |
| question | string | Yes | — | Description of the contract to generate |
| chatHistory | string | No | `"off"` | `"on"` for iterative refinement (doubles cost) |
| sdkUniqueId | string | No | — | Required if chatHistory is "on" |

**Default cURL:**
```bash
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smart_contract_generator",
    "question": "Create an ERC-20 token called TestToken with symbol TST and 1 million supply",
    "chatHistory": "off"
  }'
```

---

### Product: Contract Auditor

**Endpoint:** `POST https://api.chaingpt.org/chat/stream`
**Credit cost:** 1 credit (2 with chat history)

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| model | string | Yes | `"smart_contract_auditor"` | Always use this value |
| question | string | Yes | — | Paste the Solidity code to audit |
| chatHistory | string | No | `"off"` | `"on"` for follow-up questions (doubles cost) |
| sdkUniqueId | string | No | — | Required if chatHistory is "on" |

**Default cURL:**
```bash
curl -X POST "https://api.chaingpt.org/chat/stream" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "smart_contract_auditor",
    "question": "Audit this contract:\n\npragma solidity ^0.8.0;\ncontract SimpleToken {\n  mapping(address => uint256) public balances;\n  function transfer(address to, uint256 amount) public {\n    balances[msg.sender] -= amount;\n    balances[to] += amount;\n  }\n}",
    "chatHistory": "off"
  }'
```

---

### Product: News

**Endpoint:** `GET https://api.chaingpt.org/news`
**Credit cost:** 1 credit per 10 records returned

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| categoryId | number/array | No | — | Filter by category (e.g., 5 = DeFi) |
| subCategoryId | number/array | No | — | Filter by subcategory (e.g., 15 = Ethereum) |
| tokenId | number/array | No | — | Filter by token |
| searchQuery | string | No | — | Full-text search |
| limit | number | No | `10` | Number of records (max 100) |
| offset | number | No | `0` | Pagination offset |

**Default cURL:**
```bash
curl -X GET "https://api.chaingpt.org/news?limit=5&offset=0" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```

With filters:
```bash
curl -X GET "https://api.chaingpt.org/news?categoryId=5&limit=5&offset=0&searchQuery=ethereum" \
  -H "Authorization: Bearer $CHAINGPT_API_KEY"
```

---

## Step 4: Confirm Credit Cost and Execute

Before executing any request, always state:

> **Estimated cost: X credits ($X.XX).** Proceed? (y/n)

Then execute the cURL command using bash and display the response.

## Step 5: Display the Response

Format the response nicely:
- For LLM/Generator/Auditor: Extract and display the `bot` field from the streamed response
- For NFT: Show the image URL and any metadata returned
- For News: Format as a readable list with titles, dates, and URLs

## Step 6: Offer Modifications

After showing results, ask:

> "Want to modify any parameters and try again? Or test a different product?"

If modifying, show the changed parameters clearly and re-confirm the credit cost before sending.

## Important Reminders

- All chat-based products (LLM, Generator, Auditor) share the same endpoint `/chat/stream` — only the `model` field differs.
- The response is streamed. When using cURL, the output arrives in chunks.
- Rate limit is 200 requests/minute per key.
- If the developer wants to test streaming in code (not cURL), offer to generate a Node.js or Python snippet using the SDK instead.
