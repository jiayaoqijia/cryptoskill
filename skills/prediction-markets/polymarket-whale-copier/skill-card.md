## Description: <br>
Monitors a target Polymarket wallet and computes configurable copy-trade actions, with security evidence noting that live trading and auto-redemption are not implemented. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to monitor public Polymarket wallet activity, apply configurable copy-size and risk limits, and produce logs or dry-run trade calculations. Reviewers should treat automated trading and redemption claims cautiously because the security evidence states those behaviors are not implemented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a Polymarket private key. <br>
Mitigation: Do not provide a main wallet private key; test only with dry-run behavior and a separate low-balance wallet. <br>
Risk: The release advertises automated trading and auto-redemption, but security evidence says those behaviors are not implemented. <br>
Mitigation: Review the scripts before installation and do not rely on live trading or redemption until the implementation and documentation are corrected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cassh100k/polymarket-whale-copier) <br>
- [Polymarket Leaderboard](https://polymarket.com/leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text logs, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode is enabled by default; live trading and auto-redemption require implementation review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
