# farcaster-skill (Neynar)

Small, reliable scripts for Farcaster via the **Neynar v2 API**.

## Requirements

- bash
- curl
- jq
- python3 (for URL encoding)

## Setup

Export:

```bash
export NEYNAR_API_KEY="..."
export NEYNAR_SIGNER_UUID="..."   # required for write ops (cast, like/recast, delete)
```

## Quick start

```bash
# user lookup
./scripts/fc_user.sh --username dwr

# read a user's casts
./scripts/fc_feed.sh --fid 3 --limit 5

# post a cast (write)
./scripts/fc_cast.sh --text "Hello Farcaster!"
```

## Notes

- Some endpoints are **paid** on Neynar; scripts will surface `402 PaymentRequired`.
- All scripts emit JSON on success and emit a JSON error object to stderr on failure.

See `SKILL.md` for full agent-facing docs and `references/neynar_endpoints.md` for the endpoint reference.
