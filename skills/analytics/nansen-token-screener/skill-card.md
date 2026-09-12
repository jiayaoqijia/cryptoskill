## Description:

Discover trending tokens with Nansen screener results, smart-money holdings, Nansen indicators, and flow intelligence for promising finds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen crypto tokens with Nansen CLI research endpoints, build candidate shortlists, inspect Nansen indicators, and confirm finalists with flow intelligence. Outputs should be treated as informational token research signals, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token rankings and top-token output may be mistaken for personalized investment advice.

Mitigation: Present results as informational screening data and require independent research before any trading decision.

Risk: The skill requires access to a Nansen API key through NANSEN_API_KEY.

Mitigation: Use a revocable, usage-limited API key and avoid exposing it in prompts, logs, or shared outputs.

Risk: Flow intelligence queries can be credit-heavy when run broadly.

Mitigation: Run flow-intelligence only on finalists that already look promising from screener and indicator checks.

Risk: Stablecoins can score highly while not matching a token-discovery shortlist intent.

Mitigation: Filter stablecoins from candidate lists before drilling into token indicators.

## Reference(s):

- [Nansen Token Screener on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-screener)
- [nansen-devops publisher profile](https://clawhub.ai/user/nansen-devops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and token research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nansen CLI and a NANSEN_API_KEY for authenticated Nansen research commands.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
