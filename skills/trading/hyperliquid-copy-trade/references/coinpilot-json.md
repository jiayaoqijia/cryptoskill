## coinpilot.json format

The CLI reads credentials from a fixed user-home path on all supported
platforms:

- `~/.coinpilot/coinpilot.json`

This location is fixed. Keep this file on the local machine that is running the
trusted agent runtime, and do not paste the populated contents into chat:

This local file is the actual runtime secret container for the skill. It holds
the Coinpilot API key, Privy user ID, and wallet private keys needed for live
trading calls.

```
{
  "apiKey": "EXPERIMENTAL_API_KEY",
  "apiBaseUrl": "https://api.coinpilot.bot",
  "userId": "did:privy:...",
  "wallets": [
    {
      "index": 0,
      "address": "0x...",
      "privateKey": "...",
      "isPrimary": true
    },
    {
      "index": 1,
      "address": "0x...",
      "privateKey": "...",
      "isPrimary": false
    },
    ...
    {
      "index": 9,
      "address": "0x...",
      "privateKey": "...",
      "isPrimary": false
    }
  ]
}
```

Rules:

- Exactly one primary wallet (`isPrimary: true`) and it must be `index: 0`.
- Include exactly 10 wallets total: 1 primary + 9 subwallets.
- Subwallets must use unique indexes in the range `1-9`.
- When using `scripts/coinpilot_cli.mjs`, never pass raw private keys on the
  command line. Select follower wallets by `--follower-index`,
  `--follower-wallet`, or `--use-prepare-wallet` so the script loads keys from
  this local file in memory only.
- `apiBaseUrl` is optional. When provided, it must be an allowlisted HTTPS
  origin.
- Coinpilot requests from this skill use `apiKey`, the primary wallet
  `privateKey`, and `userId` as the values for `x-api-key`,
  `x-wallet-private-key`, and `x-user-id`.
