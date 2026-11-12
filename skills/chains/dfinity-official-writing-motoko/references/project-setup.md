# Project Setup: Compiler Flags

**Read this only when you are setting up a Motoko project yourself.** These are one-time `mops.toml` settings, not something to revisit while writing code.

**If your platform manages `mops.toml` for you, skip this file entirely** — do not inspect, add, or change `[moc] args`. The flags below are already set on your behalf, and editing them is not yours to do. This is the normal case for hosted platforms; it is only self-managed projects that need anything here.

The flags depend on the moc major pinned in `[toolchain] moc`.

## Persistence

Enhanced orthogonal persistence is `moc`'s default, so a top-level `let`/`var` in an actor is stable without the `stable` keyword. Every actor example in this skill is a plain `actor { ... }`, which must be persistent.

**moc 2:** actors are persistent by default. No flag is needed, and `--default-persistent-actors` is rejected as an unknown option.

**moc 1:** a plain `actor` is persistent only with this flag:

```toml
[moc]
args = ["--default-persistent-actors"]
```

Without it a plain `actor` fails to compile, with one of two errors depending on whether it holds state:

```text
// actor { var count = 0 }
type error [M0219], this declaration is currently implicitly transient, please declare it explicitly `transient`

// actor { public func f() : async Nat { 1 } }  — no stable declaration to complain about
type error [M0220], this actor or actor class should be declared `persistent`
```

If you cannot set the flag, write `persistent actor { ... }` instead — same semantics, declared per actor. moc 2 accepts it with warning M0217 (redundant `persistent`). `--default-persistent-actors` is not listed in `moc --help`, but it is supported.

## Style warnings

The style rules this skill enforces are compiler warnings. Enabling them makes `moc` flag violations for you, and `mops check --fix` then auto-corrects all three:

```toml
[moc]
args = ["-W", "M0236,M0237,M0223"]  # moc 1: prepend "--default-persistent-actors"
```

`M0236` non-dot-notation calls, `M0237` redundant explicit implicit arguments, `M0223` redundant type instantiation. moc 2 enables `M0236` by default; the other two are off by default on both majors.

Where a warning is off, it never fires, so `mops check --fix` has nothing to correct — the rules still hold, you just have to follow them unaided.
