# Webhook Signature Verification

All webhook deliveries are signed with HMAC-SHA256 using the secret returned by `POST /api/v1/webhooks/register`. Store that secret securely and always verify signatures before processing payloads.

## How Signing Works

1. 8004scan takes the raw JSON request body
2. Computes `HMAC-SHA256(secret, body)` using your shared secret
3. Sends the hex-encoded digest in the `X-Webhook-Signature` header

## Verification Examples

### Node.js

```javascript
const crypto = require("crypto");

function verifyWebhook(body, signature, secret) {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(body, "utf-8")
    .digest("hex");
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signature)
  );
}

// Express middleware
app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
  const signature = req.headers["x-webhook-signature"];
  const isValid = verifyWebhook(req.body, signature, process.env.WEBHOOK_SECRET);

  if (!isValid) {
    return res.status(401).json({ error: "Invalid signature" });
  }

  const event = JSON.parse(req.body);
  console.log(`Event: ${event.event}, Agent: ${event.data.agentId}`);
  res.status(200).json({ received: true });
});
```

### Python

```python
import hmac
import hashlib

def verify_webhook(body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

# Flask example
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Webhook-Signature", "")
    if not verify_webhook(request.data, signature, WEBHOOK_SECRET):
        return {"error": "Invalid signature"}, 401

    event = request.get_json()
    print(f"Event: {event['event']}, Agent: {event['data']['agentId']}")
    return {"received": True}, 200
```

### Go

```go
func verifyWebhook(body []byte, signature, secret string) bool {
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write(body)
    expected := hex.EncodeToString(mac.Sum(nil))
    return hmac.Equal([]byte(expected), []byte(signature))
}
```

### Bash / curl

```bash
BODY='{"event":"feedback.received","data":{"agentId":"8453:17"}}'
SECRET="your-webhook-secret"
EXPECTED=$(echo -n "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')
echo "Expected signature: $EXPECTED"
```

## Security Best Practices

1. **Always verify signatures** — Never process unverified payloads
2. **Use timing-safe comparison** — Prevent timing attacks (`crypto.timingSafeEqual`, `hmac.compare_digest`)
3. **Use HTTPS endpoints** — Webhook URLs must be HTTPS
4. **Secret storage** — Store the generated secret in a secret manager, not in source control
5. **Rotate by replacement** — Create a replacement webhook and retire the old one when a secret must be rotated
6. **Respond quickly** — Return 2xx within 10 seconds to avoid timeout retries
7. **Idempotency** — Use `X-Webhook-Delivery-Id` header to deduplicate, as retries may deliver the same event twice
8. **IP allowlisting** — If your firewall supports it, allowlist 8004scan delivery IPs

## Delivery Headers

Each webhook delivery includes these headers:

| Header | Description |
|--------|-------------|
| `X-Webhook-Signature` | HMAC-SHA256 hex digest of the request body |
| `X-Webhook-Event` | Event type (e.g., `feedback.received`) |
| `X-Webhook-Delivery-Id` | Unique delivery ID for idempotency |
| `Content-Type` | Always `application/json` |
| `User-Agent` | `8004scan-webhooks/1.0` |

## Retry Behavior

If your endpoint returns a non-2xx status or times out (10s), the delivery is retried:

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 hours |

After 5 failed attempts, the delivery is marked as permanently failed. Webhooks with sustained failures (>10 consecutive) may be automatically disabled — check delivery history and re-enable via the PATCH endpoint.
