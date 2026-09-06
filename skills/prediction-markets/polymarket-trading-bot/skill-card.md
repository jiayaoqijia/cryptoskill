## Description: <br>
Autonomous prediction market agent - analyzes markets, researches news, and identifies trading opportunities <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BOMBFUOCK](https://clawhub.ai/user/BOMBFUOCK) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket markets, research news and sentiment, estimate trading edge, and prepare or execute user-approved trades through a local poly CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with real-money Polymarket trading flows and asks for wallet private-key access. <br>
Mitigation: Use a dedicated low-balance wallet, avoid primary wallet keys, and confirm each trade unless explicit limits and monitoring are configured. <br>
Risk: Autonomous trading behavior could place orders based on incorrect analysis or stale market information. <br>
Mitigation: Keep autonomous mode disabled by default, require user approval for trades, and set clear trade-size limits. <br>
Risk: The install path uses Python dependencies that are not pinned in the supplied requirements. <br>
Mitigation: Install in an isolated virtual environment and pin or review dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BOMBFUOCK/polymarket-trading-bot) <br>
- [BOMBFUOCK Publisher Profile](https://clawhub.ai/user/BOMBFUOCK) <br>
- [Clawdis Homepage Metadata](https://clawdhub.com/polymarket-agent) <br>
- [Polymarket Gamma API Endpoint](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB Endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and CLI status tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local poly CLI commands and Polymarket API calls when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact pyproject.toml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
