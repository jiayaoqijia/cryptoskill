## Description:

Provides guidance for offering AI agent services through SOL micro-payments using the x402 HTTP 402 payment protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dahhan43-netizen](https://clawhub.ai/user/dahhan43-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto service operators use this skill to configure a marketplace-style API where specialized AI agent endpoints are accessed after SOL payment verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOL payments are directed to a fixed wallet with limited verification details.

Mitigation: Verify the recipient wallet, expected price, endpoint, and operator identity independently before sending funds.

Risk: Cryptocurrency payments are generally irreversible and wallet or transaction identifiers may reveal activity.

Mitigation: Use only funds and wallet identities appropriate for the transaction risk, and avoid exposing sensitive wallet history.

Risk: The submitted package lacks the server and dependency files that its instructions tell users to run.

Mitigation: Do not rely on marketplace behavior until the missing implementation files are supplied and reviewed in a sandboxed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dahhan43-netizen/skills/x402-agent-marketplace)
- [Publisher profile](https://clawhub.ai/user/dahhan43-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, endpoint tables, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment-flow guidance and local server usage notes; no executable server or dependency files were included in the submitted artifact.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
