## Description:

Controls a sandboxed MetaMask browser extension wallet for autonomous blockchain transactions with configurable spend limits, chain allowlists, protocol restrictions, and approval thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreolf](https://clawhub.ai/user/andreolf)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to let an agent interact with dapps through a separate MetaMask wallet while enforcing configured wallet permissions and transaction limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run setup and dependency commands for wallet automation code that has not been fully reviewed in the provided evidence.

Mitigation: Review package.json, the lockfile, setup scripts, source code, and MetaMask extension provenance before running npm install or npm run setup.

Risk: The skill persists browser wallet state under ~/.agent-wallet, which can retain sensitive wallet session material.

Mitigation: Use only a new low-value wallet in a dedicated unprivileged environment, and delete or rotate ~/.agent-wallet when retiring the setup.

Risk: Automated blockchain transactions can spend real assets if permission constraints are too broad or configured incorrectly.

Mitigation: Start with small funds, strict spend caps, narrow chain and protocol allowlists, and explicit approval thresholds for higher-value transactions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include transaction intents, approval requests, balances, transaction history, and setup or troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
