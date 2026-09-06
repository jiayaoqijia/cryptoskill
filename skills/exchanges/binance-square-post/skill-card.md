## Description: <br>
Post pure text content to Binance Square and return the resulting post URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-chen2050](https://clawhub.ai/user/ai-chen2050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to publish prepared text updates to Binance Square through an agent workflow. It is intended for drafting or optimizing post text, confirming the final version, submitting it through the Binance Square OpenAPI, and returning the public post URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Binance Square posts. <br>
Mitigation: Require explicit user confirmation of the exact final post text before submission. <br>
Risk: The artifact tells the agent to store the Binance Square OpenAPI key in the skill file. <br>
Mitigation: Store credentials only in a proper secret manager or environment variable, and never in SKILL.md or prompt files. <br>
Risk: A broad Binance credential could expose trading or withdrawal privileges. <br>
Mitigation: Use a dedicated least-privilege Binance Square posting key with no trading or withdrawal permissions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ai-chen2050/binance-square-post) <br>
- [Binance Square content add API endpoint](https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown text with API request guidance and post URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pure text Binance Square posts; successful posts return a Binance Square post URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
