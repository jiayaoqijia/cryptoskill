## Description: <br>
Trading Coach turns brokerage CSV trade records into FIFO-matched trading review reports with weighted quality scoring and AI-assisted improvement insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benzema216](https://clawhub.ai/user/benzema216) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to review exported brokerage CSV records, match trades into position cycles, score trading quality, and generate improvement-oriented trading summaries. It is intended for analysis and coaching support, not as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run external code on sensitive brokerage CSV data. <br>
Mitigation: Review the referenced project and dependencies before execution, prefer a virtual environment or container, and use redacted CSV copies without account numbers or unnecessary personal details. <br>
Risk: AI-generated trading scores and suggestions can be incomplete or misleading for financial decisions. <br>
Mitigation: Treat all generated analysis as informational review support and confirm decisions with independent judgment or qualified financial advice. <br>
Risk: Configuration or API keys may expose data to external services if supplied without review. <br>
Mitigation: Do not provide API keys or credentials unless the user has reviewed which services receive requests and what data will be transmitted. <br>


## Reference(s): <br>
- [Supported CSV Formats](references/csv_formats.md) <br>
- [Quality Scoring System](references/scoring_system.md) <br>
- [AI Insight Dimensions](references/insight_dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and structured trading summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes brokerage CSV exports and produces informational scores, statistics, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
