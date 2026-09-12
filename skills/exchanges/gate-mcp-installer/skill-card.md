## Description:

Gate MCP one-click installer for OpenClaw and mcporter that helps install or configure Gate MCP servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install all or selected Gate MCP servers for OpenClaw, then verify the mcporter setup and follow required authentication steps. The skill is limited to installation and post-install guidance, not exchange business actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-service credentials may be collected during setup and stored in local mcporter configuration.

Mitigation: Use least-privilege Gate API keys, avoid withdrawal permission, consider IP allowlisting, and keep credentials out of assistant output and logs.

Risk: The installer may execute unpinned npm packages.

Mitigation: Pin and verify npm package versions before running the installer in a production or sensitive environment.

Risk: The skill references mutable remote runtime rules.

Mitigation: Review the exact remote rules version before installation and treat those rules as trusted only after approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-mcp-openclaw-installer)
- [MCP execution specification](artifact/references/mcp.md)
- [Gate MCP GitHub](https://github.com/gate/gate-mcp)
- [mcporter GitHub](https://github.com/mcporter-dev/mcporter)
- [Gate API documentation](https://www.gate.com/docs/developers/apiv4/en/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status summaries with mcporter shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation verification, server lists, authentication next steps, and recovery guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter and changelog report 2026.3.25-2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
