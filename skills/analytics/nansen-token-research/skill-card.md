## Description: <br>
Token deep dive for Nansen research commands covering token info, OHLCV, holders, flows, DEX trades, PnL, and perp market views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and OpenClaw users use this skill to research a specific token through Nansen CLI token endpoints, including price history, holders, wallet flows, DEX trades, PnL, and perp leaderboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill allows the agent to run any nansen command, not only token research commands. <br>
Mitigation: Install only in environments where broad Nansen CLI access is acceptable, and prefer a version scoped to nansen research token commands for routine research. <br>
Risk: The skill requires a NANSEN_API_KEY and may expose broader Nansen account access than needed. <br>
Mitigation: Use a limited Nansen API key and avoid sharing wallet secrets or funded wallet context unless trading or payment actions are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-token-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Nansen CLI commands, command options, and natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include token research command suggestions, endpoint usage notes, table or CSV export guidance, and warnings for unsupported filters or all-zero flow results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
