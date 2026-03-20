# Send webhook based on a specific block number using stream config and addresses.

Execute.

## Method

POST

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm/:chainId/block-to-webhook/:blockNumber/:streamId`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| chainId | string | Yes | - | - |
| blockNumber | number | Yes | - | - |
| streamId | string | Yes | - | - |

## Example (curl)

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/:chainId/block-to-webhook/:blockNumber/:streamId" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
