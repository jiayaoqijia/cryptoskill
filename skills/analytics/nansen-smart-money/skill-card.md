## Description:

Tracks smart-money wallet netflows, trades, holdings, and perpetual futures activity through the Nansen CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to inspect smart-money wallet netflows, DEX and perpetual trades, and holdings for crypto market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Nansen CLI can access account-level API data using a selected API key or saved browser session.

Mitigation: Check the selected credential and its account permissions before running research commands.

Risk: Research calls, including repeated calls in loops, may consume credits or trigger authorized x402 payments.

Mitigation: Review wallet authorization, payment policy, and spending limits before running commands or loops.

## Reference(s):

- [Nansen Smart Money Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-smart-money-tracker)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI results can be viewed as a table or exported as CSV.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
