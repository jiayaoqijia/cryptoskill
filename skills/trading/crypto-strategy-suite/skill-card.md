## Description:

Crypto Strategy Suite provides BTC/USDT grid, signal, crash-buy, futures trend, and futures breakout strategy workflows across spot and futures trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holiver](https://clawhub.ai/user/holiver)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading automation developers use this skill to configure and run BTC/USDT spot and futures strategy workflows through an agent after supplying exchange and SkillPay credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated spot and futures trading can place live orders using exchange API keys without enough live-trading guardrails.

Mitigation: Use testnet or paper trading first, avoid enabling all strategies until limits are understood, and review each proposed configuration before live use.

Risk: Exchange API credentials could grant broader access than the skill needs.

Mitigation: Create keys limited to the required trading pair and permissions, and disable withdrawals.

Risk: The skill includes paid per-call SkillPay billing behavior.

Mitigation: Confirm SkillPay charging terms and account balance behavior before invocation.

## Reference(s):

- [Crypto Strategy Suite on ClawHub](https://clawhub.ai/holiver/skills/crypto-strategy-suite)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell environment commands and strategy configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exchange API credentials and a SkillPay API key; outputs should be reviewed before any live trading action.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
