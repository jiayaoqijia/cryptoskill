#!/usr/bin/env python3
"""
Yield Calculator - Investment projection tool.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import json
import math
from typing import Dict, Any

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

class YieldProjectorTool(BaseTool):
    name: str = "calc_yield"
    description: str = "Forecasting tool for investment returns."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Initial investment amount"
            },
            "apr_percent": {
                "type": "number",
                "description": "Annual Percentage Rate (e.g. 5.0)"
            },
            "days": {
                "type": "integer",
                "description": "Duration in days (default: 365)",
                "default": 365
            },
            "compounds_per_year": {
                "type": "integer", 
                "description": "Frequency (365=Daily, 0=Continuous)",
                "default": 365
            }
        },
        "required": ["principal", "apr_percent"]
    })

    async def execute(self, principal: float, apr_percent: float, days: int = 365, compounds_per_year: int = 365) -> str:
        """
        Calculates future value.
        """
        r = apr_percent / 100.0
        t = days / 365.0
        
        if compounds_per_year == 0:
            # Continuous: A = Pe^(rt)
            final_amount = principal * math.exp(r * t)
            apy = (math.exp(r) - 1) * 100
        elif compounds_per_year == 1 and days <= 365:
            # Simple Interest assumption if frequency is 1 per year? 
            # Or just standard formula A = P(1 + r/n)^(nt)
            n = compounds_per_year
            final_amount = principal * (1 + r/n)**(n * t)
            apy = ((1 + r/n)**n - 1) * 100
        else:
            # Standard Compound
            n = compounds_per_year
            # A = P(1 + r/n)^(nt)
            final_amount = principal * (1 + r/n)**(n * t)
            apy = ((1 + r/n)**n - 1) * 100
            
        profit = final_amount - principal
        
        result = {
            "input": {
                "principal": principal,
                "apr": f"{apr_percent}%",
                "duration_days": days,
                "compounding": "Continuous" if compounds_per_year == 0 else f"{compounds_per_year} times/year"
            },
            "projection": {
                "apy_effective": f"{round(apy, 3)}%",
                "final_balance": round(final_amount, 2),
                "net_profit": round(profit, 2),
                "roi_percent": round((profit / principal)*100, 2)
            }
        }
        
        return json.dumps(result, indent=2)

if __name__ == "__main__":
    import asyncio
    async def main():
        tool = YieldProjectorTool()
        print("Yield Projection...")
        res = await tool.execute(principal=1000, apr_percent=10, days=365, compounds_per_year=365)
        print(res)
    asyncio.run(main())
