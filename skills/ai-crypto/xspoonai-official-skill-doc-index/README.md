# skill-doc-index (Track: platform-challenge)

Build searchable documentation index with full-text search capabilities

## Overview

This skill builds a comprehensive searchable index of all skills in the repository with support for full-text search, keyword matching, and relevance-ranked results. It enables efficient skill discovery and documentation navigation.

## Features

- **Documentation Indexing**: Index all 50 skills with titles, descriptions, keywords, and use cases
- **Full-Text Search**: Search across skill names, titles, descriptions, keywords, and use cases
- **Relevance Ranking**: Rank results by relevance score with detailed match type information
- **Keyword Analysis**: Extract and track keyword frequency across all skills
- **Track Distribution**: View skill distribution across 5 tracks (ai-productivity, enterprise-skills, platform-challenge, web3-core-operations, web3-data-intelligence)
- **Semantic Search**: Support semantic queries with multi-word search support
- **Search Statistics**: Return search time and result counts

## Usage

Search the documentation index and retrieve relevant skills:

```bash
# Demo mode with sample searches
python3 scripts/main.py --demo

# Search for specific skills
python3 scripts/main.py --search "security"

# Custom search with parameters
python3 scripts/main.py --params '{"action": "search", "query": "NFT", "limit": 10}'
```

## Use Cases

- Discover skills by keywords or functionality
- Find skills relevant to specific use cases
- Navigate documentation by track or category
- Generate skill recommendations based on queries
- Build knowledge base with semantic search

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | No | Action to perform: "search" or "index" (default: "search") |
| query | string | No | Search query for skill discovery |
| limit | number | No | Maximum results to return (default: 10) |

## Example Output

The skill indexes all 50 skills across 5 tracks with 169 unique keywords. Sample search for "security" returns 2 results with relevance scores and match types showing which fields matched the query.

Result fields:
- **relevance_score**: Higher scores indicate better relevance matches (100+ for exact/partial name matches, 20-30 for keyword/title matches)
- **match_types**: Array indicating what matched (name_exact, name_partial, title, keyword: X, use_case: X, description:word)
- **track_distribution**: Skills available per track with counts
- **top_keywords**: Most frequently occurring keywords across all skills and use cases
