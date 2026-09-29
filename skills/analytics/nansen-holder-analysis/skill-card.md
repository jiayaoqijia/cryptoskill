## Description:

Analyzes token holder quality using Nansen holder, wallet-label flow, and recent buyer and seller data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Token researchers and developers use the Nansen CLI to assess holder concentration, wallet-label flows, and recent buyer and seller activity for a token contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated research calls can consume Nansen credits or trigger authorized wallet payments.

Mitigation: Check credits, wallet authorization, payment policy, and spending limits before running research calls or loops.

Risk: Research may fail without a valid selected API key or saved browser session.

Mitigation: Check authentication status first and stop on authentication failure rather than switching to anonymous paid access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-holder-analysis)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token holder and flow findings depend on Nansen CLI responses.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
