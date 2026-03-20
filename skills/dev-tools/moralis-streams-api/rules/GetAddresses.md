# Get addresses by stream

Get all addresses associated with a specific stream.

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm/:id/address`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| id | string | Yes | the id of the stream to get the addresses from | - |

## Query Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| limit | number | Yes | Limit response results max value 100 | \`100\` |
| cursor | string | No | Cursor for fetching next page | - |

## Cursor/Pagination

- **limit**: Limit response results max value 100
- **cursor**: Cursor for fetching next page

The response includes a **cursor** field for pagination. Use this cursor in the next request to get the next page of results.

## Response Example

Status: 200

Ok

```json
{
  "result": [
    {
      "address": "address_example"
    }
  ],
  "cursor": "cursor_example",
  "total": 0
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/streams/evm/:id/address?limit=100" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
