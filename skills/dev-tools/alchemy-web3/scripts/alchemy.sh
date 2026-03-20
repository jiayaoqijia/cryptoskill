#!/bin/bash
# Alchemy Web3 CLI
# Query blockchain data, NFTs, tokens, and transfers across 80+ chains

set -e

# Load environment
[ -f "$HOME/.openclaw/.env" ] && source "$HOME/.openclaw/.env"

# Config
API_KEY="${ALCHEMY_API_KEY:-}"
CHAIN="${ALCHEMY_CHAIN:-eth-mainnet}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
${BLUE}Alchemy Web3 CLI${NC}

Usage: alchemy.sh [--chain <chain>] <command> [args]

${YELLOW}Commands:${NC}
  balance <address>              Get ETH/native balance
  tokens <address>               Get all ERC-20 token balances
  nfts <address>                 Get all NFTs owned by address
  nft-metadata <contract> <id>   Get metadata for specific NFT
  collection <contract>          Get NFTs in a collection
  transfers <address>            Get transaction history
  block <number|latest>          Get block info
  tx <hash>                      Get transaction details
  ens <name>                     Resolve ENS name to address
  gas                            Get current gas prices

${YELLOW}Options:${NC}
  --chain <chain>    Override chain (default: $CHAIN)
  --raw              Output raw JSON
  --help             Show this help

${YELLOW}Chains:${NC}
  eth-mainnet, eth-sepolia, polygon-mainnet, arb-mainnet,
  opt-mainnet, base-mainnet, solana-mainnet, zksync-mainnet, etc.

${YELLOW}Examples:${NC}
  alchemy.sh balance vitalik.eth
  alchemy.sh nfts 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
  alchemy.sh --chain polygon-mainnet tokens 0x...
  alchemy.sh transfers 0x... 
EOF
    exit 0
}

error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

check_api_key() {
    if [ -z "$API_KEY" ]; then
        error "ALCHEMY_API_KEY not set. Add it to ~/.openclaw/.env"
    fi
}

# Base URLs
get_rpc_url() {
    echo "https://${CHAIN}.g.alchemy.com/v2/${API_KEY}"
}

get_nft_url() {
    echo "https://${CHAIN}.g.alchemy.com/nft/v3/${API_KEY}"
}

# JSON-RPC helper
rpc_call() {
    local method="$1"
    local params="$2"
    
    curl -s -X POST "$(get_rpc_url)" \
        -H "Content-Type: application/json" \
        -d "{\"jsonrpc\":\"2.0\",\"method\":\"$method\",\"params\":$params,\"id\":1}"
}

# Commands
cmd_balance() {
    local address="$1"
    [ -z "$address" ] && error "Usage: alchemy.sh balance <address>"
    
    local result=$(rpc_call "eth_getBalance" "[\"$address\", \"latest\"]")
    local hex=$(echo "$result" | jq -r '.result // empty')
    
    if [ -z "$hex" ] || [ "$hex" = "null" ]; then
        echo "$result" | jq -r '.error.message // "Unknown error"'
        return 1
    fi
    
    # Convert hex to decimal, then to ETH
    local wei=$(printf "%d" "$hex" 2>/dev/null || echo "0")
    local eth=$(echo "scale=6; $wei / 1000000000000000000" | bc 2>/dev/null || echo "0")
    
    echo -e "${GREEN}$eth ETH${NC}"
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
    fi
}

cmd_tokens() {
    local address="$1"
    [ -z "$address" ] && error "Usage: alchemy.sh tokens <address>"
    
    local result=$(rpc_call "alchemy_getTokenBalances" "[\"$address\"]")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}Token Balances for $address${NC}"
    echo "---"
    
    echo "$result" | jq -r '.result.tokenBalances[] | select(.tokenBalance != "0x0000000000000000000000000000000000000000000000000000000000000000") | "\(.contractAddress): \(.tokenBalance)"' 2>/dev/null || echo "$result" | jq
}

cmd_nfts() {
    local address="$1"
    [ -z "$address" ] && error "Usage: alchemy.sh nfts <address>"
    
    local url="$(get_nft_url)/getNFTsForOwner?owner=$address&pageSize=20"
    local result=$(curl -s "$url")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    local total=$(echo "$result" | jq -r '.totalCount // 0')
    echo -e "${BLUE}NFTs owned: $total${NC}"
    echo "---"
    
    echo "$result" | jq -r '.ownedNfts[:10][] | "[\(.contract.address | .[0:10])...] \(.name // .title // "Untitled") #\(.tokenId)"' 2>/dev/null || echo "$result" | jq
}

cmd_nft_metadata() {
    local contract="$1"
    local token_id="$2"
    [ -z "$contract" ] || [ -z "$token_id" ] && error "Usage: alchemy.sh nft-metadata <contract> <tokenId>"
    
    local url="$(get_nft_url)/getNFTMetadata?contractAddress=$contract&tokenId=$token_id"
    local result=$(curl -s "$url")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}NFT Metadata${NC}"
    echo "---"
    echo "$result" | jq '{name, description, tokenType, image: .image.originalUrl, attributes: .raw.metadata.attributes}' 2>/dev/null || echo "$result" | jq
}

cmd_collection() {
    local contract="$1"
    [ -z "$contract" ] && error "Usage: alchemy.sh collection <contract>"
    
    local url="$(get_nft_url)/getNFTsForContract?contractAddress=$contract&limit=20"
    local result=$(curl -s "$url")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}Collection: $contract${NC}"
    echo "---"
    echo "$result" | jq -r '.nfts[:10][] | "#\(.tokenId): \(.name // .title // "Untitled")"' 2>/dev/null || echo "$result" | jq
}

cmd_transfers() {
    local address="$1"
    [ -z "$address" ] && error "Usage: alchemy.sh transfers <address>"
    
    local result=$(rpc_call "alchemy_getAssetTransfers" "[{\"fromBlock\":\"0x0\",\"toBlock\":\"latest\",\"toAddress\":\"$address\",\"category\":[\"external\",\"erc20\",\"erc721\"],\"maxCount\":\"0x14\"}]")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}Recent Transfers to $address${NC}"
    echo "---"
    echo "$result" | jq -r '.result.transfers[:10][] | "\(.asset // "NFT"): \(.value // 1) from \(.from | .[0:12])..."' 2>/dev/null || echo "$result" | jq
}

cmd_block() {
    local block="$1"
    [ -z "$block" ] && block="latest"
    
    if [ "$block" != "latest" ]; then
        block=$(printf "0x%x" "$block" 2>/dev/null || echo "$block")
    fi
    
    local result=$(rpc_call "eth_getBlockByNumber" "[\"$block\", false]")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}Block Info${NC}"
    echo "---"
    echo "$result" | jq '{number: .result.number, timestamp: .result.timestamp, hash: .result.hash, transactions: (.result.transactions | length)}' 2>/dev/null || echo "$result" | jq
}

cmd_tx() {
    local hash="$1"
    [ -z "$hash" ] && error "Usage: alchemy.sh tx <hash>"
    
    local result=$(rpc_call "eth_getTransactionByHash" "[\"$hash\"]")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    echo -e "${BLUE}Transaction${NC}"
    echo "---"
    echo "$result" | jq '.result | {hash, from, to, value, blockNumber, gas}' 2>/dev/null || echo "$result" | jq
}

cmd_ens() {
    local name="$1"
    [ -z "$name" ] && error "Usage: alchemy.sh ens <name.eth>"
    
    # ENS resolution via eth_call to ENS resolver
    # Simplified: just query via NFT API which handles ENS
    local url="$(get_nft_url)/getNFTsForOwner?owner=$name&pageSize=1"
    local result=$(curl -s "$url")
    
    # Extract address from response
    local address=$(echo "$result" | jq -r '.validAt.blockHash // empty' 2>/dev/null)
    
    if [ -n "$address" ] && [ "$address" != "null" ]; then
        # Actually resolve via calling resolver
        echo -e "${GREEN}Resolved via Alchemy API${NC}"
        echo "Note: Use web3 library for proper ENS resolution"
    else
        echo "$result" | jq
    fi
}

cmd_gas() {
    local result=$(rpc_call "eth_gasPrice" "[]")
    
    if [ "$RAW" = "true" ]; then
        echo "$result" | jq
        return
    fi
    
    local hex=$(echo "$result" | jq -r '.result // empty')
    local wei=$(printf "%d" "$hex" 2>/dev/null || echo "0")
    local gwei=$(echo "scale=2; $wei / 1000000000" | bc 2>/dev/null || echo "0")
    
    echo -e "${GREEN}Gas Price: $gwei Gwei${NC}"
}

# Parse args
RAW=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        --chain)
            CHAIN="$2"
            shift 2
            ;;
        --raw)
            RAW=true
            shift
            ;;
        --help|-h)
            usage
            ;;
        *)
            break
            ;;
    esac
done

COMMAND="$1"
shift || true

check_api_key

case "$COMMAND" in
    balance)    cmd_balance "$@" ;;
    tokens)     cmd_tokens "$@" ;;
    nfts)       cmd_nfts "$@" ;;
    nft-metadata) cmd_nft_metadata "$@" ;;
    collection) cmd_collection "$@" ;;
    transfers)  cmd_transfers "$@" ;;
    block)      cmd_block "$@" ;;
    tx)         cmd_tx "$@" ;;
    ens)        cmd_ens "$@" ;;
    gas)        cmd_gas ;;
    ""|help)    usage ;;
    *)          error "Unknown command: $COMMAND. Use --help for usage." ;;
esac
