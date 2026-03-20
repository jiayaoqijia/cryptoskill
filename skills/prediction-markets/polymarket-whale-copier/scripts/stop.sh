#!/bin/bash
# Stop the whale copier
screen -X -S whale-copier quit 2>/dev/null && echo "🛑 Whale Copier stopped" || echo "⚠️ Not running"
