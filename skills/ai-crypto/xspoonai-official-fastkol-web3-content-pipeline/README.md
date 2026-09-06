# FastKOL Skill for SpoonOS

## Description
FastKOL is an automated content generation agent that monitors prediction markets (Polymarket) for trending topics, generates short video scripts, and automatically uploads content to YouTube.

## Features
- **Real-time Market Data**: Fetches trending markets from Polymarket via Gamma API.
- **Automated YouTube Upload**: Seamlessly uploads video content to a YouTube channel using the YouTube Data API v3.
- **SpoonOS Compatible**: Designed to work within the SpoonOS ecosystem (Stub provided for independent testing).

## Prerequisites
1. **Python 3.10+**
2. **Polymarket Access**: (Public API, no key required for reading trending markets)
3. **YouTube Data API Credentials**:
    - Create a project in Google Cloud Console.
    - Enable **YouTube Data API v3**.
    - Create **OAuth 2.0 Client IDs** (Desktop App).
    - Download the JSON file and save it as `client_secrets.json` in this directory.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the integration test to verify the workflow:
```bash
python test_integration.py
```

## Structure
- `agent.py`: Core logic for `FastKOLAgent`.
- `tools.py`: Real implementations of `RealPolymarketTool` and `RealYouTubeTool`.
- `spoon_ai_stub.py`: Stub classes for SpoonOS interfaces.
- `requirements.txt`: Python dependencies.

## Inputs
- `video_path`: Path to the video file to upload (e.g., "my_video.mp4").

## Outputs
- `market_data`: List of trending markets found.
- `script`: Generated script and metadata.
- `publish`: Result of the YouTube upload (Video ID, URL).
