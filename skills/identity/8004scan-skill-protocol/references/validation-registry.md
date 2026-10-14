# Validation Registry

The Validation Registry enables third-party validators to independently verify and attest to agent properties, creating a multi-tier certification network.

## Contract

- **Address**: `0x8004Cb1BFb31DAf7788923b405b754f57acEB4272` (same on all chains)
- **Proxy pattern**: UUPS (EIP-1822) with vanity address

## Flow

1. **Agent requests validation**: Owner calls `requestValidation(tokenId, validatorAddress)`
2. **Validator performs check**: Off-chain verification (TEE attestation, staking proof, manual review)
3. **Validator responds**: Calls `respondValidation(tokenId, score, proofCID)` with result

## Key Functions

```solidity
function requestValidation(uint256 agentTokenId, address validator) external
function respondValidation(uint256 agentTokenId, uint8 score, string memory proofCID) external
function getValidation(uint256 agentTokenId, address validator) external view returns (Validation memory)
```

## Validation Structure

```solidity
struct Validation {
    uint256 agentTokenId;
    address validator;
    uint8 score;           // 0-100
    string proofCID;       // IPFS CID with proof details
    uint256 timestamp;
    bool requested;
    bool responded;
}
```

## Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| 90-100 | Excellent — fully verified, all checks passed |
| 70-89 | Good — most checks passed, minor concerns |
| 50-69 | Acceptable — basic verification passed |
| 30-49 | Marginal — significant concerns identified |
| 0-29 | Poor — failed key verification checks |

## Validator Types

- **TEE Attestation**: Validator verifies agent runs in a Trusted Execution Environment
- **Staking Model**: Validator has economic stake backing their attestation
- **Manual Review**: Human validator inspects agent behavior and documentation
- **Automated Testing**: Validator runs automated test suites against agent endpoints

## Events

```solidity
event ValidationRequested(uint256 indexed agentTokenId, address indexed validator);
event ValidationResponded(uint256 indexed agentTokenId, address indexed validator, uint8 score);
```

## Multi-Tier Certification (8004scan)

8004scan implements a 6-dimension ranking system with validator tier multipliers:

| Dimension | Weight | Source |
|-----------|--------|--------|
| Feedback Score | High | Reputation Registry |
| Feedback Volume | Medium | Reputation Registry |
| Validator Score | High | Validation Registry |
| Endpoint Availability | Medium | Monitoring |
| Activity Recency | Low | On-chain events |
| Domain Verification | Low | DNS proof |

Validators themselves are tiered (Certified, Verified, Community) with multipliers applied to their endorsements.

## Status

In the current `agent0-sdk` v1.6.0, the Validation Registry is reference-only. Identity + Reputation flows are fully operational. Validation wrappers will be exposed in a future SDK release.
