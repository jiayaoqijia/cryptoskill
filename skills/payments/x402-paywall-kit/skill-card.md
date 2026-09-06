## Description: <br>
Detects x402 payment-required responses, checks a spending policy, signs USDC payments on Base, and retries requests through a fetch wrapper for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tara-quinn-ai](https://clawhub.ai/user/tara-quinn-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let agents handle x402 paywalls with policy controls, spend limits, domain filtering, and payment logging. Web developers can also use the included Express middleware to add USDC paywalls to API routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real crypto payments from an agent-controlled wallet. <br>
Mitigation: Use a dedicated low-balance or testnet wallet, strict per-request and daily limits, a domain allowlist, and human approval where possible. <br>
Risk: Wallet private keys and payment logs are sensitive financial data. <br>
Mitigation: Load private keys only from protected environment variables, avoid hardcoding secrets, and restrict access to JSONL payment logs. <br>
Risk: Bundled storefront and Stripe integration files are separate commerce code paths. <br>
Mitigation: Review and deploy those files separately from the agent auto-payment skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tara-quinn-ai/x402-paywall-kit) <br>
- [Publisher profile](https://clawhub.ai/user/tara-quinn-ai) <br>
- [Homepage](https://taraquinn.ai) <br>
- [README](README.md) <br>
- [Agent setup example](references/agent-setup.example.ts) <br>
- [Policy example](references/policy.example.json) <br>
- [Product requirements](docs/PRD.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on Node packages, x402 payment configuration, wallet environment variables, spending policy, and optional JSONL payment logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
