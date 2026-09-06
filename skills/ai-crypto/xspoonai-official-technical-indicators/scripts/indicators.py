#!/usr/bin/env python3
"""
Technical Indicators - Trading math for agents.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import json
import logging
from typing import List, Dict, Any

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

class TechnicalIndicatorsTool(BaseTool):
    name: str = "calc_indicators"
    description: str = "Calculates RSI and SMA from a list of prices."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "prices": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of prices (float), ordered ascending by time"
            },
            "period": {
                "type": "integer",
                "description": "Lookback period (default: 14)",
                "default": 14
            }
        },
        "required": ["prices"]
    })

    async def execute(self, prices: List[float], period: int = 14) -> str:
        """
        Calculates indicators.
        """
        if len(prices) < period:
            return f"Error: Need at least {period} price points, got {len(prices)}."

        # SMA
        sma = sum(prices[-period:]) / period
        
        # RSI
        # 1. Calculate changes
        deltas = []
        for i in range(1, len(prices)):
            deltas.append(prices[i] - prices[i-1])
            
        # We need at least 'period' deltas.
        if len(deltas) < period:
             # Just fallback to simple calculation on what we have
             calc_period = len(deltas)
        else:
            calc_period = period

        # Use the last 'calc_period' deltas for simple RSI
        # (Standard RSI uses smoothing, we will use simple average needed for 1-shot tool)
        relevant_deltas = deltas[-calc_period:]
        
        gains = [d for d in relevant_deltas if d > 0]
        losses = [abs(d) for d in relevant_deltas if d < 0]
        
        avg_gain = sum(gains) / calc_period if gains else 0
        avg_loss = sum(losses) / calc_period if losses else 0
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
        # Signal
        signal = "HOLD"
        current_price = prices[-1]
        
        if rsi > 70:
            signal = "SELL (Overbought)"
        elif rsi < 30:
            signal = "BUY (Oversold)"
        elif current_price > sma * 1.05 and rsi > 50:
            signal = "BUY (Trend Following)"

        result = {
            "last_price": current_price,
            "period": period,
            "sma": round(sma, 4),
            "rsi": round(rsi, 2),
            "signal": signal,
            "data_points": len(prices)
        }
        
        return json.dumps(result, indent=2)

if __name__ == "__main__":
    import asyncio
    async def main():
        tool = TechnicalIndicatorsTool()
        # Test data
        prices = [100, 102, 101, 103, 105, 106, 110, 115, 120, 118, 116, 115, 114, 113, 112]
        print("Calculating TA...")
        res = await tool.execute(prices=prices, period=10)
        print(res)
    asyncio.run(main())
