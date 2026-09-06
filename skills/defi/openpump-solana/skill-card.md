## Description: <br>
Solana token launch and trading tools via the OpenPump MCP server for creating pump.fun tokens, trading tokens, managing custodial wallets, transferring SOL and SPL tokens, running market-making and sniping workflows, and monitoring portfolio positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstacktard](https://clawhub.ai/user/fullstacktard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to connect an agent to OpenPump MCP tools for Solana pump.fun token launch, trading, wallet, transfer, market-making, sniping, stop-loss, portfolio, and creator-fee workflows. <br>

### Deployment Geography for Use: <br>
Global, excluding US persons <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real SOL and SPL tokens, launch tokens, and execute trades or transfers that may be irreversible. <br>
Mitigation: Use a dedicated low-balance account, check balances and quotes first, use dry-run previews where supported, and require explicit confirmation for every trade, transfer, launch, bundle, snipe, and market-making action. <br>
Risk: Automated market-making, sniping, stop-loss, and heartbeat workflows can create standing trading behavior with loss exposure. <br>
Mitigation: Avoid standing automation unless the operator explicitly accepts the risk; enforce position limits, drawdown limits, circuit breakers, and user approval for buy and sell actions. <br>
Risk: The OpenPump API key grants access to live wallet and trading operations. <br>
Mitigation: Keep OPENPUMP_API_KEY out of prompts, logs, and shared files; store it in the environment or a local secret store and rotate it if exposed. <br>
Risk: The stdio setup installs and runs the npm MCP package with npx. <br>
Mitigation: Pin or independently verify the @openpump/mcp package before use instead of relying on an unpinned latest install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fullstacktard/openpump-solana-mcp) <br>
- [OpenPump](https://openpump.io) <br>
- [OpenPump documentation](https://docs.openpump.io) <br>
- [@openpump/mcp npm package](https://www.npmjs.com/package/@openpump/mcp) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API/tool calls, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON configuration snippets, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js/npx and OPENPUMP_API_KEY; may direct an agent to invoke OpenPump MCP tools that affect live Solana wallets and trades.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json; artifact SKILL.md frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
