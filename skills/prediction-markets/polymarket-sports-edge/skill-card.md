## Description:

Find odds divergence between sportsbook consensus and Polymarket sports markets, then trade the gap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjims](https://clawhub.ai/user/0xjims)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan sports prediction markets for sportsbook-to-Polymarket price divergence, configure trading thresholds and position size, and run dry-run or live trading cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real-money trading when live mode is enabled, including from scheduled hourly automation.

Mitigation: Run dry-run cycles first, keep LIVE unset or false in scheduled environments, and set small trade and quota limits before any live run.

Risk: API keys and request details may be exposed if full request URLs or logs are retained.

Mitigation: Limit log exposure, avoid logging full URLs with credentials, and rotate keys if credential-bearing requests may have been captured.

Risk: Duplicate stale package copies and mismatched documented defaults can cause users to run behavior different from what they reviewed.

Mitigation: Use the release-root artifact as the reviewed package, remove stale duplicates before unattended use, and align setup documentation with code defaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xjims/skills/polymarket-sports-edge)
- [0xjims publisher profile](https://clawhub.ai/user/0xjims)
- [The Odds API](https://the-odds-api.com)
- [Simmer markets API](https://api.simmer.markets/api/sdk/markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires LIVE=true and configured API keys.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence and root SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
