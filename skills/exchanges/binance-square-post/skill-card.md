## Description:

Post text content to Binance Square and return the resulting post URL when publishing succeeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-chen2050](https://clawhub.ai/user/ai-chen2050)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draft, optionally polish, and publish pure text posts to Binance Square through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to save a Binance Square API key in the skill file while claiming secure storage without showing a secure mechanism.

Mitigation: Use a narrowly scoped Binance Square posting key, avoid trading or withdrawal permissions, and do not provide keys unless plaintext storage risk is acceptable.

Risk: A previously provided API key may have been stored or shared by the agent workflow.

Mitigation: Rotate any key that may have been exposed and review the skill before installing or using it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-chen2050/skills/binance-square-post)
- [Binance Square Content Add Endpoint](https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with posting guidance, curl examples, API response summaries, and post URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure text posts only; successful posts return a Binance Square post URL when the API response includes an id.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
