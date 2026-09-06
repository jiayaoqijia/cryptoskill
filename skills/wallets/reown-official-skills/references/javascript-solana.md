# JavaScript + Solana

> Framework-agnostic Solana wallet connection using vanilla JavaScript.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-solana
```

## Configuration

```js
// main.js
import { createAppKit } from '@reown/appkit'
import { SolanaAdapter } from '@reown/appkit-adapter-solana'
import { solana, solanaTestnet, solanaDevnet } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only
const solanaAdapter = new SolanaAdapter()

const modal = createAppKit({
  adapters: [solanaAdapter],
  networks: [solana, solanaTestnet, solanaDevnet],
  projectId,
  metadata: {
    name: 'My Solana dApp',
    description: 'Vanilla JS Solana dApp',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
})
```

## HTML

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Solana dApp</title>
</head>
<body>
  <appkit-button></appkit-button>
  <button id="get-balance">Get Balance</button>
  <button id="sign-msg">Sign Message</button>
  <div id="output"></div>
  <script type="module" src="main.js"></script>
</body>
</html>
```

## Using the Provider

```js
import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js'

modal.subscribeAccount(async (account) => {
  if (!account.isConnected) return

  const provider = modal.getWalletProvider()
  if (!provider) return

  document.getElementById('get-balance').addEventListener('click', async () => {
    const connection = new Connection('https://api.mainnet-beta.solana.com')
    const balance = await connection.getBalance(new PublicKey(account.address))
    document.getElementById('output').textContent =
      `Balance: ${balance / LAMPORTS_PER_SOL} SOL`
  })

  document.getElementById('sign-msg').addEventListener('click', async () => {
    const encoded = new TextEncoder().encode('Hello Solana!')
    const sig = await provider.signMessage(encoded)
    document.getElementById('output').textContent = `Signed!`
  })
})
```
