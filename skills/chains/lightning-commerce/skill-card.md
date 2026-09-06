## Description: <br>
End-to-end agentic commerce workflow using Lightning Network for setting up an lnd, lnget, and aperture payment stack, buying or selling data via L402, and enabling agent-to-agent micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a Lightning Network commerce stack for paid data access, L402-protected resources, and agent-to-agent micropayments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents real Lightning payment and wallet-secret authority. <br>
Mitigation: Start on testnet or with negligible funds, require manual approval for funding, channel opening, and paid fetches, and protect seed, macaroon, and wallet files. <br>
Risk: Autonomous paid fetches can spend funds unexpectedly. <br>
Mitigation: Use --no-pay for inspection first, set per-request and total budgets, and review lnget token and payment history. <br>
Risk: Aperture endpoints may be exposed publicly with insecure settings. <br>
Mitigation: Review aperture configuration before deployment and do not expose aperture publicly with --insecure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Roasbeef/lightning-agent-commerce) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, payment, cost-control, hosting, and shutdown guidance for lnd, lnget, aperture, and L402 workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
