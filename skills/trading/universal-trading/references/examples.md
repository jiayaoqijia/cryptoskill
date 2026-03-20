# Code Examples

## Buy Meme Token on Solana

```typescript
import { config } from 'dotenv';
import { CHAIN_ID, UniversalAccount } from '@particle-network/universal-account-sdk';
import { getBytes, Wallet } from 'ethers';

config();

(async () => {
    const wallet = new Wallet(process.env.PRIVATE_KEY || '');
    const universalAccount = new UniversalAccount({
        projectId: process.env.PROJECT_ID || '',
        projectClientKey: process.env.PROJECT_CLIENT_KEY || '',
        projectAppUuid: process.env.PROJECT_APP_UUID || '',
        ownerAddress: wallet.address,
        tradeConfig: {
            slippageBps: 500, // 5% slippage for meme
            universalGas: true,
            solanaMEVTipAmount: 0.001, // 0.001 SOL tip
        },
    });

    // Trump token example
    const tokenAddress = '6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN';
    
    const transaction = await universalAccount.createBuyTransaction(
        {
            token: { chainId: CHAIN_ID.SOLANA_MAINNET, address: tokenAddress },
            amountInUSD: '10', // Buy $10 worth
        },
        { addressLookupTableAccountAddresses: [] },
    );

    const sendResult = await universalAccount.sendTransaction(
        transaction, 
        wallet.signMessageSync(getBytes(transaction.rootHash))
    );

    console.log('Transaction ID:', sendResult.transactionId);
    console.log('Explorer:', `https://universalx.app/activity/details?id=${sendResult.transactionId}`);
})();
```

## Sell Token

```typescript
const transaction = await universalAccount.createSellTransaction({
    token: { chainId: CHAIN_ID.SOLANA_MAINNET, address: 'TOKEN_ADDRESS' },
    amount: '100', // Sell 100 tokens (check decimals)
});

const sendResult = await universalAccount.sendTransaction(
    transaction,
    wallet.signMessageSync(getBytes(transaction.rootHash))
);
```

## Swap USDC to USDT

```typescript
const transaction = await universalAccount.createConvertTransaction(
    {
        expectToken: { type: SUPPORTED_TOKEN_TYPE.USDT, amount: '100' },
        chainId: CHAIN_ID.SOLANA_MAINNET,
    }
);
```

## Transfer SOL

```typescript
const transaction = await universalAccount.createTransferTransaction({
    token: { chainId: CHAIN_ID.SOLANA_MAINNET, address: '0x0000000000000000000000000000000000000000' },
    amount: '0.1',
    receiver: 'RECIPIENT_ADDRESS',
});
```

## Get All Balances

```typescript
const assets = await universalAccount.getPrimaryAssets();

console.log('Total USD:', assets.totalAmountInUSD);
for (const asset of assets.assets) {
    console.log(`${asset.tokenType}: ${asset.amount} ($${asset.amountInUSD})`);
}
```

## Monitor Transaction Status (WebSocket)

```typescript
import WebSocket from 'ws';

const ws = new WebSocket('wss://universal-app-ws-proxy.particle.network');

ws.on('open', () => {
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'address-update',
        params: { addresses: ['YOUR_SOLANA_ADDRESS'] }
    }));
});

ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    
    if (msg.type === 'transaction_update') {
        const { transactionId, status } = msg.data;
        if (status === 7) {
            console.log(`✅ Transaction ${transactionId} succeeded!`);
        } else if (status === 11) {
            console.log(`❌ Transaction ${transactionId} failed!`);
        }
    }
});
```

## Full Meme Trading Workflow

```typescript
async function tradeMeme(tokenAddress: string, usdAmount: string, isBuy: boolean) {
    const wallet = new Wallet(process.env.PRIVATE_KEY || '');
    
    const universalAccount = new UniversalAccount({
        projectId: process.env.PROJECT_ID || '',
        projectClientKey: process.env.PROJECT_CLIENT_KEY || '',
        projectAppUuid: process.env.PROJECT_APP_UUID || '',
        ownerAddress: wallet.address,
        tradeConfig: {
            slippageBps: 1000, // 10% for meme volatility
            universalGas: true,
            solanaMEVTipAmount: 0.001,
        },
    });

    const options = await universalAccount.getSmartAccountOptions();
    console.log('Solana Address:', options.solanaSmartAccountAddress);

    const transaction = isBuy
        ? await universalAccount.createBuyTransaction({
            token: { chainId: CHAIN_ID.SOLANA_MAINNET, address: tokenAddress },
            amountInUSD: usdAmount,
        }, { addressLookupTableAccountAddresses: [] })
        : await universalAccount.createSellTransaction({
            token: { chainId: CHAIN_ID.SOLANA_MAINNET, address: tokenAddress },
            amount: usdAmount,
        });

    const sendResult = await universalAccount.sendTransaction(
        transaction,
        wallet.signMessageSync(getBytes(transaction.rootHash))
    );

    return sendResult.transactionId;
}

// Usage
const txId = await tradeMeme('TOKEN_ADDRESS', '100', true);
console.log('Trade submitted:', txId);
```

## Buy with Dynamic Slippage Retry (CLI)

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200
```

## Buy on Solana with Custom Tip + Tip Retry (CLI)

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain solana \
  --token-address 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200 \
  --solana-mev-tip-amount 0.001 \
  --retry-mev-tips 0.001,0.003,0.005
```
