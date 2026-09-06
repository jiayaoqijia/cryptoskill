## Description: <br>
What DeFi positions does a wallet hold? Protocol-by-protocol breakdown of assets, debts, and rewards across chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to ask the Nansen CLI for protocol-level DeFi positions and spot token balances for a wallet address across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Nansen API key and the nansen-cli package. <br>
Mitigation: Install only from a trusted nansen-cli source and provide NANSEN_API_KEY through normal secret-management practices rather than embedding it in prompts or files. <br>
Risk: Wallet addresses queried through the skill are processed by Nansen. <br>
Mitigation: Use the skill only for wallet addresses you are comfortable sending to Nansen for position and balance lookups. <br>
Risk: The DeFi position command may return empty results for wallets without tracked positions. <br>
Mitigation: Treat empty DeFi results as an absence of tracked positions and cross-check spot balances when a complete exposure view is required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nansen-devops/nansen-defi-positions) <br>
- [Publisher Profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the NANSEN_API_KEY environment variable and the nansen CLI binary; commands return wallet portfolio and token balance data from Nansen.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
