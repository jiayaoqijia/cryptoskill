#!/usr/bin/env python3
"""a2a-discovery — ERC-8004 agent registry monitor.

Polls the ERC-8004 agent registry for new registrations and alerts on
interesting ones:
- Agents with x402_supported=true (potential x402 gateway customers)
- Agents with descriptions (named agents, not just "Agent #xxxxx")
- Agents on Base chain (our primary deployment)
- Agents with high scores or feedback

Part of the GenTech Agent Kit `a2a/` module (discover -> talk -> self-audit).

Usage:
  python3 discovery.py                # normal run
  python3 discovery.py --init         # initialize state file without alerting
  python3 discovery.py --dry-run      # fetch + print, no state changes

Configuration (env vars, all optional):
  A2A_DISCOVERY_API_URL   registry API (default: https://8004scan.io/api/v1/agents)
  A2A_DISCOVERY_STATE     state file path   (default: ./a2a-discovery-state.json)
  A2A_DISCOVERY_LOG       alert log path    (default: ./a2a-discovery-log.md)
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = os.environ.get("A2A_DISCOVERY_API_URL", "https://8004scan.io/api/v1/agents")
STATE_FILE = os.environ.get("A2A_DISCOVERY_STATE", "a2a-discovery-state.json")
OUTPUT_FILE = os.environ.get("A2A_DISCOVERY_LOG", "a2a-discovery-log.md")


def fetch_agents(limit=50, offset=0):
    url = f"{API_URL}?limit={limit}&offset={offset}"
    req = Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; GenTechLabs/1.0; +https://gentechlabs.net)"
    })
    try:
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (URLError, HTTPError) as e:
        print(f"ERROR: fetch failed: {e}", file=sys.stderr)
        return None


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_seen_id": None, "last_seen_time": None, "total_agents": 0, "runs": 0}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE) or ".", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def log_alert(msg):
    os.makedirs(os.path.dirname(OUTPUT_FILE) or ".", exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"| {timestamp} | {msg} |\n"
    with open(OUTPUT_FILE, "a") as f:
        f.write(line)
    print(f"ALERT: {msg}")


def is_interesting(agent):
    """Check if an agent is worth alerting on."""
    name = agent.get("name", "")
    desc = agent.get("description") or ""
    x402 = agent.get("x402_supported", False)
    chain = agent.get("chain_id")
    score = agent.get("total_score", 0)
    feedbacks = agent.get("total_feedbacks", 0)

    # Always interesting if x402 supported
    if x402:
        return True

    # Interesting if it has a real name (not "Agent #xxxxx")
    if name and not name.startswith("Agent #"):
        return True

    # Interesting if it has a description
    if desc and len(desc) > 10:
        return True

    # Interesting if on Base (chain 8453) with any activity
    if chain == 8453 and (score > 0 or feedbacks > 0):
        return True

    return False


# Chain IDs that are testnets or staging — never leads
TESTNET_CHAINS = {84532, 11155111, 1187947933, 97, 5, 11155111}
# Repeated production spam families (same description, different owners)
NOISE_NAMES = {"Ave.ai Trading Agent"}


def triage(agents):
    """Filter raw alerts down to real leads.

    The raw registry is ~60% noise: duplicate Ave.ai Trading Agent entries,
    smoke-test agents, and testnet chains. Triage drops those and scores the
    rest so outreach targets the actual top leads.
    """
    leads = []
    for a in agents:
        name = a.get("name", "")
        chain = a.get("chain_id")
        desc = a.get("description") or ""
        if name in NOISE_NAMES:
            continue
        if chain in TESTNET_CHAINS:
            continue
        if name.startswith("smoke-") or name.startswith("Agent #"):
            continue
        score = 0
        if a.get("x402_supported"):
            score += 3
        if len(desc) > 10:
            score += 2
        if chain == 8453:  # Base = our primary deployment chain
            score += 1
        if a.get("total_score", 0) >= 10:
            score += 2
        leads.append((score, a))
    leads.sort(key=lambda x: -x[0])
    return [a for _, a in leads]


def format_agent(agent):
    name = agent.get("name", "?")
    desc = agent.get("description") or ""
    chain = agent.get("chain_id", "?")
    x402 = "✅" if agent.get("x402_supported") else "❌"
    score = agent.get("total_score", 0)
    owner = (agent.get("owner_address") or "?")[:12] + "..."

    chain_names = {1: "Ethereum", 8453: "Base", 196: "X Layer", 97: "BNB Testnet", 1776: "Injective"}
    chain_name = chain_names.get(chain, f"Chain {chain}")

    parts = [f"**{name}**", f"Chain: {chain_name}", f"x402: {x402}", f"Score: {score}", f"Owner: {owner}"]
    if desc:
        parts.append(f"_{desc[:80]}_")

    return " · ".join(parts)


def main():
    init_mode = "--init" in sys.argv
    dry_run = "--dry-run" in sys.argv

    state = load_state()
    state["runs"] += 1

    # Fetch first page (newest agents first)
    data = fetch_agents(limit=50, offset=0)
    if not data:
        print("ERROR: could not fetch agent data")
        sys.exit(1)

    items = data.get("items", [])
    total = data.get("total", 0)
    state["total_agents"] = total

    print(f"Total registered agents: {total}")
    print(f"Fetched {len(items)} recent registrations")

    if dry_run:
        for agent in items[:10]:
            print(f"  • {format_agent(agent)}")
        return

    if init_mode:
        # Just record the latest agent ID without alerting
        if items:
            state["last_seen_id"] = items[0].get("id")
            state["last_seen_time"] = items[0].get("created_at")
        save_state(state)
        print(f"Initialized. Last seen: {state['last_seen_id']}")
        return

    # Find new agents since last run
    last_id = state.get("last_seen_id")
    new_agents = []

    if last_id:
        for agent in items:
            if agent.get("id") == last_id:
                break
            new_agents.append(agent)
    else:
        # First run — just record state
        if items:
            state["last_seen_id"] = items[0].get("id")
            state["last_seen_time"] = items[0].get("created_at")
        save_state(state)
        print(f"First run — recorded latest agent: {items[0].get('name', '?') if items else 'none'}")
        return

    if not new_agents:
        print("No new agents since last check")
        save_state(state)
        return

    print(f"\nNew agents since last check: {len(new_agents)}")

    # Update state
    state["last_seen_id"] = items[0].get("id")
    state["last_seen_time"] = items[0].get("created_at")
    save_state(state)

    # Log interesting ones
    interesting = [a for a in new_agents if is_interesting(a)]
    leads = triage(interesting)

    if leads:
        print(f"\n=== Top Leads ({len(leads)}) ===")
        for agent in leads:
            line = format_agent(agent)
            print(f"  • {line}")
            log_alert(line)
    else:
        print("No interesting agents in this batch")


if __name__ == "__main__":
    main()
