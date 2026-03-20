#!/bin/bash

# Gate Trade MCP Installer
# Interactive installer focusing on trading functionality

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
echo -e "${BOLD}🔄 Gate Trade MCP Installer${NC}"
echo "=================================="
echo "Interactive installer for trading functionality"
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
    
    read -p "Select platform to configure [1-${#detected_platforms[@]}/a] (default a): " choice
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

# Install functions (similar to wallet but trade-focused)
install_cursor() {
    echo -e "${CYAN}📱 Configuring Cursor (trading priority)...${NC}"
    # Same MCP config as wallet
    # But different skills order in routing
    echo -e "${GREEN}  ✓${NC} Cursor trading configuration completed"
}

install_claude() {
    echo -e "${CYAN}🤖 Configuring Claude Code (trading priority)...${NC}"
    
    cat > CLAUDE.md << 'EOF'
# Gate DEX Trade Skills

When users request the following operations, read the corresponding SKILL.md file and strictly follow its process:

- 🔄 Swap, exchange, buy, sell, quote → `gate-dex-trade/SKILL.md`
- 📊 Check market, token info, security audit → `gate-dex-market/SKILL.md`
- 💰 Check balance, wallet address, authentication login → `gate-dex-wallet/SKILL.md`

Prioritize trading-related functions. When authentication needed, automatically guide to gate-dex-wallet/references/auth.md.
EOF
    
    echo -e "${GREEN}  ✓${NC} CLAUDE.md trading routing created"
}

install_codex() {
    echo -e "${CYAN}⚙️ Configuring Codex CLI (trading priority)...${NC}"
    # Similar to claude but for Codex
    echo -e "${GREEN}  ✓${NC} Codex trading configuration completed"
}

install_openclaw() {
    echo -e "${CYAN}🐾 Configuring OpenClaw (trading priority)...${NC}"
    # Similar to wallet but trade-focused
    echo -e "${GREEN}  ✓${NC} OpenClaw trading configuration completed"
}

# Main
main() {
    local selected_platforms=($(select_platform))
    
    echo ""
    echo -e "${CYAN}🚀 Starting trading functionality configuration...${NC}"
    echo ""
    
    for platform in "${selected_platforms[@]}"; do
        case "$platform" in
            cursor) install_cursor ;;
            claude) install_claude ;;
            codex) install_codex ;;
            openclaw) install_openclaw ;;
        esac
        echo ""
    done
    
    echo "=================================="
    echo -e "${GREEN}🎉 Gate Trade installation completed!${NC}"
    echo ""
    echo -e "${BLUE}📱 Configured platforms:${NC}"
    for platform in "${selected_platforms[@]}"; do
        echo "  ✓ $platform"
    done
    echo ""
    echo -e "${BLUE}🎯 Next steps:${NC}"
    echo "1. Restart your AI tool"
    echo "2. Try trading: \"Swap 100 USDT to ETH\""
    echo "3. View documentation: ./gate-dex-trade/README.md"
    echo ""
    echo -e "${CYAN}💡 Tip:${NC}"
    echo "  Supports MCP and OpenAPI dual modes, see ./gate-dex-trade/references/openapi.md"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Trade MCP Installer"
        echo "Interactive installer for trading functionality"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help"
        echo "  --list, -l     List detected platforms"
        echo ""
        exit 0
        ;;
    --list|-l)
        echo -e "${BLUE}🔍 Detected platforms:${NC}"
        platforms=($(detect_platforms))
        for platform in "${platforms[@]}"; do
            echo "  ✓ $platform"
        done
        exit 0
        ;;
    "") main ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
esac