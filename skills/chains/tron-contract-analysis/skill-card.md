## Description: <br>
Analyze TRON smart contracts including deployment info, ABI methods, transaction patterns, top callers, energy costs, and safety assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to investigate TRON smart contracts, identify common token standards, summarize contract activity, and assess interaction risk before acting on a contract address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could be prompted outside the documented workflow to provide wallet private keys, seed phrases, transaction-signing permissions, or local file access. <br>
Mitigation: Use the skill only for public TronGrid contract lookups and do not provide wallet secrets, signing permissions, or local file access. <br>
Risk: A contract safety score can be mistaken for a guarantee that interacting with a contract is safe. <br>
Mitigation: Treat reports as decision support, review the ABI and transaction evidence, and perform independent due diligence before interacting with a contract. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>
- [Analyze USDT contract example](examples/analyze-usdt-contract.md) <br>
- [Check contract safety example](examples/check-contract-safety.md) <br>
- [ClawHub skill page](https://clawhub.ai/greason/trongrid-contract-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown contract analysis report with tables, risk factors, positive factors, and actionable recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only TronGrid lookups; no wallet secrets, signing permissions, or local file access are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
