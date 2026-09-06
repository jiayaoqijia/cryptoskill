#!/usr/bin/env bash
# =============================================================================
# Robinhood Agent Skill — One-Click Setup
# =============================================================================
# Installs robinhood-mcp, configures MCP for your agent, and creates skill
# directories for Hermes Agent, Claude Code, OpenCode, Cline, and Codex.
#
# Usage:
#   bash scripts/install.sh                    # Interactive (default)
#   ROBINHOOD_USERNAME=x ROBINHOOD_PASSWORD=x \
#     bash scripts/install.sh --non-interactive # CI/automation
# =============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
DIM='\033[2m'
RESET='\033[0m'

info()  { echo -e "${BLUE}ℹ${RESET} $*"; }
ok()    { echo -e "${GREEN}✓${RESET} $*"; }
warn()  { echo -e "${YELLOW}⚠${RESET} $*"; }
fail()  { echo -e "${RED}✗${RESET} $*"; exit 1; }

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
NON_INTERACTIVE=false
SKIP_CREDENTIALS=false
AGENT=""
SKILL_SOURCE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --non-interactive) NON_INTERACTIVE=true; shift ;;
    --skip-credentials) SKIP_CREDENTIALS=true; shift ;;
    --agent) AGENT="$2"; shift 2 ;;
    --source) SKILL_SOURCE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: bash scripts/install.sh [options]"
      echo ""
      echo "Options:"
      echo "  --non-interactive    Run without prompts (reads from env vars)"
      echo "  --skip-credentials  Skip credential prompts (configure manually later)"
      echo "  --agent AGENT       Target agent: hermes, claude-code, opencode, cline, codex, windsurf, all"
      echo "  --source PATH       Local path to skill source (default: script directory)"
      echo "  -h, --help          Show this help"
      exit 0
      ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="${SKILL_SOURCE:-$(dirname "$SCRIPT_DIR")}"

info "Robinhood Agent Skill Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ---------------------------------------------------------------------------
# 1. Check prerequisites
# ---------------------------------------------------------------------------
info "Checking prerequisites..."

command -v python3 &>/dev/null || fail "Python 3 is required. Install it first."
ok "Python 3 found: $(python3 --version 2>&1 | head -1)"

# Check for uvx (preferred) or pip
if command -v uvx &>/dev/null; then
  ok "uvx found (recommended MCP runner)"
  MCP_CMD="uvx"
  MCP_ARGS='["robinhood-mcp"]'
elif command -v pip &>/dev/null || command -v pip3 &>/dev/null; then
  warn "uvx not found. pip install works but uvx is recommended for auto-management."
  warn "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
  MCP_CMD="python3"
  MCP_ARGS='["-m", "robinhood_mcp"]'
fi

# Check for Node.js (needed by some agents for MCP)
if command -v node &>/dev/null; then
  DIM "Node.js found: $(node --version)"
else
  warn "Node.js not found. Some agents require it for MCP subprocess management."
fi

# ---------------------------------------------------------------------------
# 2. Install Python dependencies
# ---------------------------------------------------------------------------
info "Installing Python dependencies..."

if ! python3 -c "import robin_stocks" 2>/dev/null; then
  pip install robin_stocks 2>/dev/null || pip3 install robin_stocks 2>/dev/null || \
    warn "Could not install robin_stocks. The cache script needs it for standalone mode."
else
  ok "robin_stocks already installed"
fi

if ! python3 -c "import pyotp" 2>/dev/null; then
  pip install pyotp 2>/dev/null || pip3 install pyotp 2>/dev/null || \
    warn "Could not install pyotp. Install it manually: pip install pyotp"
else
  ok "pyotp already installed"
fi

# ---------------------------------------------------------------------------
# 3. Get credentials
# ---------------------------------------------------------------------------
RH_USERNAME="${ROBINHOOD_USERNAME:-}"
RH_PASSWORD="${ROBINHOOD_PASSWORD:-}"
RH_TOTP_SECRET="${ROBINHOOD_TOTP_SECRET:-}"

if [[ "$SKIP_CREDENTIALS" == "true" ]]; then
  warn "Skipping credential setup. Configure manually later."
  warn "Set ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, and optional ROBINHOOD_TOTP_SECRET."
else
  if [[ "$NON_INTERACTIVE" == "true" ]]; then
    [[ -z "$RH_USERNAME" ]] && warn "ROBINHOOD_USERNAME not set"
    [[ -z "$RH_PASSWORD" ]] && warn "ROBINHOOD_PASSWORD not set"
  else
    if [[ -z "$RH_USERNAME" ]]; then
      echo -n "Robinhood email: "
      read -r RH_USERNAME
    fi
    if [[ -z "$RH_PASSWORD" ]]; then
      echo -n "Robinhood password: "
      read -rs RH_PASSWORD
      echo
    fi
    echo -n "Use authenticator app for 2FA? (y/N) "
    read -r USE_TOTP
    if [[ "$USE_TOTP" =~ ^[Yy]$ ]]; then
      echo -n "TOTP secret (from authenticator setup): "
      read -rs RH_TOTP_SECRET
      echo
    fi
  fi
fi

# ---------------------------------------------------------------------------
# 4. Determine target agent(s)
# ---------------------------------------------------------------------------
if [[ -z "$AGENT" ]]; then
  if [[ "$NON_INTERACTIVE" == "true" ]]; then
    AGENT="all"
  else
    echo ""
    echo "Which agent(s) are you configuring?"
    echo "  1) Hermes Agent"
    echo "  2) Claude Code / OpenClaw"
    echo "  3) Claude Desktop"
    echo "  4) Codex CLI"
    echo "  5) OpenCode"
    echo "  6) Cline"
    echo "  7) Windsurf"
    echo "  8) All of the above"
    echo -n "Enter number(s), comma-separated [8]: "
    read -r AGENT_CHOICE
    case "${AGENT_CHOICE:-8}" in
      1) AGENT="hermes" ;;
      2) AGENT="claude-code" ;;
      3) AGENT="claude-desktop" ;;
      4) AGENT="codex" ;;
      5) AGENT="opencode" ;;
      6) AGENT="cline" ;;
      7) AGENT="windsurf" ;;
      8) AGENT="all" ;;
      *) AGENT="all" ;;
    esac
  fi
fi

# ---------------------------------------------------------------------------
# 5. Configure agents
# ---------------------------------------------------------------------------
HERMES_DIR="$HOME/.hermes"
CONFIGURED_AGENTS=()

configure_hermes() {
  info "Configuring Hermes Agent..."

  # Create skill directory
  SKILL_DIR="$HERMES_DIR/skills/finance/robinhood"
  mkdir -p "$SKILL_DIR"
  cp "$SKILL_SOURCE/SKILL.md" "$SKILL_DIR/SKILL.md"

  # Copy scripts
  mkdir -p "$SKILL_DIR/scripts"
  cp "$SKILL_SOURCE/scripts/refresh_cache.py" "$SKILL_DIR/scripts/refresh_cache.py"
  chmod +x "$SKILL_DIR/scripts/refresh_cache.py"

  # Create data directory
  mkdir -p "$HERMES_DIR/data/robinhood"

  # Add MCP config
  CONFIG_FILE="$HERMES_DIR/config.yaml"
  if [[ -f "$CONFIG_FILE" ]]; then
    # Check if robinhood MCP is already configured
    if grep -q "robinhood:" "$CONFIG_FILE" 2>/dev/null; then
      ok "Robinhood MCP already configured in config.yaml"
    else
      # Append MCP config
      mkdir -p "$HERMES_DIR"
      echo "" >> "$CONFIG_FILE"
      echo "# Robinhood MCP Server (added by robinhood-agent-skill)" >> "$CONFIG_FILE"
      echo "mcp_servers:" >> "$CONFIG_FILE"
      # Check if mcp_servers section exists
      if grep -q "^mcp_servers:" "$CONFIG_FILE" 2>/dev/null; then
        # Insert under existing mcp_servers
        python3 -c "
import yaml, sys
with open('$CONFIG_FILE', 'r') as f:
    config = yaml.safe_load(f)
if 'mcp_servers' not in config:
    config['mcp_servers'] = {}
config['mcp_servers']['robinhood'] = {
    'command': 'uvx',
    'args': ['robinhood-mcp'],
    'env': {
        'ROBINHOOD_USERNAME': '${RH_USERNAME}',
        'ROBINHOOD_PASSWORD': '${RH_PASSWORD}',
    },
    'timeout': 60,
    'connect_timeout': 30,
}
with open('$CONFIG_FILE', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)
print('Added robinhood MCP config')
" 2>/dev/null || warn "Could not auto-merge config. Add manually (see templates/)"
      else
        # New config file or no mcp_servers section
        cat >> "$CONFIG_FILE" << 'YAML_EOF'
  robinhood:
    command: uvx
    args:
      - robinhood-mcp
    env:
      ROBINHOOD_USERNAME: "${RH_USERNAME}"
      ROBINHOOD_PASSWORD: "${RH_PASSWORD}"
    timeout: 60
    connect_timeout: 30
YAML_EOF
      fi
      ok "Added robinhood MCP config to config.yaml"
    fi
  else
    # Create new config
    mkdir -p "$HERMES_DIR"
    cat > "$CONFIG_FILE" << YAML_EOF
mcp_servers:
  robinhood:
    command: uvx
    args:
      - robinhood-mcp
    env:
      ROBINHOOD_USERNAME: "${RH_USERNAME}"
      ROBINHOOD_PASSWORD: "${RH_PASSWORD}"
    timeout: 60
    connect_connect: 30
YAML_EOF
    ok "Created new config.yaml with robinhood MCP config"
  fi

  # Write .env if credentials provided
  ENV_FILE="$HERMES_DIR/.env"
  if [[ -n "$RH_USERNAME" && -n "$RH_PASSWORD" ]]; then
    echo "" >> "$ENV_FILE"
    echo "# Robinhood credentials (added by robinhood-agent-skill)" >> "$ENV_FILE"
    echo "ROBINHOOD_USERNAME=${RH_USERNAME}" >> "$ENV_FILE"
    echo "ROBINHOOD_PASSWORD=${RH_PASSWORD}" >> "$ENV_FILE"
    if [[ -n "$RH_TOTP_SECRET" ]]; then
      echo "ROBINHOOD_TOTP_SECRET=${RH_TOTP_SECRET}" >> "$ENV_FILE"
    fi
    ok "Credentials saved to .env"
  fi

  # Copy refresh_cache.py to data dir
  cp "$SKILL_SOURCE/scripts/refresh_cache.py" "$HERMES_DIR/data/robinhood/"
  chmod +x "$HERMES_DIR/data/robinhood/refresh_cache.py"

  ok "Hermes Agent configured"
  CONFIGURED_AGENTS+=("hermes")
}

configure_claude_code() {
  info "Configuring Claude Code / OpenClaw..."

  # .mcp.json in current project or home directory
  MCP_FILE="$HOME/.mcp.json"
  if [[ -f "$HOME/.mcp.json" ]]; then
    # Merge with existing
    python3 -c "
import json, sys
with open('$MCP_FILE', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['robinhood'] = {
    'command': 'uvx',
    'args': ['robinhood-mcp'],
    'env': {
        'ROBINHOOD_USERNAME': '${RH_USERNAME}',
        'ROBINHOOD_PASSWORD': '${RH_PASSWORD}',
    }
}
with open('$MCP_FILE', 'w') as f:
    json.dump(config, f, indent=2)
print('Added robinhood MCP config')
" 2>/dev/null || warn "Could not merge .mcp.json. Add manually from templates/"
  else
    cat > "$MCP_FILE" << JSON_EOF
{
  "mcpServers": {
    "robinhood": {
      "command": "uvx",
      "args": ["robinhood-mcp"],
      "env": {
        "ROBINHOOD_USERNAME": "${RH_USERNAME}",
        "ROBINHOOD_PASSWORD": "${RH_PASSWORD}"
      }
    }
  }
}
JSON_EOF
  fi

  # Create skill directory
  SKILL_DIR="$HOME/.claude/skills/robinhood"
  mkdir -p "$SKILL_DIR"
  cp "$SKILL_SOURCE/SKILL.md" "$SKILL_DIR/SKILL.md"

  ok "Claude Code / OpenClaw configured"
  CONFIGURED_AGENTS+=("claude-code")
}

configure_claude_desktop() {
  info "Configuring Claude Desktop..."

  if [[ "$OSTYPE" == "darwin"* ]]; then
    DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
  else
    DESKTOP_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
  fi

  mkdir -p "$(dirname "$DESKTOP_CONFIG")"

  if [[ -f "$DESKTOP_CONFIG" ]]; then
    python3 -c "
import json
with open('$DESKTOP_CONFIG', 'r') as f:
    config = json.load(f)
if 'mcpServers' not in config:
    config['mcpServers'] = {}
config['mcpServers']['robinhood'] = {
    'command': 'uvx',
    'args': ['robinhood-mcp'],
    'env': {
        'ROBINHOOD_USERNAME': '${RH_USERNAME}',
        'ROBINHOOD_PASSWORD': '${RH_PASSWORD}',
    }
}
with open('$DESKTOP_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
print('Added robinhood MCP config')
" 2>/dev/null || warn "Could not merge Claude Desktop config. Add manually from templates/"
  else
    cp "$SKILL_SOURCE/templates/claude-desktop.json" "$DESKTOP_CONFIG"
    # Replace placeholder credentials
    if command -v sed &>/dev/null; then
      sed -i.bak "s/your_email/${RH_USERNAME}/g; s/your_password/${RH_PASSWORD}/g" "$DESKTOP_CONFIG"
      rm -f "${DESKTOP_CONFIG}.bak"
    fi
  fi

  ok "Claude Desktop configured ($DESKTOP_CONFIG)"
  CONFIGURED_AGENTS+=("claude-desktop")
}

configure_codex() {
  info "Configuring Codex CLI..."

  CODEX_DIR="$HOME/.codex"
  mkdir -p "$CODEX_DIR"
  CODEX_CONFIG="$CODEX_DIR/config.json"

  if [[ -f "$CODEX_CONFIG" ]]; then
    warn "Codex config exists. Add MCP config manually from templates/codex.json"
  else
    cp "$SKILL_SOURCE/templates/codex.json" "$CODEX_CONFIG"
    if command -v sed &>/dev/null; then
      sed -i.bak "s/your_email/${RH_USERNAME}/g; s/your_password/${RH_PASSWORD}/g" "$CODEX_CONFIG"
      rm -f "${CODEX_CONFIG}.bak"
    fi
  fi

  # Skill directory
  SKILL_DIR="$CODEX_DIR/skills/robinhood"
  mkdir -p "$SKILL_DIR"
  cp "$SKILL_SOURCE/SKILL.md" "$SKILL_DIR/SKILL.md"

  ok "Codex CLI configured"
  CONFIGURED_AGENTS+=("codex")
}

configure_opencode() {
  info "Configuring OpenCode..."

  OPENCODE_DIR="$HOME/.opencode"
  mkdir -p "$OPENCODE_DIR"
  OPENCODE_CONFIG="$OPENCODE_DIR/opencode.json"

  if [[ -f "$OPENCODE_CONFIG" ]]; then
    warn "OpenCode config exists. Add MCP config manually from templates/opencode.json"
  else
    cp "$SKILL_SOURCE/templates/opencode.json" "$OPENCODE_CONFIG"
  fi

  ok "OpenCode configured"
  CONFIGURED_AGENTS+=("opencode")
}

configure_cline() {
  info "Configuring Cline..."

  # Cline stores MCP config in VS Code settings
  CLINE_DIR="$HOME/.cline"
  mkdir -p "$CLINE_DIR"
  CLINE_MCP="$CLINE_DIR/mcp.json"

  if [[ -f "$CLINE_MCP" ]]; then
    warn "Cline MCP config exists. Add robinhood config manually from templates/cline-mcp.json"
  else
    cp "$SKILL_SOURCE/templates/cline-mcp.json" "$CLINE_MCP"
    if command -v sed &>/dev/null; then
      sed -i.bak "s/your_email/${RH_USERNAME}/g; s/your_password/${RH_PASSWORD}/g" "$CLINE_MCP"
      rm -f "${CLINE_MCP}.bak"
    fi
  fi

  ok "Cline configured"
  CONFIGURED_AGENTS+=("cline")
}

configure_windsurf() {
  info "Configuring Windsurf..."

  WINDSURF_DIR="$HOME/.codeium/windsurf"
  mkdir -p "$WINDSURF_DIR"
  WINDSURF_MCP="$WINDSURF_DIR/mcp.json"

  if [[ -f "$WINDSURF_MCP" ]]; then
    warn "Windsurf MCP config exists. Add robinhood config manually from templates/windsurf-mcp.json"
  else
    cp "$SKILL_SOURCE/templates/windsurf-mcp.json" "$WINDSURF_DIR/mcp.json"
    if command -v sed &>/dev/null; then
      sed -i.bak "s/your_email/${RH_USERNAME}/g; s/your_password/${RH_PASSWORD}/g" "$WINDSURF_DIR/mcp.json"
      rm -f "$WINDSURF_DIR/mcp.json.bak"
    fi
  fi

  ok "Windsurf configured"
  CONFIGURED_AGENTS+=("windsurf")
}

# Run configurations
case "$AGENT" in
  hermes) configure_hermes ;;
  claude-code) configure_claude_code ;;
  claude-desktop) configure_claude_desktop ;;
  codex) configure_codex ;;
  opencode) configure_opencode ;;
  cline) configure_cline ;;
  windsurf) configure_windsurf ;;
  all)
    configure_hermes
    configure_claude_code
    configure_claude_desktop
    configure_codex
    configure_opencode
    configure_cline
    configure_windsurf
    ;;
  *) warn "Unknown agent: $AGENT. Configuring Hermes only." ; configure_hermes ;;
esac

# ---------------------------------------------------------------------------
# 6. Test connection
# ---------------------------------------------------------------------------
echo ""
info "Testing robinhood-mcp connection..."

if command -v uvx &>/dev/null; then
  # Quick test — try to start and get tool list
  timeout 15 uvx robinhood-mcp --help 2>/dev/null || true
  ok "robinhood-mcp package accessible via uvx"
elif command -v python3 &>/dev/null; then
  python3 -c "import robinhood_mcp" 2>/dev/null && ok "robinhood_mcp Python package available" || \
    warn "robinhood_mcp package not found. It will be installed on first use via uvx."
fi

if command -v hermes &>/dev/null; then
  info "Testing Hermes MCP connection..."
  hermes mcp test robinhood 2>/dev/null && ok "Hermes MCP test passed" || \
    warn "Hermes MCP test failed. Restart your agent and try again."
fi

# ---------------------------------------------------------------------------
# 7. Done!
# ---------------------------------------------------------------------------
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "Robinhood Agent Skill setup complete!"
echo ""
echo "Configured agents: ${CONFIGURED_AGENTS[*]}"
echo ""
echo "Next steps:"
echo "  1. Restart your agent to pick up the MCP config"
echo "  2. Ask your agent: \"What's my portfolio worth?\""
echo "  3. Optional: Set up periodic cache refresh with cron:"
echo "     python3 ~/.hermes/data/robinhood/refresh_cache.py"
echo ""
echo "For Obsidian vault integration, run:"
echo "  python3 scripts/refresh_cache.py --vault-path /path/to/your/vault"
echo ""
info "Documentation: https://github.com/uzairansaruzi/robinhood-agent-skill"