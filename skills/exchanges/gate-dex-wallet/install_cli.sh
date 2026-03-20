#!/bin/bash

# Gate Wallet CLI Installer
# Installs gate-wallet CLI tool and configures skill routing

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
echo -e "${BOLD}🖥️  Gate Wallet CLI Installer${NC}"
echo "=================================="
echo "Install gate-wallet CLI with dual-channel support (MCP + OpenAPI)"
echo ""

# Check Node.js
check_node() {
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js not installed${NC}"
        echo ""
        echo "gate-wallet CLI requires Node.js >= 18"
        echo "Installation methods:"
        echo "  • macOS:   brew install node"
        echo "  • Linux:   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt install -y nodejs"
        echo "  • Or visit: https://nodejs.org/"
        exit 1
    fi

    local node_version
    node_version=$(node -v | sed 's/v//' | cut -d. -f1)
    if [ "$node_version" -lt 18 ]; then
        echo -e "${RED}❌ Node.js version too low: $(node -v) (requires >= 18)${NC}"
        echo "Please upgrade: brew upgrade node or visit https://nodejs.org/"
        exit 1
    fi
    echo -e "${GREEN}  ✓${NC} Node.js $(node -v)"
}

# Check npm
check_npm() {
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}  ✓${NC} npm $(npm -v)"
}

# Install gate-wallet CLI
install_cli() {
    echo ""
    echo -e "${CYAN}📦 Installing gate-wallet CLI...${NC}"

    if command -v gate-wallet &> /dev/null; then
        local current_version
        current_version=$(gate-wallet --version 2>/dev/null || echo "unknown")
        echo -e "${YELLOW}  ℹ️  gate-wallet already installed (${current_version})${NC}"
        read -p "  Reinstall/upgrade? [y/N] " upgrade
        if [[ ! "$upgrade" =~ ^[yY]$ ]]; then
            echo -e "${GREEN}  ✓${NC} Keeping current version"
            return 0
        fi
    fi

    npm install -g gate-wallet-cli

    if command -v gate-wallet &> /dev/null; then
        echo -e "${GREEN}  ✓${NC} gate-wallet CLI installed successfully: $(gate-wallet --version 2>/dev/null || echo 'installed')"
    else
        echo -e "${RED}  ✗${NC} Installation failed, try: sudo npm install -g gate-wallet-cli"
        exit 1
    fi
}

# Configure OpenAPI credentials
configure_openapi() {
    echo ""
    echo -e "${CYAN}🔑 Configuring OpenAPI credentials (optional)...${NC}"
    echo "  OpenAPI channel is used for hybrid mode Swap (openapi-swap)"
    echo "  You can skip this and configure manually later"
    echo ""

    local config_dir="$HOME/.gate-dex-openapi"
    local config_file="$config_dir/config.json"

    if [ -f "$config_file" ]; then
        echo -e "${GREEN}  ✓${NC} OpenAPI config already exists: $config_file"
        read -p "  Reconfigure? [y/N] " reconfig
        if [[ ! "$reconfig" =~ ^[yY]$ ]]; then
            return 0
        fi
    fi

    read -p "  Configure OpenAPI AK/SK? [y/N] " setup_openapi
    if [[ ! "$setup_openapi" =~ ^[yY]$ ]]; then
        echo -e "${YELLOW}  ⏭  Skipping OpenAPI configuration${NC}"
        echo "  You can manually create: $config_file"
        return 0
    fi

    read -p "  API Key (api_key): " api_key
    read -p "  Secret Key (secret_key): " secret_key

    if [ -z "$api_key" ] || [ -z "$secret_key" ]; then
        echo -e "${RED}  ✗${NC} API Key and Secret Key cannot be empty"
        return 1
    fi

    mkdir -p "$config_dir"
    cat > "$config_file" << EOF
{
  "api_key": "$api_key",
  "secret_key": "$secret_key"
}
EOF
    chmod 600 "$config_file"
    echo -e "${GREEN}  ✓${NC} OpenAPI config saved: $config_file"
}

# Update CLAUDE.md / AGENTS.md routing to include CLI
update_routing_files() {
    echo ""
    echo -e "${CYAN}📝 Updating routing configuration...${NC}"

    local cli_route="- 🖥️ CLI operations, gate-wallet commands, openapi-swap → \`gate-dex-wallet/references/cli.md\`"

    for routing_file in CLAUDE.md AGENTS.md; do
        if [ -f "$routing_file" ]; then
            if ! grep -q "cli.md" "$routing_file"; then
                echo "$cli_route" >> "$routing_file"
                echo -e "${GREEN}  ✓${NC} $routing_file updated (added CLI route)"
            else
                echo -e "${GREEN}  ✓${NC} $routing_file already contains CLI route"
            fi
        fi
    done
}

# Print summary
print_summary() {
    echo ""
    echo "=================================="
    echo -e "${GREEN}🎉 Gate Wallet CLI installation complete!${NC}"
    echo ""
    echo -e "${BLUE}🚀 Quick Start:${NC}"
    echo ""
    echo "  # 1. Login (first time)"
    echo "  gate-wallet login"
    echo ""
    echo "  # 2. Check balance"
    echo "  gate-wallet balance"
    echo ""
    echo "  # 3. Transfer"
    echo "  gate-wallet send --chain ETH --to 0x... --amount 0.01"
    echo ""
    echo "  # 4. Hybrid mode Swap (requires OpenAPI config)"
    echo "  gate-wallet openapi-swap --chain ARB --from - --to 0x... --amount 0.001 -y"
    echo ""
    echo "  # 5. Interactive REPL mode"
    echo "  gate-wallet"
    echo ""
    echo -e "${CYAN}💡 Tips:${NC}"
    echo "  • First use requires OAuth login: gate-wallet login"
    echo "  • Credentials saved at: ~/.gate-wallet/auth.json"
    echo "  • OpenAPI config: ~/.gate-dex-openapi/config.json"
    echo "  • Documentation: ./gate-dex-wallet/references/cli.md"
    echo ""
}

# Main
main() {
    echo -e "${BLUE}🔍 Checking environment...${NC}"
    check_node
    check_npm

    install_cli
    configure_openapi
    update_routing_files
    print_summary
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Wallet CLI Installer"
        echo "Installs gate-wallet CLI and configures dual-channel support"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h       Show this help"
        echo "  --skip-openapi   Skip OpenAPI credential configuration"
        echo ""
        echo "Prerequisites:"
        echo "  • Node.js >= 18"
        echo "  • npm"
        echo ""
        echo "What it installs:"
        echo "  • gate-wallet CLI (via npm global)"
        echo "  • OpenAPI credentials (~/.gate-dex-openapi/config.json)"
        echo "  • Routing file updates (CLAUDE.md / AGENTS.md)"
        exit 0
        ;;
    --skip-openapi)
        echo -e "${BLUE}🔍 Checking environment...${NC}"
        check_node
        check_npm
        install_cli
        update_routing_files
        print_summary
        ;;
    "") main ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
esac
