# Contract addresses

Snapshot of the v2.2.1 protocol deployment, checked on 2026-11-25 against `@gmx-io/sdk@2.9.1` and the [GMX interface release registry](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/contracts.ts). Protocol deployment versions (such as v2.2.1) and npm SDK versions are different version schemes.

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
| ExchangeRouter | `0x6776c2b52179BC737193DE3bc75262681006AA27` |
| SyntheticsRouter | `0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6` |
| SyntheticsReader | `0xAda708aFf0f1D784D28cd8Ff4d6D977fF9599e5D` |
| SimulationRouter | `0x3C81eBE9892431B5c9B8Eff7904c2a09397014D1` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55` |
| WithdrawalVault | `0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55` |
| OrderVault | `0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5` |
| ShiftVault | `0xfe99609C4AA83ff6816b64563Bdffd7fa68753Ab` |
| GlvReader | `0x51fe0b7919e1208a717E9B16a097C1C3D70eFbf6` |
| GlvRouter | `0x321EB66dD95ad33715ee615AAb8dAC6394E7b3F9` |
| GlvVault | `0x393053B58f9678C9c28c2cE941fF6cac49C3F8f9` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0x63e3fFcF0bBc43F2ed253134EBA534E31A268509` |
| GelatoRelayRouter | `0xE6c871230F758F03b39D4Fb5ea3fc7B49E9dAc64` |
| SubaccountGelatoRelayRouter | `0xC3969579D6ec54879F078c36F6B364cDbd1B557B` |
| MultichainOrderRouter | `0x5cFdc00811d0697D18b080f4E4fEB092a3b18671` |
| MultichainSubaccountRouter | `0xa2d9D6B0904929A1CD43c3762931Eb19ca1b4215` |
| MultichainGmRouter | `0xa334b4e3f92a91e927f061494A95d84B7F0D134d` |
| MultichainGlvRouter | `0xf9B01d45B2c5022429c3f745e5A2E700B02cEBeb` |
| MultichainClaimsRouter | `0x7b2b62a4604417d0340Ed3A837BA66ad3a5eeAd7` |
| MultichainTransferRouter | `0xC993eF170859DAE0241a3c12B8186e456Fa1c1B0` |
| MultichainVault | `0xCeaadFAf6A8C489B250e407987877c5fDfcDBE6E` |
| LayerZeroProvider | `0xCb60d0A8372Cb8f8a074d304F88bA851FC5E8e29` |

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
| ExchangeRouter | `0x5b7693839ef8d767168891797B9d2f319e351672` |
| SyntheticsRouter | `0x820F5FfC5b525cD4d88Cd91aCf2c28F16530Cc68` |
| SyntheticsReader | `0x9390285097B4a1997B91F61AF756DCD2509FcD0F` |
| SimulationRouter | `0x25B13cEE3D0d3bB318C64d121b7c9983D0EBD795` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0x90c670825d0C62ede1c5ee9571d6d9a17A722DFF` |
| WithdrawalVault | `0xf5F30B10141E1F63FC11eD772931A8294a591996` |
| OrderVault | `0xD3D60D22d415aD43b7e64b510D86A30f19B1B12C` |
| ShiftVault | `0x7fC46CCb386e9bbBFB49A2639002734C3Ec52b39` |
| GlvReader | `0x79B6Bf52D49d215724951c5a9A541f8A2Ee165Bc` |
| GlvRouter | `0x5B8c1B498CCDDCAad36B5C81e48D773Ad338145D` |
| GlvVault | `0x527FB0bCfF63C47761039bB386cFE181A92a4701` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0x2A929c97Ec71ced74675C2b5175Afa8927A28404` |
| GelatoRelayRouter | `0xE9f7E49F7304D36Aae146B5Af7cE6f9421Dac2CF` |
| SubaccountGelatoRelayRouter | `0x4fe335118106542DeD0748Eebbf276dD92F386e3` |
| MultichainOrderRouter | `0x1c9d9BF1286Ea617a4eFbCf4f0B2b4A160269229` |
| MultichainSubaccountRouter | `0x96bE3cbFfbCeb1020ddfE5689807b8C20c3659C0` |
| MultichainGmRouter | `0xC7fC0698774b4C704aCD5521368dA5BeB397289E` |
| MultichainGlvRouter | `0x13BF6A53C2aBc86b080d3E6f500d7c209F73dc82` |
| MultichainClaimsRouter | `0xd9e34687F82602780a277F891f9a33B9A1F9291e` |
| MultichainTransferRouter | `0xcD11f8277Faca1c906cB13e2447cDC9fed1d3B39` |
| MultichainVault | `0x6D5F3c723002847B009D07Fe8e17d6958F153E4e` |
| LayerZeroProvider | `0x1eEd675410879BDd9BF7f595d944F1b732019470` |

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
| ExchangeRouter | `0x048Ee03a103d5caA06704634139495Da08E62Fd8` |
| SyntheticsRouter | `0x1eAfB14236C489C28845EC04F78DECA5Fb9879Aa` |
| SyntheticsReader | `0x12c4E1A499f2fFcB55683F682549049e29d70Cba` |
| SimulationRouter | `0x79B6Bf52D49d215724951c5a9A541f8A2Ee165Bc` |

### Request vaults and GLV

| Contract | Address |
|----------|---------|
| DepositVault | `0x8231A60862F9b0bA93fFA050c0E94AC902D901d2` |
| WithdrawalVault | `0x0Ec53dda9676219dE63eC703212219b07811F33C` |
| OrderVault | `0xD5AE04762E2afb1506695b3F36286EBE7B0E6772` |
| ShiftVault | `0xC255c70b50623054CADbAD9A02E1CFE73d286666` |
| GlvReader | `0xE08885EA7860f19e5fb2AECbA892e8A6BA505C86` |
| GlvRouter | `0xF4706575f9241a07Af27E357Cac5149eac0A0AC7` |
| GlvVault | `0x52e4875EB5603d21912d30A1dBA6B0B97192459A` |

### Relay and GMX Account

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0xe6550Bc32d08e28F9b20bFB1944551E538D7De4c` |
| GelatoRelayRouter | `0xd34f5ce2a26c6B67892ef633877e381Aba4f66c5` |
| SubaccountGelatoRelayRouter | `0x5B8c1B498CCDDCAad36B5C81e48D773Ad338145D` |
| MultichainOrderRouter | `0x61F8cA02B89360b5860aa6840E5c043b319DF693` |
| MultichainSubaccountRouter | `0x9456C4E4D7b443D040318DD1225c15D49ec14562` |
| MultichainGmRouter | `0xBF877cB8E1e8B82e23Eb7c64CfD941a2a739f94a` |
| MultichainGlvRouter | `0x23E7bC6069A0336F96ea2b3EB93d6A86CE432E16` |
| MultichainClaimsRouter | `0xDA1C23829B8c9c0F5F4de04B763D64BDcb62BCC4` |
| MultichainTransferRouter | `0xd5F5F52A580787898B1c5491f48568bC9fAa9753` |
| MultichainVault | `0xd6922E889cE4CF14e59427F20e7d857ff81A5A9D` |
| LayerZeroProvider | `0xC7fC0698774b4C704aCD5521368dA5BeB397289E` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0xAd917849372eaEF498E982F90bA6459a43ecbd31` |
| Multicall | `0xF516BC01c50eebdBad4d7E506c8f690ae8EAFc52` |
| NATIVE_TOKEN | `0x4200000000000000000000000000000000000006` |

## Tokens, markets, and GLVs

Discover token and GM market addresses with `fetchTokens()` and `fetchMarkets()`. Discover GLV tokens and constituent markets with `GlvReader.getGlvInfoList(DataStore, start, end)` / `getGlvInfo(DataStore, glv)`. `GlvVault` above is a request custody contract, not the GLV share token to buy or approve. `NATIVE_TOKEN` is the wrapped native ERC-20 address, not the native-coin sentinel.
