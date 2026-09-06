## Description: <br>
Operate KuCoin public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and read KuCoin public market data, including symbols, tickers, order book snapshots, and candles, through UXC-backed OpenAPI commands. It is intended for public, read-only market-data workflows and excludes private account, order, websocket, margin, and broader platform operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may use UXC to make live public KuCoin market-data reads. <br>
Mitigation: Install only when public market-data reads are acceptable, and keep workflows limited to the documented read-only endpoints. <br>
Risk: The skill links to an external raw OpenAPI schema URL for command setup. <br>
Mitigation: For stricter supply-chain control, use the bundled schema or pin the raw schema URL to a trusted commit before linking. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated KuCoin public OpenAPI schema](references/kucoin-public.openapi.json) <br>
- [KuCoin API server](https://api.kucoin.com) <br>
- [Raw curated OpenAPI schema](https://raw.githubusercontent.com/holon-run/uxc/main/skills/kucoin-openapi-skill/references/kucoin-public.openapi.json) <br>
- [Official KuCoin authentication docs](https://www.kucoin.com/docs-new/authentication) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/kucoin-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented API usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on public read-only KuCoin market-data operations and stable JSON response fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
