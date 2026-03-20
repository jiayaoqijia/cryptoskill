# Hardhat Configuration Reference

## Complete Configuration Options

### Solidity Compiler Settings

```typescript
solidity: {
  version: "0.8.28",
  settings: {
    optimizer: {
      enabled: true,
      runs: 200,  // Optimize for average number of runs
    },
    evmVersion: "cancun",  // EVM version target
  },
},
```

### Multiple Compiler Versions

```typescript
solidity: {
  compilers: [
    { version: "0.8.28" },
    { version: "0.8.20" },
  ],
  overrides: {
    "contracts/legacy/OldContract.sol": {
      version: "0.7.6",
    },
  },
},
```

### Network Configuration

```typescript
networks: {
  // Celo Networks
  celo: {
    url: "https://forno.celo.org",
    chainId: 42220,
    accounts: [PRIVATE_KEY],
  },
  celoSepolia: {
    url: "https://forno.celo-sepolia.celo-testnet.org",
    chainId: 11142220,
    accounts: [PRIVATE_KEY],
  },

  // Other EVM Networks (examples)
  ethereum: {
    url: `https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_KEY}`,
    chainId: 1,
    accounts: [PRIVATE_KEY],
  },
  polygon: {
    url: "https://polygon-rpc.com",
    chainId: 137,
    accounts: [PRIVATE_KEY],
  },
  arbitrum: {
    url: "https://arb1.arbitrum.io/rpc",
    chainId: 42161,
    accounts: [PRIVATE_KEY],
  },
  optimism: {
    url: "https://mainnet.optimism.io",
    chainId: 10,
    accounts: [PRIVATE_KEY],
  },
  base: {
    url: "https://mainnet.base.org",
    chainId: 8453,
    accounts: [PRIVATE_KEY],
  },
},
```

### HD Wallet Configuration

```typescript
networks: {
  celo: {
    url: "https://forno.celo.org",
    accounts: {
      mnemonic: process.env.MNEMONIC,
      path: "m/44'/52752'/0'/0",  // Celo derivation path
      initialIndex: 0,
      count: 10,
    },
  },
},
```

### Gas Configuration

```typescript
networks: {
  celo: {
    url: "https://forno.celo.org",
    gasPrice: "auto",
    gas: "auto",
    timeout: 60000,  // Transaction timeout in ms
  },
},
```

### Etherscan/Celoscan Configuration

```typescript
etherscan: {
  apiKey: {
    celo: CELOSCAN_API_KEY,
    celoSepolia: CELOSCAN_API_KEY,
  },
  customChains: [
    {
      network: "celo",
      chainId: 42220,
      urls: {
        apiURL: "https://api.celoscan.io/api",
        browserURL: "https://celoscan.io",
      },
    },
    {
      network: "celoSepolia",
      chainId: 11142220,
      urls: {
        apiURL: "https://api.etherscan.io/v2/api",
        browserURL: "https://sepolia.celoscan.io",
      },
    },
  ],
},
```

### Path Configuration

```typescript
paths: {
  sources: "./contracts",
  tests: "./test",
  cache: "./cache",
  artifacts: "./artifacts",
},
```

### Gas Reporter Configuration

```typescript
gasReporter: {
  enabled: process.env.REPORT_GAS === "true",
  currency: "USD",
},
```

### Mocha Configuration

```typescript
mocha: {
  timeout: 40000,  // 40 seconds
},
```

## Complete Example

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "";
const CELOSCAN_API_KEY = process.env.CELOSCAN_API_KEY || "";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.28",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    celo: {
      url: "https://forno.celo.org",
      chainId: 42220,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
    },
    celoSepolia: {
      url: "https://forno.celo-sepolia.celo-testnet.org",
      chainId: 11142220,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: {
      celo: CELOSCAN_API_KEY,
      celoSepolia: CELOSCAN_API_KEY,
    },
    customChains: [
      {
        network: "celo",
        chainId: 42220,
        urls: {
          apiURL: "https://api.celoscan.io/api",
          browserURL: "https://celoscan.io",
        },
      },
      {
        network: "celoSepolia",
        chainId: 11142220,
        urls: {
          apiURL: "https://api.etherscan.io/v2/api",
          browserURL: "https://sepolia.celoscan.io",
        },
      },
    ],
  },
  mocha: {
    timeout: 40000,
  },
};

export default config;
```
