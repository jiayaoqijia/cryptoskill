## Description:

Discover trending tokens through screening, smart-money holdings, Nansen indicators, and flow intelligence for deeper research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Token researchers use Nansen CLI queries to shortlist trending tokens, review smart-money holdings and indicator signals, and check flows for promising candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated research grants the CLI account-level API access.

Mitigation: Use only an explicitly selected key or approved browser session; check authentication before research and stop if it fails.

Risk: Repeated, paginated, or flow-intelligence queries may consume credits or trigger wallet payments.

Mitigation: Review payment limits before use, restrict batch sizes, and reserve flow-intelligence calls for shortlisted tokens.

## Reference(s):

- [Nansen Token Screener on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-screener)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis]

**Output Format:** [Markdown with bash commands and token-research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on selected chain, timeframe, available entitlements, and queried tokens.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
