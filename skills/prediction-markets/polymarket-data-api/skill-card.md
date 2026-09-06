## Description: <br>
Query Polymarket prediction market data from the public Polymarket API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BOMBFUOCK](https://clawhub.ai/user/BOMBFUOCK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to inspect active Polymarket prediction markets, search markets by keyword, retrieve market details by slug, and list grouped market events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags weakly scoped installation and execution of an external trading utility. <br>
Mitigation: Verify the executable source and installation commands independently before installing or running the skill. <br>
Risk: Prediction-market tooling can influence financial decisions or interact with trading workflows. <br>
Mitigation: Use the skill for data inspection only unless a human explicitly reviews any trade, wallet, account, or fund-moving action. <br>
Risk: The release under-declares network and financial-trading capabilities according to the security summary. <br>
Mitigation: Run it in an environment where outbound network access and access to wallets, credentials, and account files are explicitly controlled. <br>


## Reference(s): <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [ClawHub skill page](https://clawhub.ai/BOMBFUOCK/polymarket-data-api) <br>
- [BOMBFUOCK publisher profile](https://clawhub.ai/user/BOMBFUOCK) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text summaries or JSON returned from command-line queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include market questions, prices, volume, liquidity, status, event counts, and optional raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
