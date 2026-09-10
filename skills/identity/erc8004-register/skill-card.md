## Description:

Register AI agents on-chain, update metadata, validate registrations, and auto-fix broken profiles via the ERC-8004 Identity Registry. Supports Base, Ethereum, Polygon, Monad, BNB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetherstacey](https://clawhub.ai/user/aetherstacey)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to register, update, inspect, validate, and repair ERC-8004 agent identity records across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet mnemonic or private key exposure could compromise funds or agent ownership.

Mitigation: Use a dedicated low-value wallet and avoid storing primary secrets in shell history, shared terminals, logs, or long-lived environment files.

Risk: Register, update, and fix operations can submit live on-chain transactions.

Mitigation: Confirm the selected chain, wallet, agent ID, and transaction intent before broadcasting; use --dry-run before fix operations.

Risk: Viewing or validating agent metadata can make outbound requests to URLs controlled by third parties.

Mitigation: Run in an isolated Python environment with appropriate network controls and review fetched metadata before trusting it.

Risk: Unpinned Python dependencies or ambient environments can change runtime behavior.

Mitigation: Install dependencies in an isolated environment and pin web3 and eth-account versions for repeatable operation.

## Reference(s):

- [ERC-8004 registration-v1 specification](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [ClawHub skill page](https://clawhub.ai/aetherstacey/skills/erc8004-register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Python CLI commands that require wallet environment variables, network access, and transaction confirmation.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
