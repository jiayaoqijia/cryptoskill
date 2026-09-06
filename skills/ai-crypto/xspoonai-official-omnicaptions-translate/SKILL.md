---
name: omnicaptions-translate
description: Context-aware caption translation skill for SRT/VTT/ASS with bilingual output and optional Gemini CLI fallback.
version: 1.0.0
author: ETHPanda Contributor
tags:
  - captions
  - subtitles
  - translation
  - localization
  - ai-productivity
triggers:
  - type: keyword
    keywords:
      - caption
      - subtitle
      - srt
      - vtt
      - ass
      - translate
      - localization
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(translate|localize) .*(caption|subtitle|srt|vtt|ass)"
      - "(?i)(bilingual|dual[- ]language) .*(caption|subtitle)"
    priority: 85
parameters:
  - name: input_file
    type: string
    required: true
    description: Input subtitle file path (srt/vtt/ass)
  - name: target_language
    type: string
    required: true
    description: Target language code, such as zh, ja, en, es
  - name: bilingual
    type: boolean
    required: false
    default: false
    description: Keep original line and append translated line
  - name: engine
    type: string
    required: false
    default: claude
    description: Translation engine, claude or gemini
prerequisites:
  env_vars:
    - GEMINI_API_KEY
  skills: []
composable: true
persist_state: false
---

# OmniCaptions Translate Skill

Source attribution: This submission is from ETHPanda.
Chinese attribution: this skill is from ETHPanda (来自 ETHPanda).

## Quick Start

```bash
# Claude native workflow (no API key required)
# 1) Read subtitle file
# 2) Translate with context
# 3) Save as *_Claude_<lang>.srt

# Gemini CLI workflow (optional)
omnicaptions translate input.srt -l zh --bilingual
```

## Scripts

No scripts are required for the default workflow.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | No | Optional key for Gemini CLI translation path |

## Best Practices

1. Prefer context-aware chunk translation over strict line-by-line translation.
2. Use bilingual output for QA and learning use cases.
