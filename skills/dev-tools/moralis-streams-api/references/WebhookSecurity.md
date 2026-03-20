# Webhook Security

All webhook requests sent by Moralis Streams are signed with your streams secret to verify authenticity.

**Note:** The code snippets below are illustrative examples only. They are not drop-in production code, and you are free to use any libraries or frameworks you prefer in your own project.

## Signature Header

The signature is included in the request headers:

```
x-signature: <signature>
```

## How the Signature is Created

The signature is generated using SHA3 (Keccak-256) on the concatenation of the request body and your streams secret:

```
signature = web3.utils.sha3(JSON.stringify(req.body) + secret)
```

**Important:** The `secret` is your **streams secret** (not your API key), which can be found in the Moralis Streams settings page.

**Critical:** The request body must be parsed as **JSON** (not raw text) for the signature to compute correctly.

## Verifying Webhook Signatures

### JavaScript/Node.js (Express)

```javascript
const express = require('express');
const axios = require('axios');
const { Web3 } = require('web3');

const app = express();
const PORT = 3000;

// Middleware to parse JSON
app.use(express.json());

const MORALIS_API_KEY = process.env.MORALIS_API_KEY;
let SECRET_KEY = null; // Will cache the secret for the account

async function getMoralisSecret() {
    if (SECRET_KEY === null) {
        try {
            const headers = {
                'accept': 'application/json',
                'X-API-Key': MORALIS_API_KEY
            };

            const response = await axios.get("https://api.moralis-streams.com/settings", { headers });
            SECRET_KEY = response.data.secretKey;
        } catch (error) {
            throw new Error(`Failed to get Moralis secret: ${error.message}`);
        }
    }
    return SECRET_KEY;
}

function verifySignature(req, secret) {
    const providedSignature = req.headers['x-signature'];
    console.log("Provided signature:", providedSignature);

    if (!providedSignature) {
        throw new Error("Signature not provided");
    }

    // Generate signature using JSON.stringify + secret
    const web3 = new Web3();
    const generatedSignature = web3.utils.sha3(JSON.stringify(req.body) + secret);

    console.log("Generated signature:", generatedSignature);

    if (generatedSignature !== providedSignature) {
        throw new Error("Invalid Signature");
    }
}

app.post('/webhook', async (req, res) => {
    try {
        // Verify signature
        const secret = await getMoralisSecret();
        verifySignature(req, secret);

        // Process webhook data
        const webhookData = req.body;
        console.log("✅ Webhook verified");
        console.log(`Data: ${JSON.stringify(webhookData)}`);

        return res.status(200).json({ status: "success" });

    } catch (error) {
        console.error(`❌ Webhook error: ${error.message}`);
        return res.status(401).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

### Python (Flask)

```python
import json
import os
from flask import Flask, request, jsonify
import requests
from web3 import Web3

app = Flask(__name__)

# Force JSON parsing for all requests
@app.before_request
def force_json():
    if request.method == 'POST' and not request.is_json:
        if 'application/json' not in request.content_type:
            request.environ['CONTENT_TYPE'] = 'application/json'

MORALIS_API_KEY = os.environ["MORALIS_API_KEY"]
SECRET_KEY = None  # Will cache the secret for the account

def get_moralis_secret():
    global SECRET_KEY
    if SECRET_KEY is None:
        headers = {'accept': 'application/json', 'X-API-Key': MORALIS_API_KEY}
        response = requests.get("https://api.moralis-streams.com/settings", headers=headers)
        SECRET_KEY = response.json().get('secretKey')
    return SECRET_KEY

def verify_signature(req, secret):
    provided_signature = req.headers.get("x-signature")
    print("Provided signature:", provided_signature)

    if not provided_signature:
        raise TypeError("Signature not provided")

    # Parse JSON then re-serialize to match JavaScript's JSON.stringify() output
    body = json.dumps(req.get_json(), separators=(',', ':'))
    signature = "0x" + Web3.keccak(text=body + secret).hex()

    print("Generated signature:", signature)

    if provided_signature != signature:
        raise ValueError("Invalid Signature")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Verify signature
        secret = get_moralis_secret()
        verify_signature(request, secret)

        # Parse and process webhook data
        webhook_data = request.get_json()

        print("✅ Webhook verified")
        print(f"Data: {webhook_data}")

        return jsonify({"status": "success"}), 200

    except (TypeError, ValueError) as e:
        print(f"❌ Verification failed: {e}")
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
```

## Key Implementation Notes

### JSON Parsing is Critical

Both examples ensure the request body is parsed as **JSON**, not raw text or other formats. This is essential because:

- `JSON.stringify(req.body)` in JavaScript produces consistent compact output
- `json.dumps(req.get_json(), separators=(',', ':'))` in Python matches JavaScript's `JSON.stringify()` output
- Any variation in body formatting (whitespace, key ordering) will cause signature mismatch

### Getting the Streams Secret

The examples fetch the streams secret dynamically from the Moralis Streams API:

```
GET https://api.moralis-streams.com/settings
X-API-Key: $MORALIS_API_KEY
```

Response includes `secretKey` - use this for webhook verification (not your API key).

## Security Best Practices

1. **Always verify signatures** - Never trust webhook requests without signature verification
2. **Use HTTPS** - Ensure your webhook endpoint uses HTTPS to prevent man-in-the-middle attacks
3. **Store secrets securely** - Use environment variables or secret management services
4. **Check signature first** - Verify the signature before processing any webhook data
5. **Log verification failures** - Monitor failed signature verifications for potential attacks
6. **Timing attack protection** - Use constant-time comparison when comparing signatures in production
7. **Parse as JSON** - Ensure body is parsed as JSON before computing signature

## Finding Your Streams Secret

### Option 1: Via API

```bash
curl "https://api.moralis-streams.com/settings" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

### Option 2: Via Dashboard

1. Navigate to the Moralis Streams dashboard
2. Go to Settings
3. Copy your **Streams Secret** (not the API Key)

The streams secret is different from your API key and is specifically used for webhook signature verification.
