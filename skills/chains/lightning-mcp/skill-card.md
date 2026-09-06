## Description: <br>
Builds and configures the MCP server for Lightning Node Connect so AI assistants can query lnd node state through encrypted WebSocket tunnels using pairing phrases, without direct network access or TLS certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, and register a read-only Lightning Node Connect MCP server for Claude Code. It helps an agent connect to an lnd node with a Lightning Terminal pairing phrase and query node, channel, payment, invoice, peer, graph, and on-chain data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The LNC pairing phrase and password grant access to read Lightning node state. <br>
Mitigation: Treat the pairing phrase and password as secrets, provide them only when connecting, and avoid storing or sharing them in project files or chat history. <br>
Risk: Development settings can disable TLS verification through LNC_INSECURE. <br>
Mitigation: Use insecure mode only in controlled local or regtest environments, and keep TLS verification enabled for production use. <br>
Risk: MCP setup can modify project or user configuration files. <br>
Mitigation: Review generated .mcp.json or ~/.claude.json changes before restarting Claude Code or sharing project configuration. <br>
Risk: Docker host networking broadens local network exposure. <br>
Mitigation: Prefer npx or a locally built binary unless Docker host networking is specifically required. <br>
Risk: Installing a prebuilt package or binary introduces package trust risk. <br>
Mitigation: Prefer verified packages or source-built binaries from the intended release before enabling the MCP server. <br>


## Reference(s): <br>
- [Lightning MCP Server on ClawHub](https://clawhub.ai/Roasbeef/lightning-mcp-server) <br>
- [Go Downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup through npx, a locally built binary, or Docker; accompanying scripts can write environment and MCP configuration files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
