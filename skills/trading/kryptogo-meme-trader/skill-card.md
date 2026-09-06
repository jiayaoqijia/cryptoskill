## Description: <br>
[DEPRECATED 2026-05-04] Analyze and trade meme coins using KryptoGO's on-chain cluster analysis platform; the kg-xyz analysis backend shutdown affects cluster analysis, wallet labels, signal dashboards, and DCA/limit tools, while Solana swap execution via the OKX DEX aggregator continues to function. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a00012025](https://clawhub.ai/user/a00012025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze meme-coin opportunities, monitor portfolio positions, and execute Solana swaps with local signing. Its analysis workflow is degraded after the 2026-05-04 backend shutdown, so remaining use should focus on carefully supervised swap execution and any independently verified market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the default monitoring path can execute live sells even though the documentation describes supervised notifications. <br>
Mitigation: Do not enable default cron or monitor.py automation until the auto-sell behavior is reviewed and fixed or explicitly accepted; require manual confirmation for buys and sells. <br>
Risk: The skill requires sensitive trading credentials and can sign Solana transactions. <br>
Mitigation: Use a dedicated low-value wallet, never reuse a main wallet, load secrets only from the protected environment file, and restrict access to ~/.openclaw/workspace/.env and memory/trading-*.json. <br>
Risk: The kg-xyz analysis backend shutdown means cluster analysis, wallet labels, signal dashboards, and DCA/limit tools may no longer provide reliable safeguards after 2026-05-04. <br>
Mitigation: Treat analysis-dependent recommendations as degraded, verify signals independently, and limit usage to supervised workflows unless the backend behavior is confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a00012025/kryptogo-meme-trader) <br>
- [Publisher profile](https://clawhub.ai/user/a00012025) <br>
- [KryptoGO homepage](https://www.kryptogo.xyz) <br>
- [KryptoGO user guide](https://kryptogo.notion.site/Product-Guide-EN-26c3499de8a28179aafacb68304458ea) <br>
- [KryptoGO whitepaper](https://wallet-static.kryptogo.com/public/whitepaper/kryptogo-xyz-whitepaper-v1.0.pdf) <br>
- [API Reference](references/api-reference.md) <br>
- [Autonomous Trading Reference](references/autonomous-trading.md) <br>
- [Core Concepts](references/concepts.md) <br>
- [Decision Framework](references/decision-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python scripts, JSON configuration, and trade-analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a KryptoGO API key, a Solana wallet private key and address, Python tooling, network access to wallet-data.kryptogo.app for degraded analysis paths, and local filesystem writes for environment and trading memory files.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
