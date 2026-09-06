# OpenOcean Token Registry

Common token addresses and decimals across major EVM chains. This registry is used by the OpenOcean skills to resolve token symbols to contract addresses.

## Native Token Address

All chains use the same special address for native tokens (ETH, BNB, MATIC, etc.):
```
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
```

## Ethereum (Chain ID: 1)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| ETH | Ethereum | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WETH | Wrapped ETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | 18 | Wrapped |
| USDC | USD Coin | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | 6 | Stablecoin |
| USDT | Tether USD | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0x6B175474E89094C44Da98b954EedeAC495271d0F` | 18 | Stablecoin |
| WBTC | Wrapped BTC | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` | 8 | Wrapped |
| UNI | Uniswap | `0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984` | 18 | Token |
| LINK | Chainlink | `0x514910771AF9Ca656af840dff83E8264EcF986CA` | 18 | Token |
| AAVE | Aave | `0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9` | 18 | Token |

## BNB Smart Chain (Chain ID: 56)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| BNB | Binance Coin | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WBNB | Wrapped BNB | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` | 18 | Wrapped |
| USDT | Tether USD | `0x55d398326f99059fF775485246999027B3197955` | 18 | Stablecoin |
| USDC | USD Coin | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` | 18 | Stablecoin |
| BUSD | Binance USD | `0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56` | 18 | Stablecoin |
| DAI | DAI Stablecoin | `0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3` | 18 | Stablecoin |
| BTCB | Bitcoin BEP2 | `0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c` | 18 | Wrapped |
| CAKE | PancakeSwap | `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82` | 18 | Token |

## Polygon (Chain ID: 137)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| MATIC | Polygon | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WMATIC | Wrapped MATIC | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270` | 18 | Wrapped |
| USDC | USD Coin | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | 6 | Stablecoin |
| USDT | Tether USD | `0xc2132D05D31c914a87C6611C10748AEb04B58e8F` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063` | 18 | Stablecoin |
| WBTC | Wrapped BTC | `0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6` | 8 | Wrapped |
| WETH | Wrapped ETH | `0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619` | 18 | Wrapped |

## Arbitrum (Chain ID: 42161)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| ETH | Ethereum | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WETH | Wrapped ETH | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | 18 | Wrapped |
| USDC | USD Coin | `0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8` | 6 | Stablecoin |
| USDT | Tether USD | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1` | 18 | Stablecoin |
| WBTC | Wrapped BTC | `0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f` | 8 | Wrapped |

## Optimism (Chain ID: 10)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| ETH | Ethereum | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WETH | Wrapped ETH | `0x4200000000000000000000000000000000000006` | 18 | Wrapped |
| USDC | USD Coin | `0x7F5c764cBc14f9669B88837ca1490cCa17c31607` | 6 | Stablecoin |
| USDT | Tether USD | `0x94b008aA00579c1307B0EF2c499aD98a8ce58e58` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1` | 18 | Stablecoin |

## Base (Chain ID: 8453)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| ETH | Ethereum | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WETH | Wrapped ETH | `0x4200000000000000000000000000000000000006` | 18 | Wrapped |
| USDC | USD Coin | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` | 18 | Stablecoin |

## Avalanche (Chain ID: 43114)

| Symbol | Name | Address | Decimals | Type |
|---|---|---|---|---|
| AVAX | Avalanche | `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` | 18 | Native |
| WAVAX | Wrapped AVAX | `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` | 18 | Wrapped |
| USDC | USD Coin | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` | 6 | Stablecoin |
| USDT | Tether USD | `0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7` | 6 | Stablecoin |
| DAI | DAI Stablecoin | `0xd586E7F844cEa2F87f50152665BCbc2C279D8d70` | 18 | Stablecoin |

## Token Resolution Fallback Sequence

If a token is not found in this registry, follow this sequence:

### 1. OpenOcean Token API (Preferred)
Query the OpenOcean token list endpoint:
```
GET https://open-api.openocean.finance/v4/:chain/tokenList
```

Search for the token symbol in the response. Prefer tokens with:
- Higher market cap (`usd` field)
- Verified status
- Established trading volume

### 2. Chain-specific Token Lists
For EVM chains, check common token lists:
- **Ethereum**: Check CoinGecko API or Etherscan token list
- **Other chains**: Use chain explorer APIs

### 3. Manual User Input (Final Fallback)
If automated lookup fails, ask the user to provide:
- The exact token contract address
- Token decimals (if known)

**Never guess or fabricate token addresses.** Incorrect addresses can lead to loss of funds.

## Token Safety Checks

Before using any token (especially those not in this registry):

1. **Verify Contract**: Check the token contract on a block explorer
2. **Check Liquidity**: Ensure the token has sufficient liquidity
3. **Review Security**: Look for audit reports or security assessments
4. **Test Small**: For unknown tokens, test with a small amount first

## Adding New Tokens

To add a token to this registry:

1. Confirm the token is widely used and has significant liquidity
2. Verify the contract address on the official chain explorer
3. Include all relevant chains where the token is available
4. Update both the symbol and address fields accurately

## Native Token Aliases

Recognize these common aliases for native tokens:

| Chain | Native Token | Common Aliases |
|---|---|---|
| Ethereum | ETH | Ethereum, Ether |
| BSC | BNB | Binance Coin, BNB |
| Polygon | MATIC | Polygon, Matic |
| Avalanche | AVAX | Avalanche |
| Arbitrum/Optimism/Base | ETH | Ethereum, Ether |
| Fantom | FTM | Fantom |
| Cronos | CRO | Cronos |

When users specify these aliases, use the native token address: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`

## Decimal Precision Notes

- **Stablecoins**: Typically 6 decimals (USDC, USDT on Ethereum) or 18 decimals (on other chains)
- **Native tokens**: Always 18 decimals
- **Bitcoin variants**: 8 decimals (WBTC) or 18 decimals (BTCB on BSC)
- **Always verify**: Use the `decimals` field from API responses when available

## Last Updated

This registry was last updated based on OpenOcean API documentation as of March 2025. Token addresses may change (e.g., due to contract upgrades or migrations). Always verify addresses before significant transactions.