## Description:

Manage smart alerts — list, create, update, toggle, delete. Use when setting up or managing token flow alerts, smart money alerts, or notification rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Nansen account users use this skill to create and manage smart-alert rules for token flows, token transfers, and smart-contract calls, including configuring notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs and signing secrets can grant access to notification channels, and passing a webhook secret as a command-line argument can expose it in shell history, process lists, or transcripts.

Mitigation: Keep credentials out of shared output, retain the documented redaction, and provide webhook secrets through --webhook-secret-stdin or NANSEN_WEBHOOK_SECRET instead of --webhook-secret.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-smart-alerts)
- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the Nansen CLI and an authorized account session or API key.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
