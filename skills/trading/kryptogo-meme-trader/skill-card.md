## Description:

KryptoGO Meme Trader is a deprecated agent skill for meme-coin analysis and Solana swap execution, with cluster analysis and related kg-xyz backend features marked as unavailable after 2026-05-04.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a00012025](https://clawhub.ai/user/a00012025)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and crypto traders use this skill to inspect meme-coin opportunities, monitor portfolio positions, and execute Solana swaps with local signing. The reader should treat the analysis workflow as degraded because the documented kg-xyz analysis backend was scheduled to shut down on 2026-05-04.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto trading can cause direct financial loss, and server security evidence says the default supervised monitoring path can still execute wallet sales without fresh confirmation.

Mitigation: Use a dedicated low-value wallet, review the trading scripts before installation, and do not enable cron until the monitor path is read-only by default or requires an explicit execution flag and fresh approval before signing.

Risk: Remote-built swap transactions can be risky if the signed instructions do not match the user's intent.

Mitigation: Decode and independently validate transaction instructions before signing any remote-built transaction.

Risk: The documented kg-xyz analysis backend was scheduled to shut down on 2026-05-04, so cluster analysis, wallet labels, signal dashboards, and related DCA or limit-order analysis may fail.

Mitigation: Treat analysis outputs as unavailable after the shutdown date and rely only on functions that still have current service support.

Risk: The skill depends on API keys and a Solana private key loaded from local environment state.

Mitigation: Keep secrets in the local .env file with restricted permissions, never paste them into chat or command arguments, and avoid sharing logs that may expose wallet or transaction details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a00012025/skills/kryptogo-meme-trader)
- [KryptoGO homepage](https://www.kryptogo.xyz)
- [KryptoGO product guide](https://kryptogo.notion.site/Product-Guide-EN-26c3499de8a28179aafacb68304458ea)
- [KryptoGO whitepaper](https://wallet-static.kryptogo.com/public/whitepaper/kryptogo-xyz-whitepaper-v1.0.pdf)
- [API Reference](references/api-reference.md)
- [Autonomous Trading Reference](references/autonomous-trading.md)
- [Core Concepts](references/concepts.md)
- [Decision Framework](references/decision-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and generated local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KryptoGO and Solana wallet environment variables; setup and trading paths can write local .env and memory files.]

## Skill Version(s):

2.6.0 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
