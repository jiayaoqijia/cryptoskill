## Description: <br>
Operate Bybit V5 public market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and call Bybit V5 public market-data endpoints through UXC, including server time, instruments, tickers, order book snapshots, and kline reads. It is intended for public read-only market data workflows, not private account access or trading. <br>

### Deployment Geography for Use: <br>
Global, subject to Bybit API region and IP restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The curated OpenAPI schema controls which Bybit endpoints and parameters an agent can call. <br>
Mitigation: Review or pin the OpenAPI schema before important workflows, as recommended by the security guidance. <br>
Risk: Bybit API access may be limited by region or IP restrictions. <br>
Mitigation: Verify that the execution environment is permitted for Bybit API access before treating request failures as schema or parameter issues. <br>
Risk: Adding private Bybit credentials would expand the skill beyond its documented public read-only scope. <br>
Mitigation: Do not add private credentials unless a future version clearly documents signed private endpoint support. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated Bybit V5 OpenAPI schema](references/bybit-v5.openapi.json) <br>
- [Official Bybit V5 docs](https://bybit-exchange.github.io/docs/v5/guide) <br>
- [ClawHub release page](https://clawhub.ai/jolestar/bybit-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from UXC] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public read-only Bybit market-data operations; no credential use or private trading authority in this version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
