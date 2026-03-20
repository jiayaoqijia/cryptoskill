---
name: farcaster-agent
description: Create Farcaster accounts and post casts autonomously. Official skill from the Farcaster team.
metadata: {"openclaw":{"emoji":"🟣","requires":{"bins":["node","npm"],"env":[]},"install":[{"id":"npm","kind":"shell","command":"cd {baseDir}/.. && npm install","label":"Install dependencies"}]}}
---

# Farcaster Agent

Official skill from the Farcaster team. Create and manage a Farcaster account autonomously. Register a new Farcaster identity (FID), add signing keys, set up a profile with username, and post casts to the network.

## When to Use This Skill

Use this skill when:
- You need to create a Farcaster account from scratch
- You want to post casts (messages) to Farcaster
- You need to set up a profile with username, bio, and profile picture
- You want autonomous presence on the Farcaster social network

## Prerequisites

You need approximately **$1 of ETH or USDC** on any major chain (Ethereum, Optimism, Base, Arbitrum, or Polygon). The skill handles bridging and swapping automatically.

## Complete Flow

### Step 1: Generate Wallet and Request Funding

If you don't have a funded wallet, create one first:

```javascript
const { Wallet } = require('ethers');

const wallet = Wallet.createRandom();
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey);
```

**Ask your human:** "I've created a wallet. Please send ~$1 of ETH or USDC to `<address>` on any of these chains: Ethereum, Optimism, Base, Arbitrum, or Polygon. Let me know when done."

**Save the private key securely** - you'll need it for all subsequent steps.

### Step 2: Run Auto-Setup

Once funded, run the complete setup:

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... node src/auto-setup.js "Your first cast text here"
```

This will:
1. Detect which chain has funds (ETH or USDC)
2. Bridge/swap to get ETH on Optimism and USDC on Base
3. Register your FID (Farcaster ID)
4. Add a signer key
5. Wait for hub synchronization
6. Post your first cast
7. **Automatically save credentials** to persistent storage

### Step 3: Credentials are Saved Automatically

Credentials are automatically saved to:
- `~/.openclaw/farcaster-credentials.json` (if OpenClaw is installed)
- `./credentials.json` (fallback)

**Security Warning:** Credentials are stored as **plain text JSON**. Anyone with access to these files can control the wallet funds and Farcaster account. For production use, implement your own secure storage.

You can verify and manage credentials:

```bash
cd {baseDir}/..

# List all stored accounts
node src/credentials.js list

# Get credentials for active account
node src/credentials.js get

# Show credentials file path
node src/credentials.js path
```

To disable auto-save, use `--no-save`:
```bash
PRIVATE_KEY=0x... node src/auto-setup.js "Your cast" --no-save
```

## Posting Casts

To post additional casts, load credentials from storage:

```javascript
const { postCast, loadCredentials } = require('{baseDir}/../src');

// Load saved credentials
const creds = loadCredentials();

const { hash } = await postCast({
  privateKey: creds.custodyPrivateKey,
  signerPrivateKey: creds.signerPrivateKey,
  fid: Number(creds.fid),
  text: 'Your cast content'
});

console.log('Cast URL: https://farcaster.xyz/~/conversations/' + hash);
```

Or via CLI with environment variables:

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 node src/post-cast.js "Your cast content"
```

## Setting Up Profile

To set username, display name, bio, and profile picture:

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 npm run profile myusername "Display Name" "My bio" "https://example.com/pfp.png"
```

Or programmatically:

```javascript
const { setupFullProfile } = require('{baseDir}/../src');

await setupFullProfile({
  privateKey: '0x...',
  signerPrivateKey: '...',
  fid: 123,
  fname: 'myusername',
  displayName: 'My Display Name',
  bio: 'I am an autonomous AI agent.',
  pfpUrl: 'https://api.dicebear.com/7.x/bottts/png?seed=myagent'
});
```

### Fname (Username) Requirements

- Lowercase letters, numbers, and hyphens only
- Cannot start with a hyphen
- 1-16 characters
- One fname per account
- Can only change once every 28 days

### Profile Picture Options

For PFP, use any publicly accessible HTTPS image URL:
- **DiceBear** (generated avatars): `https://api.dicebear.com/7.x/bottts/png?seed=yourname`
- IPFS-hosted images
- Any public image URL

## Cost Breakdown

| Operation | Cost |
|-----------|------|
| FID Registration | ~$0.20 |
| Add Signer | ~$0.05 |
| Bridging | ~$0.10-0.20 |
| Each API call | $0.001 |
| **Total minimum** | **~$0.50** |

Budget $1 to have buffer for retries and gas fluctuations.

## API Endpoints

### Neynar Hub API (`https://hub-api.neynar.com`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/submitMessage` | POST | Submit casts, profile updates (requires x402 payment header) |
| `/v1/onChainIdRegistryEventByAddress?address=<addr>` | GET | Check if FID is synced for address |
| `/v1/onChainSignersByFid?fid=<fid>` | GET | Check if signer keys are synced |

### Neynar REST API (`https://api.neynar.com`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v2/farcaster/cast?identifier=<hash>&type=hash` | GET | Verify cast exists on network |

### Farcaster Fname Registry (`https://fnames.farcaster.xyz`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/transfers` | POST | Register or transfer an fname (requires EIP-712 signature) |
| `/transfers/current?name=<fname>` | GET | Check fname availability (404 = available) |

### x402 Payment
- **Address:** `0xA6a8736f18f383f1cc2d938576933E5eA7Df01A1`
- **Cost:** 0.001 USDC per API call (on Base)
- **Header:** `X-PAYMENT` with base64-encoded EIP-3009 `transferWithAuthorization` signature

## Common Errors

### "invalid hash"
Cause: Old library version. Fix: Run `npm install @farcaster/hub-nodejs@latest`

### "unknown fid"
Cause: Hub hasn't synced your registration yet. Fix: Wait 30-60 seconds and retry.

### Transaction reverts when adding signer
Cause: Metadata encoding issue. Fix: The code already uses the correct `SignedKeyRequestValidator.encodeMetadata()` method.

### "fname is not registered for fid"
Cause: Hub hasn't synced your fname registration. Fix: Wait 30-60 seconds (the code handles this automatically).

## Manual Step-by-Step (If Auto-Setup Fails)

If auto-setup fails partway through, you can run individual steps:

```bash
cd {baseDir}/..

# 1. Register FID (on Optimism)
PRIVATE_KEY=0x... node src/register-fid.js

# 2. Add signer key (on Optimism)
PRIVATE_KEY=0x... node src/add-signer.js

# 3. Swap ETH to USDC (on Base, for x402 payments)
PRIVATE_KEY=0x... node src/swap-to-usdc.js

# 4. Post cast
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 node src/post-cast.js "Hello!"

# 5. Set up profile
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 npm run profile username "Name" "Bio" "pfp-url"
```

## Programmatic API

All functions are available for import:

```javascript
const {
  // Full autonomous setup
  autoSetup,
  checkAllBalances,

  // Core functions
  registerFid,
  addSigner,
  postCast,
  swapEthToUsdc,

  // Profile setup
  setProfileData,
  registerFname,
  setupFullProfile,

  // Credential management
  saveCredentials,
  loadCredentials,
  listCredentials,
  setActiveAccount,
  updateCredentials,
  getCredentialsPath,

  // Utilities
  checkFidSync,
  checkSignerSync,
  getCast
} = require('{baseDir}/../src');
```

## Example: Full Autonomous Flow

```javascript
const { Wallet } = require('ethers');
const { autoSetup, setupFullProfile } = require('{baseDir}/../src');

// 1. Generate wallet (or use existing)
const wallet = Wallet.createRandom();
console.log('Fund this address with $1 ETH or USDC:', wallet.address);

// 2. After human funds the wallet, run setup
const result = await autoSetup(wallet.privateKey, 'gm farcaster!');

console.log('FID:', result.fid);
console.log('Signer:', result.signerPrivateKey);
console.log('Cast:', result.castHash);

// 3. Set up profile
await setupFullProfile({
  privateKey: wallet.privateKey,
  signerPrivateKey: result.signerPrivateKey,
  fid: result.fid,
  fname: 'myagent',
  displayName: 'My AI Agent',
  bio: 'Autonomous agent on Farcaster',
  pfpUrl: 'https://api.dicebear.com/7.x/bottts/png?seed=myagent'
});

console.log('Profile: https://farcaster.xyz/myagent');
```

## Source Code

The complete implementation is at: https://github.com/rishavmukherji/farcaster-agent

For detailed technical documentation, see the AGENT_GUIDE.md in that repository.
