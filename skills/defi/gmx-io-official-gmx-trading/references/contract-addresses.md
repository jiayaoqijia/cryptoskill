# Contract addresses

Snapshot checked on 2026-10-13 against `@gmx-io/sdk@2.2.1` and the [GMX interface release registry](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/contracts.ts). Protocol deployment versions (such as v2.2c) and npm SDK versions are different version schemes.

Resolve addresses with the installed SDK and recheck the [official deployment list](https://docs.gmx.io/docs/api/contracts/addresses/) before writes after an upgrade. Do not combine a new address with an old ABI or copy an address from another chain. Compare addresses with viem `isAddressEqual` after an `isAddress` guard, not with `===`: registry casing is not uniform (Avalanche `ReferralStorage` is lowercase).

```typescript
import { getContract } from "@gmx-io/sdk/configs/contracts";

const chainId = 42161;
const exchangeRouter = getContract(chainId, "ExchangeRouter");
const approvalSpender = getContract(chainId, "SyntheticsRouter");
const glvRouter = getContract(chainId, "GlvRouter");
```

`SyntheticsRouter` is the ERC-20 approval spender for these standard wallet flows. `ExchangeRouter` and `GlvRouter` are transaction entry points. The Solidity `Router` / `Reader` names appear in SDK configuration as `SyntheticsRouter` / `SyntheticsReader`. Never use the bare names: they type-check but resolve elsewhere. `getContract(42161, "Reader")` returns the V1 Reader, `"Router"` throws on Arbitrum and Avalanche, and on MegaETH both return the zero address without throwing.

The retained `GelatoRelayRouter` contract name does not mean the current API uses the Gelato relay service: Express orders are submitted through GMX Relay. `SubaccountRouter` is legacy for order execution; use the API's subaccount flow rather than constructing new delegated trades through it.

## Arbitrum (42161)

### Core

| Contract | Address |
|----------|---------|
| DataStore | `0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8` |
| EventEmitter | `0xC8ee91A54287DB53897056e12D9819156D3822Fb` |
| ExchangeRouter | `0x7dE39FF2e232A2203196788d37e234cF8F1b83f1` |
| SyntheticsRouter | `0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6` |
| SyntheticsReader | `0xfA26cBb46e2614609406de08CA1Dc7f70a684184` |
| SimulationRouter | `0xaD3051cB1aE3a86b335f12A9a41BD4d995a137ea` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55` |
| WithdrawalVault | `0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55` |
| OrderVault | `0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5` |
| ShiftVault | `0xfe99609C4AA83ff6816b64563Bdffd7fa68753Ab` |
| GlvReader | `0x85fcBD684D08053f1efAB302dCb04F22E20E65B1` |
| GlvRouter | `0x167540D2DFF14120365CfDDF2F86e3045D4fa712` |
| GlvVault | `0x393053B58f9678C9c28c2cE941fF6cac49C3F8f9` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0x9c05880A2AaD7530c69e18e342eDC9E06cc757db` |
| GelatoRelayRouter | `0x5503b99308dB6923758F9A22d118207D633c4e87` |
| SubaccountGelatoRelayRouter | `0xfD0596f708d9D950E0eF7b5d191e5F8e55b8a67f` |
| MultichainOrderRouter | `0xABFC734f7CFc9352AED7a97b1F6a236eae831e8A` |
| MultichainSubaccountRouter | `0xAb3EDf0f3eed6804BAe1bD9bF90109ccadFD262e` |
| MultichainGmRouter | `0xFd26a7E3c4A9b75Bd0dce495290Fa33af2bb4b00` |
| MultichainGlvRouter | `0xA0Ef0Ace6E437458BB4b5F72A7c7bB43a1CdDa8d` |
| MultichainClaimsRouter | `0x946CC490DFedd6016645F5ce555E0036D116f50e` |
| MultichainTransferRouter | `0x3f6772B95423fC03264adf90Efb8A9922B6C8c6e` |
| MultichainVault | `0xCeaadFAf6A8C489B250e407987877c5fDfcDBE6E` |
| LayerZeroProvider | `0x0B33EBA531e5a5A331a3Ff9F418B8205F01C2869` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0xe6fab3F0c7199b0d34d7FbE83394fc0e0D06e99d` |
| Multicall | `0xe79118d6D92a4b23369ba356C90b9A7ABf1CB961` |
| NATIVE_TOKEN | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` |

## Avalanche (43114)

### Core

| Contract | Address |
|----------|---------|
| DataStore | `0x2F0b22339414ADeD7D5F06f9D604c7fF5b2fe3f6` |
| EventEmitter | `0xDb17B211c34240B014ab6d61d4A31FA0C0e20c26` |
| ExchangeRouter | `0xc002Db96E682FFF6675966F959677285a0C45Efa` |
| SyntheticsRouter | `0x820F5FfC5b525cD4d88Cd91aCf2c28F16530Cc68` |
| SyntheticsReader | `0xa34320a507493C71Fe35E982e496F7C5d1a7fa02` |
| SimulationRouter | `0xaB409fCaCc14Dd4234f6f86a2547f04ACC90a55e` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0x90c670825d0C62ede1c5ee9571d6d9a17A722DFF` |
| WithdrawalVault | `0xf5F30B10141E1F63FC11eD772931A8294a591996` |
| OrderVault | `0xD3D60D22d415aD43b7e64b510D86A30f19B1B12C` |
| ShiftVault | `0x7fC46CCb386e9bbBFB49A2639002734C3Ec52b39` |
| GlvReader | `0x321EB66dD95ad33715ee615AAb8dAC6394E7b3F9` |
| GlvRouter | `0x603B3D3aB077CA433b888c05fa59c777d5b6dCAD` |
| GlvVault | `0x527FB0bCfF63C47761039bB386cFE181A92a4701` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0xAda708aFf0f1D784D28cd8Ff4d6D977fF9599e5D` |
| GelatoRelayRouter | `0x51fe0b7919e1208a717E9B16a097C1C3D70eFbf6` |
| SubaccountGelatoRelayRouter | `0xa62BD1cFE2066c5bF4180b4125BBb5116eEA26c9` |
| MultichainOrderRouter | `0x204CC947Fddd11c90e302db2A5ac3865021D1618` |
| MultichainSubaccountRouter | `0x4A2826cAee8FF70d9392B171eaF398E0a2B55047` |
| MultichainGmRouter | `0x00205f26BCc52537D12fA9b0eFA5Fcc58F03ab76` |
| MultichainGlvRouter | `0x206B582F309724dAd259058Bc3289Ca3519F34B1` |
| MultichainClaimsRouter | `0xa664B7E894ad5777f3419C2883911Af3692a4569` |
| MultichainTransferRouter | `0xd4F6C2332b36D1Ccb22C7ac479b270fa0cA26a41` |
| MultichainVault | `0x6D5F3c723002847B009D07Fe8e17d6958F153E4e` |
| LayerZeroProvider | `0x74eECe8cC29b3d549db97F566a4445F48ed62a0d` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0x827ed045002ecdabeb6e2b0d1604cf5fc3d322f8` |
| Multicall | `0x50474CAe810B316c294111807F94F9f48527e7F8` |
| NATIVE_TOKEN | `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` |

## MegaETH (4326)

### Core

| Contract | Address |
|----------|---------|
| DataStore | `0xE43C7B694f6b652a9F4A0f275C008d18758Dce35` |
| EventEmitter | `0xAf2E131d483cedE068e21a9228aD91E623a989C2` |
| ExchangeRouter | `0xF68560cA917717639be497BF6283aC08C9Bf0264` |
| SyntheticsRouter | `0x1eAfB14236C489C28845EC04F78DECA5Fb9879Aa` |
| SyntheticsReader | `0x51fe0b7919e1208a717E9B16a097C1C3D70eFbf6` |
| SimulationRouter | `0x321EB66dD95ad33715ee615AAb8dAC6394E7b3F9` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0x8231A60862F9b0bA93fFA050c0E94AC902D901d2` |
| WithdrawalVault | `0x0Ec53dda9676219dE63eC703212219b07811F33C` |
| OrderVault | `0xD5AE04762E2afb1506695b3F36286EBE7B0E6772` |
| ShiftVault | `0xC255c70b50623054CADbAD9A02E1CFE73d286666` |
| GlvReader | `0x804f206a2ec78F505FD5D397450EAB9E7CBD1b21` |
| GlvRouter | `0xef1BA2A3fcf0244361d63FCAe0c4772586Cd1925` |
| GlvVault | `0x52e4875EB5603d21912d30A1dBA6B0B97192459A` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0x03B59961bF30b973fBd793A6C8ad57dA38D4D0a6` |
| GelatoRelayRouter | `0xbAAA3a693191e2e3E0973DE641C879D1aDD84e04` |
| SubaccountGelatoRelayRouter | `0x603B3D3aB077CA433b888c05fa59c777d5b6dCAD` |
| MultichainOrderRouter | `0x00205f26BCc52537D12fA9b0eFA5Fcc58F03ab76` |
| MultichainSubaccountRouter | `0xDB8906520812840b9835E3B84dE62C826249e20B` |
| MultichainGmRouter | `0x5CCD0b91Cfe6B0FBA1c98290dc39E71ff806d9bF` |
| MultichainGlvRouter | `0x5F65a3B91923840cD5254489A57c873427bA3A91` |
| MultichainClaimsRouter | `0x6614E9eAfE2FE583049333C03a2D6f9D7F252121` |
| MultichainTransferRouter | `0x62B1691B067278E5B1167d0443d4c957473611D2` |
| MultichainVault | `0xd6922E889cE4CF14e59427F20e7d857ff81A5A9D` |
| LayerZeroProvider | `0x8A959d38216ad67AEBBF31F46Cb3cA4D7fe584c8` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0xAd917849372eaEF498E982F90bA6459a43ecbd31` |
| Multicall | `0xF516BC01c50eebdBad4d7E506c8f690ae8EAFc52` |
| NATIVE_TOKEN | `0x4200000000000000000000000000000000000006` |

## Tokens, markets, and GLVs

Discover token and GM market addresses with `fetchTokens()` and `fetchMarkets()`. Discover GLV tokens and constituent markets with `GlvReader.getGlvInfoList(DataStore, start, end)` / `getGlvInfo(DataStore, glv)`. `GlvVault` above is a request custody contract, not the GLV share token to buy or approve. `NATIVE_TOKEN` is the wrapped native ERC-20 address, not the native-coin sentinel.
