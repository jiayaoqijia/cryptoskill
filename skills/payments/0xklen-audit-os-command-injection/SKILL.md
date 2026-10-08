---
name: audit-os-command-injection
description: Use when user input can reach a shell or an exec that passes a command string. Finds the sinks, removes the shell, and proves injection is closed with a metacharacter payload.
---

# Audit OS command injection

Command injection happens when input reaches a shell interpreter with its metacharacters intact —
`;`, `|`, `&&`, backticks, `$()`, and newlines. The primary fix is to stop invoking a shell and pass
an argument vector to the kernel directly.

## Procedure

1. Find shell-invoking sinks across languages:

       rg -n "subprocess\.(run|call|Popen).*shell=True|os\.system\(|os\.popen\(|commands\.getoutput" .   # Python
       rg -n "exec\(|execSync|child_process|shelljs" .                                                  # Node
       rg -n "Runtime\.getRuntime\(\)\.exec|ProcessBuilder" .                                            # Java
       rg -n "system\(|popen\(|`.*`" .                                                                    # C/PHP/Ruby

2. Trace which part of the command string comes from input — often a filename, hostname, or a
   user-chosen option, not the whole command.

3. Replace `shell=True` with an argument list; the process is then invoked without shell parsing:

       # vulnerable
       subprocess.run(f"convert {src} {dst}", shell=True)
       # fixed — argv form, no shell
       subprocess.run(["convert", src, dst], check=True)

   In Node, use `execFile`/`spawn` with an args array rather than `exec('cmd ' + input)`.

4. When a shell is genuinely required, pass the untrusted value as a positional argument
   (`sh -c 'mytool "$1"' _ "$input"`) so the shell never re-parses it, or quote with the shell's own
   escaper (`shlex.quote`), never a hand-rolled regex.

5. Watch option injection: even with an argv form, input like `-o /etc/cron.d/x` becomes a flag.
   Prefix user paths with `--` and validate the value.

6. Restrict the child's environment and working directory to shrink the blast radius.

7. Prove the fix with a metacharacter payload and confirm the file it would create does not appear:

       filename='x; touch /tmp/pwned'
       # after the fix: /tmp/pwned must not exist

## Pitfalls

- `shell=True` with a *constant* string is fine; the danger is any input concatenated in — review
  every format/f-string that feeds it.
- A denylist of `;` and `|` misses newlines, `$IFS`, `$(...)`, and `%0a`.
- `subprocess.run(..., shell=True)` on Windows uses `cmd.exe`, whose escaping differs from POSIX.
- Escaping with `shlex.quote` at the wrong layer (before a second interpolation) still exposes.
- Backtick interpolation in Ruby/PHP shell functions executes before the argument is passed.
- Time-of-check/time-of-use: validating a filename then passing the string lets a symlink race.

## Verification

    rg -n "shell=True|os\.system|execSync|child_process.*exec\(" src/ | rg -v none-expr
    printf '%s' 'x; touch /tmp/pwned' | xargs -I{} sh -c 'true' ; test ! -e /tmp/pwned && echo "no injection"

Pass: the sink search returns only argv-form invocations (no `shell=True` with input) and the
metacharacter payload creates no side-effect file. Report the sinks converted, any remaining shell
use with its quoting strategy, and the payload result.
