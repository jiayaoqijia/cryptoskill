# Contract Addresses

Deployed GMX V2 Synthetics contracts per chain. Addresses sourced from [`sdk/src/configs/contracts.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/contracts.ts) in the gmx-interface repository.

> **Note:** Most contract addresses may change on upgrades. `DataStore` and `EventEmitter` are permanent.

## Arbitrum (42161)

### Core Synthetics

| Contract | Address |
|----------|---------|
| DataStore | `0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8` |
| EventEmitter | `0xC8ee91A54287DB53897056e12D9819156D3822Fb` |
| ExchangeRouter | `0x1C3fa76e6E1088bCE750f23a5BFcffa1efEF6A41` |
| SyntheticsRouter | `0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6` |
| SyntheticsReader | `0x470fbC46bcC0f16532691Df360A07d8Bf5ee0789` |

### Vaults

| Contract | Address |
|----------|---------|
| DepositVault | `0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55` |
| WithdrawalVault | `0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55` |
| OrderVault | `0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5` |
| ShiftVault | `0xfe99609C4AA83ff6816b64563Bdffd7fa68753Ab` |

### Relay & Subaccounts

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0xdD00F639725E19a209880A44962Bc93b51B1B161` |
| GelatoRelayRouter | `0xa9090E2fd6cD8Ee397cF3106189A7E1CFAE6C59C` |
| SubaccountGelatoRelayRouter | `0x517602BaC704B72993997820981603f5E4901273` |

### GLV (Liquidity Vaults)

| Contract | Address |
|----------|---------|
| GlvReader | `0x2C670A23f1E798184647288072e84054938B5497` |
| GlvRouter | `0x7EAdEE2ca1b4D06a0d82fDF03D715550c26AA12F` |
| GlvVault | `0x393053B58f9678C9c28c2cE941fF6cac49C3F8f9` |

### Multichain (GMX Account)

| Contract | Address |
|----------|---------|
| MultichainOrderRouter | `0xD38111f8aF1A7Cd809457C8A2303e15aE2170724` |
| MultichainVault | `0xCeaadFAf6A8C489B250e407987877c5fDfcDBE6E` |
| LayerZeroProvider | `0xB6DE222dAef5029f31b8fABE498D34f3c491Ef85` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0xe6fab3f0c7199b0d34d7fbe83394fc0e0d06e99d` |
| Multicall | `0xe79118d6D92a4b23369ba356C90b9A7ABf1CB961` |
| NATIVE_TOKEN (WETH) | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` |

---

## Avalanche (43114)

### Core Synthetics

| Contract | Address |
|----------|---------|
| DataStore | `0x2F0b22339414ADeD7D5F06f9D604c7fF5b2fe3f6` |
| EventEmitter | `0xDb17B211c34240B014ab6d61d4A31FA0C0e20c26` |
| ExchangeRouter | `0x8f550E53DFe96C055D5Bdb267c21F268fCAF63B2` |
| SyntheticsRouter | `0x820F5FfC5b525cD4d88Cd91aCf2c28F16530Cc68` |
| SyntheticsReader | `0x62Cb8740E6986B29dC671B2EB596676f60590A5B` |

### Vaults

| Contract | Address |
|----------|---------|
| DepositVault | `0x90c670825d0C62ede1c5ee9571d6d9a17A722DFF` |
| WithdrawalVault | `0xf5F30B10141E1F63FC11eD772931A8294a591996` |
| OrderVault | `0xD3D60D22d415aD43b7e64b510D86A30f19B1B12C` |
| ShiftVault | `0x7fC46CCb386e9bbBFB49A2639002734C3Ec52b39` |

### Relay & Subaccounts

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0xf43F559774d2cF7882e6E846fCb87BDe183a6Da7` |
| GelatoRelayRouter | `0xEE2d3339CbcE7A42573C96ACc1298A79a5C996Df` |
| SubaccountGelatoRelayRouter | `0xfaBEb65bB877600be3A2C2a03aA56a95F9f845B9` |

### GLV (Liquidity Vaults)

| Contract | Address |
|----------|---------|
| GlvReader | `0x5C6905A3002f989E1625910ba1793d40a031f947` |
| GlvRouter | `0x7E425c47b2Ff0bE67228c842B9C792D0BCe58ae6` |
| GlvVault | `0x527FB0bCfF63C47761039bB386cFE181A92a4701` |

### Multichain (GMX Account)

| Contract | Address |
|----------|---------|
| MultichainOrderRouter | `0xd099565957046a2d2CF41B0CC9F95e14a8afD13b` |
| MultichainVault | `0x6D5F3c723002847B009D07Fe8e17d6958F153E4e` |
| LayerZeroProvider | `0xF85Fd576bBe22Bce785B68922C1c9849d62737c0` |

### Other

| Contract | Address |
|----------|---------|
| ReferralStorage | `0x827ed045002ecdabeb6e2b0d1604cf5fc3d322f8` |
| Multicall | `0x50474CAe810B316c294111807F94F9f48527e7F8` |
| NATIVE_TOKEN (WAVAX) | `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` |

---

## Botanix (3637)

### Core Synthetics

| Contract | Address |
|----------|---------|
| DataStore | `0xA23B81a89Ab9D7D89fF8fc1b5d8508fB75Cc094d` |
| EventEmitter | `0xAf2E131d483cedE068e21a9228aD91E623a989C2` |
| ExchangeRouter | `0xBCB5eA3a84886Ce45FBBf09eBF0e883071cB2Dc8` |
| SyntheticsRouter | `0x3d472afcd66F954Fe4909EEcDd5c940e9a99290c` |
| SyntheticsReader | `0x922766ca6234cD49A483b5ee8D86cA3590D0Fb0E` |

### Vaults

| Contract | Address |
|----------|---------|
| DepositVault | `0x4D12C3D3e750e051e87a2F3f7750fBd94767742c` |
| WithdrawalVault | `0x46BAeAEdbF90Ce46310173A04942e2B3B781Bf0e` |
| OrderVault | `0xe52B3700D17B45dE9de7205DEe4685B4B9EC612D` |
| ShiftVault | `0xa7EE2737249e0099906cB079BCEe85f0bbd837d4` |

### Relay & Subaccounts

| Contract | Address |
|----------|---------|
| SubaccountRouter | `0xa1793126B6Dc2f7F254a6c0E2F8013D2180C0D10` |
| GelatoRelayRouter | `0x98e86155abf8bCbA566b4a909be8cF4e3F227FAf` |
| SubaccountGelatoRelayRouter | `0xd6b16f5ceE328310B1cf6d8C0401C23dCd3c40d4` |

### GLV (Liquidity Vaults)

| Contract | Address |
|----------|---------|
| GlvReader | `0x955Aa50d2ecCeffa59084BE5e875eb676FfAFa98` |
| GlvRouter | `0xC92741F0a0D20A95529873cBB3480b1f8c228d9F` |
| GlvVault | `0xd336087512BeF8Df32AF605b492f452Fd6436CD8` |

### Multichain (GMX Account)

| Contract | Address |
|----------|---------|
| MultichainOrderRouter | `0xbC074fF8b85f9b66884E1EdDcE3410fde96bd798` |
| MultichainVault | `0x9a535f9343434D96c4a39fF1d90cC685A4F6Fb20` |
| LayerZeroProvider | `0x9E721ef9b908B4814Aa18502692E4c5666d1942e` |

### Botanix-Specific Tokens

| Token | Address |
|-------|---------|
| NATIVE_TOKEN (PBTC) | `0x0D2437F93Fed6EA64Ef01cCde385FB1263910C56` |
| StBTC | `0xF4586028FFdA7Eca636864F80f8a3f2589E33795` |

### Other

| Contract | Address |
|----------|---------|
| Multicall | `0x4BaA24f93a657f0c1b4A0Ffc72B91011E35cA46b` |

---

## Source

For the latest addresses, check these files in the [gmx-interface](https://github.com/gmx-io/gmx-interface/tree/release) repository:

- **Contract addresses**: [`sdk/src/configs/contracts.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/contracts.ts)
- **Token addresses**: [`sdk/src/configs/tokens.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/tokens.ts)
- **Market addresses**: [`sdk/src/configs/markets.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/markets.ts)
