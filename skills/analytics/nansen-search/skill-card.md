## Description:

Search for tokens or entities by name to find token addresses or identify entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to find tokens by name and retrieve addresses, or to search for named entities through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated searches may consume account credits or trigger authorized wallet payments, especially when repeated in loops.

Mitigation: Confirm authentication before research, keep Nansen spending limits configured, and avoid repeated or anonymous paid searches without explicit intent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nansen-devops/skills/nansen-general-search)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with Bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports token or entity searches with optional chain, result-limit, and field filters.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
