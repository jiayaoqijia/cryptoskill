#!/bin/bash

# Gate Wallet MCP Installer
# Interactive multi-platform installer with user selection

set -e

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
    
    if command -v cursor &> /dev/null; then
        platforms+=("cursor")
    fi
    
    if command -v claude &> /dev/null; then
        platforms+=("claude")
    fi
    
    if command -v codex &> /dev/null; then
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
    
    echo -e "${BLUE}🔍 Detected AI platforms:${NC}"
    if [ ${#detected_platforms[@]} -eq 0 ]; then
        echo "  ❌ No supported platforms detected"
        echo ""
        echo -e "${YELLOW}Please install one of the following AI platforms first:${NC}"
        echo "  • Cursor: https://cursor.com"
        echo "  • Claude Code: https://docs.anthropic.com/claude-code"
        echo "  • Codex CLI: https://developers.openai.com/codex"
        echo "  • OpenClaw (mcporter): https://github.com/mcporter-dev/mcporter"
        exit 1
    fi
    
    local i=1
    for platform in "${detected_platforms[@]}"; do
        case "$platform" in
            cursor) echo "  $i) Cursor ✅" ;;
            claude) echo "  $i) Claude Code ✅" ;;
            codex) echo "  $i) Codex CLI ✅" ;;
            openclaw) echo "  $i) OpenClaw (mcporter) ✅" ;;
        esac
        ((i++))
    done
    echo "  a) All platforms (recommended)"
    echo ""
    
    read -p "Please select platform to configure [1-${#detected_platforms[@]}/a] (default a): " choice
    choice=${choice:-a}
    
    if [ "$choice" = "a" ]; then
        echo "${detected_platforms[@]}"
    elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#detected_platforms[@]} ]; then
        echo "${detected_platforms[$((choice-1))]}"
    else
        echo -e "${RED}Invalid selection, using all platforms${NC}"
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
        echo "$existing_config" | jq '.mcpServers["gate-wallet"] = {
          "url": "https://api.gatemcp.ai/mcp/dex",
          "headers": {
            "x-api-key": "MCP_AK_8W2N7Q",
            "Authorization": "Bearer <your_mcp_token>"
          }
        }' > "$config_file"
    else
        cat > "$config_file" << 'EOF'
{
  "mcpServers": {
    "gate-wallet": {
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "x-api-key": "MCP_AK_8W2N7Q",
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
EOF
    fi
    
    # Install skills
    mkdir -p ".cursor/skills"
    local current_dir=$(pwd)
    for skill in gate-dex-wallet gate-dex-market gate-dex-trade; do
        if [ -d "$skill" ]; then
            ln -sf "$current_dir/$skill" ".cursor/skills/$skill"
        fi
    done
    
    echo -e "${GREEN}  ✓${NC} MCP configuration updated: $config_file"
    echo -e "${GREEN}  ✓${NC} Skills symbolic links created"
}

# Install for Claude Code
install_claude() {
    echo -e "${CYAN}🤖 Configuring Claude Code...${NC}"
    
    # Try CLI first
    if claude mcp add --transport http gate-wallet --scope project https://api.gatemcp.ai/mcp/dex 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} MCP server added successfully via CLI"
    else
        cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "gate-wallet": {
      "type": "http",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "x-api-key": "MCP_AK_8W2N7Q",
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
EOF
        echo -e "${GREEN}  ✓${NC} .mcp.json configuration created"
    fi
    
    # Create routing file
    cat > CLAUDE.md << 'EOF'
# Gate DEX Wallet Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its workflow:

- 🔐 Login, authentication, session management → `gate-dex-wallet/references/auth.md`
- 💰 Check balance, assets, wallet address, transaction history → `gate-dex-wallet/SKILL.md`
- 💸 Transfer, send tokens → `gate-dex-wallet/references/transfer.md`
- 🎯 DApp interaction, signing, contract calls → `gate-dex-wallet/references/dapp.md`
- 📊 Check prices, token info, security audits → `gate-dex-market/SKILL.md`
- 🔄 Swap, exchange, trading → `gate-dex-trade/SKILL.md`
EOF
    echo -e "${GREEN}  ✓${NC} CLAUDE.md routing file created"
}

# Install for Codex CLI
install_codex() {
    echo -e "${CYAN}⚙️ Configuring Codex CLI...${NC}"
    
    # Try CLI first
    if codex mcp add gate-wallet --transport http --url https://api.gatemcp.ai/mcp/dex 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} MCP server added successfully via CLI"
    else
        local config_file="$HOME/.codex/config.toml"
        mkdir -p "$(dirname "$config_file")"
        
        cat >> "$config_file" << 'EOF'

[mcp.gate-wallet]
transport = "http"
url = "https://api.gatemcp.ai/mcp/dex"

[mcp.gate-wallet.headers]
x-api-key = "MCP_AK_8W2N7Q"
Authorization = "Bearer <your_mcp_token>"
EOF
        echo -e "${GREEN}  ✓${NC} ~/.codex/config.toml updated"
    fi
    
    # Create AGENTS.md (same as CLAUDE.md)
    cat > AGENTS.md << 'EOF'
# Gate DEX Wallet Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its workflow:

- 🔐 Login, authentication, session management → `gate-dex-wallet/references/auth.md`
- 💰 Check balance, assets, wallet address, transaction history → `gate-dex-wallet/SKILL.md`
- 💸 Transfer, send tokens → `gate-dex-wallet/references/transfer.md`
- 🎯 DApp interaction, signing, contract calls → `gate-dex-wallet/references/dapp.md`
- 📊 Check prices, token info, security audits → `gate-dex-market/SKILL.md`
- 🔄 Swap, exchange, trading → `gate-dex-trade/SKILL.md`
EOF
    echo -e "${GREEN}  ✓${NC} AGENTS.md routing file created"
}

# Install for OpenClaw
install_openclaw() {
    echo -e "${CYAN}🐾 Configuring OpenClaw (mcporter)...${NC}"
    
    if mcporter config list 2>/dev/null | grep -q "^gate-wallet$"; then
        echo -e "${YELLOW}  ✓${NC} gate-wallet already configured"
        return 0
    fi
    
    echo "  MCP Server authentication configuration needed"
    read -p "  Enter MCP API Key [leave blank to use default]: " user_key
    user_key=${user_key:-"MCP_AK_8W2N7Q"}
    
    if mcporter config add gate-wallet --url "https://api.gatemcp.ai/mcp/dex" \
       --header "x-api-key:$user_key" --header "Authorization:Bearer <your_mcp_token>" 2>/dev/null; then
        echo -e "${GREEN}  ✓${NC} gate-wallet MCP server configured successfully"
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
    echo "1. Restart your AI tool to load configuration"
    echo "2. Complete initial login to get mcp_token"
    echo "3. Try conversation: \"Help me check USDT balance on ETH\""
    echo ""
    echo -e "${CYAN}💡 Tips:${NC}"
    echo "  First-time use requires Google OAuth login to get mcp_token"
    echo "  Detailed docs: ./gate-dex-wallet/README.md"
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
            echo "  (None detected)"
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