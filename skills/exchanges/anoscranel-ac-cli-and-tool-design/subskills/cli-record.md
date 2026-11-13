---
name: cli-record
domain: software-engineering/cli-record
trigger: "Writing the record of a tool's interface contract."
anti_trigger: "Not for user documentation, and not for API reference."
scope: "The written record: the interface contract a tool promises."
status: seedling
---

# CLI record

## Standard

The command-line record states the interface the tool promises: the flags, the exit codes, the output format, the stream separation, and the behaviours that scripts may depend on. It is an interface contract rather than user documentation, and its audience is the person writing a script against the tool and the person who will later change it.

Its second function is to bound what may change without a version boundary. A flag's default, an exit code's meaning, and the shape of the stdout output are all things a script can rely on, and a record that names them as stable is what allows a later change to be recognised as breaking rather than as an improvement.

Primary sources: <https://pubs.opengroup.org/> and <https://semver.org/>.

## Decision rules

- The record lists every flag with its form, type, and default.
- The exit codes are enumerated with their meanings and which are stable.
- The stdout format is recorded with its schema and its stability promise.
- The stream separation is recorded, including where progress appears.
- The behaviours that are explicitly not promised are recorded, so they are not relied upon.
- Review triggers are dated: flag addition, default change, format change, exit code change.

## Procedure

1. Enumerate flags with forms, types, and defaults.
2. Enumerate exit codes and mark which are stable.
3. Record the stdout schema and its versioning.
4. Record stream separation and progress behaviour.
5. Record explicitly unstable behaviours.
6. Review at each change and classify it as breaking or additive.

## Anti-patterns

- Documenting the interface only in the help output.
- Omitting exit codes, which scripts depend on most.
- Leaving the output schema implicit, so any change breaks a parser.
- Not naming what is unstable, so everything appears guaranteed.
- Changing a default without recording it as breaking.

## Done checklist

- [ ] Flags enumerated with defaults.
- [ ] Exit codes enumerated with stability.
- [ ] Stdout schema recorded.
- [ ] Stream separation recorded.
- [ ] Unstable behaviours recorded.
- [ ] Triggers dated.

The unstable list is the part of the record that prevents the most arguments: a human-readable summary line, a progress format, and an error message's wording are all things users will notice and none is a contract, and saying so in the record turns a later change from a regression report into a documented non-promise.


## Sources

- POSIX utility conventions: <https://pubs.opengroup.org/>
- Semantic versioning reference: <https://semver.org/>
- CLI design guidance: <https://clig.dev/>
