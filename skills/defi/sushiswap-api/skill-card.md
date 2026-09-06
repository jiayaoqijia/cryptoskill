## Description: <br>
REST API reference for optimized token swapping, executable swap transaction generation, swap quoting, token pricing, token metadata, and liquidity-source discovery using the SushiSwap Aggregator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmasayoshi](https://clawhub.ai/user/0xmasayoshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to construct schema-conformant SushiSwap REST requests for quotes, executable swap transactions, token prices, token metadata, and supported liquidity sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated swap transaction data can lead to financial loss if signed without review. <br>
Mitigation: Before signing, verify the chain, token addresses, amount, recipient, slippage, fee settings, referrer, target contract, and transaction value. <br>
Risk: Using the SwaggerHub mock server instead of the production Sushi API server can return non-production behavior. <br>
Mitigation: Prefer https://api.sushi.com for real integration work and use the mock server only when intentionally testing request shape. <br>
Risk: Fabricated or stale transaction calldata could misrepresent the requested swap. <br>
Mitigation: Use the bundled OpenAPI schema as the source of truth and do not fabricate transaction calldata. <br>


## Reference(s): <br>
- [OpenAPI usage guide](references/OPENAPI.md) <br>
- [Sushi API OpenAPI schema](references/openapi.yaml) <br>
- [Sushi API production server](https://api.sushi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with OpenAPI-derived HTTP request details and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires schema-conformant request parameters, including an explicit referrer for quote and swap endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
