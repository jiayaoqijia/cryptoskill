#!/usr/bin/env python3
"""Minimal agent demo for database-migration-assistant.

Author: Apple
Version: 1.0.0
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from spoon_ai.agents import SpoonReactSkill


async def main() -> None:
    prompt_path = Path(__file__).parent / "demo_prompt.txt"
    prompt = prompt_path.read_text(encoding="utf-8").strip()

    agent = SpoonReactSkill(
        name="db_migration_agent",
        skill_paths=["./ai-productivity"],
        scripts_enabled=True,
    )

    result = await agent.run(prompt)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
