## Description:

Is this token held by quality wallets or retail noise? SM holder ratio, flow breakdown by label, and recent buyer quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, traders, and on-chain researchers use this skill to assess token holder quality by reviewing smart-money holders, flows by wallet label, and recent buyer and seller activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each supported x402 research call can spend funds from the configured wallet, and loops can multiply charges.

Mitigation: Run only the needed calls and review wallet authorization, payment policy, and spending limits before researching.

Risk: Cached session metadata does not prove credentials are valid; continuing after authentication failure or switching to anonymous access can create unsafe or unintended access and payment behavior.

Mitigation: Use an explicitly selected API key or saved browser session, check authentication status, and stop if authentication or renewal fails.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands]

**Output Format:** [Text analysis with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Holder values and ownership percentages, flows by wallet label, and recent buyer and seller volumes.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
