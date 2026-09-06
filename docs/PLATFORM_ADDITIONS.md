# Robinhood, Fomo, GMGN and pump.fun additions

Added 14 entries on 2026-09-06. The catalog now contains **1,773 entries**, including **139 MCP servers**, across 14 categories.

| Area | Additions | Classification |
|---|---:|---|
| Robinhood | 4 | Official hosted Trading MCP; three community integrations |
| Fomo | 1 | Community research integration by Cope Capital for fomo.family |
| GMGN | 5 | Official project skills |
| pump.fun | 4 | Official project skills |

## Added entries

- [community-robinhood](skills/analytics/community-robinhood.html)
- [fomo-research](skills/analytics/fomo-research.html)
- [robinscan](skills/analytics/robinscan.html)
- [pumpfun-official-coin-fees](skills/defi/pumpfun-official-coin-fees.html)
- [pumpfun-official-create-coin](skills/defi/pumpfun-official-create-coin.html)
- [pumpfun-official-swap](skills/defi/pumpfun-official-swap.html)
- [pumpfun-official-tokenized-agents](skills/defi/pumpfun-official-tokenized-agents.html)
- [robinhood-for-agents](skills/exchanges/robinhood-for-agents.html)
- [robinhood-trading-mcp](skills/mcp-servers/robinhood-trading-mcp.html)
- [gmgnai-official-gmgn-contract-dd](skills/trading/gmgnai-official-gmgn-contract-dd.html)
- [gmgnai-official-gmgn-cooking](skills/trading/gmgnai-official-gmgn-cooking.html)
- [gmgnai-official-gmgn-dev-score](skills/trading/gmgnai-official-gmgn-dev-score.html)
- [gmgnai-official-gmgn-holder-analysis](skills/trading/gmgnai-official-gmgn-holder-analysis.html)
- [gmgnai-official-gmgn-wallet-analysis](skills/trading/gmgnai-official-gmgn-wallet-analysis.html)

GMGN now has 13 individual upstream skills in the registry, alongside the pre-existing collection overview. Eight individual skills were already current. The older overview remains a README snapshot and was preserved because the generic SKILL.md matcher cannot uniquely map it.

The Robinhood hosted service is confirmed by its own [support documentation](https://robinhood.com/us/en/support/articles/agentic-trading-overview/). CryptoSkill authored the local connection guide; it is explicitly identified as registry-maintained. Community Robinhood clients and Robinscan are not labeled Robinhood-authored.

The new sources are recorded in `scripts/curated-sources.json` and included in recurring updates. [Targeted fetch results](targeted-sync-report.json) and [hosted MCP documentation status](hosted-mcp-status.json) are recorded separately from the earlier full-corpus refresh.

## Implementation and verification

- Imported upstream SKILL.md files, references, supporting code and available license files at pinned commits.
- Corrected the seed-phrase scanner: ordinary English prose no longer triggers the mnemonic gate. English BIP-39 validation and labelled-seed checks remain active.
- Added official Robinhood and pump.fun project cards and included all GMGN skill names in its existing card.
- Published the actual HTTP MCP endpoint in Robinhood’s card, modal and detail page.
- Rebuilt catalog metadata, scores, trust manifests, pages, sitemap and counts.
- 32 Python tests and 24 Playwright tests passed.
- Verified all 14 new trust manifests and the hashes of 104 newly imported upstream files.
- Preserved the four pre-existing QuantaBot files.

No accounts were connected, trading programs executed, or transactions placed.
