## Description:

AI-powered trading insights suite: prediction markets (Polymarket/Kalshi) and social sentiment signals powered by UnifAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbruceli](https://clawhub.ai/user/zbruceli)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to query prediction-market data, compare Polymarket and Kalshi markets, and summarize social sentiment signals for market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-backed tool execution may be under-scoped for a trading analysis workflow.

Mitigation: Use dedicated low-privilege API keys and review permissions before installation or execution.

Risk: Trade or portfolio-related behavior may be misleading if treated as confirmed execution or investment advice.

Mitigation: Do not rely on trade or portfolio actions unless they are verified as read-only, simulated, or protected by explicit human confirmation and platform-side limits.

Risk: The included web interface may expose trading analysis capabilities if bound to a public interface.

Mitigation: Run the web server only on a trusted local or private interface unless separately reviewed and secured.

## Reference(s):

- [UnifAI SDK](https://github.com/unifai-network/unifai-sdk-py)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Kalshi API Documentation](https://docs.kalshi.com)
- [Polymarket Documentation](https://docs.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured API keys for UnifAI-backed and LLM-backed analysis paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
