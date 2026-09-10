## Description:

Tracks Polymarket wallet activity and provides scripts intended to calculate mirrored trade sizes, log activity, and manage a local copy-trading process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor a selected Polymarket wallet, calculate proposed mirrored trade sizes under configured limits, and operate local start, status, stop, and log commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a wallet private key while server security evidence says automatic trading and redeeming are not implemented as written.

Mitigation: Do not provide a real funded wallet private key; use dry-run behavior only unless the implementation is reviewed and replaced with a complete, trusted trading flow.

Risk: Running the scripts can make repeated network calls to Polymarket data APIs and Polygon RPC while writing local logs and state.

Mitigation: Run in a controlled environment, review generated logs for sensitive data, and use a separate low-risk wallet/address for experimentation.

Risk: Mirroring another trader's activity can produce financial loss even when trade sizing limits are configured.

Mitigation: Keep conservative min/max limits, start with dry-run output, and independently review proposed trades before taking market action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cassh100k/skills/polymarket-whale-copier)
- [Polymarket Leaderboard](https://polymarket.com/leaderboard)
- [Polymarket trades data API](https://data-api.polymarket.com/trades?user={wallet}&limit={limit})
- [Polymarket positions data API](https://data-api.polymarket.com/positions?user={wallet})
- [Polygon RPC endpoint](https://polygon-rpc.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local trade logs and state files when scripts are run; the bundled default configuration sets dry_run to true.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
