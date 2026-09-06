## Description: <br>
Operate MEXC Spot REST APIs through UXC with a curated OpenAPI schema, HMAC query signing, and separate public/signed workflow guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect MEXC Spot market data and run signed account or order workflows through UXC. It is intended for public market reads, signed account reads, and explicitly confirmed Spot order create, cancel, and lookup operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signed commands can affect a real MEXC Spot exchange account. <br>
Mitigation: Use a dedicated least-privilege API key, disable withdrawals, enable trading only when required, and manually confirm every order or cancellation. <br>
Risk: API credentials are required for signed account and order operations. <br>
Mitigation: Keep secrets in environment variables and bind credentials through the documented UXC signer configuration. <br>
Risk: Incorrect schema or parameter use can produce unintended account or order behavior. <br>
Mitigation: Review the curated schema source, inspect operation help before execution, query exchange information before orders, and keep automation on the JSON output envelope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/mexc-openapi-skill) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/mexc-spot.openapi.json) <br>
- [Published OpenAPI schema URL](https://raw.githubusercontent.com/holon-run/uxc/main/skills/mexc-openapi-skill/references/mexc-spot.openapi.json) <br>
- [Official MEXC Spot v3 docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented API output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Signed operations require MEXC API credentials, HMAC query signing, and explicit confirmation for order creation or cancellation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
