## Description:

Pay for x402-enabled Agent endpoints using USDT on TRON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hades-ye](https://clawhub.ai/user/hades-ye)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to invoke x402-enabled agent endpoints and handle USDT payment negotiation on TRON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet credentials and funds may be exposed if the skill uses broad shared configuration or a high-balance wallet.

Mitigation: Use a dedicated low-balance TRON wallet and remove broad shared-config key discovery before sensitive use.

Risk: Untrusted endpoints can trigger automatic payment signing or token approval behavior.

Mitigation: Invoke only trusted endpoints, review payment requirements before mainnet use, and prefer exact or capped approvals.

## Reference(s):

- [x402](https://x402.org)
- [ClawHub skill page](https://clawhub.ai/hades-ye/skills/x402-payment-tron)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files]

**Output Format:** [JSON response with optional temporary file paths for binary responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRON payment credentials; binary responses may be written to temporary files for the agent to manage.]

## Skill Version(s):

0.0.4 (source: server release metadata; artifact frontmatter/package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
