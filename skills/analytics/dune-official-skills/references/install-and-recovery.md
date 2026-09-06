# Install & Recovery

> **Prerequisite:** Read the [main skill](../SKILL.md) for authentication, global flags, and key concepts.

This reference covers CLI installation, authentication failure recovery, and version compatibility checks. These steps are only needed when a `dune` command fails.

---

## CLI Not Found Recovery

If the command fails because `dune` is not found on PATH (e.g. "command not found"), follow the installation steps in the [shared CLI install reference](../../shared/cli-install.md#cli-not-found-recovery).

---

## Authentication Failure Recovery

If a command fails with an authentication or authorization error (e.g. 401, "unauthorized", "missing API key"), the user needs to authenticate. **Stop and ask the user** to authenticate in a separate terminal:

1. Go to Dune (https://dune.com), navigate to the "APIs & Connectors" section, and then the "API Keys" tab to generate an API key (if they don't have one)
2. Run `dune auth` in their terminal and follow the prompts
3. Come back to the conversation once done

Then retry the original command. If it still fails, inform the user their key appears invalid and ask them to retry.

Do **not** attempt to handle the API key yourself -- the user must authenticate outside of this session.

---

## Version Compatibility

See the [shared CLI version compatibility reference](../../shared/cli-install.md#version-compatibility).

---

## See Also

- [Main skill](../SKILL.md) -- Command overview and key concepts
