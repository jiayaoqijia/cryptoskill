## Description: <br>
Operate CoinGecko and GeckoTerminal market data APIs through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure UXC authentication and run read-only CoinGecko and GeckoTerminal market-data lookups through a curated OpenAPI surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials may be delegated too broadly if the UXC auth binding is not scoped to the intended CoinGecko host and path. <br>
Mitigation: Use a CoinGecko API key appropriate for delegation, bind it only to the intended CoinGecko host and /api/v3 path, and validate the active binding before use. <br>
Risk: Large or repeated market-data reads can exceed public, Demo, or Pro API limits. <br>
Mitigation: Prefer narrow validation calls and avoid large paginated loops unless the user explicitly requests them. <br>
Risk: The curated OpenAPI schema is loaded from a remote URL, which can reduce reproducibility if the referenced content changes. <br>
Mitigation: Review or pin the OpenAPI schema URL when stronger reproducibility is required. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/coingecko-market.openapi.json) <br>
- [CoinGecko API docs](https://docs.coingecko.com/reference/endpoint-overview) <br>
- [CoinGecko authentication docs](https://docs.coingecko.com/reference/authentication) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API operation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on read-only API calls, API-key binding, and JSON response handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and curated OpenAPI schema) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
