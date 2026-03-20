# Universal Account SDK API Reference

## UniversalAccount Class

### Constructor

```typescript
new UniversalAccount({
    projectId: string,
    projectClientKey: string,
    projectAppUuid: string,
    ownerAddress: string,
    tradeConfig?: {
        slippageBps?: number;
        universalGas?: boolean;
        usePrimaryTokens?: SUPPORTED_TOKEN_TYPE[];
        solanaMEVTipAmount?: number;
    }
})
```

### Methods

#### getSmartAccountOptions()
Returns smart account addresses.

```typescript
const options = await universalAccount.getSmartAccountOptions();
// options.smartAccountAddress - EVM address
// options.solanaSmartAccountAddress - Solana address
```

#### createBuyTransaction()
Create a buy transaction.

```typescript
createBuyTransaction(
    params: {
        token: { chainId: number; address: string };
        amountInUSD: string;
    },
    options?: {
        addressLookupTableAccountAddresses?: string[];
    }
)
```

#### createSellTransaction()
Create a sell transaction.

```typescript
createSellTransaction(params: {
    token: { chainId: number; address: string };
    amount: string;
})
```

#### createConvertTransaction()
Create a token swap transaction.

```typescript
createConvertTransaction(
    params: {
        expectToken: { type: SUPPORTED_TOKEN_TYPE; amount: string };
        chainId: number;
    },
    options?: {
        usePrimaryTokens?: SUPPORTED_TOKEN_TYPE[];
    }
)
```

#### createTransferTransaction()
Create a transfer transaction.

```typescript
createTransferTransaction(params: {
    token: { chainId: number; address: string };
    amount: string;
    receiver: string;
})
```

#### sendTransaction()
Send a transaction.

```typescript
sendTransaction(transaction: Transaction, signature: string): Promise<{
    transactionId: string;
    status: number;
}>
```

#### getPrimaryAssets()
Get account balances.

```typescript
getPrimaryAssets(): Promise<{
    assets: Array<{
        tokenType: string;
        amount: string;
        amountInUSD: string;
    }>;
    totalAmountInUSD: string;
}>
```

## Chain IDs

```typescript
CHAIN_ID.SOLANA_MAINNET
CHAIN_ID.POLYGON
CHAIN_ID.ARBITRUM
CHAIN_ID.OPTIMISM
CHAIN_ID.BSC
CHAIN_ID.ETHEREUM
```

## Supported Token Types

```typescript
SUPPORTED_TOKEN_TYPE.USDC
SUPPORTED_TOKEN_TYPE.USDT
SUPPORTED_TOKEN_TYPE.SOL
SUPPORTED_TOKEN_TYPE.ETH
SUPPORTED_TOKEN_TYPE.BNB
```

## WebSocket

### Connect

```typescript
const ws = new WebSocket('wss://universal-app-ws-proxy.particle.network');
```

### Subscribe to Transaction Updates

```typescript
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'address-update',
    params: { addresses: ['SOLANA_ADDRESS'] }
}));
```

### Subscribe to Balance Updates

```typescript
ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'user-assets',
    params: {
        ownerAddress: 'OWNER_ADDRESS',
        name: 'UNIVERSAL',
        version: '1.0.3',
        useEIP7702: false
    }
}));
```

### Message Types

```typescript
// Transaction update
{
    type: 'transaction_update',
    channel: 'address-update',
    data: {
        transactionId: string;
        status: number; // 7 = success, 11 = failure
        sender: string;
    }
}

// Balance update
{
    channel: 'user-assets',
    data: {
        assets: Array<{
            chainId: number;
            address: string;
            amountOnChain: string;
            isToken2022: boolean;
            accountExists: boolean;
        }>;
    }
}
```
