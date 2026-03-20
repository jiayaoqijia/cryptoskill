# SushiSwap SDK Reference

This document provides practical examples for interacting with the SushiSwap
Aggregator using the Sushi SDK.

The SDK functions shown here are thin wrappers around the SushiSwap REST API and
are provided for convenience. All swap execution data ultimately comes from the
API.

---

## Getting a Swap Quote

Use `getQuote` to retrieve pricing, routing, and estimated output information for
a token swap.

This endpoint is read-only and does not generate executable transaction data.

```ts
import { getQuote, EvmChainId } from 'sushi/evm'

const data = await getQuote({
  chainId: EvmChainId.ETHEREUM,
  tokenIn: '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
  tokenOut: '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',
  amount: 1000000000000000000n,
  maxSlippage: 0.005,
})

```

---

## Generating and Executing a Swap

Use `getSwap` to generate executable transaction data for a swap.

The API returns calldata that must be used exactly as provided.

```ts
import { getSwap, EvmChainId } from 'sushi/evm'
import { createPublicClient, createWalletClient, http, type Hex } from 'viem'
import { privateKeyToAccount } from 'viem/accounts'
import { mainnet } from 'viem/chains'

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(),
})

const data = await getSwap({
  chainId: EvmChainId.ETHEREUM,
  tokenIn: '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
  tokenOut: '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',
  sender: '0xYourAddressHere',
  amount: 1000000000000000000n,
  maxSlippage: 0.005,
})

if (data.status === 'Success') {
  const { tx } = data

  const callResult = await publicClient.call({
    account: tx.from,
    data: tx.data,
    to: tx.to,
    value: tx.value,
  })

  console.log('Simulated output:', callResult)

  const PRIVATE_KEY = process.env.PRIVATE_KEY as Hex
  const walletClient = createWalletClient({
    chain: mainnet,
    transport: http(),
  })

  const hash = await walletClient.sendTransaction({
    account: privateKeyToAccount(PRIVATE_KEY),
    data: tx.data,
    to: tx.to,
    value: tx.value,
  })

  console.log('Tx:', hash)
}
```
