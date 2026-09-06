# JavaScript + Ethers v6

> Framework-agnostic EVM wallet connection using vanilla JavaScript with ethers.js.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-ethers ethers
```

## Configuration

```js
// main.js
import { createAppKit } from '@reown/appkit'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

const modal = createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum, base],
  projectId,
  metadata: {
    name: 'My dApp',
    description: 'Vanilla JS dApp with Ethers',
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
  <title>My dApp</title>
</head>
<body>
  <appkit-button></appkit-button>
  <button id="get-balance">Get Balance</button>
  <button id="sign-msg">Sign Message</button>
  <button id="send-tx">Send ETH</button>
  <div id="output"></div>
  <script type="module" src="main.js"></script>
</body>
</html>
```

## Using the Provider

```js
import { BrowserProvider, formatEther, parseEther } from 'ethers'

// Wait for connection
modal.subscribeAccount(async (account) => {
  if (!account.isConnected) return

  // Get the EVM provider from the modal
  const provider = modal.getWalletProvider()
  if (!provider) return

  const ethersProvider = new BrowserProvider(provider)

  // Get balance
  document.getElementById('get-balance').addEventListener('click', async () => {
    const balance = await ethersProvider.getBalance(account.address)
    document.getElementById('output').textContent =
      `Balance: ${formatEther(balance)} ETH`
  })

  // Sign message
  document.getElementById('sign-msg').addEventListener('click', async () => {
    const signer = await ethersProvider.getSigner()
    const sig = await signer.signMessage('Hello from vanilla JS!')
    document.getElementById('output').textContent = `Signature: ${sig}`
  })

  // Send transaction
  document.getElementById('send-tx').addEventListener('click', async () => {
    const signer = await ethersProvider.getSigner()
    const tx = await signer.sendTransaction({
      to: '0x...',
      value: parseEther('0.01'),
    })
    const receipt = await tx.wait()
    document.getElementById('output').textContent = `TX: ${receipt.hash}`
  })
})
```
