---
name: rocketpool-governance
description: Interact with Rocket Pool governance contracts — protocol DAO (pDAO) proposals and voting, oracle DAO (oDAO) membership and proposals, security council operations, and all DAO settings contracts. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Governance

Rocket Pool has three governance bodies:
1. **Protocol DAO (pDAO)** — all node operators vote on protocol parameters and treasury
2. **Oracle DAO (oDAO)** — trusted nodes that submit oracle data (balances, prices, rewards)
3. **Security Council** — emergency response team that can veto proposals and adjust parameters

## Quick Start

### Check Total pDAO Proposals
```bash
cast call 0x2D627A50Dc1C4EDa73E42858E8460b0eCF300b25 "getTotal()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Proposal State
```bash
cast call 0x2D627A50Dc1C4EDa73E42858E8460b0eCF300b25 "getState(uint256)(uint8)" 1 --rpc-url https://ethereum-rpc.publicnode.com
```

## Workflow

1. Look up the contract address from `references/addresses.json`
2. Find the function signature below
3. Load the ABI from `assets/abis/<contractName>.json` when available (some Saturn-era contracts in this skill are signature-only)
4. Execute via `cast call` (read) or `cast send` (write)

## Network Configuration

| Network | Chain ID | RPC | rocketStorage |
|---|---|---|---|
| Mainnet | 1 | `https://ethereum-rpc.publicnode.com` | `0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46` |
| Hoodi | 560048 | `https://rpc.hoodi.ethpandaops.io` | `0x594Fb75D3dc2DFa0150Ad03F99F97817747dd4E1` |

## Architecture

- **RocketStorage** is the central registry — all contracts resolve each other's addresses through it
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)

## rocketDAOProposal

Base proposal storage shared across all governance bodies.

### Functions

```
getTotal() → uint256 [view]
getState(uint256 _proposalID) → uint8 [view]
getProposer(uint256 _proposalID) → address [view]
getDAO(uint256 _proposalID) → string [view]
```

## Protocol DAO

### rocketDAOProtocolProposal

Core proposal lifecycle for pDAO governance.

```
propose(string _proposalMessage, bytes _payload, uint32 _blockNumber, tuple[] _treeNodes) → uint256
vote(uint256 _proposalID, uint8 _voteDirection, uint256 _votingPower, uint256 _nodeIndex, tuple[] _witness)
overrideVote(uint256 _proposalID, uint8 _voteDirection)
execute(uint256 _proposalID)
finalise(uint256 _proposalID)
destroy(uint256 _proposalID)
```

Vote directions: 0=Against, 1=For, 2=AgainstWithVeto, 3=Abstain

Proposal queries:
```
getTotal() → uint256 [view]
getState(uint256 _proposalID) → uint8 [view]
getMessage(uint256 _proposalID) → string [view]
getProposer(uint256 _proposalID) → address [view]
getStart(uint256 _proposalID) → uint256 [view]
getPhase1End(uint256 _proposalID) → uint256 [view]
getPhase2End(uint256 _proposalID) → uint256 [view]
getExpires(uint256 _proposalID) → uint256 [view]
getExecuted(uint256 _proposalID) → bool [view]
getFinalised(uint256 _proposalID) → bool [view]
getVetoed(uint256 _proposalID) → bool [view]
getVotingPowerFor(uint256 _proposalID) → uint256 [view]
getVotingPowerAgainst(uint256 _proposalID) → uint256 [view]
getVotingPowerAbstained(uint256 _proposalID) → uint256 [view]
getVotingPowerVeto(uint256 _proposalID) → uint256 [view]
getVotingPowerRequired(uint256 _proposalID) → uint256 [view]
getReceiptHasVoted(uint256 _proposalID, address _nodeAddress) → bool [view]
```

Proposal states: 0=Pending, 1=ActivePhase1, 2=ActivePhase2, 3=Succeeded, 4=Executed, 5=Cancelled, 6=Defeated, 7=Expired, 8=Vetoed, 9=QuorumNotMet, 10=Destroyed

#### Examples

```bash
cast call $PDAO_PROPOSAL "getTotal()(uint256)" --rpc-url $RPC_URL
cast call $PDAO_PROPOSAL "getState(uint256)(uint8)" 1 --rpc-url $RPC_URL
cast call $PDAO_PROPOSAL "getVotingPowerFor(uint256)(uint256)" 1 --rpc-url $RPC_URL
```

### rocketDAOProtocolProposals

Proposal actions — what governance can vote on:

```
proposalSettingUint(string _settingContractName, string _settingPath, uint256 _value)
proposalSettingBool(string _settingContractName, string _settingPath, bool _value)
proposalSettingAddress(string _settingContractName, string _settingPath, address _value)
proposalSettingMulti(string[] _settingContractNames, string[] _settingPaths, uint8[] _types, bytes[] _data)
proposalSettingRewardsClaimers(uint256 _trustedNodePercent, uint256 _protocolPercent, uint256 _nodePercent)
proposalTreasuryOneTimeSpend(string _invoiceID, address _recipientAddress, uint256 _amount)
proposalTreasuryNewContract(string _contractName, address _recipientAddress, uint256 _amountPerPeriod, uint256 _periodLength, uint256 _startTime, uint256 _numPeriods)
proposalTreasuryUpdateContract(string _contractName, address _recipientAddress, uint256 _amountPerPeriod, uint256 _periodLength, uint256 _numPeriods)
proposalSecurityInvite(string _id, address _memberAddress)
proposalSecurityKick(address _memberAddress)
proposalSecurityReplace(address _existingAddr, string _newMemberId, address _newAddr)
```

### rocketDAOProtocolVerifier

Optimistic fraud proof system for proposal voting trees.

```
createChallenge(uint256 _proposalID, uint256 _index, tuple _node, tuple[] _witness)
defeatProposal(uint256 _proposalID, uint256 _index)
submitRoot(uint256 _proposalID, uint256 _index, tuple[] _nodes)
claimBondProposer(uint256 _proposalID, uint256[] _indices)
claimBondChallenger(uint256 _proposalID, uint256[] _indices)
getChallengeState(uint256 _proposalID, uint256 _index) → uint8 [view]
```

### rocketDAOProtocol

```
getBootstrapModeDisabled() → bool [view]
bootstrapSettingUint(string _settingContractName, string _settingPath, uint256 _value)
bootstrapSettingBool(string _settingContractName, string _settingPath, bool _value)
bootstrapSettingAddress(string _settingContractName, string _settingPath, address _value)
```

### rocketDAOProtocolActions

```
version() → uint8 [view]
```

The bundled `rocketDAOProtocolActions` ABI is minimal (version-only). For setting updates, use `rocketDAOProtocolProposals` proposal payload methods.

## Oracle DAO (oDAO)

### rocketDAONodeTrusted

```
getMemberCount() → uint256 [view]
getMemberAt(uint256 _index) → address [view]
getMemberIsValid(address _nodeAddress) → bool [view]
getMemberID(address _nodeAddress) → string [view]
getMemberJoinedTime(address _nodeAddress) → uint256 [view]
getMemberRPLBondAmount(address _nodeAddress) → uint256 [view]
getMemberQuorumVotesRequired() → uint256 [view]
```

### rocketDAONodeTrustedActions

```
actionJoin()
actionLeave(address _rplBondRefundAddress)
actionChallengeMake(address _nodeAddress) [payable]
actionChallengeDecide(address _nodeAddress)
actionKick(address _nodeAddress, uint256 _rplFine)
```

### rocketDAONodeTrustedProposals

```
propose(string _proposalMessage, bytes _payload) → uint256
vote(uint256 _proposalID, bool _support)
execute(uint256 _proposalID)
cancel(uint256 _proposalID)
proposalInvite(string _id, string _url, address _nodeAddress)
proposalKick(address _nodeAddress, uint256 _rplFine)
proposalLeave(address _nodeAddress)
proposalSettingUint(string _settingContractName, string _settingPath, uint256 _value)
proposalSettingBool(string _settingContractName, string _settingPath, bool _value)
proposalUpgrade(string _type, string _name, string _contractAbi, address _contractAddress)
```

### rocketDAONodeTrustedUpgrade

```
upgrade(string _type, string _name, string _contractAbi, address _contractAddress)
execute(uint256 _upgradeProposalID)
veto(uint256 _upgradeProposalID)
getTotal() → uint256 [view]
getState(uint256 _upgradeProposalID) → uint8 [view]
getName(uint256 _upgradeProposalID) → string [view]
```

## Security Council

### rocketDAOSecurity

```
getMemberCount() → uint256 [view]
getMemberAt(uint256 _index) → address [view]
getMemberIsValid(address _memberAddress) → bool [view]
getMemberID(address _memberAddress) → string [view]
getMemberQuorumVotesRequired() → uint256 [view]
```

### rocketDAOSecurityActions

```
actionJoin()
actionLeave()
actionRequestLeave()
actionKick(address _memberAddress)
actionKickMulti(address[] _memberAddresses)
```

### rocketDAOSecurityProposals

```
propose(string _proposalMessage, bytes _payload) → uint256
vote(uint256 _proposalID, bool _support)
execute(uint256 _proposalID)
cancel(uint256 _proposalID)
proposalSettingUint(string _settingNameSpace, string _settingPath, uint256 _value)
proposalSettingBool(string _settingNameSpace, string _settingPath, bool _value)
proposalSettingAddress(string _settingNameSpace, string _settingPath, address _value)
proposalInvite(string _id, address _memberAddress)
proposalKick(address _memberAddress)
proposalReplace(address _existingAddr, string _newMemberId, address _newAddr)
```

### rocketDAOSecurityUpgrade (Saturn)

No ABI file is bundled for this contract in this skill. Use the raw signatures below with `cast call` / `cast send`.

```
proposeVeto(string _proposalMessage, uint256 _upgradeProposalID) → uint256
proposalVeto(uint256 _upgradeProposalID)
vote(uint256 _proposalID, bool _support)
execute(uint256 _proposalID)
cancel(uint256 _proposalID)
```

## DAO Settings Contracts

All settings follow `getSettingUint/Bool/Address` pattern.

| Contract | Controls |
|----------|----------|
| rocketDAOProtocolSettingsDeposit | Deposit pool limits, fees, queue rates |
| rocketDAOProtocolSettingsNode | Registration, RPL stake minimums, bond sizes |
| rocketDAOProtocolSettingsMinipool | Launch timeout, max count, bond reduction |
| rocketDAOProtocolSettingsMegapool | Dissolve penalty, notify threshold (Saturn) |
| rocketDAOProtocolSettingsNetwork | Commission shares, oracle frequency, fees |
| rocketDAOProtocolSettingsRewards | Reward intervals, claimer percentages |
| rocketDAOProtocolSettingsProposals | Voting periods, quorum, bonds |
| rocketDAOProtocolSettingsInflation | RPL inflation rate and start time |
| rocketDAOProtocolSettingsSecurity | Security council quorum, timing |
| rocketDAONodeTrustedSettingsMembers | oDAO quorum, RPL bond, challenge params |
| rocketDAONodeTrustedSettingsMinipool | Scrub period, bond reduction windows |
| rocketDAONodeTrustedSettingsProposals | oDAO proposal timing |
| rocketDAONodeTrustedSettingsRewards | Network reward enablement |
