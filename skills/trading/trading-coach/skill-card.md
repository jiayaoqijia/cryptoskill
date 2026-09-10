## Description:

Trading Coach turns brokerage CSV exports into trading review reports with FIFO position matching, eight-dimension trade quality scoring, and ten-dimension improvement insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzema216](https://clawhub.ai/user/benzema216)

### License/Terms of Use:


## Use Case:

External traders and reviewers use this skill to analyze brokerage CSV exports, calculate trading performance, identify repeated trading-pattern issues, and produce concise post-trade review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run remote trading-analysis code on sensitive brokerage files.

Mitigation: Review the referenced code and requirements, pin a known commit, run it in an isolated environment, and redact account identifiers or unnecessary personal fields before use.

Risk: Trading reports and recommendations can be misleading if source records, matching, scoring, or assumptions are incomplete.

Mitigation: Treat outputs as decision-support material, verify calculations against brokerage records, and avoid relying on the skill as financial advice.

## Reference(s):

- [Supported CSV Formats](references/csv_formats.md)
- [Quality Scoring System](references/scoring_system.md)
- [AI Insight Dimensions](references/insight_dimensions.md)
- [ClawHub Skill Page](https://clawhub.ai/benzema216/skills/trading-coach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with CLI commands, scoring summaries, and actionable trading review recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize sensitive brokerage CSV data; review inputs and outputs before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
