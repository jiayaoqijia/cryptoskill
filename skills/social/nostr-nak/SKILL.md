---
name: nostr-nak
description: General purpose skill for using the Nostr Army Knife (nak) CLI tool with PTY support.
---
# nostr-nak

General purpose skill for using the Nostr Army Knife (nak) CLI tool.

## Critical Technical Note (PTY Requirement)
`nak` hangs in non-interactive environments due to stdout buffering. 
**Always** wrap `nak` commands in `script` to force a pseudo-TTY:
`script -q -c "nak req ..." /dev/null | cat`

## Relay Logic
By default, use discovery relays if no relay is specified:
- `wss://relay.damus.io`
- `wss://relay.primal.net`
- `wss://relay.nostr.band`

If the user specifies a relay, override these defaults.

## Identity Handling
- **Querying**: Use `npub...` or hex pubkey with the `-a` flag.
- **Posting**: Use `nsec...` or hex private key with the `--sec` flag.

## Usage Examples
Fetch last 5 notes:
`script -q -c "nak req -k 1 -a <npub> <relays> -l 5" /dev/null | cat`
