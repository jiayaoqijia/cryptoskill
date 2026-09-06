## Description: <br>
Live crypto trading on Hyperliquid via Katbot.ai. Signal-triggered research to recommendation to execution workflow with Market Intelligence, research, and configurable signal monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claytantor](https://clawhub.ai/user/claytantor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Katbot.ai for signal-triggered Hyperliquid portfolio research, recommendations, monitoring, and user-confirmed trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live crypto trading actions that affect real funds and depends on persistent trading credentials. <br>
Mitigation: Use paper/testnet mode or a dedicated limited-permission agent wallet with minimal funds, and keep auto-execution disabled unless explicitly reviewed. <br>
Risk: The skill requires trust in Katbot.ai with a Hyperliquid agent key and remote API calls. <br>
Mitigation: Install only if the user trusts Katbot.ai with the agent key, review any cron schedule before enabling it, and remove the local identity directory when no longer using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/claytantor/katbot-trading) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/claytantor) <br>
- [Katbot API endpoint](https://api.katbot.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local identity and signal-trigger configuration files during setup.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
