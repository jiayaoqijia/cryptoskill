## Description: <br>
Operate Coinbase Advanced Trade REST APIs through UXC with a curated OpenAPI schema, products-first discovery, and explicit JWT bearer auth guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to discover Coinbase Advanced Trade products, inspect accounts and orders, and run selected Coinbase REST operations through UXC with JWT bearer authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable live Coinbase trading actions using persistent API credentials. <br>
Mitigation: Use a dedicated least-privilege Coinbase API key, keep it read-only unless trading is required, protect and rotate the private key, and require manual approval for every live order or cancellation. <br>
Risk: The curated OpenAPI schema controls which Coinbase operations the agent can call. <br>
Mitigation: Prefer a reviewed or pinned schema and inspect operation help before running private account, order, or cancellation workflows. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/coinbase-advanced-trade.openapi.json) <br>
- [Coinbase Advanced Trade overview](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/overview) <br>
- [Coinbase OpenAPI Skill on ClawHub](https://clawhub.ai/jolestar/coinbase-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses UXC command output envelopes; keep automation on stable JSON fields such as ok, kind, protocol, data, and error.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
