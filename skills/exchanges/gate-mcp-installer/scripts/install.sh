#!/bin/bash

# Gate MCP Installer
# One-click setup for ALL Gate.com MCP servers
# Usage: ./install.sh         # Install all (default)
#        ./install.sh --select # Interactive selection

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "Gate MCP OpenClaw Installer"
echo "====================="
echo ""

# Check dependencies
if ! command -v mcporter &> /dev/null; then
    echo -e "${RED}Error: mcporter is not installed${NC}"
    echo ""
    echo "Install mcporter:"
    echo "  npm install -g mcporter"
    echo ""
    echo "Or visit: https://github.com/mcporter-dev/mcporter"
    exit 1
fi

echo -e "${GREEN}✓${NC} mcporter found"
echo ""

# Parse arguments
SELECT_MODE=false
if [ "$1" = "--select" ] || [ "$1" = "-s" ]; then
    SELECT_MODE=true
fi

# DEX MCP fixed x-api-key (consistent with Cursor/Claude/Codex installers)
GATE_DEX_API_KEY="MCP_AK_8W2N7Q"

# MCP Server definitions
# Format: name|type|endpoint|auth_type|description
declare -a SERVERS=(
    "gate|stdio|npx -y gate-mcp|api_key_secret|Spot/Futures/Options Trading"
    "gate-dex|http|https://api.gatemcp.ai/mcp/dex|x_api_key|DEX Operations"
    "gate-info|http|https://api.gatemcp.ai/mcp/info|none|Market Data"
    "gate-news|http|https://api.gatemcp.ai/mcp/news|none|News Feed"
)

# Check if server exists
check_existing() {
    local server="$1"
    mcporter config list 2>/dev/null | grep -q "^${server}$"
}

# Install stdio server
install_stdio() {
    local name="$1"
    local cmd="$2"
    local api_key="$3"
    local api_secret="$4"
    
    if [ -n "$api_key" ] && [ -n "$api_secret" ]; then
        mcporter config add "$name" --stdio --command "$cmd" \
            --env "GATE_API_KEY=$api_key" \
            --env "GATE_API_SECRET=$api_secret" 2>/dev/null || return 1
    else
        mcporter config add "$name" --stdio --command "$cmd" \
            --env "GATE_API_KEY=your-api-key" \
            --env "GATE_API_SECRET=your-api-secret" 2>/dev/null || return 1
    fi
}

# Install HTTP server
install_http() {
    local name="$1"
    local url="$2"
    local api_key="$3"
    
    if [ -n "$api_key" ]; then
        mcporter config add "$name" --url "$url" \
            --header "x-api-key:$api_key" \
            --header "Authorization:Bearer \${GATE_MCP_TOKEN}" 2>/dev/null || return 1
    else
        mcporter config add "$name" --url "$url" 2>/dev/null || return 1
    fi
}

# Install single server
install_server() {
    local config="$1"
    local gate_key="$2"
    local gate_secret="$3"
    local dex_key="$4"
    
    IFS='|' read -r name type endpoint auth_type desc <<< "$config"
    
    printf "  %-15s " "$name"
    
    # Skip if exists
    if check_existing "$name"; then
        echo -e "${YELLOW}exists${NC}"
        return 0
    fi
    
    # Install based on type and auth
    case "$auth_type" in
        api_key_secret)
            install_stdio "$name" "$endpoint" "$gate_key" "$gate_secret" || {
                echo -e "${RED}failed${NC}"
                return 1
            }
            ;;
        x_api_key)
            install_http "$name" "$endpoint" "$dex_key" || {
                echo -e "${RED}failed${NC}"
                return 1
            }
            ;;
        none)
            if [ "$type" = "stdio" ]; then
                install_stdio "$name" "$endpoint" "" "" || {
                    echo -e "${RED}failed${NC}"
                    return 1
                }
            else
                install_http "$name" "$endpoint" "" || {
                    echo -e "${RED}failed${NC}"
                    return 1
                }
            fi
            ;;
    esac
    
    echo -e "${GREEN}installed${NC}"
}

# Test server
test_server() {
    local name="$1"
    
    if mcporter list "$name" --schema &>/dev/null; then
        local count=$(mcporter list "$name" 2>/dev/null | grep -c "function" 2>/dev/null || echo "?")
        echo -e "${GREEN}✓${NC} $name ($count tools)"
    else
        echo -e "${YELLOW}⚠${NC} $name (check credentials)"
    fi
}

# Selective mode
selective_install() {
    echo "Select Gate MCP server to install:"
    echo ""
    
    local i=1
    for server in "${SERVERS[@]}"; do
        IFS='|' read -r name type endpoint auth_type desc <<< "$server"
        local status=""
        check_existing "$name" && status=" ${YELLOW}[installed]${NC}"
        printf "  %d) %-15s - %s%s\n" "$i" "$name" "$desc" "$status"
        ((i++))
    done
    
    echo ""
    read -p "Enter choice [1-4]: " choice
    
    case $choice in
        1) local selected="${SERVERS[0]}" ;;
        2) local selected="${SERVERS[1]}" ;;
        3) local selected="${SERVERS[2]}" ;;
        4) local selected="${SERVERS[3]}" ;;
        *) echo -e "${RED}Invalid choice${NC}"; exit 1 ;;
    esac
    
    echo ""
    IFS='|' read -r name type endpoint auth_type desc <<< "$selected"
    echo -e "Installing: ${CYAN}$name${NC} - $desc"
    echo ""
    
    # Get required credentials (gate-dex uses fixed x-api-key, no prompt needed)
    local gate_key="" gate_secret="" dex_key="$GATE_DEX_API_KEY"
    
    case "$auth_type" in
        api_key_secret)
            echo "This server requires Gate API credentials."
            echo "Get API Key from: https://www.gate.com/myaccount/profile/api-key/manage"
            echo ""
            read -p "  API Key: " gate_key
            read -s -p "  API Secret: " gate_secret
            echo ""
            if [ -z "$gate_key" ] || [ -z "$gate_secret" ]; then
                echo -e "${RED}Error: API Key and Secret are required${NC}"
                exit 1
            fi
            ;;
        x_api_key)
            # Uses fixed GATE_DEX_API_KEY, consistent with Cursor/Claude/Codex installers
            ;;
    esac
    
    echo ""
    install_server "$selected" "$gate_key" "$gate_secret" "$dex_key"
    
    echo ""
    echo "Testing connection..."
    test_server "$name"
}

# Install all mode
install_all() {
    echo -e "${BLUE}Installing ALL Gate MCP servers${NC}"
    echo ""
    
    # Check if gate (main) needs credentials
    local need_gate=false
    for server in "${SERVERS[@]}"; do
        IFS='|' read -r name type endpoint auth_type desc <<< "$server"
        if ! check_existing "$name"; then
            case "$auth_type" in
                api_key_secret) need_gate=true ;;
            esac
        fi
    done
    
    # Collect credentials (gate-dex uses fixed x-api-key, no prompt needed)
    local gate_key="" gate_secret="" dex_key="$GATE_DEX_API_KEY"
    
    if [ "$need_gate" = true ]; then
        echo "${CYAN}Gate Trading API${NC} (for gate server)"
        echo "Get API Key from: https://www.gate.com/myaccount/profile/api-key/manage"
        read -p "  API Key: " gate_key
        read -s -p "  API Secret: " gate_secret
        echo ""
        echo ""
    fi
    
    if [ -z "$gate_key" ] && [ "$need_gate" = true ]; then
        echo -e "${YELLOW}Warning: No Gate API credentials provided${NC}"
        echo "The gate server will be skipped."
        echo ""
    fi
    
    # Install all (gate-dex always uses GATE_DEX_API_KEY)
    echo "Installing servers..."
    for server in "${SERVERS[@]}"; do
        IFS='|' read -r name type endpoint auth_type desc <<< "$server"
        
        case "$auth_type" in
            api_key_secret)
                [ -z "$gate_key" ] && continue
                ;;
        esac
        
        install_server "$server" "$gate_key" "$gate_secret" "$dex_key"
    done
    
    # Test all
    echo ""
    echo "Testing connections..."
    for server in "${SERVERS[@]}"; do
        IFS='|' read -r name type endpoint auth_type desc <<< "$server"
        test_server "$name"
    done
}

# Main
if [ "$SELECT_MODE" = true ]; then
    selective_install
else
    install_all
fi

echo ""
echo "====================="
echo "Installation Complete!"
echo ""
echo -e "${BLUE}Installed servers:${NC}"
for server in "${SERVERS[@]}"; do
    IFS='|' read -r name type endpoint auth_type desc <<< "$server"
    if check_existing "$name"; then
        echo "  ✓ $name"
    fi
done

echo ""
# Gate-Dex: authorization guidance when queries return auth-required
if mcporter config list 2>/dev/null | grep -q "^gate-dex$"; then
    echo -e "${CYAN}Gate-Dex authorization note:${NC}"
    echo "  When a gate-dex query (balance/transfer/swap, etc.) returns an authorization required message:"
    echo "  1) First open the wallet page below to create or bind a wallet (if you don't have one yet):"
    echo "     https://web3.gate.com/"
    echo "  2) The assistant will return a clickable Google authorization link for you to complete OAuth."
    echo ""
fi
echo "Quick commands:"
echo "  mcporter call gate-info.list_tickers currency_pair=BTC_USDT"
echo "  mcporter call gate-news.list_news"
echo "  mcporter call gate.list_spot_accounts"
echo "  mcporter call gate-dex.list_balances"
echo ""
