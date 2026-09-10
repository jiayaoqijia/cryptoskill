## Description:

Build and configure the MCP server for Lightning Node Connect (LNC) that connects AI assistants to lnd nodes via encrypted WebSocket tunnels using pairing phrases, without direct network access or TLS certs, and provides 18 read-only tools for querying node state, channels, payments, invoices, peers, and on-chain data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and node operators use this skill to build, configure, and register a read-only MCP server that lets an assistant inspect Lightning Network node state through Lightning Node Connect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can register persistent assistant tooling through project or global MCP configuration.

Mitigation: Prefer project scope, review any .mcp.json or ~/.claude.json changes, and remove entries that are no longer needed.

Risk: The release guidance allows unpinned remote packages or Docker execution with broad networking.

Mitigation: Use a locally audited build, pin npm packages to an exact version, and pin Docker images by digest while avoiding host networking unless required.

Risk: The MCP server handles sensitive Lightning Node Connect pairing phrases and passwords.

Mitigation: Treat pairing phrases and passwords as secrets, keep LNC_INSECURE=false outside isolated development, and avoid logging or sharing connection credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roasbeef/skills/lightning-mcp-server)
- [Go downloads](https://go.dev/dl/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local MCP configuration and environment files when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
