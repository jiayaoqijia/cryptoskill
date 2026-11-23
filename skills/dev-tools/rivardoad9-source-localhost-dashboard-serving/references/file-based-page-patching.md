# Editing and probing a one-file dashboard: work from script files, not inline payloads

Companion to `nav-tap-wiring.md` / `web3-glass-theme.md`. Those cover *what* to change; this covers the
mechanics that repeatedly bit while doing it (ZEMIZ RISK rewrite, Oct 2026).

## 1. A heredoc full of page code can be refused before it runs

Ran: `python3 - <<'EOF' … playwright code … EOF` → terminal returned
`Foreground command uses '&' backgrounding. Re-send WITHOUT the '&' …`. Nothing in the command was
backgrounding anything — the guard's scanner just matched `&&`/`&`-looking text inside the payload.
It fired twice on heredocs that contained browser JS and jQuery-free DOM code.

**Workaround (works every time):**

```
write_file  /tmp/t_nav.py   ← the probe/patch script
terminal    python3 /tmp/t_nav.py
```

Same rule for the dozens of tiny CSS/markup edits: instead of one-off `patch` calls (or `sed`), write
`/tmp/fix_<thing>.py` that does

```python
s = open(p, encoding="utf-8").read()
for old, new in reps:
    if old not in s: miss.append(old[:60])
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("changed", s != original, "| zerowidth:", s.count("\u200b"), "| miss:", miss)
```

- **Print the `miss:[...]` list.** A silently-unmatched anchor is exactly how a "fix" ends up not applied
  while the report says it landed; a non-empty miss list means re-anchor and re-run before verifying.
- Check for stray zero-width characters (`\u200b`) you may have typed into CSS — they quietly break a
  selector (a `\u200b.note{…}` rule simply never matches).

## 2. Replacement strings written inside Python eat quotes

Patching a template literal through a Python list of tuples produced
`${d.port_score??''}` → written out as `${d.port_score??}` and `node --check` failed with
`Expected '}' but found '}'`. The `''` inside a single-quoted Python string terminates it.

- Put replacement strings that contain quotes in a **separate `write_file`**d script, or use `patch`
  (`mode=replace`) for those specific edits — it does not go through Python string syntax.
- Then always re-extract the inline `<script>` and run `node --check`:

```python
h = open(p, encoding="utf-8").read()
open("/tmp/x.js", "w").write(h[h.rindex("<script>") + 8 : h.rindex("</script>")])
```

## 3. Prove the served build is the fixed build

After every change to the page or the service worker:

```bash
curl -s -m 20 "$TUNNEL/risk"        | grep -c "<a new symbol you just added>"
curl -s -m 20 "$TUNNEL/sw.js"       | head -2          # CACHE name bumped?
curl -s -o /dev/null -w '%{http_code}\n' "$TUNNEL/risk" # 200
```

A non-zero grep count is the only evidence that the phone will actually fetch the new HTML; telling the
user to "close and reopen the installed app" without it is hopium.

## 4. Order of operations that kept each pass verifiable

1. `write_file` the patch script → run → `changed True`, `miss: []`.
2. Re-extract inline JS → `node --check` ("JS OK").
3. `write_file` the browser probe (`t_v3.py` style) → run → JS errors, overflow at 390 **and** 1366,
   emoji count, mask-leak count, per-row alignment, plus per-card screenshots.
4. `vision_analyze` one card image at a time with a targeted question; fix what it names; go back to 1.

Never combine a data-binding change with a theme change in the same pass — a pure-CSS/markup pass keeps
steps 2–4 meaningful.
