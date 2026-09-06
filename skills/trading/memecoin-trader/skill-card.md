## Description: <br>
Automates Solana memecoin trading with fdv.lol CLI and Agent Gary full AI control using a locally generated user profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[build23w](https://clawhub.ai/user/build23w) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to configure and run a headless fdv.lol memecoin trading workflow with local wallet, RPC, Jupiter, and LLM credentials. It is intended for users who understand that autonomous trading can execute financial actions and lose the funded balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous trading can spend or lose the wallet balance. <br>
Mitigation: Use only a fresh burner wallet funded with a very small amount, and assume the funded balance can be lost. <br>
Risk: The workflow requires wallet secrets, RPC credentials, Jupiter API keys, and LLM API keys. <br>
Mitigation: Keep the profile local, restrict file permissions, never publish real secrets, and avoid printing secrets in logs. <br>
Risk: The documented run path includes unpinned remote code execution for fdv.lol CLI. <br>
Mitigation: Prefer a pinned and verified fdv.lol release instead of curl-pipe execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/build23w/agentic-powered-memecoin-trader) <br>
- [fdv.lol upstream repository](https://github.com/build23w/fdv.lol) <br>
- [fdv.lol profile example](https://github.com/build23w/fdv.lol/blob/main/tools/profiles/fdv.profiles.example.json) <br>
- [Jupiter API pricing](https://portal.jup.ag/pricing) <br>
- [QuickNode signup](https://quicknode.com/signup?via=lf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local profile setup guidance and command-line run instructions; generated profiles may contain secrets and should remain local.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
