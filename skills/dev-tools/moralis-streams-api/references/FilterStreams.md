# Filter Streams

Filter the data received from webhooks to reduce noise and focus on relevant events.

## Overview

Streams can be configured with filters to control which events trigger webhooks. Filters help:
- Reduce webhook volume and costs
- Focus on specific value ranges or conditions
- Exclude spam transactions
- Monitor specific contract behaviors

## Spam Filtering

### Filter Possible Spam Addresses

Exclude transactions involving contracts labeled as spam, phishing, or suspicious:

```json
{
  "filterPossibleSpamAddresses": true
}
```

**Default:** `false`

**Behavior:** When enabled, any transactions (native, internal, contract events) involving contracts with `possibleSpam = true` are excluded from webhooks and do not consume usage.

**UI Configuration:** Check "Exclude Possible Spam Events" in Step 1: Events.

## Filter Operators

| Operator | Function | Requirements | Example |
|----------|----------|--------------|---------|
| `or` | Either condition matches | Need at least 2 filters | `{"or": [{filter1}, {filter2}]}` |
| `and` | All conditions must match | Need at least 2 filters | `{"and": [{filter1}, {filter2}]}` |
| `eq` | Equal to | - | `{"eq": ["value", "1000"]}` |
| `ne` | Not equal to | - | `{"ne": ["address", "0x...325"]}` |
| `lt` | Less than | Value must be a number | `{"lt": ["amount", "50"]}` |
| `gt` | Greater than | Value must be a number | `{"gt": ["price", "500000"]}` |
| `lte` | Less than or equal | Value must be a number | `{"lte": ["value", "100"]}` |
| `gte` | Greater than or equal | Value must be a number | `{"gte": ["value", "100"]}` |
| `in` | Value in array | Must provide an array | `{"in": ["city", ["berlin", "paris"]]}` |
| `nin` | Value not in array | Must provide an array | `{"nin": ["name", ["bob", "alice"]]}` |

## Special Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `moralis_streams_contract_address` | Current contract address (lowercase) | `{"eq": ["moralis_streams_contract_address", "0x0000...000"]}` |
| `moralis_streams_chain_id` | Current chain ID | `{"eq": ["moralis_streams_chain_id", "0x1"]}` |
| `moralis_streams_possibleSpam` | Filter on possibleSpam flag | `{"eq": ["moralis_streams_possibleSpam", "false"]}` |

## Examples

### Monitor USDC Transfers Above 5000

```javascript
{
  "and": [
    {"gt": ["value", "5000000000"]},
    {"lt": ["value", "50000000000"]}
  ]
}
```

Note: USDC uses 6 decimals, so 5000 USDC = `5000000000`.

### Monitor Mint/Burn Events

A zero address in `from` = Mint, in `to` = Burn:

```javascript
{
  "or": [
    {
      "and": [
        {"eq": ["from", "0x0000000000000000000000000000000000000000"]},
        {"gte": ["value", "10000000000"]}
      ]
    },
    {
      "and": [
        {"eq": ["to", "0x0000000000000000000000000000000000000000"]},
        {"gte": ["value", "10000000000"]}
      ]
    }
  ]
}
```

### Different Filters for Different Contracts

```javascript
const filter = {
  or: [
    {
      and: [
        {eq: ["moralis_streams_contract_address", "0x1"]},
        {gte: ["value", 1000000000]}, // USDT (6 decimals)
      ],
    },
    {
      and: [
        {eq: ["moralis_streams_contract_address", "0x2"]},
        {gte: ["value", 1000000000000000000000]}, // BUSD (18 decimals)
      ],
    },
  ],
};
```

## Important Notes

- **ABI Required:** You must add a valid ABI for the event you want to filter
- **Lowercase Addresses:** Contract addresses in filters must be lowercase
- **Decimal Awareness:** Token amounts require accounting for contract decimals
- **UI Configuration:** Filters can be added via Admin Panel with visual builder

## UI Configuration Steps

1. Go to Streams page and add contract address (e.g., USDC)
2. Add the event ABI and select topic
3. Click "Select topic to filter"
4. Click "Choose variable" to select field
5. Select operator and enter value
6. Click "Add filter" for additional conditions
7. Click "Update" to apply

## References

- [Filter Streams Documentation](https://docs.moralis.com/streams-api/evm/streams-configuration/filter-streams)
- [CreateStream](./CreateStream.md) - For creating streams with filters
- [UpdateStream](./UpdateStream.md) - For updating existing stream filters
