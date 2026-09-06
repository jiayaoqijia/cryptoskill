# CIP-1694 Summary: Cardano On-Chain Governance

CIP-1694 defines Cardano's on-chain governance mechanism, enacted in the Conway era. It establishes a decentralized decision-making system with three governance bodies.

## Governance Structure

### Three Governance Bodies

1. **Constitutional Committee (CC)**
   - A group of members who certify that governance actions are constitutional
   - Does not propose or prioritize -- only votes on constitutionality
   - Has term limits and can be replaced via governance action
   - Operates under a defined quorum threshold
   - Members identified by credential (key hash or script hash)

2. **Delegated Representatives (DReps)**
   - ADA holders who actively vote on governance actions
   - Any ADA holder can register as a DRep (requires deposit)
   - Voting power proportional to delegated stake
   - Must remain active (vote within a defined period) to stay registered
   - Two special "auto-DReps": Abstain and No-Confidence

3. **Stake Pool Operators (SPOs)**
   - Vote on specific action types (hard forks, no-confidence, CC changes)
   - Voting power proportional to delegated stake
   - Existing infrastructure, no additional registration needed for governance

### Delegation

Every ADA holder delegates their voting power to exactly one DRep (or auto-DRep):

- **Specific DRep**: Your stake counts toward that DRep's voting power
- **Abstain**: Your stake is excluded from governance thresholds entirely
- **No-Confidence**: Your stake counts as a perpetual no-confidence vote against the CC

Delegation is separate from stake delegation to pools. You delegate to a DRep for governance and to a pool for staking independently.

## Governance Action Types

Seven types of governance actions can be proposed and voted on:

### 1. Motion of No-Confidence
- **Purpose**: Express lack of confidence in the current Constitutional Committee
- **Required votes**: DReps + SPOs
- **CC vote**: Not required (they cannot block their own removal)
- **Effect**: Removes the current CC, triggering need for a new one

### 2. New Constitutional Committee / Quorum Size
- **Purpose**: Elect new CC members or change quorum requirements
- **Required votes**: DReps + SPOs
- **CC vote**: Not required
- **Effect**: Replaces or modifies the CC membership and thresholds

### 3. Update to the Constitution
- **Purpose**: Change the Cardano Constitution document
- **Required votes**: DReps + CC
- **SPO vote**: Not required
- **Effect**: New constitution hash recorded on-chain

### 4. Hard Fork Initiation
- **Purpose**: Trigger a hard fork to a new protocol version
- **Required votes**: DReps + SPOs + CC
- **Effect**: All three bodies must agree on protocol upgrades

### 5. Protocol Parameter Changes
- **Purpose**: Modify protocol parameters (fees, block size, cost models, etc.)
- **Required votes**: DReps + CC
- **SPO vote**: Required additionally for **security-relevant parameters**
  (`maxBlockBodySize`, `maxTxSize`, `maxBlockHeaderSize`, `maxValueSize`,
  `maxBlockExecutionUnits`, `txFeePerByte`, `txFeeFixed`, `utxoCostPerByte`,
  `govActionDeposit`, `minFeeRefScriptCostPerByte`) — separate threshold `Q5`
- **Effect**: Parameters grouped into categories with different thresholds
- **Categories**: Network, Economic, Technical, Governance

### 6. Treasury Withdrawal
- **Purpose**: Withdraw ADA from the treasury for funding proposals
- **Required votes**: DReps + CC
- **SPO vote**: Not required
- **Effect**: ADA transferred from treasury to specified addresses

### 7. Info Action
- **Purpose**: Non-binding poll or sentiment check
- **Required votes**: All three bodies — CC, DReps, and SPOs
- **Thresholds**: DRep and SPO thresholds are both set to 100% (per CIP-1694,
  so polls can only be read against the maximum bar, never "passed" cheaply)
- **Effect**: No on-chain effect; records community sentiment

## Voting Thresholds

Each action type has specific thresholds that must be met for approval:

| Action | DRep threshold | SPO threshold | CC threshold |
|---|---|---|---|
| No-confidence | 67% | 51% | -- |
| New CC (normal) | 67% | 51% | -- |
| New CC (no-confidence state) | 60% | 51% | -- |
| Update Constitution | 75% | -- | 2/3 quorum |
| Hard fork | 60% | 51% | 2/3 quorum |
| Protocol params (network) | 67% | --* | 2/3 quorum |
| Protocol params (economic) | 67% | --* | 2/3 quorum |
| Protocol params (technical) | 67% | --* | 2/3 quorum |
| Protocol params (governance) | 75% | --* | 2/3 quorum |
| Treasury withdrawal | 67% | -- | 2/3 quorum |
| Info action | 100% | 100% | 2/3 quorum |

\* Security-relevant parameter changes additionally require an SPO vote with
its own threshold (`Q5`, ~51%), regardless of parameter group.

Thresholds are expressed as percentage of active voting stake (not total
stake). Exact values are themselves governance parameters
(`dRepVotingThresholds` / `poolVotingThresholds`) — query the current ones
rather than trusting a table.

## Proposal Lifecycle

1. **Submission**: Anyone can submit a governance action by including a `proposalProcedure` in a transaction, along with a deposit
2. **Voting period**: Actions are open for voting for a defined number of epochs
3. **Ratification**: If thresholds are met, the action is ratified at the epoch boundary
4. **Enactment**: Ratified actions are enacted (applied) at the following epoch boundary
5. **Expiration**: Actions that do not meet thresholds within the voting period expire; deposit is returned

## Deposits

- **DRep registration deposit**: Configurable protocol parameter (initially 500 ADA). Returned on deregistration.
- **Governance action deposit**: Configurable protocol parameter (initially 100,000 ADA). Returned when action is enacted or expires.

## Treasury

- The Cardano treasury accumulates ADA from transaction fees and monetary expansion
- Treasury withdrawals require DRep + CC approval
- Enables community-directed funding of development, marketing, education

## Constitutional Committee Details

- Members serve term-limited roles (defined in epochs)
- A quorum of CC members must vote for an action to be considered constitutionally valid
- CC can be in normal state or no-confidence state
- In no-confidence state, governance can still operate with adjusted thresholds
- CC members can be added/removed via governance action

## Guardrails

The Constitution includes guardrails -- constraints on what governance actions can do:

- **Parameter bounds**: Min/max values for protocol parameters
- **Spending limits**: Caps on treasury withdrawals per period
- **Procedural requirements**: Metadata requirements, rationale standards
- **Script-enforced guardrails**: Some guardrails can be enforced by on-chain scripts (guardrails script)

Guardrails protect the network from harmful parameter changes while still allowing governance flexibility.

## Key Protocol Parameters for Governance

- `dRepDeposit`: Deposit for DRep registration
- `govActionDeposit`: Deposit for governance action proposals
- `dRepActivity`: Number of epochs before inactive DRep is considered dormant
- `govActionLifetime`: Number of epochs a governance action stays open for voting
- `committeeMinSize`: Minimum number of CC members
- `committeeMaxTermLength`: Maximum term for CC members in epochs
- `dRepVotingThresholds`: Thresholds for each action type (DRep)
- `poolVotingThresholds`: Thresholds for each action type (SPO)
