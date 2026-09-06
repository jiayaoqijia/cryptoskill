# skill-coverage-map (Track: platform-challenge)

Map skill coverage across tracks and identify category gaps

## Overview

This skill analyzes the skills repository and maps coverage of skills across different categories within each track. It identifies where coverage is complete and highlights gaps that need to be addressed with new skill implementations.

## Features

- **Track Analysis**: Analyze coverage for all tracks or a specific track (ai-productivity, enterprise-skills, platform-challenge, web3-core-operations, web3-data-intelligence)
- **Category Mapping**: Map all skills to their functional categories
- **Coverage Metrics**: Calculate coverage percentage for each track (0-100%)
- **Gap Identification**: Identify categories without any skill implementations
- **Recommendations**: Generate actionable recommendations for closing coverage gaps
- **Detailed Breakdown**: View which skills belong to each category

## Usage

Analyze skills coverage across all tracks or a specific track:

```bash
# Analyze all tracks
python3 scripts/main.py --demo

# Analyze specific track
python3 scripts/main.py --track web3-core-operations

# Custom analysis with parameters
python3 scripts/main.py --params '{"skills": [...], "categories": [...]}'
```

## Use Cases

- Identify missing skill implementations for a track
- Plan new skill development based on coverage gaps
- Understand skill distribution across categories
- Generate reports for skill portfolio planning
- Validate complete coverage of functional areas

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| track | string | No | Specific track to analyze (ai-productivity, enterprise-skills, platform-challenge, web3-core-operations, web3-data-intelligence) |
| skills | array | No | List of skill objects with name and categories fields |
| categories | array | No | List of category names to analyze |

## Example Output

```json
{
  "ok": true,
  "data": {
    "overall_coverage_percentage": 100.0,
    "tracks_analyzed": 5,
    "total_categories": 50,
    "total_skills": 50,
    "coverage_by_track": {
      "ai-productivity": {
        "coverage_percentage": 100.0,
        "total_skills": 10,
        "gaps": [],
        "detail": {
          "API": ["api-webhook-signer"],
          "Database": ["db-sql-runner"]
        }
      }
    },
    "status": "excellent"
  }
}
```
