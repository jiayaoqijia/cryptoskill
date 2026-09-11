## Description:

WalletConnect Requester lets agents connect to user wallets through WalletConnect v2 to request transactions and signatures while users approve actions in their own wallet and private keys stay out of the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create WalletConnect sessions, request wallet-approved transactions, request wallet-approved signatures, list sessions, and disconnect sessions without handling private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request wallet transactions and signatures, and custom methods may broaden wallet permissions.

Mitigation: Use a dedicated wallet, read every wallet prompt carefully, avoid custom --methods unless understood, and disconnect sessions when finished.

Risk: WalletConnect session data and audit logs are stored under ~/.walletconnect-requester/ and may expose sensitive session or activity metadata.

Mitigation: Restrict file permissions, delete stale session files, and review audit logs before sharing them.

Risk: WalletConnect URIs contain a symKey and are printed for connection or QR generation.

Mitigation: Treat WalletConnect URIs and QR codes as sensitive and avoid logging or sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bevanding/skills/walletconnect-requester)
- [WalletConnect Cloud](https://cloud.walletconnect.com/)
- [Security Model](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create WalletConnect session data and audit logs under ~/.walletconnect-requester/ and optional QR code image files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
