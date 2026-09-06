## Description: <br>
Is this token held by quality wallets or retail noise? SM holder ratio, flow breakdown by label, and recent buyer quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Nansen CLI token-holder analysis for Ethereum token contracts, including smart-money holder ratios, label-based flow breakdowns, and recent buyer quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Nansen CLI queries with the user's Nansen API key, which may consume quota or affect billing on usage-limited plans. <br>
Mitigation: Install only after trusting the nansen-cli package, provide a scoped NANSEN_API_KEY where possible, and monitor Nansen API usage or billing. <br>
Risk: Holder analysis can be inaccurate for unsupported native or wrapped token inputs. <br>
Mitigation: Use a specific Ethereum token contract address, matching the skill's documented input requirement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-holder-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; expects a specific Ethereum token contract address.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
