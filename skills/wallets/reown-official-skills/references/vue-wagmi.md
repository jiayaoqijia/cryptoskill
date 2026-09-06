# Vue + Wagmi

> EVM wallet connection in Vue 3 apps using Wagmi.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi @tanstack/vue-query @wagmi/vue viem
```

## Configuration

```vue
<!-- App.vue -->
<script lang="ts" setup>
import { createAppKit } from '@reown/appkit/vue'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'
import type { AppKitNetwork } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

const networks: [AppKitNetwork, ...AppKitNetwork[]] = [mainnet, arbitrum, base]

const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})

createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Vue dApp',
    description: 'Vue dApp with AppKit',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})
</script>

<template>
  <appkit-button />
  <RouterView />
</template>
```

## Using Composables

```vue
<script lang="ts" setup>
import { useAppKit, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/vue'
import { useDisconnect } from '@reown/appkit/vue'

const { open, close } = useAppKit()
const { address, isConnected, caipAddress } = useAppKitAccount()
const { caipNetwork, chainId, switchNetwork } = useAppKitNetwork()
const { disconnect } = useDisconnect()
</script>

<template>
  <div v-if="!isConnected">
    <button @click="open()">Connect Wallet</button>
  </div>
  <div v-else>
    <p>Address: {{ address }}</p>
    <p>Network: {{ caipNetwork?.name }}</p>
    <button @click="open({ view: 'Networks' })">Switch Network</button>
    <button @click="disconnect()">Disconnect</button>
  </div>
</template>
```

## Smart Contract Interaction

```vue
<script lang="ts" setup>
import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/vue'
import { BrowserProvider, Contract, formatEther, parseEther } from 'ethers'

const { walletProvider } = useAppKitProvider('eip155')
const { address, isConnected } = useAppKitAccount()

async function getBalance() {
  if (!walletProvider.value) return
  const provider = new BrowserProvider(walletProvider.value)
  const balance = await provider.getBalance(address.value!)
  console.log(formatEther(balance))
}

async function sendTransaction() {
  if (!walletProvider.value) return
  const provider = new BrowserProvider(walletProvider.value)
  const signer = await provider.getSigner()
  const tx = await signer.sendTransaction({
    to: '0x...',
    value: parseEther('0.01'),
  })
  await tx.wait()
}
</script>
```

Note: Vue composables return reactive `ref` values — access them with `.value` in script, directly in template.
