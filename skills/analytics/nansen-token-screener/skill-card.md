## Description: <br>
Discover trending tokens - screener, smart money holdings, Nansen indicators, and flow intelligence for promising finds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto analysts use this skill to shortlist trending tokens, inspect Nansen Score candidates, review smart money holdings, and confirm promising tokens with indicators and flow intelligence before deeper research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The allowed nansen CLI access is broader than the read-only token-screener workflow. <br>
Mitigation: Review generated commands before execution and avoid login, wallet, trade, export, send, or payment operations unless explicitly intended. <br>
Risk: The skill requires a sensitive NANSEN_API_KEY credential. <br>
Mitigation: Use a least-privileged Nansen API key and keep funded wallets or trading credentials out of the same agent environment. <br>
Risk: Flow intelligence can consume significant Nansen credits. <br>
Mitigation: Run flow-intelligence only on finalist tokens after top-tokens, stablecoin filtering, and indicator review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nansen-devops/nansen-token-screener) <br>
- [Nansen CLI package](https://www.npmjs.com/package/nansen-cli) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
