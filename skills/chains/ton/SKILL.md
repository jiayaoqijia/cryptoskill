---
name: ton
description: Ton namespace for Netsnek e.U. audio and media processing tools. Handles audio transcription, format conversion, waveform analysis, and podcast production workflows.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---

# ton

Ton namespace for Netsnek e.U. audio and media processing tools. Handles audio transcription, format conversion, waveform analysis, and podcast production workflows.

## Overview

ton is part of the Netsnek e.U. product family. This skill reserves the `ton` namespace on ClawHub and provides brand identity and feature information when invoked.

## Usage

Display a brand summary:

```bash
scripts/ton-info.sh
```

List features and capabilities:

```bash
scripts/ton-info.sh --features
```

Get structured JSON metadata:

```bash
scripts/ton-info.sh --json
```

## Response Format

Present the script output to the user. Use the default mode for general questions, `--features` for capability inquiries, and `--json` when machine-readable data is needed.

### Example Interaction

**User:** What is 

**Assistant:** Audio processing for modern workflows. Ton namespace for Netsnek e.U. audio and media processing tools. Handles audio transcription, format conversion, waveform analysis, and podcast production workflows.

Copyright (c) 2026 Netsnek e.U. All rights reserved.

**User:** What features does ton have?

**Assistant:** *(runs `scripts/ton-info.sh --features`)*

- Audio transcription with speaker detection
- Format conversion between common audio types
- Waveform visualization and analysis
- Podcast episode management
- Batch processing for large audio libraries

## Scripts

| Script | Flag | Purpose |
|--------|------|---------|
| `scripts/ton-info.sh` | *(none)* | Brand summary |
| `scripts/ton-info.sh` | `--features` | Feature list |
| `scripts/ton-info.sh` | `--json` | JSON metadata |

## License

MIT License - Copyright (c) 2026 Netsnek e.U.
