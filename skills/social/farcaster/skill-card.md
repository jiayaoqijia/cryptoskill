## Description: <br>
Post, read, search, and engage on Farcaster via the Neynar API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to read Farcaster data and perform account actions through Neynar, including posting casts, replying, searching, looking up users, reacting, deleting casts, and browsing channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live Farcaster account authority for posting, deleting, liking, recasting, following, and unfollowing. <br>
Mitigation: Require explicit user confirmation before any public or account-changing action. <br>
Risk: API keys and signer UUIDs may be exposed if passed on command lines or loaded through shell eval patterns in shared or logged environments. <br>
Mitigation: Prefer environment or secret-management mechanisms that avoid command history and logs, and avoid the eval credential-loading example. <br>
Risk: Media upload workflows can send local files and metadata to third-party hosts before embedding them in casts. <br>
Mitigation: Review file contents and metadata before upload and only use third-party hosts that the operator accepts. <br>
Risk: Some Neynar endpoints require paid access and may fail at runtime with payment or rate-limit errors. <br>
Mitigation: Confirm the Neynar plan and handle 402 and 429 errors before relying on automated workflows. <br>


## Reference(s): <br>
- [Farcaster Skill on ClawHub](https://clawhub.ai/openclaw-consensus-bot/farcaster-skill) <br>
- [Neynar v2 API Endpoint Reference](references/neynar_endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts emit JSON on success and JSON error objects to stderr on failure.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
