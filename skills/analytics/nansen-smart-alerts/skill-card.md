## Description:

Helps agents list, create, update, toggle, and delete Nansen Smart Alerts for token flows, transfers, and contract interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Nansen account holders and their agents use this skill to manage alert rules for smart-money flows, token transfers, and contract calls, with notifications sent to configured channels.

### Deployment Geography for Use:

Global, subject to Nansen account eligibility and geographic checks.

## Known Risks and Mitigations:

Risk: Creating, updating, toggling, or deleting alerts may change account notifications unexpectedly.

Mitigation: Review alert-management commands and their target alert IDs before execution.

Risk: Webhook destinations and secrets may expose alert data or credentials if misconfigured.

Mitigation: Check destination URLs and handle webhook secrets carefully; prefer a scoped Nansen API key where possible.

## Reference(s):

- [Nansen Smart Alerts skill on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-smart-alerts)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Text with Nansen CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alert configuration and management depend on the user's Nansen account permissions.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
