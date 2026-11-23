# Calling a keeper that pkills by filename (self-kill from the INSIDE)

The SKILL.md pitfall covers the caller-side version (`pkill -f "<script>.py"` typed by the agent matches
the shell's own command line). This is the variant that bit twice on 10 Oct 2026 and is NOT covered by
the bracket trick:

The keeper script itself contains the pattern, e.g. `insider_chain_up.sh`:

```bash
if ! curl -sf -m 5 "http://127.0.0.1:$PORT/healthz" >/dev/null 2>&1; then
  pkill -f "insider_board_server.py"     # <-- matches the CALLER's command line too
  sleep 1
  setsid nohup env INSIDER_PORT="$PORT" python3 -u "$SCRIPTS/insider_board_server.py" …
fi
```

So this invocation kills the calling shell mid-run:

```bash
# BAD: the caller's own command line contains the pattern the keeper will pkill
python3 -m py_compile insider_board_server.py && bash insider_chain_up.sh
# → exit -15 (SIGTERM), one line of output ("sintaks ok"), keeper left half-done,
#   the relaunched server's fate unknown
```

`pkill -f` matches the FULL command line of every process, and the agent's shell running that compound
command has the string in its own argv. Syntactic fixes:

- Never name the target file in the same command that runs the keeper. Compile/syntax-check in one call,
  run the keeper in another (`bash insider_chain_up.sh` alone).
- Or invoke it through a wrapper whose argv doesn't contain the name:
  `bash -c "$(cat ~/.hermes/scripts/<keeper>.sh)"` still carries it — prefer the separate-call form.
- The keeper's own `pkill` is fine for the keeper: it runs the pattern from a *different* argv than the
  process it intends to kill.

After any keeper-triggered restart, confirm it actually landed instead of assuming:

```bash
ss -ltnp | grep <port>                 # listener present again
curl -s http://127.0.0.1:<port>/healthz
ps -eo pid,etime,cmd | grep -i "<name>" | grep -v grep   # fresh etime = relaunched
```
