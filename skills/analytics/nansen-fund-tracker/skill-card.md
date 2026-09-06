## Description: <br>
What are crypto funds and VCs holding right now? Cross-chain fund portfolios and net accumulation signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, researchers, and agents use this skill to query Nansen smart-money holdings and netflow data for crypto funds and VCs across Ethereum and Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external nansen-cli package and a Nansen API key. <br>
Mitigation: Confirm the package source before installation and provide an API key with only the access needed for research queries. <br>
Risk: Unexpected Nansen CLI commands could expose more account data than intended if the API key has broad permissions. <br>
Mitigation: Review proposed nansen commands before execution, especially when using API keys with privileges beyond read-only research. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-fund-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
