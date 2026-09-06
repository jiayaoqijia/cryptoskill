# JavaScript + Wagmi

> Framework-agnostic EVM wallet connection using vanilla JavaScript with Wagmi.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem
```

## Configuration

```js
// main.js
import { createAppKit } from '@reown/appkit'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const networks = [mainnet, arbitrum, base]

const wagmiAdapter = new WagmiAdapter({
  networks,
  projectId,
})

const modal = createAppKit({
  adapters: [wagmiAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My dApp',
    description: 'Vanilla JS dApp',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})
```

Note: Import from `@reown/appkit` (not `/react` or `/vue`).

## HTML

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>My dApp</title>
</head>
<body>
  <appkit-button></appkit-button>

  <button id="connect-btn">Connect</button>
  <button id="network-btn">Switch Network</button>
  <div id="account-info"></div>

  <script type="module" src="main.js"></script>
</body>
</html>
```

## Programmatic Modal Control

```js
// Open connect modal
document.getElementById('connect-btn').addEventListener('click', () => {
  modal.open()
})

// Open network selector
document.getElementById('network-btn').addEventListener('click', () => {
  modal.open({ view: 'Networks' })
})
```

## Subscribe to State Changes

```js
// Subscribe to account changes
modal.subscribeAccount((account) => {
  const el = document.getElementById('account-info')
  if (account.isConnected) {
    el.textContent = `Connected: ${account.address}`
  } else {
    el.textContent = 'Not connected'
  }
})

// Subscribe to network changes
modal.subscribeNetwork((network) => {
  console.log('Network:', network.caipNetwork?.name)
})
```

## Smart Contract Interaction (Wagmi Core)

```bash
npm install @wagmi/core
```

```js
import { readContract, writeContract, waitForTransactionReceipt } from '@wagmi/core'

// Read
const balance = await readContract(wagmiAdapter.wagmiConfig, {
  address: '0x...',
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: ['0x...'],
})

// Write
const hash = await writeContract(wagmiAdapter.wagmiConfig, {
  address: '0x...',
  abi: erc20Abi,
  functionName: 'transfer',
  args: ['0x...', 1000000n],
})

const receipt = await waitForTransactionReceipt(wagmiAdapter.wagmiConfig, { hash })
```
