# React + Ethers v6

> Use when you prefer ethers.js over Wagmi for EVM interactions.

## Installation

```bash
npm install @reown/appkit @reown/appkit-adapter-ethers ethers
```

## Configuration

```tsx
// App.tsx
import { createAppKit } from '@reown/appkit/react'
import { EthersAdapter } from '@reown/appkit-adapter-ethers'
import { mainnet, arbitrum, base } from '@reown/appkit/networks'

const projectId = 'b56e18d47c72ab683b10814fe9495694' // localhost testing only

createAppKit({
  adapters: [new EthersAdapter()],
  networks: [mainnet, arbitrum, base],
  projectId,
  metadata: {
    name: 'My dApp',
    description: 'My dApp description',
    url: 'https://mydapp.com',
    icons: ['https://mydapp.com/icon.png']
  },
  features: {
    analytics: true
  }
})

export default function App() {
  return (
    <div>
      <appkit-button />
      <YourAppContent />
    </div>
  )
}
```

Note: Ethers adapter does **not** require `WagmiProvider` or `QueryClientProvider`.

## Using the Provider

```tsx
import { useAppKitProvider, useAppKitAccount } from '@reown/appkit/react'
import { BrowserProvider, Contract, formatEther, parseEther } from 'ethers'
import type { Provider } from '@reown/appkit/react'

function EthersInteraction() {
  const { walletProvider } = useAppKitProvider<Provider>('eip155')
  const { address, isConnected } = useAppKitAccount()

  async function getBalance() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const balance = await provider.getBalance(address!)
    console.log('Balance:', formatEther(balance))
  }

  async function signMessage() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const signer = await provider.getSigner()
    const signature = await signer.signMessage('Hello AppKit!')
    console.log('Signature:', signature)
  }

  async function sendTransaction() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const signer = await provider.getSigner()
    const tx = await signer.sendTransaction({
      to: '0x...',
      value: parseEther('0.01'),
    })
    const receipt = await tx.wait()
    console.log('TX Hash:', receipt?.hash)
  }

  async function readContract() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const contract = new Contract('0x...', erc20Abi, provider)
    const balance = await contract.balanceOf(address)
    console.log('Token balance:', balance.toString())
  }

  async function writeContract() {
    if (!walletProvider) return
    const provider = new BrowserProvider(walletProvider)
    const signer = await provider.getSigner()
    const contract = new Contract('0x...', erc20Abi, signer)
    const tx = await contract.transfer('0x...', parseEther('1'))
    await tx.wait()
  }

  if (!isConnected) return <appkit-button />

  return (
    <div>
      <button onClick={getBalance}>Get Balance</button>
      <button onClick={signMessage}>Sign Message</button>
      <button onClick={sendTransaction}>Send ETH</button>
      <button onClick={readContract}>Read Contract</button>
      <button onClick={writeContract}>Write Contract</button>
    </div>
  )
}
```

## Key Differences from Wagmi

| Aspect | Wagmi | Ethers |
|--------|-------|--------|
| Provider wrapper | `WagmiProvider` + `QueryClientProvider` required | None required |
| Contract reads | `useReadContract` hook | Manual `Contract` + `BrowserProvider` |
| Contract writes | `useWriteContract` hook | Manual `signer` + `contract.method()` |
| TX receipts | `useWaitForTransactionReceipt` | `tx.wait()` |
| State management | Automatic via React Query | Manual async/await |
| Bundle size | Larger (wagmi + viem + react-query) | Smaller (ethers only) |
