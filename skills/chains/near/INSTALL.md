# NEAR Intents Skill — Installation Guide

Quick setup guide for the NEAR Intents cross-chain swap skill.

---

## Prerequisites

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **OpenClaw**: Installed and running

Check versions:
```bash
node --version  # Should be >= v18
npm --version   # Should be >= v9
```

---

## Installation

### Option 1: Direct Installation (Recommended)

```bash
# Navigate to OpenClaw skills directory
cd /root/.openclaw/skills/

# Extract the skill
tar -xzf near-intents-v2.0.0.tar.gz

# Enter directory
cd near-intents

# Install dependencies
npm install
```

### Option 2: Symlink (For Development)

```bash
# If skill is in a workspace directory
cd /root/.openclaw/skills/
ln -s /path/to/near-intents near-intents
cd near-intents
npm install
```

---

## Configuration

### For Manual Mode Only (No Configuration Needed!)

If you only want to generate quotes and have users send tokens manually:
- **No configuration needed**
- Skip the `.env` file entirely
- Just use `mode: 'manual'` in your calls

### For Auto Mode (Optional)

To enable automatic sending from a NEAR account:

1. **Copy the example config**:
```bash
cp .env.example .env
```

2. **Edit `.env`** with your NEAR account details:
```env
NEAR_ACCOUNT_ID=your-account.near
NEAR_PRIVATE_KEY=ed25519:your_private_key_here
NEAR_RPC_URL=https://rpc.mainnet.fastnear.com
NEAR_NETWORK_ID=mainnet
ONE_CLICK_JWT=optional_jwt_token
```

3. **Get your NEAR private key**:
```bash
# If using NEAR CLI
cat ~/.near-credentials/mainnet/your-account.near.json
```

4. **(Optional) Register for JWT**:
- Visit: https://partners.near-intents.org
- Register to get a JWT token
- Avoids 0.2% platform fee
- Add to `.env` as `ONE_CLICK_JWT`

---

## Verification

Test that everything works:

```bash
# Check token list (requires internet)
npx ts-node lib-1click/1-get-tokens.ts

# Test manual mode quote (no NEAR account needed)
npx ts-node lib-1click/2-get-quote.ts
```

If using auto mode (NEAR account configured):
```bash
# Run a test swap (WARNING: Uses real NEAR!)
npm run swap:test
```

---

## Usage in OpenClaw

### Import in Your Agent Code

```typescript
import { executeIntent } from './skills/near-intents/index';

// Use the function
const result = await executeIntent({
  assetIn: 'NEAR',
  assetOut: 'base:USDC',
  amount: '1.0',
  recipient: '0x...',
});
```

### Via Skill System

The skill is automatically available to OpenClaw agents when installed in `/root/.openclaw/skills/near-intents/`.

Agents can invoke it using the standard skill invocation pattern.

---

## Quick Test

Create a test file: `test-install.ts`

```typescript
import { executeIntent } from './index';

async function test() {
  try {
    // Test manual mode (no credentials needed)
    const quote = await executeIntent({
      assetIn: 'NEAR',
      assetOut: 'base:USDC',
      amount: '0.1',
      recipient: '0x0000000000000000000000000000000000000000',
      mode: 'manual',
    });
    console.log('✅ Installation successful!');
    console.log(quote);
  } catch (error) {
    console.error('❌ Installation failed:', error.message);
  }
}

test();
```

Run it:
```bash
npx ts-node test-install.ts
```

If you see a quote with a deposit address → ✅ Installation successful!

---

## Troubleshooting

### "Cannot find module '@defuse-protocol/one-click-sdk-typescript'"

**Fix**: Run `npm install` in the skill directory
```bash
cd /root/.openclaw/skills/near-intents
npm install
```

### "NEAR_ACCOUNT_ID and NEAR_PRIVATE_KEY must be set"

**Fix**: Either:
1. Configure `.env` file (for auto mode), OR
2. Use `mode: 'manual'` (no config needed)

### "Token not found: X"

**Fix**: Check `TOKENS.md` for the correct token symbol format
- NEAR chain: `NEAR`, `USDC`, `USDT`
- Other chains: `chain:SYMBOL` (e.g., `base:USDC`, `arb:ARB`)

### "Bad Request - Invalid input data"

**Possible causes**:
1. Missing `refundAddress` for cross-chain swap
2. Unsupported token pair (low liquidity)
3. Amount too small (minimum ~$0.10 USD)

**Fix**: Check error message and adjust parameters

### Dependencies won't install

**Fix**: Update Node.js and npm
```bash
node --version  # Should be >= v18
npm --version   # Should be >= v9

# If outdated, update via nvm or your package manager
```

---

## File Structure

After installation, you should have:

```
near-intents/
├── index.ts                    # Main entry point
├── package.json                # Dependencies
├── manifest.json               # Skill metadata
├── .env.example                # Config template
├── README.md                   # Overview
├── SKILL.md                    # API reference
├── AI-AGENT-GUIDE.md           # Agent workflows
├── TOKENS.md                   # Token reference
├── USAGE_GUIDE.md              # Patterns
├── INSTALL.md                  # This file
├── RELEASE_NOTES.md            # Version history
├── lib-1click/                 # SDK examples
├── node_modules/               # Dependencies (after npm install)
└── ...
```

---

## Next Steps

1. **Read the documentation**:
   - `SKILL.md` — Primary reference
   - `AI-AGENT-GUIDE.md` — Agent workflow patterns
   - `TOKENS.md` — Supported tokens

2. **Test with manual mode** (no config needed)

3. **(Optional) Configure auto mode** for NEAR-origin swaps

4. **Integrate into your agent**

---

## Uninstallation

```bash
# Remove the skill
cd /root/.openclaw/skills/
rm -rf near-intents

# Or if using symlink
unlink near-intents
```

---

## Support

- **Documentation**: See `SKILL.md` and other docs in this directory
- **NEAR Intents**: https://docs.near-intents.org
- **1Click SDK**: https://github.com/defuse-protocol/one-click-sdk-typescript
- **OpenClaw**: https://openclaw.ai

---

**Version**: 2.0.0
**Status**: ✅ Production Ready
**Installation Time**: ~2 minutes
