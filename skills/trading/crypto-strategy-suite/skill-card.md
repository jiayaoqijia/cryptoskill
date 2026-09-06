## Description: <br>
Provides five BTC/USDT quantitative trading strategies covering spot and futures workflows: grid trading, signal trading, crash buying, futures trend, and futures breakout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Holiver](https://clawhub.ai/user/Holiver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto strategy operators use this skill to configure and run BTC/USDT spot and futures trading workflows from an agent. It requires exchange API credentials and SkillPay billing credentials before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run live automated spot and leveraged futures trading through exchange credentials. <br>
Mitigation: Start on testnet, use a separate low-balance account, create trade-only exchange keys with withdrawals disabled and IP restrictions, and set external trading and leverage limits. <br>
Risk: The skill uses paid per-call billing through SkillPay. <br>
Mitigation: Install only if paid billing is intended, and verify pricing, balance, and billing key scope before use. <br>
Risk: Automated monitoring loops and open orders may continue after launch. <br>
Mitigation: Confirm how to stop the monitoring loop and cancel open orders before running strategies against a live account. <br>


## Reference(s): <br>
- [SkillPay](https://skillpay.me) <br>
- [ClawHub skill listing](https://clawhub.ai/Holiver/crypto-strategy-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, environment-variable examples, and strategy-selection prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SkillPay payment links when billing fails and strategy-monitoring instructions after selection.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
