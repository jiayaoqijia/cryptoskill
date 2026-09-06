## Description: <br>
Smart money tracking - netflow, trades, holdings, perp trades. Use when finding what smart money wallets are buying/selling or tracking whale activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run Nansen smart-money CLI queries for token netflow, DEX trades, holdings, and Hyperliquid perpetual trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external nansen-cli package and uses NANSEN_API_KEY for analytics queries. <br>
Mitigation: Install only from a trusted nansen-cli source, use a restricted or dedicated API key where possible, and monitor API usage or quota. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-smart-money-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI option guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce table or CSV output when the referenced Nansen CLI commands are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
