## Description:

Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction. Also supports raw signing and polymarket betting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piperwallet](https://clawhub.ai/user/piperwallet)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent create and operate policy-controlled wallets for EVM transfers, swaps, smart contract transactions, raw signing, and Polymarket activity without exposing private keys to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent transaction-capable wallet access with broad financial authority.

Mitigation: Claim the wallet before funding it, configure strict policies first, and require human approval for meaningful transactions.

Risk: Raw signing and arbitrary calldata can authorize actions that are difficult for users or agents to inspect safely.

Mitigation: Avoid raw signing and arbitrary calldata unless the user fully understands the payload and the receiving contract or protocol.

Risk: API keys may be exposed if stored in a project directory or another shared, synced, logged, or committed location.

Mitigation: Store API keys only in a private credential store or protected credentials directory, not in project files.

## Reference(s):

- [Vincent Agent Wallet skill page](https://clawhub.ai/piperwallet/skills/vincent-agent-wallet)
- [Vincent wallet service](https://heyvincent.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, API request examples, configuration guidance, and user-facing wallet details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include claim URLs, wallet addresses, API-key handling steps, policy guidance, transaction status, and approval instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
