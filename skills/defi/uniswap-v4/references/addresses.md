# Uniswap V4 Contract Addresses (Reference)

This file is **informational**.

- **Canonical source of truth (used by the code):** `src/lib/addresses.ts`
- **Official deployments reference:** https://docs.uniswap.org/contracts/v4/deployments

## Base Mainnet (chainId: 8453)
- **PoolManager**: `0x498581fF718922c3f8e6A244956aF099B2652b2b`
- **UniversalRouter**: `0x6ff5693b99212da76ad316178a184ab56d299b43`
- **Permit2 (universal)**: `0x000000000022D473030F116dDEE9F6B43aC78BA3`
- **StateView**: `0xa3c0c9b65bad0b08107aa264b0f3db444b867a71`
- **V4Quoter**: `0x0d5e0f971ed27fbff6c2837bf31316121532048d`
- **WETH**: `0x4200000000000000000000000000000000000006`
- **USDC**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

## Ethereum Mainnet (chainId: 1)
- **PoolManager**: `0x000000000004444c5dc75cB358380D2e3dE08A90`
- **UniversalRouter**: `0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af`
- **Permit2 (universal)**: `0x000000000022D473030F116dDEE9F6B43aC78BA3`
- **StateView**: `0x7ffe42c4a5deea5b0fec41c94c136cf115597227`
- **V4Quoter**: `0x52f0e24d1c21c8a0cb1e5a5dd6198556bd9e1203`
- **WETH**: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`

## Base (Common Tokens)
- **USDC**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **DAI**: `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb`
- **cbBTC**: `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf`

## RPC Endpoints
Avoid public RPCs for anything important. Prefer a paid endpoint (Alchemy).
- Base: `https://mainnet.base.org` (public)
- Ethereum: `https://eth.llamarpc.com` (public)
