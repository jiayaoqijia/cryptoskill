---
name: configuration-load
domain: software-engineering/configuration-load
trigger: "Loading configuration so that bad config fails before traffic."
anti_trigger: "Not for secret storage and rotation, and not for a config product choice."
scope: "Loading and validating configuration before accepting work."
status: seedling
---

# Configuration load

## Standard

Configuration is a schema, and treating it as strings that are read when first used means a typo survives until the code path that reads it runs in production. The alternative is to parse and validate configuration once, at startup, against explicit expectations — required keys present, values in range, URLs well-formed, credentials loadable — and to refuse to start when any check fails. Failure before the port opens is an outage of one deploy; failure after is an outage with customer traffic attached.

Two mechanics make validation real. Defaults must be explicit and safe or absent, never implicit: a timeout defaulted to zero and a missing key defaulted to empty are both silent production incidents. Secrets are referenced, not embedded: the configuration names where a secret comes from, and the load step resolves it, failing if it cannot — a service that starts with an unresolved secret serves its first request with a broken credential.

Primary sources: <https://sre.google/> and <https://12factor.net/>.

## Decision rules

- Record every configuration key, its type, its default or its requiredness, and the failure if absent.
- Validation runs at startup and fails closed: invalid config exits before the port binds.
- Secrets are referenced by source and resolved at load; a failed resolution is a startup failure.
- Record the precedence order: file, environment, overrides, and document which wins.
- Record keys that may change without restart and those that require one.
- Log the loaded configuration with secret values redacted, at startup, once.

## Procedure

1. Enumerate keys with types, defaults, and requiredness.
2. Write the validator and its failure messages.
3. Reference secrets by source and resolve at load.
4. Record precedence and the no-restart list.
5. Add a redacted startup log line of the effective configuration.
6. Test with a missing key, a malformed value, and an unresolved secret.

## Anti-patterns

- Keys read lazily, so a typo fails at the worst moment in the worst path.
- Implicit zero and empty-string defaults for safety-critical settings.
- Secrets pasted into config files rather than referenced.
- An override precedence nobody wrote down, resolved by whichever loaded last.
- A changed value expected live when the service only reads it at startup.

## Done checklist

- [ ] Keys enumerated with types and defaults.
- [ ] Startup validator fails closed.
- [ ] Secrets referenced and resolved at load.
- [ ] Precedence recorded.
- [ ] Effective config logged redacted.
- [ ] Three failure cases tested.

## Sources

- Configuration practice: <https://sre.google/>
- Twelve-factor configuration: <https://12factor.net/>
- Application configuration patterns: <https://martinfowler.com/>
