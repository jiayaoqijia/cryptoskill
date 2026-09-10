## Description:

Ton is an informational ClawHub namespace package for Netsnek e.U. audio and media processing tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to present the ton brand summary, list claimed audio and media workflow capabilities, and return structured metadata about the namespace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes audio-processing capabilities that the bundled artifact does not implement.

Mitigation: Present it as an informational namespace placeholder unless the publisher adds working audio-processing behavior.

Risk: The bundled shell script may fail to execute because security evidence reports a UTF-8 BOM and mixed line endings.

Mitigation: Normalize the script file before relying on its command examples in an execution workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/ton)
- [Publisher profile](https://clawhub.ai/user/kleberbaum)
- [Netsnek e.U.](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static informational output; no audio files are processed by the packaged script.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
