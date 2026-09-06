---
name: governance-guide
description: >-
  Guides Cardano on-chain governance under CIP-1694 and the Conway era. Triggers: "governance", "DRep", "CIP-1694", "Conway era", "governance action", "vote on proposal", "constitutional committee", "treasury withdrawal", "GovTool".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Cardano On-Chain Governance Guide

Help developers, DReps, SPOs, and ADA holders understand and participate in Cardano's on-chain governance system introduced by CIP-1694 in the Conway era.

## When to use

- Developer needs to integrate governance features into a dApp
- Someone wants to understand how CIP-1694 governance works
- Registering as a DRep or delegating voting power
- Building governance-aware tools or dashboards
- Submitting or voting on governance actions
- Understanding the Constitutional Committee, DReps, and SPO roles
- Practicing governance on preprod/preview (or SanchoNet for bleeding-edge features)

## When NOT to use

- General smart contract development (use Aiken/Plutus skills)
- Stake pool setup or configuration (separate topic)
- Token minting or NFT creation
- Basic wallet integration without governance (use `connect-wallet` skill)

## Key principles

1. **Three governance bodies share power.** Constitutional Committee, DReps, and SPOs each have defined voting roles. No single body controls governance.
2. **Every ADA holder participates.** Either directly as a DRep or by delegating to one. Abstain and No-Confidence are also valid delegation choices.
3. **The Constitution constrains governance.** All actions must be constitutional. The Constitutional Committee certifies this.
4. **Governance actions have specific types.** Each type has its own voting thresholds and required approvals.
5. **Tools are maturing.** GovTool, SanchoNet, and SDK support are actively developing. Check current status before advising.

## Workflow

### Step 1: Identify the role

Ask the developer (if not already clear):

- **What is your role?** (developer | drep | stake-pool-operator | ada-holder)
- **What do you want to do?** (understand governance | vote | build governance features | register as DRep)

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cips/` - CIP specifications (CIP-1694, CIP-95)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/sanchonet/` - SanchoNet governance testnet docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/govtool/` - GovTool docs

### Step 3: Explain how governance works

Reference the CIP-1694 summary for detailed structure:

```
File: skills/governance-guide/references/cip-1694-summary.md
```

#### Quick overview

Cardano governance has three pillars:

1. **Delegated Representatives (DReps)**: ADA holders who vote on governance actions. Any ADA holder can become a DRep or delegate to one.
2. **Stake Pool Operators (SPOs)**: Vote on specific governance actions (hard forks, no-confidence, new committees, security-relevant protocol parameters).
3. **Constitutional Committee (CC)**: A group that certifies governance actions are constitutional. Does not propose or select -- only approves/rejects constitutionality.

#### Governance action types

| Action | DRep vote | SPO vote | CC vote |
|---|---|---|---|
| Motion of no-confidence | Yes | Yes | No |
| New Constitutional Committee | Yes | Yes | No |
| Update Constitution | Yes | No | Yes |
| Hard fork initiation | Yes | Yes | Yes |
| Protocol parameter changes | Yes | Security-relevant only* | Yes |
| Treasury withdrawal | Yes | No | Yes |
| Info action | Yes | Yes | Yes |

\* Changes to security-relevant parameters (block/tx sizes, fees,
`utxoCostPerByte`, `govActionDeposit`, and similar) require an **additional SPO
vote** with its own threshold (`Q5`, ~0.51) — see CIP-1694.

### Step 4: Role-specific guidance

#### For developers

**Integrating governance into a dApp:**

1. **Read governance state**: Query current proposals, DRep list, voting results
   - Use Blockfrost, Koios, or Ogmios governance endpoints
   - Governance state is on-chain in Conway era

2. **Build governance transactions**: Use CIP-95 wallet extensions
   - Register as DRep: `dRepRegistration` certificate
   - Vote on action: `votingProcedure` in transaction body
   - Delegate vote: `voteDelegation` certificate
   - Submit proposal: `proposalProcedure` in transaction body

3. **CIP-95 wallet integration**: Extension to CIP-30 for governance
   - `getRegisteredPubStakeKeys()` -- get stake keys
   - `getPubDRepKey()` -- get DRep key
   - Enables signing governance transactions in browser wallets

4. **SDK support**:
   - **Mesh SDK**: Governance transaction builders available
   - **Evolution SDK**: Conway-era governance — DRep registration via `.registerDRep({ drepCredential })`, voting via `.vote({ votingProcedures })`, DRep delegation, proposals, and committee operations
   - **cardano-cli**: Full governance command set (`cardano-cli latest governance ...`; the era-pinned `conway` group also still works, but prefer `latest`)

#### For DReps

**Getting started as a DRep:**

1. **Register**: Submit a DRep registration certificate with a deposit (currently 500 ADA)
2. **Set metadata**: Publish a metadata document (name, bio, motivations) to a URL
3. **Vote**: Review and vote on governance actions through GovTool or CLI
4. **Communicate**: Share your voting rationale with delegators
5. **Stay active**: DReps must vote periodically to remain active (inactivity period defined by protocol)

**Tools for DReps:**
- **GovTool** (https://gov.tools): Web interface for DRep registration, voting, delegation
- **cardano-cli**: Command-line governance operations
- **Preprod/Preview**: Practice governance flows with test ADA (SanchoNet only for bleeding-edge features)

#### For stake pool operators

**SPO governance participation:**

1. SPOs cast votes actively — a vote is a transaction signed with the pool cold key; pool registration alone casts nothing
2. Optionally, delegate the pool's reward account to a pre-defined voting option (Abstain / No-Confidence) as a standing default — this does NOT apply to hard-fork actions, which always need an explicit vote
3. Vote on: hard fork initiation, motion of no-confidence, new CC members, security-relevant parameter changes, info actions
4. Voting weight proportional to delegated stake
5. Use cardano-cli or SPO-specific tools to cast votes

#### For ADA holders

**Participating in governance:**

1. **Delegate to a DRep**: Choose a DRep whose values align with yours
2. **Delegate to Abstain**: Opt out of governance (your stake does not count toward thresholds)
3. **Delegate to No-Confidence**: Signal dissatisfaction with the Constitutional Committee
4. **Become a DRep yourself**: Register and vote directly
5. **Use GovTool**: Web interface for delegation and exploration

### Step 5: Tools and resources

#### GovTool

- Web-based governance participation tool
- Features: DRep registration, delegation, proposal viewing, voting
- URL: https://gov.tools
- Supports mainnet and testnets

#### Test environments

- Conway governance is live on **mainnet** (since 2024) and fully available on
  **preprod** and **preview** — practice DRep registration, voting, and
  proposals there with faucet test ADA
- **SanchoNet** is the bleeding-edge governance testnet; use it only for
  features not yet on the public testnets

#### cardano-cli governance commands

```bash
# Register as a DRep
cardano-cli latest governance drep registration-certificate \
  --drep-verification-key-file drep.vkey \
  --key-reg-deposit-amt 500000000 \
  --out-file drep-reg.cert

# Create a vote
cardano-cli latest governance vote create \
  --yes \
  --governance-action-tx-id <tx-id> \
  --governance-action-index 0 \
  --drep-verification-key-file drep.vkey \
  --out-file vote.json

# Query governance state
cardano-cli latest query gov-state
cardano-cli latest query drep-state --all-dreps
```

### Step 6: SDK integration examples

#### Querying governance data

```typescript
// Using Blockfrost
const proposals = await blockfrost.governanceProposals();
const dreps = await blockfrost.governanceDReps();
const votes = await blockfrost.governanceProposalVotes(proposalId);
```

```python
# Using Koios
import requests
dreps = requests.get("https://api.koios.rest/api/v1/drep_list").json()
proposals = requests.get("https://api.koios.rest/api/v1/proposal_list").json()
```

#### Building governance transactions

```typescript
// Using Mesh SDK
import { MeshTxBuilder } from "@meshsdk/core";

// DRep registration
const tx = new MeshTxBuilder({ fetcher, submitter });
tx.drepRegistrationCertificate(drepKeyHash, deposit);
// ... build, sign, submit
```

### Step 7: Common issues

- **Deposit requirements**: DRep registration and proposals require deposits (returned when deregistered/enacted)
- **Voting thresholds**: Different action types have different thresholds (see CIP-1694 summary)
- **Era mismatch**: Governance transactions require Conway era; ensure node and tools are up to date
- **Metadata hosting**: DRep and proposal metadata must be hosted at a stable URL with a matching hash
- **Wallet support**: Not all wallets support CIP-95 yet; check wallet compatibility

## References

- `skills/governance-guide/references/cip-1694-summary.md` -- CIP-1694 structure and voting thresholds
- CIP-1694: https://github.com/cardano-foundation/CIPs/tree/master/CIP-1694
- CIP-95: https://github.com/cardano-foundation/CIPs/tree/master/CIP-0095
- GovTool: https://gov.tools
- SanchoNet: https://sancho.network
- Intersect governance: https://www.intersectmbo.org
