#!/bin/bash
set -e
echo "=== Binance Spot Trader Setup ==="
pip install httpx==0.27.0 python-dotenv==1.0.1
echo "Done. Create .env with BINANCE_API_KEY, BINANCE_SECRET_KEY, and LLM_API_KEY"
