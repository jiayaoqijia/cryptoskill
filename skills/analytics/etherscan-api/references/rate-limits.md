# Rate Limits (Etherscan V2)

Source:
- `https://docs.etherscan.io/resources/rate-limits`

Current headline limits from official docs:

| Tier | Calls / second | Daily cap |
| --- | ---: | ---: |
| Free | `5` | `100,000` |
| Standard | `10` | `200,000` |
| Advanced | `20` | `500,000` |
| Professional | `30` | `1,000,000` |
| Pro Plus | `30` | `1,500,000` |

Historical endpoints:
- Historical endpoints are capped at `2` calls/second regardless of paid tier.

Operational guidance:
- Implement global token-bucket throttling per API key.
- Add jittered exponential backoff for transient failures.
- Keep scans resumable by persisting the latest processed block/page.
- For long windows, split by block ranges and run sequentially.
