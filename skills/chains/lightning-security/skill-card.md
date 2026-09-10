## Description:

Set up an lnd remote signer container that holds private keys separately from the agent. Exports a credentials bundle (accounts JSON, TLS cert, admin macaroon) for watch-only litd nodes. Container-first with Docker, native fallback. Use when firewalling private key material from AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and Lightning node operators use this skill to configure an lnd remote signer that keeps private key material on a separate signer machine while a watch-only litd node handles agent-facing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The credential bundle may include an admin macaroon with broad RPC authority.

Mitigation: Replace the admin macaroon with a signer-scoped macaroon before production use.

Risk: Seed, wallet password, and credential bundle handling can expose sensitive material through plaintext files or copy-paste transfer.

Mitigation: Protect secret files with strict permissions, avoid plaintext seed storage when possible, and transfer credentials through a secured channel.

Risk: Signer REST/RPC endpoints can be exposed beyond the intended watch-only node.

Mitigation: Bind services to private interfaces and restrict access with a VPN, firewall, or equivalent network controls.

Risk: Docker images or source builds can introduce supply-chain risk.

Mitigation: Pin and verify Docker images, source commits, and release artifacts before using the signer with real funds.

## Reference(s):

- [Remote Signer Architecture](references/architecture.md)
- [ClawHub release page](https://clawhub.ai/roasbeef/skills/lightning-security-module)
- [lnd source repository](https://github.com/lightningnetwork/lnd.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce credential bundle file paths and operational commands for Docker or native lnd signer setup.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
