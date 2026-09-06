## Description: <br>
Search for tokens or entities by name. Use when you have a token name and need the full address, or want to find an entity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run Nansen searches for token or entity names, including optional filters for type, chain, result limit, and selected fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Nansen API key. <br>
Mitigation: Use a dedicated or limited key if available and keep it scoped to the documented Nansen search workflow. <br>
Risk: The skill depends on the third-party nansen-cli package. <br>
Mitigation: Install it only in environments where the package is trusted and review proposed nansen commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nansen-devops/nansen-general-search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash command examples and an option table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the nansen CLI and requires NANSEN_API_KEY for the documented search workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
