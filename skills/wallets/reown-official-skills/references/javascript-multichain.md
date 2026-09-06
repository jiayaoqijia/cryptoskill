# JavaScript + Multichain

> Support EVM + Solana + Bitcoin in vanilla JavaScript without a framework.

## Installation

```bash
# EVM + Solana
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana wagmi viem

# EVM + Solana + Bitcoin
npm install @reown/appkit @reown/appkit-adapter-wagmi @reown/appkit-adapter-solana @reown/appkit-adapter-bitcoin wagmi viem
```

## Configuration

```js
// main.js
import { createAppKit } from '@reown/appkit'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import { BitcoinAdapter } from '@reown/appkit-adapter-bitcoin'
import {
  mainnet, arbitrum, base,
  solana, solanaDevnet,
  bitcoin, bitcoinTestnet
} from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const networks = [mainnet, arbitrum, base, solana, solanaDevnet, bitcoin, bitcoinTestnet]

const wagmiAdapter = new WagmiAdapter({ networks, projectId })
const solanaAdapter = new SolanaAdapter()
const bitcoinAdapter = new BitcoinAdapter({ projectId })

const modal = createAppKit({
  adapters: [wagmiAdapter, solanaAdapter, bitcoinAdapter],
  networks,
  projectId,
  metadata: {
    name: 'My Multichain dApp',
    description: 'Vanilla JS Multichain dApp',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})
```

## HTML

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Multichain dApp</title>
</head>
<body>
  <appkit-button></appkit-button>
  <div id="account-info"></div>
  <div id="network-info"></div>
  <script type="module" src="main.js"></script>
</body>
</html>
```

## Subscribe to State

```js
modal.subscribeAccount((account) => {
  const el = document.getElementById('account-info')
  if (account.isConnected) {
    el.textContent = `Connected: ${account.address}`
  } else {
    el.textContent = 'Not connected'
  }
})

modal.subscribeNetwork((network) => {
  const el = document.getElementById('network-info')
  el.textContent = `Network: ${network.caipNetwork?.name} (${network.caipNetwork?.chainNamespace})`
})
```

## Chain-Specific Interactions

Detect the active namespace and use the appropriate provider:

```js
modal.subscribeNetwork((network) => {
  const namespace = network.caipNetwork?.chainNamespace
  const provider = modal.getWalletProvider()

  switch (namespace) {
    case 'eip155':
      // Use ethers.js or @wagmi/core
      break
    case 'solana':
      // Use @solana/web3.js
      break
    case 'bip122':
      // Use Bitcoin provider methods
      break
  }
})
```
