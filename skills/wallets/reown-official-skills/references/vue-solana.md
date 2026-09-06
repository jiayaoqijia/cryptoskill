# Vue + Solana

> Connect Solana wallets in Vue 3 apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-solana
```

## Configuration

```vue
<!-- App.vue -->
<script lang="ts" setup>
import { createAppKit } from '@reown/appkit/vue'
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import { solana, solanaTestnet, solanaDevnet } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [solanaAdapter],
  networks: [solana, solanaTestnet, solanaDevnet],
  projectId,
  metadata: {
    name: 'My Solana dApp',
    description: 'Vue Solana dApp',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
})
</script>

<template>
  <appkit-button />
  <RouterView />
</template>
```

## Using the Provider

```vue
<script lang="ts" setup>
import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/vue'
import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js'

const { walletProvider } = useAppKitProvider('solana')
const { address, isConnected } = useAppKitAccount()

async function getBalance() {
  if (!address.value) return
  const connection = new Connection('https://api.mainnet-beta.solana.com')
  const balance = await connection.getBalance(new PublicKey(address.value))
  console.log('Balance:', balance / LAMPORTS_PER_SOL, 'SOL')
}

async function signMessage() {
  if (!walletProvider.value) return
  const encoded = new TextEncoder().encode('Hello Solana!')
  const sig = await walletProvider.value.signMessage(encoded)
  console.log('Signature:', sig)
}
</script>

<template>
  <div v-if="isConnected">
    <p>{{ address }}</p>
    <button @click="getBalance">Get Balance</button>
    <button @click="signMessage">Sign Message</button>
  </div>
</template>
```
