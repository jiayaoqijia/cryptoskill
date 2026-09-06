---
name: x402-agent-api-skill
description: AI agent skill for x402 paid APIs with live image-hosting and qrcode-generate, plus planned image/video/vision APIs (colorize, super-resolution, enhance, smart-redact, smart-crop, inpaint, qrcode-decode, tags, game-scene-detect, quality-score, face/human/pet/plate-detect, OCR, idcard-ocr, background-remove, video object-detection, portrait-segmentation).
version: 1.2.0
---

# x402 Agent API Skill

Use this skill to let your AI agent call paid endpoints on `https://www.x402api.app/` with x402.

## Quick start for AI agents

1. Place this file in your OpenClaw, Codex, or Claude project root.
2. Tell your AI agent: "Help me convert this text into a QR code." or "Help me upload this image and return an online URL."
3. The agent should follow x402 payment flow automatically.

## Install dependencies

```bash
npm install @x402/core @x402/evm viem
```

## Required environment variables

```bash
EVM_PRIVATE_KEY=0x_your_private_key
API_BASE_URL=https://www.x402api.app/
```

## Currently available features

1. QR code generation
2. Image hosting

## Available endpoints

### Live

- `GET /api/health` - health check
- `GET /api/v1/capabilities` - capability discovery
- `POST /api/v1/qrcode/generate` - generate QR code image (x402 protected)
- `POST /api/v1/image/upload` - upload image and return public URL (x402 protected, max 10MB)

### Planned

- `POST /api/v1/image/colorize`
- `POST /api/v1/image/super-resolution`
- `POST /api/v1/image/enhance`
- `POST /api/v1/image/smart-redact`
- `POST /api/v1/image/smart-crop`
- `POST /api/v1/image/inpaint`
- `POST /api/v1/image/qrcode/decode`
- `POST /api/v1/image/tags`
- `POST /api/v1/image/game-scene-detect`
- `POST /api/v1/image/quality-score`
- `POST /api/v1/vision/face-detect`
- `POST /api/v1/vision/human-detect`
- `POST /api/v1/vision/pet-detect`
- `POST /api/v1/vision/plate-detect`
- `POST /api/v1/image/ocr`
- `POST /api/v1/image/idcard-ocr`
- `POST /api/v1/image/background-remove`
- `POST /api/v1/video/object-detection`
- `POST /api/v1/video/portrait-segmentation`

## How to call each live endpoint

### 1) QR code generation

Endpoint: `POST /api/v1/qrcode/generate`

JSON body:

```json
{
  "text": "https://example.com",
  "size": 512,
  "ecc": "M",
  "format": "png",
  "margin": 2
}
```

- `text` is required (1-2048 chars).
- `format` is currently `png` only.
- `size` range: `128-2048`.
- `margin` range: `0-16`.
- `ecc` supports: `L | M | Q | H`.
- Success response contains `result.image_base64` and `result.mime_type`.

### 2) Image hosting

Endpoint: `POST /api/v1/image/upload`

Request type: `multipart/form-data`

- Use one form-data field named `file`.
- File type must be `image/*`.
- File size must be `<= 10MB`.

Success response contains `result.image_url`.

## Payment flow

1. Call protected endpoint and expect `402 Payment Required`.
2. Parse payment requirements from response headers.
3. Sign payment and retry with x402 payment header.
4. Read business result (`result.image_url` for upload).

## Example client flow

This example follows the same pattern as `scripts/buyer-quickstart-test.ts`.

```ts
import { x402Client, x402HTTPClient } from "@x402/core/client";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const baseUrl =
  process.env.X402_API_BASE_URL ??
  process.env.API_BASE_URL ??
  "https://www.x402api.app/";
const endpoint = `${baseUrl.replace(/\/$/, "")}/api/v1/qrcode/generate`;

async function main() {
  const privateKey = process.env.EVM_PRIVATE_KEY;
  if (!privateKey) throw new Error("Missing EVM_PRIVATE_KEY");
  if (!privateKey.startsWith("0x")) throw new Error("EVM_PRIVATE_KEY must start with 0x");

  const account = privateKeyToAccount(privateKey as `0x${string}`);
  const publicClient = createPublicClient({ chain: base, transport: http() });
  const signer = toClientEvmSigner(account, publicClient);
  const client = new x402Client().register("eip155:*", new ExactEvmScheme(signer));
  const httpClient = new x402HTTPClient(client);

  const payload = { text: "https://example.com", size: 512, ecc: "M" };

  const unpaid = await fetch(endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (unpaid.status !== 402) {
    const unpaidBody = await unpaid.text();
    throw new Error(`Expected unpaid status 402, got ${unpaid.status}. body=${unpaidBody}`);
  }

  const paymentRequired = httpClient.getPaymentRequiredResponse(
    (name) => unpaid.headers.get(name),
    {},
  );

  const paymentPayload = await httpClient.createPaymentPayload(paymentRequired);
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...httpClient.encodePaymentSignatureHeader(paymentPayload),
    },
    body: JSON.stringify(payload),
  });

  const body = await response.json();
  if (!response.ok) throw new Error(`Request failed with status ${response.status}: ${JSON.stringify(body)}`);

  console.log(body);
}

void main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

## Error handling

- `402 Payment Required`: build payment payload, sign, and retry.
- `500 Internal Server Error`: retry with backoff and log request context.

## Endpoint-specific error codes

### `POST /api/v1/image/upload`

- `image_file_required` (`400`): `file` field is missing.
- `image_file_empty` (`400`): uploaded file is empty.
- `image_file_too_large` (`413`): image is larger than 10MB.
- `image_mime_not_supported` (`400`): only `image/*` is supported.
- `invalid_image_request` (`400`): other validation errors.

### `POST /api/v1/qrcode/generate`

- `invalid_json_body` (`400`): request body is not valid JSON.
- `invalid_request_body` (`400`): body is not a JSON object.
- `qrcode_content_required` (`400`): `text` is missing or empty.
- `qrcode_content_too_long` (`400`): `text` exceeds 2048 characters.
- `qrcode_format_not_supported` (`400`): only `png` format is supported.
- `invalid_qrcode_request` (`400`): other validation errors.

