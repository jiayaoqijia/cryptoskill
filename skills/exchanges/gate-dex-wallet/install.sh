#!/bin/bash

# Gate Wallet MCP Installer
# Interactive multi-platform installer with user selection

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repository root is one level up from gate-dex-wallet/
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}🎯 Gate Wallet MCP Installer${NC}"
echo "=================================="
echo "Interactive installer for comprehensive wallet functionality"
echo ""

# Platform detection
detect_platforms() {
    local platforms=()
    
    if command -v cursor &> /dev/null || [ -d "$HOME/.cursor" ] || [ -d "/Applications/Cursor.app" ]; then
        platforms+=("cursor")
    fi
    
    if command -v claude &> /dev/null || [ -d "$HOME/.claude" ]; then
        platforms+=("claude")
    fi
    
    if command -v codex &> /dev/null || [ -d "$HOME/.codex" ]; then
        platforms+=("codex")
    fi
    
    if command -v mcporter &> /dev/null; then
        platforms+=("openclaw")
    fi
    
    echo "${platforms[@]}"
}

# Interactive platform selection
select_platform() {
    local detected_platforms=($(detect_platforms))
    
    echo -e "${BLUE}🔍 Detected AI platforms:${NC}" >&2
    if [ ${#detected_platforms[@]} -eq 0 ]; then
        echo "  ❌ No supported platforms detected" >&2
        echo "" >&2
        echo -e "${YELLOW}Please install one of the following AI platforms first:${NC}" >&2
        echo "  • Cursor: https://cursor.com" >&2
        echo "  • Claude Code: https://docs.anthropic.com/claude-code" >&2
        echo "  • Codex CLI: https://developers.openai.com/codex" >&2
        echo "  • OpenClaw (mcporter): https://github.com/mcporter-dev/mcporter" >&2
        exit 1
    fi
    
    local i=1
    for platform in "${detected_platforms[@]}"; do
        case "$platform" in
            cursor) echo "  $i) Cursor ✅" >&2 ;;
            claude) echo "  $i) Claude Code ✅" >&2 ;;
            codex) echo "  $i) Codex CLI ✅" >&2 ;;
            openclaw) echo "  $i) OpenClaw (mcporter) ✅" >&2 ;;
        esac
        ((i++))
    done
    echo "  a) All platforms (recommended)" >&2
    echo "" >&2
    
    read -p "Please select platforms to configure [1-${#detected_platforms[@]}/a] (default a): " choice
    choice=${choice:-a}
    
    if [ "$choice" = "a" ]; then
        echo "${detected_platforms[@]}"
    elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#detected_platforms[@]} ]; then
        echo "${detected_platforms[$((choice-1))]}"
    else
        echo -e "${RED}Invalid choice, using all platforms${NC}" >&2
        echo "${detected_platforms[@]}"
    fi
}

# Install for Cursor
install_cursor() {
    echo -e "${CYAN}📱 Configuring Cursor...${NC}"
    
    local config_file="$HOME/.cursor/mcp.json"
    mkdir -p "$(dirname "$config_file")"
    
    # Create or update MCP configuration
    if command -v jq &> /dev/null; then
        local existing_config="{}"
        if [ -f "$config_file" ]; then
            existing_config=$(cat "$config_file")
        fi
        echo "$existing_config" | jq '.mcpServers["gate-dex"] = {
          "url": "https://api.gatemcp.ai/mcp/dex"
        }' > "$config_file"
    else
        cat > "$config_file" << 'EOF'
{
  "mcpServers": {
    "gate-dex": {
      "url": "https://api.gatemcp.ai/mcp/dex"
    }
  }
}
EOF
    fi
    
    # Install skills to ~/.cursor/skills/
    local skills_dir="$HOME/.cursor/skills"
    mkdir -p "$skills_dir"
    for skill in gate-dex-wallet gate-dex-market gate-dex-trade; do
        if [ -d "$REPO_ROOT/$skill" ]; then
            rm -rf "$skills_dir/$skill"
            cp -r "$REPO_ROOT/$skill" "$skills_dir/$skill"
            echo -e "${GREEN}  ✓${NC} Installed: $skill → $skills_dir/$skill"
        else
            echo -e "${YELLOW}  ⚠${NC} $skill directory not found: $REPO_ROOT/$skill"
        fi
    done
    
    echo -e "${GREEN}  ✓${NC} MCP configuration updated: $config_file"
    echo -e "${GREEN}  ✓${NC} Skills installed to: $skills_dir"
}

# Install for Claude Code
install_claude() {
    echo -e "${CYAN}🤖 Configuring Claude Code...${NC}"
    
    # Try CLI first
    if claude mcp add --transport http gate-dex --scope project https://api.gatemcp.ai/mcp/dex 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} MCP server added successfully via CLI"
    else
        cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "gate-dex": {
      "type": "http",
      "url": "https://api.gatemcp.ai/mcp/dex"
    }
  }
}
EOF
        echo -e "${GREEN}  ✓${NC} .mcp.json configuration created"
    fi

    # Create or update routing file (do not overwrite existing content)
    local routing_content='# Gate DEX Wallet Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its process:

- 🔐 Login, authentication, session management → `gate-dex-wallet/references/auth.md`
- 💰 Check balance, assets, wallet address, transaction history → `gate-dex-wallet/SKILL.md`
- 💸 Transfer, send tokens → `gate-dex-wallet/references/transfer.md`
- 🎯 DApp interaction, signing, contract calls → `gate-dex-wallet/references/dapp.md`
- 📊 Check quotes, token info, security audits → `gate-dex-market/SKILL.md`
- 🔄 Swap, exchange, trading → `gate-dex-trade/SKILL.md`
- 🖥️ CLI, gate-wallet, openapi-swap → `gate-dex-wallet/references/cli.md`'

    if [ -f "CLAUDE.md" ]; then
        if grep -q "gate-dex-wallet" "CLAUDE.md"; then
            echo -e "${GREEN}  ✓${NC} CLAUDE.md already contains Gate DEX routing"
        else
            echo "" >> CLAUDE.md
            echo "$routing_content" >> CLAUDE.md
            echo -e "${GREEN}  ✓${NC} CLAUDE.md updated (appended Gate DEX routing)"
        fi
    else
        echo "$routing_content" > CLAUDE.md
        echo -e "${GREEN}  ✓${NC} CLAUDE.md routing file created"
    fi
}

# Install for Codex CLI
install_codex() {
    echo -e "${CYAN}⚙️ Configuring Codex CLI...${NC}"
    
    # Try CLI first
    if codex mcp add gate-dex --transport http --url https://api.gatemcp.ai/mcp/dex 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} MCP server added successfully via CLI"
    else
        local config_file="$HOME/.codex/config.toml"
        mkdir -p "$(dirname "$config_file")"

        if [ -f "$config_file" ] && grep -q '\[mcp\.gate-dex\]' "$config_file"; then
            echo -e "${GREEN}  ✓${NC} gate-dex already configured in $config_file"
        else
            cat >> "$config_file" << 'EOF'

[mcp.gate-dex]
transport = "http"
url = "https://api.gatemcp.ai/mcp/dex"
EOF
            echo -e "${GREEN}  ✓${NC} ~/.codex/config.toml updated"
        fi
    fi

    # Create or update AGENTS.md (do not overwrite existing content)
    local agents_content='# Gate DEX Wallet Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its process:

- 🔐 Login, authentication, session management → `gate-dex-wallet/references/auth.md`
- 💰 Check balance, assets, wallet address, transaction history → `gate-dex-wallet/SKILL.md`
- 💸 Transfer, send tokens → `gate-dex-wallet/references/transfer.md`
- 🎯 DApp interaction, signing, contract calls → `gate-dex-wallet/references/dapp.md`
- 📊 Check quotes, token info, security audits → `gate-dex-market/SKILL.md`
- 🔄 Swap, exchange, trading → `gate-dex-trade/SKILL.md`
- 🖥️ CLI, gate-wallet, openapi-swap → `gate-dex-wallet/references/cli.md`'

    if [ -f "AGENTS.md" ]; then
        if grep -q "gate-dex-wallet" "AGENTS.md"; then
            echo -e "${GREEN}  ✓${NC} AGENTS.md already contains Gate DEX routing"
        else
            echo "" >> AGENTS.md
            echo "$agents_content" >> AGENTS.md
            echo -e "${GREEN}  ✓${NC} AGENTS.md updated (appended Gate DEX routing)"
        fi
    else
        echo "$agents_content" > AGENTS.md
        echo -e "${GREEN}  ✓${NC} AGENTS.md routing file created"
    fi
}

# Install for OpenClaw
install_openclaw() {
    echo -e "${CYAN}🐾 Configuring OpenClaw (mcporter)...${NC}"
    
    if mcporter config list 2>/dev/null | grep -q "^gate-dex$"; then
        echo -e "${YELLOW}  ✓${NC} gate-dex already configured"
        return 0
    fi
    
    if mcporter config add gate-dex --url "https://api.gatemcp.ai/mcp/dex" 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} gate-dex MCP server configured successfully"
    else
        echo -e "${RED}  ✗${NC} Configuration failed, please check manually"
        return 1
    fi
}

# Main installation
main() {
    local selected_platforms=($(select_platform))
    
    echo ""
    echo -e "${CYAN}🚀 Starting wallet functionality configuration...${NC}"
    echo ""
    
    for platform in "${selected_platforms[@]}"; do
        case "$platform" in
            cursor) install_cursor ;;
            claude) install_claude ;;
            codex) install_codex ;;
            openclaw) install_openclaw ;;
            *)
                echo -e "${RED}Unknown platform: $platform${NC}"
                continue
                ;;
        esac
        echo ""
    done
    
    # Installation summary
    echo "=================================="
    echo -e "${GREEN}🎉 Gate Wallet installation complete!${NC}"
    echo ""
    echo -e "${BLUE}📱 Configured platforms:${NC}"
    for platform in "${selected_platforms[@]}"; do
        echo "  ✓ $platform"
    done
    echo ""
    echo -e "${BLUE}🎯 Next steps:${NC}"
    echo "1. Restart your AI tool to load the configuration"
    echo "2. Complete first login to obtain mcp_token"
    echo "3. Try conversation: \"Help me check USDT balance on ETH\""
    echo ""
    echo -e "${CYAN}💡 Tips:${NC}"
    echo "  First-time use requires logging in via Google OAuth or Gate OAuth to get mcp_token"
    echo "  For CLI command line tool (gate-wallet command), run: ./gate-dex-wallet/install_cli.sh"
    echo "  Detailed documentation: ./gate-dex-wallet/README.md"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Wallet MCP Installer"
        echo "Interactive installer with platform selection"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help"
        echo "  --list, -l     List detected platforms"
        echo ""
        echo "Supported platforms:"
        echo "  • Cursor, Claude Code, Codex CLI, OpenClaw"
        exit 0
        ;;
    --list|-l)
        echo -e "${BLUE}🔍 Detected platforms:${NC}"
        platforms=($(detect_platforms))
        if [ ${#platforms[@]} -eq 0 ]; then
            echo "  (none detected)"
        else
            for platform in "${platforms[@]}"; do
                echo "  ✓ $platform"
            done
        fi
        exit 0
        ;;
    "") main ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
esac