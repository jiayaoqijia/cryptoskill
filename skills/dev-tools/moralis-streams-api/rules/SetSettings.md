# Set project settings

Set the settings for the current project based on the project api-key.

## Method

POST

## Base URL

`https://api.moralis-streams.com`

## Path

`/settings`

## Body

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| region | string (us-east-1, us-west-2, eu-central-1, ap-southeast-1) | No | The region from where all the webhooks will be posted for this project | \`string\` |
| secretKey | string | No | The secret key to validate the webhooks | \`string\` |

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
curl -X POST "https://api.moralis-streams.com/settings" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "region": "string",
  "secretKey": "string"
}'
```
