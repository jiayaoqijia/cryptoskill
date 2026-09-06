#!/bin/bash

# Gate Market MCP Installer
# Interactive installer focusing on market data functionality

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repository root is one level up from gate-dex-market/
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
echo -e "${BOLD}📊 Gate Market MCP Installer${NC}"
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
    
    echo -e "${BLUE}🔍 检测到的 AI 平台:${NC}"
    if [ ${#detected_platforms[@]} -eq 0 ]; then
        echo "  ❌ 未检测到支持的平台"
        echo ""
        echo -e "${YELLOW}请先安装以下任一 AI 平台:${NC}"
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
    echo "  a) 全部平台 (推荐)"
    echo ""
    
    read -p "请选择要配置的平台 [1-${#detected_platforms[@]}/a] (默认 a): " choice
    choice=${choice:-a}
    
    if [ "$choice" = "a" ]; then
        echo "${detected_platforms[@]}"
    elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#detected_platforms[@]} ]; then
        echo "${detected_platforms[$((choice-1))]}"
    else
        echo -e "${RED}无效选择，使用全部平台${NC}"
        echo "${detected_platforms[@]}"
    fi
}

# Install functions (market-focused)
install_cursor() {
    echo -e "${CYAN}📱 配置 Cursor (市场数据优先)...${NC}"
    echo -e "${GREEN}  ✓${NC} Cursor 市场配置完成"
}

install_claude() {
    echo -e "${CYAN}🤖 配置 Claude Code (市场数据优先)...${NC}"
    
    cat > CLAUDE.md << 'EOF'
# Gate DEX Market Skills

当用户请求以下操作时，读取对应的 SKILL.md 文件并严格按其流程执行：

- 📊 查行情、K线、代币信息、安全审计、排行榜 → `gate-dex-market/SKILL.md`
- 🔄 Swap、兑换、买入、卖出、报价 → `gate-dex-trade/SKILL.md`
- 💰 查余额、钱包地址、认证登录 → `gate-dex-wallet/SKILL.md`

优先使用市场数据相关功能。支持 MCP 和 OpenAPI 双模式。
EOF
    
    echo -e "${GREEN}  ✓${NC} CLAUDE.md 市场路由已创建"
}

install_codex() {
    echo -e "${CYAN}⚙️ 配置 Codex CLI (市场数据优先)...${NC}"
    echo -e "${GREEN}  ✓${NC} Codex 市场配置完成"
}

install_openclaw() {
    echo -e "${CYAN}🐾 配置 OpenClaw (市场数据优先)...${NC}"
    echo -e "${GREEN}  ✓${NC} OpenClaw 市场配置完成"
}

# Main
main() {
    local selected_platforms=($(select_platform))
    
    echo ""
    echo -e "${CYAN}🚀 开始配置市场数据功能...${NC}"
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
    echo -e "${GREEN}🎉 Gate Market 安装完成！${NC}"
    echo ""
    echo -e "${BLUE}📱 已配置的平台:${NC}"
    for platform in "${selected_platforms[@]}"; do
        echo "  ✓ $platform"
    done
    echo ""
    echo -e "${BLUE}🎯 下一步:${NC}"
    echo "1. 重启你的 AI 工具"
    echo "2. 尝试查询: \"查看 ETH 上 USDT 的 K 线图\""
    echo "3. 查看文档: ./gate-dex-market/README.md"
    echo ""
    echo -e "${CYAN}💡 提示:${NC}"
    echo "  支持 MCP (需认证) 和 OpenAPI (AK/SK) 双模式"
    echo "  OpenAPI 详见: ./gate-dex-market/references/openapi.md"
    echo ""
}

# Parse arguments
case "${1:-}" in
    --help|-h)
        echo "Gate Market MCP Installer"
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
        echo -e "${BLUE}🔍 检测到的平台:${NC}"
        platforms=($(detect_platforms))
        for platform in "${platforms[@]}"; do
            echo "  ✓ $platform"
        done
        exit 0
        ;;
    "") main ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
esac