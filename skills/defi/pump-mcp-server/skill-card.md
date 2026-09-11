## Description:

Model Context Protocol server exposing 7 tools, 3 resource types, and 3 prompts for AI agent consumption: Solana wallet operations, vanity address generation, message signing, and address validation over stdio transport.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speraxos](https://clawhub.ai/user/speraxos)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to expose Solana wallet operations through an MCP server, including keypair generation, vanity address generation, address validation, message signing, signature verification, and keypair restoration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restoring a keypair requires handling sensitive secret key bytes in a local agent workflow.

Mitigation: Use restore_keypair only in a trusted local setup, avoid valuable private keys in transcripts or tool calls, and prefer generating a fresh keypair for routine use.

Risk: The active session keypair is ephemeral and is lost when the MCP server restarts.

Mitigation: Treat generated session keypairs as temporary unless the workflow explicitly exports or stores required wallet material outside the MCP session.

Risk: Vanity address generation is single-threaded and long prefixes or suffixes may be slow.

Mitigation: Estimate vanity generation time before running expensive searches and keep requested patterns short when latency matters.

## Reference(s):

- [Pump MCP Server on ClawHub](https://clawhub.ai/speraxos/skills/pump-mcp-server)
- [Pump Fun SDK GitHub Repository](https://github.com/nirholas/pump-fun-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text for MCP server setup, tool usage, and wallet operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing guidance for stdio MCP interactions; tool responses are described as structured JSON by the artifact.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
