## Description: <br>
Executes perpetual trades through Maxxit's Lazy Trading API, supports Indian stock trading through Zerodha Kite, and provides market research, risk management, copy-trading, and ZK-verified alpha workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhi152003](https://clawhub.ai/user/abhi152003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and trading agents use this skill to inspect account state, research markets, and execute or manage confirmed trades on supported venues. Developers can also run bundled strategy scripts that fetch Binance market data and route signals through Maxxit endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or change live financial trades automatically with limited safeguards. <br>
Mitigation: Run only with intentional trading access, require an approval gate or dry-run controls before live funds, and set strict venue, symbol, collateral, and leverage limits. <br>
Risk: MAXXIT_API_KEY and related trading credentials can authorize account access and order execution. <br>
Mitigation: Keep credentials secret, verify MAXXIT_API_URL is the official HTTPS Maxxit origin, and rotate or revoke keys when access is no longer needed. <br>
Risk: Strategy scripts derive trading signals from market data and can route those signals to Maxxit execution endpoints. <br>
Mitigation: Review generated orders and strategy parameters before deployment, start with minimal exposure, and monitor logs and account positions during execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abhi152003/skills/maxxit-lazy-trading) <br>
- [Maxxit App](https://maxxit.ai) <br>
- [Lazy Trading Setup](https://maxxit.ai/lazy-trading) <br>
- [Maxxit OpenClaw Verification](https://www.maxxit.ai/openclaw) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXXIT_API_KEY and MAXXIT_API_URL; bundled strategy scripts may create local state and log files.] <br>

## Skill Version(s): <br>
1.2.20 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
