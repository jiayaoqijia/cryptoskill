# Vue + Ethers v6

> EVM wallet connection in Vue 3 apps using ethers.js.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-ethers ethers
```

## Configuration

```vue
<!-- App.vue -->
<script lang="ts" setup>
import { createAppKit } from '@reown/appkit/vue'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum, base],
  projectId,
  metadata: {
    name: 'My Vue dApp',
    description: 'Vue dApp with Ethers',
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

Note: Ethers adapter does **not** require Wagmi or TanStack Query packages.

## Using the Provider

```vue
<script lang="ts" setup>
import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/vue'
import { BrowserProvider, formatEther, parseEther } from 'ethers'

const { walletProvider } = useAppKitProvider('eip155')
const { address, isConnected } = useAppKitAccount()

async function getBalance() {
  if (!walletProvider.value) return
  const provider = new BrowserProvider(walletProvider.value)
  const balance = await provider.getBalance(address.value!)
  console.log(formatEther(balance))
}

async function signMessage() {
  if (!walletProvider.value) return
  const provider = new BrowserProvider(walletProvider.value)
  const signer = await provider.getSigner()
  const sig = await signer.signMessage('Hello from Vue!')
  console.log(sig)
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

<template>
  <div v-if="isConnected">
    <p>{{ address }}</p>
    <button @click="getBalance">Get Balance</button>
    <button @click="signMessage">Sign</button>
    <button @click="sendTransaction">Send ETH</button>
  </div>
</template>
```
