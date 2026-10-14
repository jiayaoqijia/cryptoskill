# Identity Registry

The Identity Registry is an ERC-721 contract with URIStorage extension that gives every agent a portable, transferable, censorship-resistant on-chain identity.

## Contract

- **Testnet address**: `0x8004A818BFB912233c491871b3d84c89A494BD9e`
- **Mainnet address**: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Standard**: ERC-721 + URIStorage (OpenZeppelin v5.4.0)
- **Proxy pattern**: UUPS (EIP-1822) with deterministic vanity addresses via CREATE2

## Key Functions

### Minting

```solidity
function register(string memory agentURI) external returns (uint256 tokenId)
```

- Mints a new NFT to `msg.sender`
- Sets `agentURI` as the token URI
- Returns the new `tokenId`
- Emits `Transfer(address(0), owner, tokenId)` + `AgentRegistered(tokenId, owner, agentURI)`

### URI Management

```solidity
function tokenURI(uint256 tokenId) external view returns (string memory)
function setAgentURI(uint256 tokenId, string memory newURI) external
```

- `tokenURI` returns the current `agentURI` for the agent
- `setAgentURI` updates the URI (owner only)
- URI can point to IPFS (`ipfs://Qm...`), HTTP, or on-chain data

### Ownership

```solidity
function ownerOf(uint256 tokenId) external view returns (address)
function transferFrom(address from, address to, uint256 tokenId) external
function safeTransferFrom(address from, address to, uint256 tokenId) external
```

Standard ERC-721 ownership and transfer functions.

### On-chain Metadata

```solidity
function setMetadata(uint256 tokenId, string memory key, string memory value) external
function getMetadata(uint256 tokenId, string memory key) external view returns (string memory)
```

- Key-value pairs stored on-chain
- Reserved key: `agentWallet` (requires EIP-712 signature for verification)
- Owner-only write access

## Events

```solidity
event AgentRegistered(uint256 indexed tokenId, address indexed owner, string agentURI);
event AgentURIUpdated(uint256 indexed tokenId, string newURI);
event MetadataUpdated(uint256 indexed tokenId, string key, string value);
```

## Domain Verification

Optional proof at `/.well-known/agent-registration.json` on the agent's endpoint domain:

```json
{
  "agentId": "eip155:1:0x8004...9432:42",
  "chainId": 1,
  "tokenId": 42,
  "registryAddress": "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
}
```

## Storage Layout

- `_identityRegistry` at slot 0 (outside ERC-7201 namespace for persistence across upgrades)
- All other storage uses ERC-7201 namespaced layout
- Each implementation exposes `getVersion()` for version tracking
