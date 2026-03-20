# Replaces address from stream

Replaces address from a Stream.

## Method

PATCH

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm/:id/address`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| id | string | Yes | The id of the stream to replace the address from | - |

## Body

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| address | - | No | The address or a list of addresses to be replace from the Stream. | \`string\` |

## Response Example

Status: 200

Ok

```json
{
  "streamId": "streamId_example"
}
```

## Example (curl)

```bash
curl -X PATCH "https://api.moralis-streams.com/streams/evm/:id/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "address": "string"
}'
```
