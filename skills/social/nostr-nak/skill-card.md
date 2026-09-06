## Description: <br>
General purpose skill for using the Nostr Army Knife (nak) CLI tool with PTY support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samthomson](https://clawhub.ai/user/samthomson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query and post to Nostr through the nak CLI, including relay selection and PTY wrapping needed for reliable command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose Nostr private keys when asking an agent to sign or post events. <br>
Mitigation: Only provide a private key when intentionally signing or posting, and avoid placing nsec or hex private keys in prompts, reusable chat context, shell history, logs, or transcripts. <br>
Risk: Running nak from an untrusted installation source can execute an unexpected CLI binary. <br>
Mitigation: Install nak only from a trusted source and review generated commands before execution. <br>


## Reference(s): <br>
- [Nostr Nak on ClawHub](https://clawhub.ai/samthomson/nostr-nak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nostr relay URLs, public-key query arguments, and posting command examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
