# Host Sizing

Use this before bootstrap or install steps when the agent needs to recommend server specs or validate whether a host is a reasonable fit.

## Recommended Baseline For Ethereum

- Storage: `2-4+ TB` SSD or NVMe
- Memory: `16-64+ GB` RAM
- CPU: `4-8+` cores
- OS: Ubuntu `20+`

These are the repo's current recommended specs for an Ethereum node host.

## Guidance

- Prefer bare metal VPS or local bare metal when possible.
- Cloud instances may install successfully but still struggle to finish syncing.
- If the host is below the baseline, warn clearly before install instead of silently proceeding.
- Ask whether the goal is:
  - production validator
  - RPC node
  - temporary test host
- For temporary test hosts, smaller boxes may be acceptable for limited validation, but they should not be presented as a production recommendation.

## Agent Rules

- State the baseline explicitly before recommending a host.
- If disk size is the bottleneck, treat that as the highest-priority blocker.
- If the user asks for the cheapest workable option, distinguish between test-only and production-capable hosts.
- If the request is chain-specific and the repo docs do not define a better baseline, fall back to the Ethereum baseline and say it is a conservative default.
