---
name: nft-tracker
description: "Track NFT collection prices, floor prices, and sales data. Supports Ethereum collections including BAYC, MAYC, CryptoPunks, and more."
homepage: https://docs.opensea.io/reference/api-overview
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["curl", "jq"] },
        "credentials":
          [
            {
              "id": "opensea-api-key",
              "name": "OpenSea API Key",
              "description": "API key from https://docs.opensea.io/reference/api-keys",
              "env": "OPENSEA_API_KEY",
            },
          ],
      },
  }
---

# NFT Price Tracker

Track NFT collection stats, floor prices, and recent sales using the OpenSea API.

## Setup

Export your OpenSea API key (free tier available):

```bash
export OPENSEA_API_KEY="your-key"
```

## Popular Collection Slugs

- `boredapeyachtclub` - Bored Ape Yacht Club (BAYC)
- `mutant-ape-yacht-club` - Mutant Ape Yacht Club (MAYC)
- `cryptopunks` - CryptoPunks
- `azuki` - Azuki
- `pudgypenguins` - Pudgy Penguins
- `doodles-official` - Doodles
- `clonex` - CloneX

## Collection Stats

Get collection floor and volume stats:

```bash
curl -s "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '{
  floor: .total.floor_price,
  volume: .total.volume,
  sales: .total.sales,
  num_owners: .total.num_owners,
  average_price: .total.average_price
}'
```

BAYC example:

```bash
curl -s "https://api.opensea.io/api/v2/collections/boredapeyachtclub/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.'
```

## Collection Metadata

```bash
curl -s "https://api.opensea.io/api/v2/collections/mutant-ape-yacht-club" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '{
  name: .name,
  description: .description,
  image_url: .image_url,
  contracts: .contracts
}'
```

## Recent Events / Sales

```bash
curl -s "https://api.opensea.io/api/v2/events/collection/boredapeyachtclub?event_type=sale&limit=10" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.asset_events[] | {
  event_type: .event_type,
  order_hash: .order_hash,
  chain: .chain
}'
```

Contract addresses:
- BAYC: `0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d`
- MAYC: `0x60e4d786628fea6478f785a6d7e704777c86a7c6`
- CryptoPunks: `0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb`

## NFT Lookup

Get details for a specific token (MAYC #1234):

```bash
curl -s "https://api.opensea.io/api/v2/chain/ethereum/contract/0x60e4d786628fea6478f785a6d7e704777c86a7c6/nfts/1234" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq '.nft | {name, image_url, owners, traits}'
```

## Price Alerts (Script Example)

Monitor floor price and alert when below threshold:

```bash
#!/bin/bash
COLLECTION="mutant-ape-yacht-club"
THRESHOLD=5  # ETH (or collection floor units)

FLOOR=$(curl -s "https://api.opensea.io/api/v2/collections/$COLLECTION/stats" \
  -H "X-API-KEY: $OPENSEA_API_KEY" | jq -r '.total.floor_price // empty')

if [ -n "$FLOOR" ] && (( $(echo "$FLOOR < $THRESHOLD" | bc -l) )); then
  echo "ALERT: $COLLECTION floor is $FLOOR (below $THRESHOLD)"
fi
```

## Tips

- OpenSea requires an API key for most endpoints — get one at https://docs.opensea.io/reference/api-keys
- Rate limits apply — cache responses when possible
- Use collection slugs for stats; use chain + contract + token id for precise NFT lookups
- The old Reservoir `api.reservoir.tools` host no longer resolves; prefer OpenSea
