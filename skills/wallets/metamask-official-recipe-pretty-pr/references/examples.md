# Evidence Examples

## Good

```md
### Recipe validation

Verdict: pass

Proved:
- PT-1: The warning appears when the quote expires.
- PT-2: Refreshing the quote removes the warning and enables Continue.

Artifacts:
- `summary.json` — pass status, branch, device, command.
- `trace.json` — ordered recipe nodes.
- `screenshots/quote-expired.png` — warning state after settle.
- `screenshots/quote-refreshed.png` — valid refreshed state after settle.
```

## Bad

```md
Tested manually and it works.
```

This is not recipe evidence. It has no proof targets, no run status, no artifact links, and no reproducible command.
