# Nuxt + Wagmi

> EVM wallet connection in Nuxt 3 apps.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @wagmi/vue @tanstack/vue-query
```

## Step 1 — Nuxt Config

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: false,
  modules: ['@wagmi/vue/nuxt'],
  runtimeConfig: {
    public: {
      projectId: process.env.NUXT_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only,
    },
  },
})
```

Note: `ssr: false` is required. The `@wagmi/vue/nuxt` module is needed for Wagmi.

## Step 2 — Plugins (Wagmi-specific)

```ts
// plugins/1.vue-query.ts
import { defineNuxtPlugin } from '#imports'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'

export default defineNuxtPlugin((nuxt) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { staleTime: 5000 } },
  })

  nuxt.vueApp.use(VueQueryPlugin, {
    queryClient,
    enableDevtoolsV6Plugin: true,
  })
})
```

```ts
// plugins/2.wagmi.ts
import { WagmiPlugin } from '@wagmi/vue'
import { defineNuxtPlugin } from 'nuxt/app'
import { wagmiAdapter } from '~/config/appkit'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(WagmiPlugin, { config: wagmiAdapter.wagmiConfig })
})
```

## Step 3 — AppKit Config

```ts
// config/appkit.ts
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

export const projectId = process.env.NUXT_PROJECT_ID || 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
export const networks = [mainnet, arbitrum, base]

export const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})
```

## Step 4 — App Setup

```vue
<!-- app.vue -->
<script setup lang="ts">
import { createAppKit } from '@reown/appkit/vue'
import { wagmiAdapter, networks, projectId } from './config/appkit'

createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Nuxt dApp',
    description: 'Nuxt dApp with AppKit',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
})
</script>

<template>
  <client-only>
    <appkit-button />
    <NuxtPage />
  </client-only>
</template>
```

## Step 5 — Page Component

```vue
<!-- pages/index.vue -->
<script lang="ts" setup>
import { useAppKit, useAppKitAccount, useAppKitNetwork } from '@reown/appkit/vue'

const { open } = useAppKit()
const { address, isConnected } = useAppKitAccount()
const { caipNetwork } = useAppKitNetwork()
</script>

<template>
  <div>
    <div v-if="isConnected">
      <p>Address: {{ address }}</p>
      <p>Network: {{ caipNetwork?.name }}</p>
    </div>
    <button @click="open()">Connect</button>
    <button @click="open({ view: 'Networks' })">Networks</button>
  </div>
</template>
```

## Environment Variables

```bash
# .env
NUXT_PROJECT_ID=b56e18d47c72ab683b10814fe9495694 # localhost testing only
```

## Ethers Variant (simpler — no plugins needed)

```vue
<!-- app.vue -->
<script setup lang="ts">
import { createAppKit } from '@reown/appkit/vue'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum } from '@reown/appkit/networks'

const config = useRuntimeConfig()

createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum],
  projectId: config.public.projectId,
  metadata: {
    name: 'My Nuxt dApp',
    description: 'Nuxt + Ethers',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
})
</script>

<template>
  <client-only>
    <appkit-button />
    <NuxtPage />
  </client-only>
</template>
```

For Ethers, remove `@wagmi/vue/nuxt` module and both plugins. Only need `ssr: false` and `runtimeConfig` in `nuxt.config.ts`.

## Nuxt-Specific Checklist

- [ ] `ssr: false` in `nuxt.config.ts`
- [ ] All AppKit components wrapped in `<client-only>`
- [ ] For Wagmi: `@wagmi/vue/nuxt` module + numbered plugins for Vue Query and WagmiPlugin
- [ ] For Ethers/Solana: no modules or plugins needed
- [ ] Project ID via `useRuntimeConfig().public.projectId`
