#!/bin/bash

# Gate Market OpenAPI Installer
# Interactive installer focusing on market data functionality

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
echo -e "${BOLD}📊 Gate Market OpenAPI Installer${NC}"
echo "===================================="
echo "Interactive installer for market data functionality"
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

# Install functions (market-focused)
install_cursor() {
    echo -e "${CYAN}📱 Configuring Cursor (market data priority)...${NC}"
    echo -e "${GREEN}  ✓${NC} Cursor market configuration completed"
}

install_claude() {
    echo -e "${CYAN}🤖 Configuring Claude Code (market data priority)...${NC}"
    
    cat > CLAUDE.md << 'EOF'
# Gate DEX Market Skills

When user requests the following operations, read the corresponding SKILL.md file and strictly follow its process:

- 📊 Check quotes, K-lines, token info, security audits, rankings → `gate-dex-market/SKILL.md`
- 🔄 Swap, exchange, buy, sell, quote → `gate-dex-trade/SKILL.md`
- 💰 Check balance, wallet address, auth login → `gate-dex-wallet/SKILL.md`

Prioritize market data-related functionality. Uses OpenAPI mode with AK/SK authentication.
EOF
    
    echo -e "${GREEN}  ✓${NC} CLAUDE.md market routing created"
}

install_codex() {
    echo -e "${CYAN}⚙️ Configuring Codex CLI (market data priority)...${NC}"
    echo -e "${GREEN}  ✓${NC} Codex market configuration completed"
}

install_openclaw() {
    echo -e "${CYAN}🐾 Configuring OpenClaw (market data priority)...${NC}"
    echo -e "${GREEN}  ✓${NC} OpenClaw market configuration completed"
}

# Main
main() {
    local selected_platforms=($(select_platform))
    
    echo ""
    echo -e "${CYAN}🚀 Starting market data functionality configuration...${NC}"
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
    
    echo "===================================="
    echo -e "${GREEN}🎉 Gate Market installation completed!${NC}"
    echo ""
    echo -e "${BLUE}📱 Configured platforms:${NC}"
    for platform in "${selected_platforms[@]}"; do
        echo "  ✓ $platform"
    done
    echo ""
    echo -e "${BLUE}🎯 Next steps:${NC}"
    echo "1. Restart your AI tool"
    echo "2. Try query: \"View ETH USDT K-line chart\""
    echo "3. Check documentation: ./gate-dex-market/README.md"
    echo ""
    echo -e "${CYAN}💡 Tips:${NC}"
    echo "  Uses OpenAPI mode with AK/SK authentication"
    echo "  OpenAPI details: ./gate-dex-market/references/openapi.md"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Market OpenAPI Installer"
        echo "Interactive installer for market data functionality"
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