---
name: flag-conventions
domain: software-engineering/flag-conventions
trigger: "Designing flags that will not surprise the people parsing them."
anti_trigger: "Not for API parameter design, and not for configuration file formats."
scope: "Long and short options, defaults, and the least surprising parse."
status: seedling
---

# Flag conventions

## Standard

Flags are parsed by conventions the user already holds, and violating them creates bugs that are blamed on the parser. A long option takes a value after an equals sign or a space, a short option clusters with its value attached, a double dash ends option parsing, and a repeated flag either accumulates or overrides depending on what it means. Those are the rules a user's shell history and their muscle memory assume.

Defaults are the second half of the contract. A flag that changes a default silently between versions breaks scripts that were correct; a flag whose default is unsafe makes the unsafe path the one people take. The record states each flag's default and whether the tool's behaviour with no flags is safe.

Primary sources: <https://pubs.opengroup.org/> and <https://clig.dev/>.

## Decision rules

- Record each flag with its long form, its short form, and its argument type.
- Record the behaviour of a repeated flag: accumulate, override, or error.
- Record the default and whether the no-flag invocation is the safe one.
- Record the `--` terminator behaviour and positional argument handling.
- Record the deprecated flags still accepted, and their replacement.
- Record the environment variables the tool reads, since they are flags by another name.

## Procedure

1. Enumerate flags with forms and argument types.
2. Assign short forms only where they are mnemonic and unambiguous.
3. Record each default and confirm the safe path is the default.
4. Implement the `--` terminator and record positional handling.
5. Record deprecated flags and warnings.
6. Record environment variables and their precedence relative to flags.

## Anti-patterns

- A short option whose letter means something unrelated.
- Changing a default without a major version boundary.
- A destructive operation as the default action.
- Ignoring the `--` terminator, so a filename beginning with a dash is unusable.
- Environment variables that silently override flags.

## Done checklist

- [ ] Flags enumerated with forms and types.
- [ ] Repeat behaviour recorded.
- [ ] Defaults recorded and safe.
- [ ] Terminator and positionals recorded.
- [ ] Deprecated flags recorded.
- [ ] Environment variables and precedence recorded.

The environment variable question is where most surprise lives: a variable that overrides a flag, or a flag that overrides a variable without saying so, produces behaviour that depends on a shell the operator did not write, and recording the precedence order is the only way to make the tool's behaviour predictable across environments.


## Sources

- POSIX utility syntax guidelines: <https://pubs.opengroup.org/>
- CLI interface guidance: <https://clig.dev/>
- GNU coding standards: <https://www.gnu.org/prep/standards/>
