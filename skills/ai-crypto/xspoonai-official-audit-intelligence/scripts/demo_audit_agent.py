#!/usr/bin/env python3
"""Minimal SpoonReactSkill demo runner for audit-intelligence.

Use this script to record a local demo video that shows:
1) agent configuration
2) skill activation
3) prompt execution
4) final output
"""

from __future__ import annotations

import argparse
import asyncio
import os
from datetime import datetime

from spoon_ai.agents import SpoonReactSkill
from spoon_ai.chat import ChatBot

DEFAULT_PROMPT = (
    "Analyze this snippet for security risks and provide evidence-backed remediation: "
    "function withdraw(uint256 amount) external { "
    "(bool ok,) = msg.sender.call{value: amount}(\"\"); "
    "balances[msg.sender] -= amount; require(ok, 'failed'); }"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run audit-intelligence demo agent")
    parser.add_argument(
        "--skill-path",
        default="./web3-data-intelligence",
        help="Path containing the audit-intelligence skill",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Prompt sent to the agent",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="Model name for ChatBot",
    )
    parser.add_argument(
        "--provider",
        default=os.getenv("LLM_PROVIDER", "openai"),
        help="LLM provider for ChatBot",
    )
    return parser


async def run_demo(skill_path: str, prompt: str, provider: str, model: str) -> None:
    print("=" * 72)
    print("AUDIT-INTELLIGENCE DEMO")
    print("=" * 72)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Skill path: {skill_path}")
    print(f"Provider/Model: {provider}/{model}")
    print()

    agent = SpoonReactSkill(
        name="audit_demo_agent",
        description="Demo agent for audit-intelligence skill",
        skill_paths=[skill_path],
        scripts_enabled=True,
        auto_trigger_skills=False,
        llm=ChatBot(llm_provider=provider, model_name=model),
        max_steps=8,
    )

    print("[Step 1] Initializing agent...")
    await agent.initialize()

    print("[Step 2] Activating skill: audit-intelligence")
    await agent.activate_skill("audit-intelligence")

    print("[Step 3] Sending prompt:")
    print(prompt)
    print()

    print("[Step 4] Running agent...")
    result = await agent.run(prompt)

    print("\n[Final Output]")
    print("-" * 72)
    print(result)
    print("-" * 72)


async def main() -> None:
    args = build_parser().parse_args()
    await run_demo(
        skill_path=args.skill_path,
        prompt=args.prompt,
        provider=args.provider,
        model=args.model,
    )


if __name__ == "__main__":
    asyncio.run(main())
