## Description: <br>
Query Kraken crypto account balances, portfolio, trades, market data, funding details, and staking positions from an agent workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesethrose](https://clawhub.ai/user/thesethrose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to inspect Kraken account holdings, net worth, performance, transaction history, open orders, staking allocations, and selected market data. It is suited for read-oriented portfolio analysis where the user intentionally exposes Kraken account data to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal confidential Kraken balances, ledger history, open orders, staking positions, and deposit addresses. <br>
Mitigation: Use it only when the agent session is allowed to display that account data, and run raw account-history or deposit-address commands only intentionally. <br>
Risk: Kraken API credentials could grant more access than the skill needs if broad permissions are configured. <br>
Mitigation: Create a Kraken API key limited to query, balance, ledger, and earn permissions, and avoid trading or withdrawal permissions. <br>
Risk: API secrets stored in environment variables or a .env file can be exposed if copied into chat or source control. <br>
Mitigation: Keep KRAKEN_API_KEY and KRAKEN_API_SECRET out of chat and repositories, and protect any local .env file. <br>


## Reference(s): <br>
- [ClawHub Kraken Skill Page](https://clawhub.ai/thesethrose/skills/kraken) <br>
- [Artifact Skill Guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text summaries and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display sensitive Kraken account, ledger, order, staking, and deposit-address data when private commands are run.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
