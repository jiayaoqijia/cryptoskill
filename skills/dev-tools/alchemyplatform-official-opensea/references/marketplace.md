# OpenSea Marketplace Reference

**Primary tool:** `npx @opensea/cli@latest <command>` (or `opensea` if installed globally with `npm install -g @opensea/cli`)
**REST API base:** `https://api.opensea.io/api/v2` (set `X-API-KEY: $OPENSEA_API_KEY`)

For NFT metadata outside the marketplace context, route to `alchemy-api` (NFT API). For pure cross-chain token swaps, route to `lifi`.

---

## Listings

### Best listings for a collection

```bash
opensea listings best <slug> [--limit <n>]
# Example: opensea listings best boredapeyachtclub --limit 5
```

### Best listing for a specific NFT

```bash
opensea listings best-for-nft <slug> <token_id>
```

The response includes `order_hash` — needed for fulfillment.

### All listings (collection-wide)

```bash
opensea listings all <slug> [--limit <n>]
```

---

## Offers

### Best offer for a specific NFT

```bash
opensea offers best-for-nft <slug> <token_id>
```

### All offers on a collection

```bash
opensea offers all <slug> [--limit <n>]
```

### Collection-wide offers (offers on the whole collection, not a specific NFT)

```bash
opensea offers collection <slug> [--limit <n>]
```

### Trait-targeted offers

```bash
opensea offers traits <slug> --type <trait-type> --value <trait-value>
# Example: opensea offers traits boredapeyachtclub --type Background --value Aquamarine
```

---

## Collection stats + discovery

### Stats (floor, volume, supply)

```bash
opensea collections stats <slug>
# Example response: floor_price, total_volume, num_owners, total_supply, market_cap
```

### Trending

```bash
opensea collections trending [--timeframe ONE_HOUR | ONE_DAY | SEVEN_DAYS] [--chains ethereum,base]
```

### Top by metric

```bash
opensea collections top [--sort-by floor_price | total_volume | num_owners] [--chains ethereum,base]
```

### Collection traits (rarity)

```bash
opensea collections traits <slug>
```

---

## Seaport trade execution

### Buy an NFT (fulfill a listing)

```bash
# 1. Get best listing
opensea listings best-for-nft boredapeyachtclub 1234
# Response includes `order_hash`

# 2. Build fulfillment payload
./scripts/opensea-fulfill-listing.sh ethereum 0xORDER_HASH 0xBUYER_WALLET

# 3. The response contains the tx data (`to`, `data`, `value`) — sign + submit via wallet
```

### Sell (accept an offer)

```bash
# 1. Get best offer for your NFT
opensea offers best-for-nft boredapeyachtclub 1234
# Response includes `order_hash`

# 2. Build fulfillment payload
./scripts/opensea-fulfill-offer.sh ethereum 0xOFFER_HASH 0xSELLER_WALLET 0xNFT_CONTRACT 1234

# 3. Execute the returned tx data
```

### Create a listing or offer (requires wallet signature)

Listings and offers are Seaport orders signed by the wallet — call them via `opensea-post.sh` with the full Seaport order structure. The signature happens client-side (or via Privy if configured) before posting.

```bash
./scripts/opensea-post.sh /api/v2/orders/ethereum/seaport/listings '<seaport-order-json>'
./scripts/opensea-post.sh /api/v2/orders/ethereum/seaport/offers '<seaport-order-json>'
```

For the Seaport order shape, see [Seaport docs](https://docs.opensea.io/reference/seaport-overview).

---

## Events + monitoring

### Recent events (filterable)

```bash
opensea events list [--event-type sale | transfer | mint | listing | offer | trait_offer | collection_offer] [--limit <n>]
```

### By collection

```bash
opensea events by-collection <slug> [--event-type sale]
```

### By NFT

```bash
opensea events by-nft <chain> <contract> <token_id>
```

### By account

```bash
opensea events by-account <address>
```

### Real-time streaming (sales)

```bash
./scripts/opensea-stream-collection.sh <slug>
# Requires websocat
# Filters to sales by default; pipe through jq for formatting
```

If `websocat` isn't installed, poll `events by-collection` on a short interval as a fallback.

---

## Drops + minting

```bash
# Browse drops
opensea drops list [--type featured | upcoming | recent] [--chains ethereum,base]

# Get drop details
opensea drops get <slug>

# Build a mint tx (returns calldata, doesn't submit)
opensea drops mint <slug> --minter 0xMINTER_WALLET [--quantity 1]
```

For drop creators (deploy SeaDrop contracts), use the MCP tools `deploy_seadrop_contract` and `get_deploy_receipt` if the OpenSea MCP server is wired in.

---

## Search

```bash
opensea search <query> --types collection,nft,token,account [--chains ethereum,base]
```

`--types` accepts a comma-separated list. Combine with `--chains` to constrain.

---

## Account utilities

### Account details

```bash
opensea accounts get <address>
```

### Resolve ENS / username / address

```bash
opensea accounts resolve <identifier>
# Identifier can be:
#   - 0x address
#   - vitalik.eth
#   - opensea-username
```

---

## Token swaps (caveat)

OpenSea's API includes a cross-chain DEX aggregator:

```bash
opensea swaps quote \
  --from-chain base --from-address 0x0000000000000000000000000000000000000000 \
  --to-chain base --to-address 0xTokenAddress \
  --quantity 0.02 --address 0xYOUR_WALLET
```

Useful when the user is already in an NFT-buying flow that involves a token swap. For pure swap flows (no NFT marketplace context), prefer the `lifi` ecosystem skill — it aggregates more bridges and DEXs across more chains.

---

## Generic GET / POST

For endpoints not covered by the CLI:

```bash
./scripts/opensea-get.sh /api/v2/<path> "[query_string]"
./scripts/opensea-post.sh /api/v2/<path> '<json_body>'
```

---

## Common gotchas

- API key required on every request — set `OPENSEA_API_KEY` before running CLI commands.
- Slug vs. address: collections are by slug (e.g., `boredapeyachtclub`), NFTs by `(chain, contract, tokenId)`.
- `order_hash` from listings / offers is needed for fulfillment — don't lose it between calls.
- Privy creds are optional but required for end-to-end write flows that sign through Privy. Otherwise the skill returns calldata and the app handles signing.
- Real-time event streaming needs `websocat` installed; check `which websocat` first or fall back to polling.
- Some endpoints rate-limit hard — paginate with `--limit` and back off on 429.
