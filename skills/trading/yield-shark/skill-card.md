## Description:

YieldShark helps agents monitor stablecoin DeFi yields, compare APYs across supported platforms, estimate gas-adjusted returns, and generate yield reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gztanht](https://clawhub.ai/user/gztanht)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query and compare DeFi stablecoin yield opportunities for USDT, USDC, and DAI across supported protocols and chains. Its outputs are informational and should be independently verified before any financial action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print financial-looking APYs, rankings, risk ratings, and recommendations that may be hard-coded, stale, or misleading.

Mitigation: Treat all outputs as informational only and independently verify APYs, protocol risk, liquidity, and destination URLs before making any financial decision.

Risk: The skill prints sponsorship wallet addresses that could be mistaken for user wallets or deposit destinations.

Mitigation: Do not send funds to any printed address unless you intentionally choose to sponsor the publisher and have verified the address through a trusted source.

Risk: Bundled publishing-token instructions may be unsafe for users who are not the authorized publisher.

Mitigation: Ignore publishing-token workflows unless you are the authorized publisher using a secure, pinned CLI workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gztanht/skills/yield-shark)
- [DeFiLlama Yields API](https://yields.llama.fi/pools)
- [Platform Configuration](config/platforms.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Console text, Markdown reports, and JSON reports from Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include APY rankings, gas estimates, risk ratings, platform links, sponsorship wallet addresses, and locally generated report files.]

## Skill Version(s):

1.0.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
