## Description: <br>
Search and discover 43k+ AI agents registered via ERC-8004. Find agents by skill, chain, or reputation. View leaderboards, ecosystem stats, and monitor metadata changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aetherstacey](https://clawhub.ai/user/aetherstacey) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to search ERC-8004 agent listings, inspect agent details, compare reputation signals, view ecosystem statistics, and monitor selected agents for metadata changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch untrusted agent metadata URLs, including HTTP(S) or IPFS-derived content, which may contact internal or attacker-controlled services. <br>
Mitigation: Run the script in an environment with constrained outbound network access and add URL allowlists plus private and link-local address blocking before autonomous use. <br>
Risk: Automated monitor workflows may act on untrusted or misleading agent metadata changes. <br>
Mitigation: Avoid cron or notifier automation unless monitored agents are trusted, and review change output before taking follow-up action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aetherstacey/erc8004-discover) <br>
- [Agentscan](https://agentscan.info) <br>
- [Agentscan agents API](https://agentscan.info/api/agents) <br>
- [Agentscan networks API](https://agentscan.info/api/networks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API lookups; monitor command writes local cache files under /tmp.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
