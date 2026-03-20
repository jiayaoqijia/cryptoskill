# Square Post Skill

Post content to Binance Square.

## Features

- Post pure text content to Binance Square
- Auto-optimize content
- Auto-manage API Key

## Usage

### Examples

```
post to square: BTC is pumping, feeling bullish
```

```
square post: Market looking strong today, BTC breaking out
```

## Posting Flow

1. **Trigger Skill** - Use the trigger phrases above
2. **Content Optimization** - Agent auto-optimizes content
3. **Choose Version** - Select optimized version or post original text
4. **Post Success** - Returns post URL

### Interaction Example

```
User: post to square: btc pumping feels like bull market

Agent: Optimized content:
       BTC surging, bull market signals are strong!

       Choose:
       1. Use optimized version
       2. Use original text

User: 1

Agent: Post successful!
       Post URL: https://www.binance.com/square/post/298177291743282
```

## First Time Setup

On first use, Claude will prompt you for API Key:

1. Get your `X-Square-OpenAPI-Key`
2. Provide it to Claude
3. Key will be stored securely for future use

> ⚠️ **Security Reminder**: When creating a Square-OpenAPI-Key, please minimize its permissions. Avoid granting highly sensitive permissions such as withdrawal or trading privileges.

## Common Errors

| Code | Description |
|------|-------------|
| 000000 | Success |
| 10004 | Network error. Please try again |
| 10005 | Only allowed for users who have completed identity verification |
| 10007 | Feature unavailable |
| 20002 | Detected sensitive words |
| 20013 | Content length is limited |
| 20020 | Publishing empty content is not supported |
| 20022 | Detected sensitive words (with risk segments) |
| 20041 | Potential security risk with the URL |
| 30004 | User not found |
| 30008 | Banned for violating platform guidelines |
| 220003 | API Key not found |
| 220004 | API Key expired |
| 220009 | Daily post limit exceeded for OpenAPI |
| 220010 | Unsupported content type |
| 220011 | Content body must not be empty |
| 2000001 | Account permanently blocked from posting |
| 2000002 | Device permanently blocked from posting |

## Notes

- Only pure text posts are supported currently
- Daily post limit applies
