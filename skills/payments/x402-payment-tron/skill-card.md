## Description: <br>
Pay for x402-enabled Agent endpoints using USDT on TRON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hades-ye](https://clawhub.ai/user/hades-ye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to call x402-enabled HTTP endpoints that require TRON USDT payment, including endpoint discovery and paid request retries after payment negotiation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make TRON USDT payments when invoking paid x402 endpoints. <br>
Mitigation: Use a dedicated low-balance wallet, prefer testnet first, and verify each endpoint and network before use. <br>
Risk: The skill can create persistent high-limit USDT approvals for paid endpoint calls. <br>
Mitigation: Review allowances before use and revoke USDT approvals after use. <br>
Risk: Untrusted prompts could steer an agent toward paid URLs or unwanted networks. <br>
Mitigation: Do not let untrusted prompts choose paid URLs, endpoints, or networks without explicit user review. <br>
Risk: Wallet signing secrets are required and could be exposed through unsafe handling. <br>
Mitigation: Load the key internally from configured sources, avoid literal export commands, and never print or echo the private key. <br>
Risk: Binary or image endpoint responses may remain in temporary files. <br>
Mitigation: Delete temporary files after the agent has used or processed them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hades-ye/skills/x402-payment-tron) <br>
- [Publisher profile](https://clawhub.ai/user/hades-ye) <br>
- [x402 protocol homepage](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON result object with HTTP status, response headers, response body, or temporary file metadata for binary responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write image or binary endpoint responses to temporary files; the calling agent is responsible for deleting those files.] <br>

## Skill Version(s): <br>
0.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
