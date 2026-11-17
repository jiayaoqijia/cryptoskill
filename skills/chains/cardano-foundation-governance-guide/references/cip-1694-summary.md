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
   - Must vote or submit an update certificate within `dRepActivity` epochs to stay active (simplified, the ledger tracks this as an expiry epoch, read that rather than counting epochs). An inactive DRep stays registered, but its delegated stake stops counting as active voting stake until it votes or updates again
   - Two special "auto-DReps": Abstain and No-Confidence

3. **Stake Pool Operators (SPOs)**
   - Vote on specific action types (no-confidence, CC changes, hard forks, security-relevant parameter changes, Info)
   - Voting power proportional to delegated stake
   - Existing infrastructure, no additional registration needed for governance

### Delegation

A stake credential can delegate its voting power to exactly one DRep (or auto-DRep) at a time. Since the end of the bootstrap phase (protocol versions 10 and 11), every key-hash stake credential in a transaction's withdrawals, including a zero-amount withdrawal, must be delegated to a DRep or an auto-DRep, or the transaction is rejected (`ConwayWdrlNotDelegatedToDRep`). Script-hash reward credentials are exempt. Undelegated rewards are not lost, and become withdrawable as soon as the credential delegates. [CIP-0181](../../../docs/sources/cips/CIP-0181/README.md) (Proposed) would remove this requirement. A credential delegates to one of:

- **Specific DRep**: Your stake counts toward that DRep's voting power
- **Abstain**: Your stake is excluded from the active voting stake used for DRep thresholds (it still counts as registered stake for incentives)
- **No-Confidence**: Your stake counts as `Yes` on every motion of no-confidence and as `No` on every other action, and it stays part of the active voting stake

Delegation is separate from stake delegation to pools. You delegate to a DRep for governance and to a pool for staking independently.

## Governance Action Types

Seven types of governance actions can be proposed and voted on:

### 1. Motion of No-Confidence
- **Purpose**: Express lack of confidence in the current Constitutional Committee
- **Required votes**: DReps + SPOs
- **CC vote**: Not required (they cannot block their own removal)
- **Effect**: Puts governance into a state of no-confidence: the current CC can no longer vote, and it must be replaced before other actions can be ratified

### 2. New Constitutional Committee / Quorum Size
- **Purpose**: Elect new CC members or change quorum requirements
- **Required votes**: DReps + SPOs
- **CC vote**: Not required
- **Effect**: Replaces or modifies the CC membership and thresholds

### 3. New Constitution or Guardrails Script
- **Purpose**: Change the Cardano Constitution document and/or the guardrails script
- **Required votes**: DReps + CC
- **SPO vote**: Not required
- **Effect**: New constitution anchor and optional guardrails script hash recorded on-chain (no hash means no guardrails script)

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
- **Categories**: Network, Economic, Technical, Governance. An update that touches several groups needs the highest threshold among them

### 6. Treasury Withdrawal
- **Purpose**: Withdraw ADA from the treasury for funding proposals
- **Required votes**: DReps + CC
- **SPO vote**: Not required
- **Effect**: ADA transferred from the treasury to the listed reward accounts (a map of stake credentials to lovelace)

### 7. Info Action
- **Purpose**: Non-binding poll or sentiment check
- **Votes**: CC, DReps and SPOs can all vote
- **Thresholds**: DRep and SPO thresholds are both 100%. CIP-1694 sets them that
  high because any lower threshold would make it impossible to poll support above it
- **Effect**: Never ratified or enacted, it only records sentiment on-chain

## Voting Thresholds

Each action type has specific thresholds that must be met for approval. The values below are the Conway defaults (source: `../../docs/sources/developer-portal/developers/curriculum/staking-governance/governance.md`), the thresholds themselves are governance parameters:

| Action | DRep threshold | SPO threshold | CC threshold |
|---|---|---|---|
| No-confidence | 67% | 51% | -- |
| New CC (normal) | 67% | 51% | -- |
| New CC (no-confidence state) | 60% | 51% | -- |
| New Constitution / guardrails | 75% | -- | 2/3 quorum |
| Hard fork | 60% | 51% | 2/3 quorum |
| Protocol params (network) | 67% | --* | 2/3 quorum |
| Protocol params (economic) | 67% | --* | 2/3 quorum |
| Protocol params (technical) | 67% | --* | 2/3 quorum |
| Protocol params (governance) | 75% | --* | 2/3 quorum |
| Treasury withdrawal | 67% | -- | 2/3 quorum |
| Info action | 100% | 100% | can vote, never ratified |

\* Security-relevant parameter changes additionally require an SPO vote with
its own threshold (`Q5`, 51% by default), regardless of parameter group.

The CC column is not fixed either: the committee threshold is the share of
non-expired committee members voting `Yes`, it is set and changed by Update
committee actions, so query `committee-state` for the current value. If fewer
non-expired members remain than `committeeMinSize`, the committee cannot
ratify anything that needs its approval.

DRep thresholds are a share of the DRep active voting stake: registered stake
delegated to an active DRep or to No-Confidence. Stake delegated to Abstain and
explicit `Abstain` votes are not part of it, and stake whose DRep does not vote
counts like `No`. SPO thresholds are measured against the SPOs' active voting
stake, computed separately, except for a hard fork, where they are measured
against the stake of all stake pools.

Exact values are themselves governance parameters
(`dRepVotingThresholds` / `poolVotingThresholds`) — query the current ones
rather than trusting a table.

## Proposal Lifecycle

1. **Submission**: Anyone can submit a governance action by including a `proposalProcedure` in a transaction, along with a deposit
2. **Voting period**: Actions are open for voting for a defined number of epochs
3. **Ratification**: If thresholds and the other ratification conditions below are met, the action is ratified at the epoch boundary (Info actions never are)
4. **Enactment**: Ratified actions are enacted (applied) at the following epoch boundary
5. **Expiration**: Actions not ratified within the voting period expire. The deposit is returned on ratification or expiry, whichever comes first

Apart from treasury withdrawals and Info actions, each action names the ID of
the most recently enacted action of its kind, or none if no such action was
enacted yet. Motions of no-confidence and committee updates share one kind:
both point at the most recent of either. This keeps actions of the same kind
from clashing by accident. Two actions of the same kind can still be enacted
at the same time, but only when they are deliberately designed to do so.

A successful (ratified) motion of no-confidence, committee update,
constitution change or hard fork delays the ratification of all other actions
until the epoch after its enactment.

The bootstrap phase, in which only some action types could be ratified, ended
with protocol version 10 (the Plomin hard fork). On networks at protocol version 10 or later all action types are live.

## Deposits

- **DRep registration deposit**: Protocol parameter `dRepDeposit`, query the current value. Returned on deregistration.
- **Governance action deposit**: Protocol parameter `govActionDeposit`, query the current value. Returned as soon as the action is ratified or expires.

## Treasury

- The Cardano treasury accumulates ADA from transaction fees and monetary expansion
- Treasury withdrawals require DRep + CC approval
- Enables community-directed funding of development, marketing, education

## Constitutional Committee Details

- Members serve term-limited roles (defined in epochs)
- Enough non-expired CC members must vote `Yes` to meet the committee threshold for an action to count as constitutional
- CC can be in normal state or no-confidence state
- An elected empty committee is different: it is not a state of no-confidence, and actions can still be enacted
- In no-confidence state the committee cannot vote, and it must be replaced before other actions can be ratified. The replacement is an Update committee action, which needs no CC vote and has its own thresholds for this state (see the table)
- CC members can be added/removed via governance action

## Guardrails

The Constitution includes guardrails -- constraints on what governance actions can do:

- **Parameter bounds**: Min/max values for protocol parameters
- **Spending limits**: Caps on treasury withdrawals per period
- **Procedural requirements**: Metadata requirements, rationale standards
- **Script-enforced guardrails**: When a guardrails script is set, every protocol parameter change and treasury withdrawal proposal must carry its hash as the proposal's policy hash, include the script as a witness (directly or via a reference input) and satisfy it. Without a guardrails script the policy hash must be absent

Guardrails protect the network from harmful parameter changes while still allowing governance flexibility.

## Key Protocol Parameters for Governance

- `dRepDeposit`: Deposit for DRep registration
- `govActionDeposit`: Deposit for governance action proposals
- `dRepActivity`: Epochs a DRep can go without voting or updating before it becomes inactive; an inactive DRep stays registered, but its stake stops counting until it votes or updates
- `govActionLifetime`: Number of epochs a governance action stays open for voting
- `committeeMinSize`: Minimum number of CC members
- `committeeMaxTermLength`: Maximum term for CC members in epochs
- `dRepVotingThresholds`: Thresholds for each action type (DRep)
- `poolVotingThresholds`: Thresholds for each action type (SPO)
