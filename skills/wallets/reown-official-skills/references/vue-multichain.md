# Vue + Multichain

> Support EVM + Solana + Bitcoin in a single Vue 3 app.

## Installation

```bash
# EVM + Solana
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana @tanstack/vue-query @wagmi/vue viem
```

## Configuration

```vue
<!-- App.vue -->
<script lang="ts" setup>
import { createAppKit } from '@reown/appkit/vue'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import {
  mainnet, arbitrum, base,
  solana, solanaTestnet, solanaDevnet
} from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const networks = [mainnet, arbitrum, base, solana, solanaTestnet, solanaDevnet]

const wagmiAdapter = new WagmiAdapter({ networks, projectId })
const solanaAdapter = new SolanaAdapter()

createAppKit({
  adapters: [wagmiAdapter, solanaAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Multichain dApp',
    description: 'Vue Multichain dApp',
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

## Using Chain-Specific Providers

```vue
<script lang="ts" setup>
import { useAppKitProvider, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/vue'

const { address, isConnected } = useAppKitAccount()
const { caipNetwork } = useAppKitNetwork()

// Access providers per namespace
const { walletProvider: evmProvider } = useAppKitProvider('eip155')
const { walletProvider: solanaProvider } = useAppKitProvider('solana')

const activeNamespace = computed(() => caipNetwork.value?.chainNamespace)
</script>

<template>
  <appkit-button />
  <div v-if="isConnected">
    <p>Address: {{ address }}</p>
    <p>Network: {{ caipNetwork?.name }}</p>
    <p>Namespace: {{ activeNamespace }}</p>
  </div>
</template>
```
