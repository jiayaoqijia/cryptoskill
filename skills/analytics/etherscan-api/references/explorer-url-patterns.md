# Explorer URL Patterns

Use these when you want human-readable pages alongside API results.

## Explorer Roots
- Ethereum mainnet: `https://etherscan.io/`
- Ethereum hoodi: `https://hoodi.etherscan.io/`
- Taiko mainnet: `https://taikoscan.io/`
- Taiko hoodi: `https://hoodi.taikoscan.io/`

## Common Paths
Address page:
- `<explorer>/address/<0xaddress>`

Transaction page:
- `<explorer>/tx/<0xtxhash>`

Token page:
- `<explorer>/token/<0xtoken>`

Block page:
- `<explorer>/block/<blockNumber>`

Verified contract code tab (from address page):
- open `<explorer>/address/<0xaddress>#code`

Operational pattern:
1. Query API first for machine-readable data.
2. Open explorer URL for quick manual validation/debugging.
3. If proxy, inspect runtime address page and implementation metadata together.
