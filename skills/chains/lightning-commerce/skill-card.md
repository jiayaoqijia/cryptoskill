## Description:

End-to-end agentic commerce workflow using Lightning Network. Use when an agent needs to set up a full payment stack (lnd + lnget + aperture), buy or sell data via L402, or enable agent-to-agent micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure a Lightning Network commerce stack for buying L402-protected resources, hosting paid endpoints, and managing agent-to-agent micropayments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents through Lightning payment workflows that can put real funds at risk.

Mitigation: Use isolated testnet or intentionally small funded wallets by default, and require explicit user approval before any payment-capable command runs.

Risk: The security evidence notes plaintext wallet seed and passphrase storage.

Mitigation: Replace plaintext seed and passphrase storage with stronger secret handling before use with meaningful funds.

Risk: The workflow includes insecure paywall setup options that are unsafe for exposed endpoints.

Mitigation: Avoid insecure endpoint configuration on exposed services and review transport and access controls before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roasbeef/skills/lightning-agent-commerce)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, funding, channel, L402 client, paywall, cost-control, and shutdown workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
