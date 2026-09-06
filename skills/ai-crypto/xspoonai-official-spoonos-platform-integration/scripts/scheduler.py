#!/usr/bin/env python3
"""Scheduled Tasks for SpoonOS Agents using APScheduler."""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager


scheduler = AsyncIOScheduler()

# Initialize agent
agent = SpoonReactMCP(
    name="scheduled_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([])
)


async def daily_market_report():
    """Generate daily market report at 9 AM."""
    result = await agent.run(
        "Generate a daily market report for top 10 cryptocurrencies"
    )
    # Send to Telegram, Discord, email, etc.
    print(f"Daily report: {result}")


async def hourly_price_check():
    """Check prices every hour."""
    result = await agent.run(
        "Check current BTC and ETH prices, alert if >5% change"
    )
    print(f"Price check: {result}")


async def weekly_portfolio_review():
    """Weekly portfolio analysis on Monday 10 AM."""
    result = await agent.run(
        "Review portfolio performance for the past week"
    )
    print(f"Weekly review: {result}")


def setup_schedules():
    """Configure scheduled tasks."""

    # Daily at 9:00 AM
    scheduler.add_job(
        daily_market_report,
        CronTrigger(hour=9, minute=0),
        id="daily_report"
    )

    # Every hour
    scheduler.add_job(
        hourly_price_check,
        CronTrigger(minute=0),
        id="hourly_check"
    )

    # Monday 10 AM
    scheduler.add_job(
        weekly_portfolio_review,
        CronTrigger(day_of_week="mon", hour=10),
        id="weekly_review"
    )


async def main():
    setup_schedules()
    scheduler.start()
    print("Scheduler started...")

    # Keep running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
