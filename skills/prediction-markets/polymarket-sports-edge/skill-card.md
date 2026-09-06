## Description: <br>
Find odds divergence between sportsbook consensus and Polymarket sports markets, then trade the gap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjims](https://clawhub.ai/user/0xjims) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to monitor sports prediction markets for sportsbook consensus divergence and optionally execute Polymarket trades through Simmer. It is intended for users who understand prediction-market trading risk and can configure API keys, trade sizing, dry-run review, and live execution controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run as a scheduled prediction-market trading bot and can place real-money trades when LIVE=true. <br>
Mitigation: Keep LIVE=false until dry-run output has been reviewed over multiple cycles, use small trade sizes, and add approval and loss-limit controls before enabling live execution. <br>
Risk: The release evidence reports ambiguous duplicate manifests and limited live-trading safeguards. <br>
Mitigation: Confirm which manifest and script will run in the deployment environment, then restrict or revoke API keys when not in active use. <br>
Risk: Market matching and sportsbook consensus signals can be wrong, stale, or incomplete. <br>
Mitigation: Review proposed trades, tune divergence thresholds and resolution windows, and avoid relying on the skill as the sole basis for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xjims/polymarket-sports-edge) <br>
- [The Odds API](https://the-odds-api.com) <br>
- [Simmer markets API endpoint](https://api.simmer.markets/api/sdk/markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs and Markdown setup guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and THE_ODDS_API_KEY; dry-run is the default unless LIVE=true is set.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
