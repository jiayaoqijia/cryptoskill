# Privy Setup

Get your Privy API credentials to start creating agentic wallets.

## 1. Create a Privy Account

Go to [dashboard.privy.io](https://dashboard.privy.io) and sign up or log in.

## 2. Create an App

Click "Create App" and give it a name (e.g., "My Agent Wallet").

## 3. Get API Credentials

Navigate to **Configuration → App settings → Basics**.

You'll find:
- **App ID** — Public identifier, safe to expose in client code
- **App Secret** — Private key, keep secure (backend/server only)

## 4. Store Credentials in OpenClaw

Add your credentials to your OpenClaw gateway config so the agent can use them for API calls.

**Option A: Edit config directly**

Add to `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "env": {
      "PRIVY_APP_ID": "your-app-id",
      "PRIVY_APP_SECRET": "your-app-secret"
    }
  }
}
```

Then restart the gateway:
```bash
openclaw gateway restart
```

**Option B: Shell environment variables**

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PRIVY_APP_ID="your-app-id"
export PRIVY_APP_SECRET="your-app-secret"
```

Then restart your terminal and the OpenClaw gateway.

## 5. Test Your Setup

Verify credentials work:

```bash
curl -X GET "https://api.privy.io/v1/wallets" \
  --user "$PRIVY_APP_ID:$PRIVY_APP_SECRET" \
  -H "privy-app-id: $PRIVY_APP_ID" \
  -H "Content-Type: application/json"
```

Should return `{"data": [], ...}` (empty wallet list for new apps).

## Authorization Keys (Advanced)

For agentic wallets with multi-party approval:

1. In the dashboard, go to **Authorization Keys**
2. Create a new key pair
3. Store the private key securely — your agent signs requests with it
4. The public key is registered with Privy

Authorization keys enable:
- Multi-party approval for critical actions
- Key quorums for enhanced security
- Granular access control per wallet

For basic agentic wallets, App ID + Secret is sufficient.
