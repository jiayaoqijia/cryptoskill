## Description:

What is the state of the Hyperliquid perp market? Top contracts by volume/OI, trader leaderboard, and SM perp activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto market analysts and developers can use the skill to review current Hyperliquid perpetual market activity, including contracts by volume and open interest, trader rankings, and smart-money trades. They can filter results by trader type, labels, sector, sorting, and time range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported HTTP 402 challenge can spend funds from the configured wallet, and repeated calls in a loop can incur repeated payments.

Mitigation: Review wallet authorization, payment policy, and spending limits before running research calls; keep call counts bounded.

Risk: Research calls require an explicitly selected API key or saved browser session, and credentials or session renewal can fail.

Mitigation: Check `nansen auth status` before research, follow the CLI's authentication error guidance, and stop on invalid or uncertain authentication state.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-perp-screener)

## Skill Output:

**Output Type(s):** [Analysis, Text, Tabular data, Shell commands]

**Output Format:** [Text and tabular market metrics returned through Nansen CLI research commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market snapshot with configurable filters, sorting, time range, and result limits. Data availability depends on Nansen coverage and account entitlements.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
