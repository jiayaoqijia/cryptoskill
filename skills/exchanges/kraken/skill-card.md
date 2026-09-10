## Description:

Query Kraken crypto account balances, portfolio value, trades, ledger entries, staking positions, deposit addresses, and public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect Kraken account and market information from a CLI wrapper, including portfolio summaries, holdings, staking rewards, trade history, ledger entries, and deposit-address lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Kraken account, order, ledger, earn, and deposit-address data to the agent session.

Mitigation: Install only when that access is intended, avoid pasting secrets into chat, and review generated outputs before sharing them.

Risk: Over-scoped Kraken API credentials could expand the impact of misuse or credential exposure.

Mitigation: Use a minimally scoped Kraken API key with no trading or withdrawal permissions and protect any .env file that stores credentials.

Risk: Dependency ranges are not pinned or locked for production use.

Mitigation: Pin or lock dependency versions before production deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive Kraken account, order, ledger, earn, and deposit-address data.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
