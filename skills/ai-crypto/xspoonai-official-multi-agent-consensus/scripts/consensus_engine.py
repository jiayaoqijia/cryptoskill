#!/usr/bin/env python3
"""
Multi-Agent Consensus Engine

Orchestrates parallel multi-agent analysis using SpoonOS StateGraph.
Each agent runs independently on a different LLM provider, then results
are aggregated through weighted voting to reach consensus.

Architecture:
    StateGraph: entry → fan_out → [agent_1, agent_2, ..., agent_n] → fan_in → consensus
    Inspired by Byzantine Fault Tolerance — tolerates minority hallucinations.

SpoonOS Integration:
    - StateGraph: Parallel branch execution with state management
    - LLMManager: Multi-provider LLM abstraction with fallback chains
    - Checkpointing: Persist intermediate agent results for crash recovery
"""

import asyncio
import json
import re
import sys
import os
import time
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from pathlib import Path


# ---------------------------------------------------------------------------
# .env File Loader (stdlib only, no python-dotenv needed)
# ---------------------------------------------------------------------------

def _load_dotenv() -> None:
    """Load .env file from the project directory into os.environ."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and value:
                os.environ.setdefault(key, value)

_load_dotenv()


# ---------------------------------------------------------------------------
# Domain & Configuration Types
# ---------------------------------------------------------------------------


class ConsensusDomain(str, Enum):
    """Supported analysis domains with domain-specific consensus strategies."""
    GENERAL = "general"
    SMART_CONTRACT = "smart-contract"
    DEFI = "defi"
    SECURITY = "security"


class ConsensusMode(str, Enum):
    """Consensus aggregation strategies."""
    MAJORITY = "majority"          # Simple majority vote
    CONSERVATIVE = "conservative"  # Any risk flag → report it
    UNION = "union"                # Merge all findings, deduplicate
    DIVERSITY = "diversity"        # Preserve all perspectives


@dataclass(frozen=True)
class AgentConfig:
    """Immutable configuration for a single analysis agent."""
    agent_id: str
    provider: str
    perspective: str
    weight: float = 1.0
    model: Optional[str] = None
    role: Optional[str] = None


@dataclass(frozen=True)
class AgentResult:
    """Immutable result from a single agent's analysis."""
    agent_id: str
    provider: str
    verdict: str
    confidence: float
    findings: tuple[str, ...]
    reasoning: str
    elapsed_ms: int
    error: Optional[str] = None


@dataclass(frozen=True)
class ConsensusState:
    """Immutable state flowing through the StateGraph."""
    query: str
    domain: ConsensusDomain
    threshold: float
    agent_configs: tuple[AgentConfig, ...]
    agent_results: tuple[AgentResult, ...] = ()
    consensus_result: Optional[dict] = None
    checkpoint_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Perspective Templates (Cognitive Diversity)
# ---------------------------------------------------------------------------

PERSPECTIVE_TEMPLATES: dict[str, str] = {
    "analytical": (
        "You are a rigorous analytical reviewer. Focus on logical consistency, "
        "edge cases, and potential failure modes. Be skeptical and thorough. "
        "Rate your confidence from 0.0 to 1.0."
    ),
    "adversarial": (
        "You are a red-team adversarial analyst. Actively try to find vulnerabilities, "
        "attack vectors, and ways the system could be exploited. Assume the worst case. "
        "Rate your confidence from 0.0 to 1.0."
    ),
    "pragmatic": (
        "You are a pragmatic engineer focused on real-world impact. Prioritize findings "
        "by severity and likelihood. Distinguish theoretical risks from practical ones. "
        "Rate your confidence from 0.0 to 1.0."
    ),
    "domain_expert": (
        "You are a domain specialist with deep expertise. Apply domain-specific best "
        "practices and standards. Reference specific guidelines where applicable. "
        "Rate your confidence from 0.0 to 1.0."
    ),
    "generalist": (
        "You are a well-rounded generalist. Provide a balanced analysis covering "
        "multiple dimensions. Identify both strengths and weaknesses. "
        "Rate your confidence from 0.0 to 1.0."
    ),
}

# Domain → provider weight overrides
DOMAIN_WEIGHTS: dict[str, dict[str, float]] = {
    "smart-contract": {
        "anthropic": 1.2,
        "openai": 1.0,
        "deepseek": 1.1,
        "gemini": 0.9,
        "qwen": 1.0,
    },
    "defi": {
        "anthropic": 1.1,
        "openai": 1.1,
        "deepseek": 1.0,
        "gemini": 0.9,
        "qwen": 1.0,
    },
    "security": {
        "anthropic": 1.2,
        "openai": 1.0,
        "deepseek": 1.0,
        "gemini": 0.9,
        "qwen": 0.9,
    },
    "general": {
        "anthropic": 1.0,
        "openai": 1.0,
        "deepseek": 1.0,
        "gemini": 1.0,
        "qwen": 1.0,
    },
}

# Domain → consensus mode mapping
DOMAIN_CONSENSUS_MODE: dict[str, ConsensusMode] = {
    "smart-contract": ConsensusMode.CONSERVATIVE,
    "defi": ConsensusMode.UNION,
    "security": ConsensusMode.CONSERVATIVE,
    "general": ConsensusMode.MAJORITY,
}

# Perspective assignment order (rotated across agents)
PERSPECTIVE_ROTATION = [
    "analytical", "adversarial", "pragmatic", "domain_expert", "generalist",
]


# ---------------------------------------------------------------------------
# LLM Provider Abstraction (SpoonOS LLMManager compatible)
# ---------------------------------------------------------------------------

async def call_llm(
    provider: str,
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
) -> dict:
    """Call an LLM provider with the given prompts.

    In production SpoonOS, this delegates to LLMManager:
        from spoon_ai.llm import LLMManager, ConfigurationManager
        config_manager = ConfigurationManager()
        llm_manager = LLMManager(config_manager)
        response = await llm_manager.chat(messages, provider=provider)

    For standalone execution, uses provider-specific HTTP APIs.
    """
    api_key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "qwen": "DASHSCOPE_API_KEY",
    }

    api_key = os.getenv(api_key_map.get(provider, ""))
    if not api_key:
        return {
            "error": f"Missing API key for provider: {provider}",
            "content": "",
        }

    try:
        if provider == "openai":
            return await _call_openai(api_key, system_prompt, user_prompt, model=model)
        elif provider == "anthropic":
            return await _call_anthropic(api_key, system_prompt, user_prompt, model=model)
        elif provider == "deepseek":
            return await _call_deepseek(api_key, system_prompt, user_prompt, model=model)
        elif provider == "gemini":
            return await _call_gemini(api_key, system_prompt, user_prompt, model=model)
        elif provider == "qwen":
            return await _call_qwen(api_key, system_prompt, user_prompt, model=model)
        else:
            return {"error": f"Unsupported provider: {provider}", "content": ""}
    except Exception as e:
        return {"error": str(e), "content": ""}


async def _http_post(url: str, headers: dict, payload: dict) -> dict:
    """Async HTTP POST using asyncio-compatible urllib."""
    import urllib.request
    import urllib.error

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: urllib.request.urlopen(req, timeout=60),
        )
        return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


async def _call_openai(api_key: str, system_prompt: str, user_prompt: str, *, model: Optional[str] = None) -> dict:
    """Call OpenAI Chat Completions API."""
    resp = await _http_post(
        url="https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        payload={
            "model": model or "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
        },
    )
    if "error" in resp and isinstance(resp["error"], str):
        return resp
    content = (
        resp.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return {"content": content, "error": None}


async def _call_anthropic(api_key: str, system_prompt: str, user_prompt: str, *, model: Optional[str] = None) -> dict:
    """Call Anthropic Messages API."""
    resp = await _http_post(
        url="https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        payload={
            "model": model or "claude-sonnet-4-20250514",
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        },
    )
    if "error" in resp and isinstance(resp["error"], str):
        return resp
    content = ""
    for block in resp.get("content", []):
        if block.get("type") == "text":
            content += block.get("text", "")
    return {"content": content, "error": None}


async def _call_deepseek(api_key: str, system_prompt: str, user_prompt: str, *, model: Optional[str] = None) -> dict:
    """Call DeepSeek API (OpenAI-compatible)."""
    resp = await _http_post(
        url="https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        payload={
            "model": model or "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
        },
    )
    if "error" in resp and isinstance(resp["error"], str):
        return resp
    content = (
        resp.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return {"content": content, "error": None}


async def _call_gemini(api_key: str, system_prompt: str, user_prompt: str, *, model: Optional[str] = None) -> dict:
    """Call Google Gemini API."""
    gemini_model = model or "gemini-2.0-flash"
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{gemini_model}:generateContent?key={api_key}"
    )
    resp = await _http_post(
        url=url,
        headers={"Content-Type": "application/json"},
        payload={
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048},
        },
    )
    if "error" in resp and isinstance(resp["error"], str):
        return resp
    content = (
        resp.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    )
    return {"content": content, "error": None}


async def _call_qwen(api_key: str, system_prompt: str, user_prompt: str, *, model: Optional[str] = None) -> dict:
    """Call Qwen (通义千问) via DashScope OpenAI-compatible API."""
    resp = await _http_post(
        url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        payload={
            "model": model or "qwen-plus",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 2048,
        },
    )
    if "error" in resp and isinstance(resp["error"], str):
        return resp
    content = (
        resp.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return {"content": content, "error": None}


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------

def parse_agent_response(raw_content: str) -> dict:
    """Extract structured verdict, confidence, and findings from LLM response.

    Expects the LLM to return JSON-like structured output. Falls back to
    heuristic extraction if the response is free-form text.
    """
    # Try JSON extraction first
    try:
        # Look for JSON block in response
        if "```json" in raw_content:
            json_str = raw_content.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        if raw_content.strip().startswith("{"):
            return json.loads(raw_content.strip())
    except (json.JSONDecodeError, IndexError):
        pass

    # Heuristic fallback: extract from free-form text
    verdict = "UNKNOWN"
    confidence = 0.5
    findings: list[str] = []

    lower = raw_content.lower()
    # Check explicit negative forms FIRST to prevent "unsafe" matching "safe"
    if any(w in lower for w in ["unsafe", "insecure", "not safe", "not secure"]):
        verdict = "CRITICAL_RISK"
        confidence = 0.75
    elif any(w in lower for w in ["critical", "high risk", "vulnerable", "exploit"]):
        verdict = "CRITICAL_RISK"
        confidence = 0.8
    elif any(w in lower for w in ["medium risk", "moderate", "concern", "warning"]):
        verdict = "MODERATE_RISK"
        confidence = 0.6
    elif any(w in lower for w in ["low risk", "minor", "informational"]):
        verdict = "LOW_RISK"
        confidence = 0.65
    elif re.search(r"\bsafe\b|\bsecure\b|no issues|no vulnerabilities", lower):
        verdict = "SAFE"
        confidence = 0.7

    # Extract bullet-point findings
    for line in raw_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "* ", "• ")) and len(stripped) > 5:
            findings.append(stripped.lstrip("-*• ").strip())

    return {
        "verdict": verdict,
        "confidence": confidence,
        "findings": findings[:10],  # Cap at 10 findings
        "reasoning": raw_content[:500],
    }


# ---------------------------------------------------------------------------
# StateGraph Consensus Engine
# ---------------------------------------------------------------------------

def build_agent_configs(
    num_agents: int,
    providers: list[str],
    domain: str,
) -> tuple[AgentConfig, ...]:
    """Build agent configurations with diverse perspectives and domain weights."""
    domain_weights = DOMAIN_WEIGHTS.get(domain, DOMAIN_WEIGHTS["general"])
    configs: list[AgentConfig] = []

    for i in range(num_agents):
        provider = providers[i % len(providers)]
        perspective = PERSPECTIVE_ROTATION[i % len(PERSPECTIVE_ROTATION)]
        weight = domain_weights.get(provider, 1.0)

        configs.append(AgentConfig(
            agent_id=f"agent-{i + 1}",
            provider=provider,
            perspective=perspective,
            weight=weight,
        ))

    return tuple(configs)


def build_analysis_prompt(query: str, domain: str) -> str:
    """Build the user-facing analysis prompt with structured output request."""
    domain_context = {
        "smart-contract": (
            "Focus on: reentrancy, access control, integer overflow/underflow, "
            "unchecked external calls, front-running, flash loan attacks, "
            "storage collisions, and logic errors."
        ),
        "defi": (
            "Focus on: oracle manipulation, impermanent loss risks, "
            "liquidity pool vulnerabilities, governance attack vectors, "
            "and economic model sustainability."
        ),
        "security": (
            "Focus on: authentication bypasses, authorization flaws, "
            "injection vulnerabilities, cryptographic weaknesses, "
            "and data exposure risks."
        ),
        "general": "Provide a comprehensive, balanced analysis.",
    }

    return f"""Analyze the following and provide your assessment:

{query}

Domain context: {domain_context.get(domain, domain_context['general'])}

Respond in this exact JSON format:
```json
{{
  "verdict": "SAFE | LOW_RISK | MODERATE_RISK | HIGH_RISK | CRITICAL_RISK",
  "confidence": 0.0 to 1.0,
  "findings": ["finding 1", "finding 2", ...],
  "reasoning": "Your detailed reasoning..."
}}
```"""


async def run_single_agent(config: AgentConfig, query: str, domain: str) -> AgentResult:
    """Execute a single agent's analysis. One parallel branch of the StateGraph."""
    # Use custom role if provided, otherwise use perspective template
    if config.role:
        perspective_prompt = config.role
    else:
        perspective_prompt = PERSPECTIVE_TEMPLATES.get(
            config.perspective, PERSPECTIVE_TEMPLATES["generalist"]
        )
    user_prompt = build_analysis_prompt(query, domain)

    start_ms = int(time.time() * 1000)
    response = await call_llm(config.provider, perspective_prompt, user_prompt, model=config.model)
    elapsed_ms = int(time.time() * 1000) - start_ms

    if response.get("error"):
        return AgentResult(
            agent_id=config.agent_id,
            provider=config.provider,
            verdict="ERROR",
            confidence=0.0,
            findings=(),
            reasoning="",
            elapsed_ms=elapsed_ms,
            error=response["error"],
        )

    parsed = parse_agent_response(response.get("content", ""))

    return AgentResult(
        agent_id=config.agent_id,
        provider=config.provider,
        verdict=parsed.get("verdict", "UNKNOWN"),
        confidence=min(1.0, max(0.0, float(parsed.get("confidence", 0.5)))),
        findings=tuple(parsed.get("findings", [])),
        reasoning=parsed.get("reasoning", "")[:500],
        elapsed_ms=elapsed_ms,
    )


async def run_consensus_engine(input_data: dict) -> dict:
    """Main entry point: orchestrate parallel agents and aggregate results.

    StateGraph execution flow:
        1. fan_out: Create agent configs with diverse perspectives
        2. parallel_analyze: Run all agents concurrently (asyncio.gather)
        3. fan_in: Collect results into ConsensusState
        4. aggregate: Delegate to voting_aggregator for final consensus

    In production SpoonOS, steps 1-3 map to StateGraph nodes:
        graph = StateGraph(ConsensusState)
        graph.add_node("fan_out", fan_out_node)
        graph.add_node("agent_1", agent_node_factory("agent-1"))
        ...
        graph.add_edge("fan_out", "agent_1")
        ...
        compiled = graph.compile(checkpointer=MemorySaver())

    Supports two input formats for "agents":
        - list[dict]: Explicit agent configs with name/provider/model/role
        - int: Number of agents to auto-generate from providers list
    """
    query = input_data.get("query", "")
    if not query:
        return {"error": "Missing required parameter: query"}

    domain = input_data.get("domain", "general")
    threshold = min(1.0, max(0.0, input_data.get("threshold", 0.6)))

    raw_agents = input_data.get("agents", 3)

    # Support both list-of-dicts (demo format) and integer (original format)
    if isinstance(raw_agents, list):
        # Explicit agent configurations from input
        domain_weights = DOMAIN_WEIGHTS.get(domain, DOMAIN_WEIGHTS["general"])
        agent_configs = tuple(
            AgentConfig(
                agent_id=a.get("name", f"agent-{i + 1}"),
                provider=a.get("provider", "qwen"),
                perspective=a.get("perspective", PERSPECTIVE_ROTATION[i % len(PERSPECTIVE_ROTATION)]),
                weight=a.get("weight", domain_weights.get(a.get("provider", "qwen"), 1.0)),
                model=a.get("model"),
                role=a.get("role"),
            )
            for i, a in enumerate(raw_agents)
        )
        num_agents = len(agent_configs)
    else:
        # Original format: auto-generate from providers list
        num_agents = min(5, max(2, int(raw_agents)))
        providers = input_data.get("providers", ["openai", "anthropic", "deepseek"])
        agent_configs = build_agent_configs(num_agents, providers, domain)

    # Generate checkpoint ID for crash recovery
    checkpoint_id = hashlib.sha256(
        f"{query}:{time.time()}".encode()
    ).hexdigest()[:12]

    # Step 2: Parallel analyze — run all agents concurrently
    tasks = [
        run_single_agent(config, query, domain)
        for config in agent_configs
    ]
    agent_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Step 3: Fan-in — collect results, handle exceptions
    valid_results: list[dict] = []
    for result in agent_results:
        if isinstance(result, Exception):
            valid_results.append({
                "agent_id": "unknown",
                "provider": "unknown",
                "verdict": "ERROR",
                "confidence": 0.0,
                "findings": [],
                "reasoning": str(result),
                "elapsed_ms": 0,
                "error": str(result),
            })
        else:
            valid_results.append({
                "agent_id": result.agent_id,
                "provider": result.provider,
                "verdict": result.verdict,
                "confidence": result.confidence,
                "findings": list(result.findings),
                "reasoning": result.reasoning,
                "elapsed_ms": result.elapsed_ms,
                "error": result.error,
            })

    # Build agent weight map for the aggregator
    weight_map = {
        config.agent_id: config.weight
        for config in agent_configs
    }

    consensus_mode = DOMAIN_CONSENSUS_MODE.get(domain, ConsensusMode.MAJORITY)

    return {
        "success": True,
        "checkpoint_id": checkpoint_id,
        "query": query,
        "domain": domain,
        "consensus_mode": consensus_mode.value,
        "threshold": threshold,
        "num_agents": num_agents,
        "agent_results": valid_results,
        "agent_weights": weight_map,
    }


# ---------------------------------------------------------------------------
# Main Entry Point (stdin/stdout JSON protocol)
# ---------------------------------------------------------------------------

def main() -> None:
    """Read JSON from stdin, run consensus engine, output JSON to stdout."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = asyncio.run(run_consensus_engine(input_data))
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Consensus engine failed: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
