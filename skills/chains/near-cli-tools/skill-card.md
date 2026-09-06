## Description: <br>
Guides agents through installing, configuring, verifying, and using near-cli-rs for NEAR Protocol account, token, staking, smart contract, and transaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuongdcdev](https://clawhub.ai/user/cuongdcdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the NEAR CLI across Linux, macOS, Windows, WSL, Node.js, and Rust environments. It supports setup, verification, troubleshooting, and common NEAR blockchain actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NEAR CLI actions can send tokens, stake assets, deploy contracts, sign transactions, or change account state. <br>
Mitigation: Before execution, confirm the exact account, network, recipient, amount, fees, and full command text with the user. <br>
Risk: Account import and export workflows can expose seed phrases, private keys, or other credentials. <br>
Mitigation: Do not ask users to share seed phrases or private keys in chat or logs, and prefer testnet or low-value accounts for first runs. <br>
Risk: Installer examples include remote shell scripts and package-manager commands. <br>
Mitigation: Use verified release downloads and review installer commands before running them, especially when commands pipe remote content into a shell. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cuongdcdev/near-cli-tools) <br>
- [NEAR CLI GitHub Repository](https://github.com/near/near-cli-rs) <br>
- [NEAR CLI Releases](https://github.com/near/near-cli-rs/releases) <br>
- [NEAR Protocol Documentation](https://docs.near.org/) <br>
- [Rustup](https://rustup.rs/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
