## Description:

This skill guides agents through installing, configuring, verifying, and using the NEAR Protocol CLI (near-cli-rs) across common platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuongdcdev](https://clawhub.ai/user/cuongdcdev)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to help agents install NEAR CLI, find the absolute near binary path, verify setup, and prepare safe commands for NEAR account, token, staking, contract, and transaction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or unpinned installer commands can execute changing code during setup.

Mitigation: Prefer a pinned, verified NEAR CLI release and review installer sources before running shell, npx, npm, or cargo installation commands.

Risk: Mainnet signing, transfer, staking, deployment, account import, or account export actions can move assets or expose credentials.

Mitigation: Use testnet or read-only commands by default, never share seed phrases or private keys with an agent, and require explicit confirmation before any mainnet signing or credential operation.

## Reference(s):

- [NEAR CLI GitHub](https://github.com/near/near-cli-rs)
- [NEAR CLI Releases](https://github.com/near/near-cli-rs/releases)
- [NEAR Protocol Docs](https://docs.near.org/)
- [Rustup](https://rustup.rs/)
- [NEAR Explorer](https://nearblocks.io/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use the absolute path to the near binary before execution.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
