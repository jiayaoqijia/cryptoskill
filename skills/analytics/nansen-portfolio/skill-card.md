## Description: <br>
How has a wallet's portfolio changed over time? Historical balances, current snapshot, and per-token PnL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to inspect how a blockchain wallet's portfolio changed over time, compare historical and current balances, and review per-token profit and loss through the Nansen CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the nansen-cli package and a Nansen API key. <br>
Mitigation: Install nansen-cli only from a trusted source and provide the API key through the NANSEN_API_KEY environment variable. <br>
Risk: Wallet address lookups can reveal sensitive research interests or link searched addresses to the user's account. <br>
Mitigation: Avoid querying addresses when the lookup itself, or its association with the account, would be sensitive. <br>
Risk: CLI output may be incomplete or misunderstood when used to compare historical balances, current holdings, and per-token PnL. <br>
Mitigation: Review the returned fields and compare historical-balances, balance, and pnl outputs before making decisions from the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-portfolio-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI result-field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the NANSEN_API_KEY environment variable and the nansen CLI from the nansen-cli Node package.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
