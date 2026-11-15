# Reputation Registry

The Reputation Registry provides a standard interface for posting and fetching feedback signals about agents. It enables both on-chain composability and off-chain aggregation.

## Contract

- **Address**: `0x8004B663056A597Dffe9eCcC1965A193B7388713` (same on all chains)
- **Proxy pattern**: UUPS (EIP-1822) with vanity address

## Feedback Structure

```solidity
struct Feedback {
    uint256 agentTokenId;    // Target agent
    address client;          // Feedback submitter
    int128 value;            // Signed feedback value
    uint8 decimals;          // Decimal precision
    string tag1;             // Primary category tag
    string tag2;             // Secondary category tag (optional)
    string endpoint;         // Specific endpoint reviewed
    string payloadCID;       // Optional IPFS CID for extended data
    bool revoked;            // Whether feedback has been revoked
    uint256 timestamp;       // Block timestamp
}
```

## Key Functions

### Submit Feedback

```solidity
function submitFeedback(
    uint256 agentTokenId,
    int128 value,
    uint8 decimals,
    string memory tag1,
    string memory tag2,
    string memory endpoint,
    string memory payloadCID
) external returns (uint256 feedbackIndex)
```

### Revoke Feedback

```solidity
function revokeFeedback(uint256 agentTokenId, uint256 feedbackIndex) external
```

- Only the original submitter can revoke
- Sets `revoked = true` (does not delete)

### Respond to Feedback

```solidity
function respondToFeedback(
    uint256 agentTokenId,
    address client,
    uint256 feedbackIndex,
    string memory responseURI,
    bytes32 responseHash
) external
```

- Only the agent owner can respond
- `responseURI` points to the response content
- `responseHash` is a content hash for verification

### Query Feedback

```solidity
function getFeedback(uint256 agentTokenId, address client, uint256 feedbackIndex) external view returns (Feedback memory)
function getFeedbackCount(uint256 agentTokenId) external view returns (uint256)
function getAverageValue(uint256 agentTokenId) external view returns (int128)
```

## Events

```solidity
event FeedbackSubmitted(uint256 indexed agentTokenId, address indexed client, uint256 feedbackIndex, int128 value);
event FeedbackRevoked(uint256 indexed agentTokenId, address indexed client, uint256 feedbackIndex);
event FeedbackResponse(uint256 indexed agentTokenId, address indexed client, uint256 feedbackIndex, string responseURI);
```

## Value Interpretation

The `value` field is a signed integer (`int128`) with `decimals` precision. This supports flexible rating systems:

### Common Scales

| Tag | Scale | Example | Meaning |
|-----|-------|---------|---------|
| `starred` | 0-100 | value=85, decimals=0 | 85/100 quality |
| `uptime` | 0-10000 | value=9977, decimals=2 | 99.77% uptime |
| `successRate` | 0-100 | value=95, decimals=0 | 95% success |
| `responseTime` | milliseconds | value=150, decimals=0 | 150ms response |
| `revenues` | currency units | value=1500, decimals=2 | $15.00 |
| `tradingYield` | percentage | value=1250, decimals=2 | 12.50% yield |

### Star Rating Conversion

| Stars | Value |
|-------|-------|
| 1★ | 20 |
| 2★ | 40 |
| 3★ | 60 |
| 4★ | 80 |
| 5★ | 100 |

### Negative Feedback

Values below 0 indicate disputes, fraud reports, or negative experiences. The v2.0 spec introduces support for configurable scales (int256 with decimals) and negative values.

## Best Practices (from v2.0 spec)

1. Use descriptive tags to categorize feedback
2. Include endpoint when reviewing a specific service
3. Use IPFS payload for detailed reviews with evidence
4. Star ratings use 0-100 scale (not 0-5) for precision
5. Negative values are valid for disputes and fraud reports
6. Include OASF skills/domains in payload when applicable
