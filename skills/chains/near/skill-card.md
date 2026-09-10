## Description:

Universal cross-chain swap and bridge guidance for OpenClaw using the NEAR Intents 1Click SDK across chains including NEAR, Base, Ethereum, Solana, and Bitcoin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuongdcdev](https://clawhub.ai/user/cuongdcdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a reference for preparing NEAR Intents 1Click cross-chain swap or bridge workflows, including quote requests, deposit instructions, refund-address handling, and optional NEAR auto mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto swap guidance may lead an agent to prepare transfers involving real funds, and the security summary notes that auto mode can spend from a configured NEAR wallet without a clearly required final user confirmation.

Mitigation: Prefer manual mode, verify the asset, amount, recipient, refund address, quote, deadline, and fees with the user, and require explicit approval before any transaction.

Risk: Incorrect refund addresses for non-NEAR origin chains can cause permanent loss if a swap fails.

Mitigation: Ask the user for the origin-chain refund wallet, repeat it back for confirmation, and never infer or substitute a refund address.

Risk: Auto mode requires wallet credentials and may increase financial exposure.

Mitigation: Use a limited wallet for auto mode, avoid exposing private keys, and keep credentials out of committed files.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/cuongdcdev/openclaw-near-skills/tree/main/near-intents)
- [ClawHub skill page](https://clawhub.ai/cuongdcdev/skills/near-intents)
- [NEAR Intents 1Click API documentation](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api)
- [1Click SDK TypeScript repository](https://github.com/defuse-protocol/one-click-sdk-typescript)
- [NEAR Intents documentation](https://docs.near-intents.org)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with TypeScript examples and environment configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the release artifact; guidance may describe manual and auto crypto swap workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
