## Description: <br>
Use OKX OnchainOS MCP through UXC for token discovery, market data, wallet balance, and swap execution planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect OKX MCP operation schemas, configure OKX API-key authentication, retrieve token and market data, check wallet balances, and plan DEX quote or swap workflows with explicit confirmation for high-impact operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a shared demo OKX API key example that may be unsuitable for stable or production workflows. <br>
Mitigation: Use a personal least-privilege OKX API key stored through an environment variable or secret manager. <br>
Risk: Wallet, quote, approval, and swap operations may send sensitive context to OKX or produce transaction payloads with financial impact. <br>
Mitigation: Run these commands only with explicit user approval, and manually verify chain IDs, token contracts, amounts, recipients, and transaction payloads before approving. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [OKX OnchainOS MCP endpoint](https://web3.okx.com/api/v1/onchainos-mcp) <br>
- [ClawHub release page](https://clawhub.ai/jolestar/okx-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON output envelopes for OKX MCP responses where available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
