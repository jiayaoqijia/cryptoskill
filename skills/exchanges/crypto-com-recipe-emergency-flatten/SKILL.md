---
name: recipe-emergency-flatten
description: Emergency flatten — cancel all open orders and close every open position as quickly as possible. Use when markets turn against you or credentials may be compromised.
---

# Emergency Flatten

## When to Use

- Market is moving violently against current exposure
- Suspect API key compromise — reduce blast radius
- End-of-session sweep to go flat overnight
- Agent has behaved unexpectedly and the human wants a hard stop

This is a destructive workflow. Only run when the user asks for it explicitly.

## Assumptions

- Authentication is configured (`CDCX_API_KEY` / `CDCX_API_SECRET`, or a profile)
- MCP mode: server must be started with `--allow-dangerous` (this workflow uses tier-`dangerous` commands)
- CLI mode: use `--yes` to skip prompts, or acknowledge each prompt

## Workflow

```
# 1. Cancel every open order (dangerous)
cdcx trade cancel-all --yes -o json

# 2. Confirm no open orders remain
cdcx trade open-orders -o json

# 3. List every open position
cdcx account positions -o json

# 4. Close each position at market
#    Run this per row returned in step 3
cdcx trade close-position <INSTRUMENT_NAME> --type MARKET --yes -o json

# 5. Verify positions are flat
cdcx account positions -o json

# 6. Also sweep advanced (OTO/OTOCO) orders — they live in a separate namespace
cdcx advanced cancel-all --yes -o json
cdcx advanced open-orders -o json

# 7. Final wallet check
cdcx account summary -o json
```

## Automated One-Liner

```
cdcx trade cancel-all --yes && \
cdcx advanced cancel-all --yes && \
cdcx account positions -o json | \
    jq -r '.data[].instrument_name' | \
    while read i; do cdcx trade close-position "$i" --type MARKET --yes; done && \
cdcx account positions -o json
```

## Notes

- `cancel-all` without an instrument cancels *every* open order across the account
- `close-position` is asynchronous — it returns an ack, not a fill. The position may remain open for a moment; step 5 confirms
- Advanced orders (OTO/OTOCO) are not cancelled by `cdcx trade cancel-all` — sweep them separately with `cdcx advanced cancel-all`
- If you are in doubt about the current state, re-run `cdcx account positions` and `cdcx trade open-orders` until both are empty
- If API access itself is the concern, also rotate the API key at https://crypto.com/exchange/settings/api afterwards
