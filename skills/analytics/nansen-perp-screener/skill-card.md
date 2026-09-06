## Description: <br>
What is the state of the Hyperliquid perp market? Top contracts by volume/OI, trader leaderboard, and SM perp activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Nansen market-data views for Hyperliquid perpetual contracts, trader leaderboards, and smart-money perpetual trade activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires NANSEN_API_KEY to be available to the nansen-cli package. <br>
Mitigation: Install and use it only in environments where sharing that credential with the third-party CLI is acceptable, and scope or rotate the key according to local policy. <br>
Risk: The workflow depends on a third-party CLI package for market-data queries. <br>
Mitigation: Review the nansen-cli package provenance before installation and keep execution limited to the documented read-only Nansen market-data commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-perp-screener) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with Nansen CLI command examples and market-data field descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY for live market-data queries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
