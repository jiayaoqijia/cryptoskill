## Description:

Monitor Bitfinex lending (funding) performance via API for funding income summaries and lending status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch Bitfinex funding wallet balances, active funding credits, and recent funding ledger entries, then summarize lending income without opening the Bitfinex app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bitfinex API credentials are required to fetch account funding data.

Mitigation: Use a dedicated read-only API key limited to wallet, funding, and ledger/history reads; do not grant trading, transfer, or withdrawal permissions.

Risk: Running the script fetches funding account data from Bitfinex.

Mitigation: Run it only when an account holder intentionally wants a lending status or income summary.

## Reference(s):

- [Bitfinex API Notes (Funding Monitor)](references/api-notes.md)
- [Bitfinex API Base URL](https://api.bitfinex.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json]

**Output Format:** [Markdown guidance with shell commands and optional JSON summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Bitfinex API credentials through environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
