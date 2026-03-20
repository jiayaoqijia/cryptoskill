# Get project settings

Get the settings for the current project based on the project api-key.

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/settings`

## Response Example

Status: 200

Ok

```json
{
  "region": "region_example",
  "secretKey": "secretKey_example"
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/settings" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
