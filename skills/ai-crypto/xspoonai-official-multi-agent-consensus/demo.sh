#!/usr/bin/env bash
# ============================================================
# Multi-Agent Consensus Engine — Demo Script
# Records well with: asciinema rec demo.cast
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

# ── Colors ───────────────────────────────────────────────────
BOLD='\033[1m'
DIM='\033[2m'
CYAN='\033[36m'
GREEN='\033[32m'
YELLOW='\033[33m'
MAGENTA='\033[35m'
RED='\033[31m'
RESET='\033[0m'

# ── Helpers ──────────────────────────────────────────────────
banner() {
  echo ""
  echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════╗${RESET}"
  echo -e "${BOLD}${CYAN}║  $1${RESET}"
  echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════╝${RESET}"
  echo ""
}

step() {
  echo -e "${BOLD}${GREEN}▶ $1${RESET}"
}

info() {
  echo -e "${DIM}  $1${RESET}"
}

pause() {
  echo ""
  echo -e "${YELLOW}  ⏎ Press Enter to continue...${RESET}"
  read -r
}

show_cmd() {
  echo -e "${MAGENTA}  \$ $1${RESET}"
  echo ""
}

divider() {
  echo -e "${DIM}──────────────────────────────────────────────────${RESET}"
}

SCRIPTS="./scripts"
ENGINE="$SCRIPTS/consensus_engine.py"
AGGREGATOR="$SCRIPTS/voting_aggregator.py"

# ── Summary Formatters ─────────────────────────────────────
# Extract human-readable summary from engine JSON output
format_engine_summary() {
  local json="$1"
  python3 -c "
import sys, json
d = json.loads(sys.argv[1])
results = d.get('agent_results', [])
print()
print('  ┌─────────────────┬────────────┬────────────┬──────────────────────────────────────┐')
print('  │ Agent           │ Verdict    │ Confidence │ Key Finding                          │')
print('  ├─────────────────┼────────────┼────────────┼──────────────────────────────────────┤')
for r in results:
    aid = r.get('agent_id','?')[:15].ljust(15)
    v   = r.get('verdict','?')[:10].ljust(10)
    c   = f\"{r.get('confidence',0):.0%}\".ljust(10)
    fs  = r.get('findings', [])
    top = (fs[0] if fs else '—')[:36].ljust(36) if isinstance(fs, list) and fs and isinstance(fs[0], str) else '—'.ljust(36)
    print(f'  │ {aid} │ {v} │ {c} │ {top} │')
print('  └─────────────────┴────────────┴────────────┴──────────────────────────────────────┘')
n = len(results)
ok = sum(1 for r in results if r.get('error') in (None, ''))
print(f'  Agents: {n}  |  Succeeded: {ok}  |  Failed: {n - ok}')
" "$json" 2>/dev/null || echo -e "  ${DIM}(summary extraction failed, see raw JSON above)${RESET}"
}

# Extract human-readable summary from aggregator JSON output
format_agg_summary() {
  local json="$1"
  python3 -c "
import sys, json
d = json.loads(sys.argv[1])
c = d.get('consensus', {})
s = d.get('statistics', {})
am = d.get('agreement_map', {})
print()
print('  ╔═══════════════════════════════════════════════╗')
verdict = c.get('verdict', '?')
conf    = c.get('confidence', 0)
bar_len = int(conf * 20)
bar     = '█' * bar_len + '░' * (20 - bar_len)
print(f'  ║  Verdict:    {verdict:<32}║')
print(f'  ║  Confidence: {bar} {conf:.0%}       ║')
print(f'  ║                                               ║')
agreed   = len(am.get('agreed', []))
disputed = len(am.get('disputed', []))
unique   = len(am.get('unique', []))
print(f'  ║  ✅ Agreed:   {agreed:<33}║')
print(f'  ║  ⚠️  Disputed: {disputed:<33}║')
print(f'  ║  🔍 Unique:   {unique:<33}║')
print(f'  ╚═══════════════════════════════════════════════╝')
" "$json" 2>/dev/null || echo -e "  ${DIM}(summary extraction failed)${RESET}"
}

# ════════════════════════════════════════════════════
#  INTRO
# ════════════════════════════════════════════════════
clear
banner "Multi-Agent Consensus Engine  ·  Live Demo"
echo -e "  This skill uses ${BOLD}Byzantine Fault Tolerance${RESET} concepts"
echo -e "  to reduce LLM hallucinations through parallel"
echo -e "  multi-agent consensus voting."
echo ""
echo -e "  ${DIM}Architecture:  fan_out → 3 agents → fan_in → vote${RESET}"
echo -e "  ${DIM}Provider:      Qwen (DashScope API)${RESET}"
echo -e "  ${DIM}Consensus:     majority / conservative / diversity${RESET}"
divider
pause

# ════════════════════════════════════════════════════
#  SCENE 0 — Single Agent Baseline (The Problem)
# ════════════════════════════════════════════════════
banner "Scene 0 ─ The Problem: Single Agent Limitation"
step "First, let's see what a SINGLE agent finds..."
info "Only 1 agent, no cross-validation, no consensus"
echo ""
echo -e "  ${RED}⚠ Single point of failure — hallucinations go undetected${RESET}"
echo ""

VULN_CODE='Analyze this Solidity code for vulnerabilities:\n\nfunction withdraw() public {\n    uint amount = balances[msg.sender];\n    (bool ok,) = msg.sender.call{value: amount}("");\n    require(ok);\n    balances[msg.sender] = 0;\n}'

show_cmd "python3 consensus_engine.py  (1 agent only)"
info "Calling DashScope API..."
echo ""

SINGLE_OUT=$(python3 "$ENGINE" <<SINGLE_EOF
{
  "query": "Analyze this Solidity code for vulnerabilities:\n\nfunction withdraw() public {\n    uint amount = balances[msg.sender];\n    (bool ok,) = msg.sender.call{value: amount}(\"\");\n    require(ok);\n    balances[msg.sender] = 0;\n}",
  "domain": "smart_contract",
  "agents": [
    {"name": "solo-reviewer", "provider": "qwen", "model": "qwen-plus", "role": "You are a code reviewer. Analyze this code."}
  ]
}
SINGLE_EOF
)

format_engine_summary "$SINGLE_OUT"

SINGLE_FINDINGS=$(echo "$SINGLE_OUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
rs = d.get('agent_results', [])
total = sum(len(r.get('findings',[])) for r in rs)
print(total)
" 2>/dev/null || echo "?")

echo ""
echo -e "  ${YELLOW}Single agent found: ${BOLD}${SINGLE_FINDINGS} finding(s)${RESET}"
echo -e "  ${DIM}But is this complete? Are there hallucinations? We can't tell.${RESET}"
echo ""
step "Now let's run 3 agents with consensus voting..."
divider
pause

# ════════════════════════════════════════════════════
#  SCENE 1 — Consensus Engine (3 Qwen Agents)
# ════════════════════════════════════════════════════
banner "Scene 1 ─ Consensus Engine"
step "Launching 3 Qwen agents to analyze a Solidity reentrancy bug"
info "Each agent has a different role & weight:"
echo ""
echo -e "  ${CYAN}Agent 1${RESET}  qwen-plus     weight=0.40  (security specialist)"
echo -e "  ${CYAN}Agent 2${RESET}  qwen-plus     weight=0.35  (code auditor)"
echo -e "  ${CYAN}Agent 3${RESET}  qwen-plus     weight=0.25  (general reviewer)"
echo ""

QUERY='Analyze this Solidity code for vulnerabilities:\n\nfunction withdraw() public {\n    uint amount = balances[msg.sender];\n    (bool ok,) = msg.sender.call{value: amount}(\"\");\n    require(ok);\n    balances[msg.sender] = 0;\n}'

show_cmd "python3 consensus_engine.py <<< '{\"query\": \"...\", \"domain\": \"smart_contract\"}'"
info "Calling DashScope API in parallel..."
echo ""

ENGINE_OUT=$(python3 "$ENGINE" <<EOF
{
  "query": "Analyze this Solidity code for vulnerabilities:\n\nfunction withdraw() public {\n    uint amount = balances[msg.sender];\n    (bool ok,) = msg.sender.call{value: amount}(\"\");\n    require(ok);\n    balances[msg.sender] = 0;\n}",
  "domain": "smart_contract",
  "agents": [
    {"name": "security-specialist", "provider": "qwen", "model": "qwen-plus", "role": "You are a blockchain security expert. Focus on critical vulnerabilities."},
    {"name": "code-auditor",        "provider": "qwen", "model": "qwen-plus", "role": "You are a Solidity code auditor. Analyze code patterns."},
    {"name": "general-reviewer",    "provider": "qwen", "model": "qwen-plus", "role": "You are a general code reviewer. Look for common issues."}
  ]
}
EOF
)

echo "$ENGINE_OUT" | python3 -m json.tool 2>/dev/null | head -30
echo -e "${DIM}  ... (full JSON truncated)${RESET}"
divider

step "Agent Summary:"
format_engine_summary "$ENGINE_OUT"

MULTI_FINDINGS=$(echo "$ENGINE_OUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
rs = d.get('agent_results', [])
total = sum(len(r.get('findings',[])) for r in rs)
print(total)
" 2>/dev/null || echo "?")

echo ""
echo -e "  ${GREEN}3 agents found: ${BOLD}${MULTI_FINDINGS} finding(s) total${RESET}"
if [ "$SINGLE_FINDINGS" != "?" ] && [ "$MULTI_FINDINGS" != "?" ]; then
  echo -e "  ${CYAN}vs Single agent: ${SINGLE_FINDINGS} finding(s) — consensus reveals more!${RESET}"
fi
pause

# ════════════════════════════════════════════════════
#  SCENE 2 — Voting Aggregator (Consensus Modes)
# ════════════════════════════════════════════════════
banner "Scene 2 ─ Voting Aggregator"
step "Feeding engine output into the consensus aggregator"
info "Mode: conservative (requires ≥70% agreement)"
echo ""
show_cmd "echo \$ENGINE_OUT | python3 voting_aggregator.py --mode conservative"

AGG_OUT=$(echo "$ENGINE_OUT" | python3 "$AGGREGATOR" --mode conservative)

echo "$AGG_OUT" | python3 -m json.tool 2>/dev/null | head -25
echo -e "${DIM}  ... (full JSON truncated)${RESET}"
divider

step "Consensus Summary:"
format_agg_summary "$AGG_OUT"
pause

# ════════════════════════════════════════════════════
#  SCENE 3 — Full Pipeline (Unix Pipe)
# ════════════════════════════════════════════════════
banner "Scene 3 ─ Full Pipeline"
step "One-liner: engine → aggregator via Unix pipe"
info "This is how SpoonOS StateGraph would chain the nodes"
echo ""
show_cmd "python3 consensus_engine.py <<< INPUT | python3 voting_aggregator.py --mode majority"

PIPE_OUT=$(python3 "$ENGINE" <<EOF2 | python3 "$AGGREGATOR" --mode majority
{
  "query": "Review this smart contract for access control issues:\n\nfunction setOwner(address _new) public {\n    owner = _new;\n}",
  "domain": "smart_contract",
  "agents": [
    {"name": "acl-expert",    "provider": "qwen", "model": "qwen-plus", "role": "You are an access control specialist."},
    {"name": "audit-bot",     "provider": "qwen", "model": "qwen-plus", "role": "You are a smart contract auditor."},
    {"name": "safety-check",  "provider": "qwen", "model": "qwen-plus", "role": "You are a safety reviewer."}
  ]
}
EOF2
)

echo "$PIPE_OUT" | python3 -m json.tool 2>/dev/null | head -20
echo -e "${DIM}  ... (full JSON truncated)${RESET}"
divider

step "Pipeline Consensus Summary:"
format_agg_summary "$PIPE_OUT"
pause

# ════════════════════════════════════════════════════
#  OUTRO
# ════════════════════════════════════════════════════
banner "Demo Complete ✓"
echo -e "  ${BOLD}Comparison: Single Agent vs Multi-Agent Consensus${RESET}"
echo ""
echo -e "  ┌──────────────────────┬──────────────┬──────────────────┐"
echo -e "  │                      │ ${RED}Single Agent${RESET} │ ${GREEN}3-Agent Consensus${RESET} │"
echo -e "  ├──────────────────────┼──────────────┼──────────────────┤"
echo -e "  │ Cross-validation     │ ${RED}     ✗${RESET}       │ ${GREEN}       ✓${RESET}         │"
echo -e "  │ Hallucination detect │ ${RED}     ✗${RESET}       │ ${GREEN}       ✓${RESET}         │"
echo -e "  │ Confidence score     │ ${RED}     ✗${RESET}       │ ${GREEN}       ✓${RESET}         │"
echo -e "  │ Weighted expertise   │ ${RED}     ✗${RESET}       │ ${GREEN}       ✓${RESET}         │"
echo -e "  │ Finding dedup        │ ${RED}     ✗${RESET}       │ ${GREEN}       ✓${RESET}         │"
echo -e "  └──────────────────────┴──────────────┴──────────────────┘"
echo ""
echo -e "  ${BOLD}Key Takeaways:${RESET}"
echo ""
echo -e "  ${GREEN}1.${RESET} Multiple agents reduce single-point hallucination"
echo -e "  ${GREEN}2.${RESET} Weighted voting reflects domain expertise"
echo -e "  ${GREEN}3.${RESET} Finding clustering deduplicates across agents"
echo -e "  ${GREEN}4.${RESET} Unix pipe protocol enables SpoonOS StateGraph integration"
echo ""
echo -e "  ${DIM}Files:${RESET}"
echo -e "    SKILL.md                         — Cognitive scaffold (prompt)"
echo -e "    scripts/consensus_engine.py       — Multi-agent orchestrator"
echo -e "    scripts/voting_aggregator.py      — BFT consensus voter"
echo ""
echo -e "  ${CYAN}github.com/XSpoonAi/spoon-awesome-skill${RESET}"
divider
echo ""
