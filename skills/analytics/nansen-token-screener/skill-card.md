## Description:

Helps agents discover trending tokens and examine smart-money holdings, Nansen indicators, and token flows for further research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agents use this skill to screen tokens, review smart-money holdings and indicator signals, and investigate flows before making their own investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated research calls can consume credits or trigger wallet-authorized x402 payments, including on every iteration of a loop.

Mitigation: Confirm the CLI package is trusted, set spending limits, and obtain approval before running costly or repeated queries.

Risk: Screener searches may omit lower-ranked tokens, and indicator coverage can be incomplete.

Mitigation: Check result-completeness metadata, widen or narrow the search when needed, and verify individual indicators before drawing conclusions.

## Reference(s):

- [Nansen Token Screener on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-screener)
- [Publisher profile](https://clawhub.ai/user/nansen-devops)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with CLI examples and token-research results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research results depend on account entitlements, token coverage, and query limits.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
