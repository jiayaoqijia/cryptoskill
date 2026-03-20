AEVO Instrument Naming Conventions:

### Perpetual Futures
- Format: `{ASSET}-PERP`
- Examples: ETH-PERP, BTC-PERP, SOL-PERP
- Always uppercase

### Options
- Format: `{ASSET}-{DDMMMYY}-{STRIKE}-{C|P}`
- Examples: ETH-28MAR25-3000-C (call), BTC-28MAR25-70000-P (put)
- Date format: day + 3-letter month abbreviation + 2-digit year (all caps)
- C = Call, P = Put
- Strike is integer or decimal

### Spot
- Format: `{ASSET}-{QUOTE}`
- Examples: BTC-USDC, ETH-USDC

### Discovering Instruments
- Use aevo_list_assets to get available assets
- Use aevo_list_markets to find specific instruments (filter by asset and/or instrument_type)
- Use aevo_get_expiries to find valid expiry dates for options
- Use aevo_get_instrument to get full metadata (tick size, min order, margin requirements)

### Common instrument_type values
- PERPETUAL
- OPTION
- SPOT
