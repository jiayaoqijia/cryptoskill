---
name: connect-wallet
description: >-
  Guides integrating a Cardano wallet into a web dApp using CIP-30. Triggers: "connect wallet", "CIP-30", "wallet integration", "browser wallet", "sign transaction", "wallet connector", "dApp wallet", "Nami", "Eternl", "Lace".
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Connect a Cardano Wallet to a Web dApp

Help the developer integrate a Cardano browser wallet into their web application using the CIP-30 standard.

## When to use

- Developer needs to connect a Cardano wallet to a web dApp
- Implementing CIP-30 wallet bridge in any web framework
- Reading wallet state (balance, UTxOs, addresses)
- Building and signing transactions through the wallet
- Adding CIP-95 governance capabilities to wallet integration
- Troubleshooting wallet connection issues

## When NOT to use

- Building a wallet application itself
- Server-side transaction building without browser wallet
- Mobile wallet integration (different approach)
- Choosing which tools to use (use `suggest-tooling` skill)
- Understanding governance concepts (use `governance-guide` skill)

## Key principles

1. **CIP-30 is the standard.** All major Cardano browser wallets implement it. Build against the standard, not a specific wallet.
2. **Use an SDK when possible.** Mesh SDK and others abstract CIP-30 complexity. Only use raw CIP-30 when you need fine control.
3. **Handle multiple wallets.** Users may have several wallet extensions. Let them choose.
4. **Always handle errors gracefully.** Wallets can refuse connections, reject signatures, or be unavailable.
5. **Test with multiple wallets.** Each wallet has subtle differences in CIP-30 implementation.

## Workflow

### Step 1: Identify the setup

Ask the developer (if not already clear):

- **What framework are you using?** (react | nextjs | svelte | vue | vanilla-js)
- **Which SDK do you prefer?** (mesh | evolution-sdk | none/raw CIP-30)
- **What do you need to do?** (connect only | read state | sign transactions | governance)
- **Which network?** (mainnet | preprod | preview | local devnet)

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk/` - Mesh SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cips/` - CIP specifications (CIP-30, CIP-95)

### Step 3: CIP-30 basics

Reference the CIP-30 API reference for the full specification:

```
File: skills/connect-wallet/references/cip30-api-reference.md
```

#### How CIP-30 works

1. Wallet extensions inject themselves into `window.cardano.<walletName>`
2. Each wallet provides an `enable()` method that requests user permission
3. Once enabled, the wallet returns an API object with methods for reading state and signing
4. The dApp never has access to private keys -- the wallet signs internally

#### Discovering available wallets

```javascript
// List all available Cardano wallets
const availableWallets = [];
for (const key in window.cardano) {
  if (window.cardano[key]?.enable && window.cardano[key]?.name) {
    availableWallets.push({
      id: key,
      name: window.cardano[key].name,
      icon: window.cardano[key].icon,
    });
  }
}
```

### Step 4: Framework-specific integration

#### React with Mesh SDK (recommended for React)

```bash
npm install @meshsdk/react @meshsdk/core
```

```tsx
// App.tsx - Wrap with MeshProvider
import { MeshProvider } from "@meshsdk/react";

function App() {
  return (
    <MeshProvider>
      <MyDApp />
    </MeshProvider>
  );
}
```

```tsx
// WalletConnect.tsx
import { CardanoWallet, useWallet } from "@meshsdk/react";

function WalletConnect() {
  const { connected, wallet } = useWallet();

  const readBalance = async () => {
    if (!connected) return;
    const balance = await wallet.getBalance();
    console.log("Balance:", balance);
  };

  return (
    <div>
      <CardanoWallet />
      {connected && <button onClick={readBalance}>Get Balance</button>}
    </div>
  );
}
```

#### Next.js with Mesh SDK

```bash
npm install @meshsdk/react @meshsdk/core
```

Important: CIP-30 requires `window`, so wallet code must be client-side only.

```tsx
// components/WalletButton.tsx
"use client";
import dynamic from "next/dynamic";

const CardanoWallet = dynamic(
  () => import("@meshsdk/react").then((mod) => mod.CardanoWallet),
  { ssr: false }
);

export default function WalletButton() {
  return <CardanoWallet />;
}
```

```tsx
// app/layout.tsx or _app.tsx
"use client";
import { MeshProvider } from "@meshsdk/react";

export default function Layout({ children }) {
  return <MeshProvider>{children}</MeshProvider>;
}
```

#### Svelte (raw CIP-30 or with SDK)

```svelte
<script>
  let wallet = null;
  let connected = false;
  let availableWallets = [];

  import { onMount } from "svelte";

  onMount(() => {
    // Discover wallets after DOM load
    for (const key in window.cardano) {
      if (window.cardano[key]?.enable) {
        availableWallets.push(key);
      }
    }
    availableWallets = availableWallets;
  });

  async function connect(walletName) {
    try {
      wallet = await window.cardano[walletName].enable();
      connected = true;
    } catch (e) {
      console.error("Connection refused:", e);
    }
  }
</script>

{#each availableWallets as w}
  <button on:click={() => connect(w)}>{w}</button>
{/each}
```

#### Vue

```vue
<template>
  <div>
    <button v-for="w in wallets" :key="w" @click="connect(w)">
      {{ w }}
    </button>
    <p v-if="connected">Connected!</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const wallets = ref([]);
const wallet = ref(null);
const connected = ref(false);

onMounted(() => {
  for (const key in window.cardano) {
    if (window.cardano[key]?.enable) {
      wallets.value.push(key);
    }
  }
});

async function connect(name) {
  try {
    wallet.value = await window.cardano[name].enable();
    connected.value = true;
  } catch (e) {
    console.error("Connection refused:", e);
  }
}
</script>
```

#### Vanilla JavaScript

```html
<div id="wallet-buttons"></div>
<script>
  window.addEventListener("load", () => {
    const container = document.getElementById("wallet-buttons");
    for (const key in window.cardano) {
      if (window.cardano[key]?.enable) {
        const btn = document.createElement("button");
        btn.textContent = window.cardano[key].name || key;
        btn.onclick = async () => {
          try {
            const api = await window.cardano[key].enable();
            console.log("Connected:", api);
            // Use api.getBalance(), api.getUtxos(), etc.
          } catch (e) {
            console.error("Refused:", e);
          }
        };
        container.appendChild(btn);
      }
    }
  });
</script>
```

### Step 5: Reading wallet state

Once connected (via SDK or raw API):

```javascript
// Using raw CIP-30 API object
const networkId = await api.getNetworkId();     // 0 = testnet, 1 = mainnet
const balance = await api.getBalance();          // CBOR-encoded Value
const utxos = await api.getUtxos();              // Array of CBOR-encoded UTxOs
const usedAddresses = await api.getUsedAddresses(); // Array of CBOR addresses
const changeAddress = await api.getChangeAddress();  // CBOR address

// Using Mesh SDK (already decoded)
const balance = await wallet.getBalance();       // Array of { unit, quantity }
const utxos = await wallet.getUtxos();           // Decoded UTxO objects
const addresses = await wallet.getUsedAddresses(); // Bech32 addresses
```

> Note: these Mesh examples target the released `@meshsdk/*` 1.9.x (npm
> `latest`). Mesh 2.0 (currently beta-only) renames the wallet API
> (`MeshCardanoBrowserWallet`, `getBalanceMesh()`, `getChangeAddressBech32()`,
> …) — don't mix the two API generations.

### Step 6: Building, signing, and submitting transactions

#### With Mesh SDK

```typescript
import { MeshTxBuilder, MeshWallet } from "@meshsdk/core";

const txBuilder = new MeshTxBuilder({ fetcher: provider });

// Simple ADA transfer
const tx = await txBuilder
  .txOut(recipientAddress, [{ unit: "lovelace", quantity: "5000000" }])
  .changeAddress(await wallet.getChangeAddress())
  .selectUtxosFrom(await wallet.getUtxos())
  .complete();

const signedTx = await wallet.signTx(tx);
const txHash = await wallet.submitTx(signedTx);
```

#### With Evolution SDK

Evolution SDK's CIP-30 client is **signing-only by design** — it carries no provider, so the browser cannot build or submit transactions itself. A provider-backed backend builds the unsigned transaction and submits the signed one; the wallet only signs. (See `wallets/api-wallet.mdx` in the bundled docs.)

```typescript
import { Client, Transaction, TransactionWitnessSet, mainnet } from "@evolution-sdk/evolution";

// Connect the browser wallet, then create a signing-only client (no provider).
const walletApi = await window.cardano.eternl.enable();
const client = Client.make(mainnet).withCip30(walletApi);

// `unsignedTxCbor` comes from your backend's provider-backed transaction builder.
const witnessSet = await client.signTx(unsignedTxCbor); // prompts the user
const signedTxCbor = Transaction.addVKeyWitnessesHex(
  unsignedTxCbor,
  TransactionWitnessSet.toCBORHex(witnessSet),
);
// POST signedTxCbor back to the backend for provider-backed submission.
```

#### With raw CIP-30

```javascript
// Build tx using any serialization library, get CBOR hex
const unsignedTxCbor = buildTransaction(/* ... */);

// Sign via wallet
const witnessSetCbor = await api.signTx(unsignedTxCbor, false);

// Assemble and submit
const signedTxCbor = assembleTx(unsignedTxCbor, witnessSetCbor);
const txHash = await api.submitTx(signedTxCbor);
```

### Step 7: Message signing (CIP-8)

Wallets can sign arbitrary data — not just transactions — to prove the user controls an address. This backs "sign in with wallet" logins, attestations, and off-chain authorization. No transaction, no fee.

```javascript
// Raw CIP-30 — returns a COSE_Sign1 signature + key
const { signature, key } = await api.signData(addressHex, payloadHex);
```

Evolution SDK exposes this as `client.signMessage(payload)` on a CIP-30 client, and ships `COSE.SignData.verifyData(...)` to verify a signature server-side (see `wallets/message-signing.mdx` in the bundled docs). Always verify server-side — a signature proves key ownership only once you check it against the claimed address.

### Step 8: CIP-95 governance extensions

For dApps that need governance features (DRep registration, voting, delegation):

```javascript
// Enable with CIP-95 extensions
const api = await window.cardano[walletName].enable({
  extensions: [{ cip: 95 }]
});

// CIP-95 methods (if supported by wallet)
const pubDRepKey = await api.cip95.getPubDRepKey();
const registeredPubStakeKeys = await api.cip95.getRegisteredPubStakeKeys();
const unregisteredPubStakeKeys = await api.cip95.getUnregisteredPubStakeKeys();
```

Not all wallets support CIP-95 yet. Check wallet compatibility before relying on it. Wallets listed as CIP-95 implementors in the spec: Eternl, GeroWallet, Lace, NuFi, Typhon, Vespr, Yoroi — but verify against the spec's Implementors list (`docs/sources/cips/CIP-0095/README.md`) rather than trusting a static list.

### Step 9: Common issues and solutions

| Issue | Cause | Solution |
|---|---|---|
| `window.cardano` is undefined | No wallet installed, or SSR | Check for `window` existence; use dynamic imports in Next.js |
| `enable()` throws error | User rejected connection | Show friendly message, allow retry |
| Wrong network | Wallet on different network | Check `getNetworkId()` and show warning |
| `signTx()` fails | Invalid transaction CBOR | Validate tx before sending to wallet; check collateral |
| UTxOs empty after tx | Node not synced | Wait a block, re-query; some providers lag |
| Multiple wallets conflict | Wallet detection order | Let user explicitly choose which wallet |
| CORS errors | API proxy needed | Use backend proxy for chain data; wallet calls are local |
| Balance shows CBOR | Using raw CIP-30 | Decode CBOR with a serialization library or use an SDK |
| `submitTx()` fails | Insufficient funds, bad fee | Build tx with proper fee estimation; ensure enough UTxOs |
| Wallet not detected on page load | Extension loads asynchronously | Add a short delay or poll for `window.cardano` |

## References

- `skills/connect-wallet/references/cip30-api-reference.md` -- Full CIP-30 API reference
- CIP-30 specification: https://github.com/cardano-foundation/CIPs/tree/master/CIP-0030
- CIP-95 specification: https://github.com/cardano-foundation/CIPs/tree/master/CIP-0095
- Mesh SDK docs: https://meshjs.dev
- Evolution SDK: https://github.com/IntersectMBO/evolution-sdk
