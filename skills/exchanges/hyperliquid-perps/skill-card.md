## Description: <br>
Paper and live perpetual futures trading on Hyperliquid with leverage selection, OBV divergence, and auto-stop-loss guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamieRossouw](https://clawhub.ai/user/JamieRossouw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and trading automation developers use this skill to guide agents working with Hyperliquid perpetual futures workflows, including paper trading, live trading, leverage management, signal handling, and stop-loss setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence live leveraged crypto trades without documented opt-in, confirmation, or risk limits. <br>
Mitigation: Use paper trading by default and require explicit live opt-in, per-trade confirmation, strict leverage and position limits, maximum-loss rules, and easy credential revocation before connecting live Hyperliquid credentials. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline commands or setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May influence real leveraged trading decisions and should default to paper trading unless live-trading controls are explicitly enforced.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
