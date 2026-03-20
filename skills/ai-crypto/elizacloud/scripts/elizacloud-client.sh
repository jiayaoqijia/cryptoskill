#!/bin/bash

# elizaOS Cloud CLI Client
# Simple bash wrapper for elizaOS Cloud API

set -e

# Configuration
ELIZACLOUD_BASE_URL="${ELIZACLOUD_BASE_URL:-https://elizacloud.ai/api/v1}"
ELIZACLOUD_API_KEY="${ELIZACLOUD_API_KEY:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
error() {
    echo -e "${RED}Error:${NC} $1" >&2
    exit 1
}

success() {
    echo -e "${GREEN}Success:${NC} $1"
}

info() {
    echo -e "${BLUE}Info:${NC} $1"
}

warn() {
    echo -e "${YELLOW}Warning:${NC} $1"
}

check_api_key() {
    if [[ -z "$ELIZACLOUD_API_KEY" ]]; then
        error "ELIZACLOUD_API_KEY environment variable is required"
    fi
}

# Escape a string for safe JSON embedding
json_escape() {
    printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'
}

# Validate ID format (alphanumeric, hyphens, underscores only)
validate_id() {
    if [[ ! "$1" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        error "Invalid ID format: $1 (must be alphanumeric, hyphens, underscores)"
    fi
}

make_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local headers="$4"
    
    local curl_args=(
        -s
        -X "$method"
        -H "Authorization: Bearer $ELIZACLOUD_API_KEY"
        -H "Content-Type: application/json"
    )
    
    if [[ -n "$headers" ]]; then
        while IFS= read -r header; do
            [[ -n "$header" ]] && curl_args+=(-H "$header")
        done <<< "$headers"
    fi
    
    if [[ -n "$data" ]]; then
        curl_args+=(-d "$data")
    fi
    
    curl "${curl_args[@]}" "$ELIZACLOUD_BASE_URL$endpoint"
}

# Command handlers
cmd_status() {
    info "Checking elizaOS Cloud status..."
    
    # Try to get dashboard info
    local response
    response=$(make_request "GET" "/dashboard" 2>/dev/null)
    
    if [[ $? -eq 0 ]]; then
        success "elizaOS Cloud API is accessible"
        echo "Base URL: $ELIZACLOUD_BASE_URL"
        echo "API Key: configured"
    else
        error "Unable to connect to elizaOS Cloud API"
    fi
}

cmd_agents_list() {
    info "Listing your agents..."
    
    local response
    response=$(make_request "GET" "/my-agents/characters")
    
    if command -v jq >/dev/null 2>&1; then
        echo "$response" | jq -r '.data.characters[] | "\(.id) - \(.name) (\(.createdAt))"'
    else
        echo "$response"
    fi
}

cmd_agents_create() {
    local name="$1"
    local bio="$2"
    
    if [[ -z "$name" ]]; then
        error "Agent name is required. Usage: agents create <name> [bio]"
    fi
    
    info "Creating agent: $name"
    
    local safe_name
    safe_name=$(json_escape "$name")
    local data="{\"name\": \"$safe_name\""
    if [[ -n "$bio" ]]; then
        local safe_bio
        safe_bio=$(json_escape "$bio")
        data="$data, \"bio\": \"$safe_bio\""
    fi
    data="$data}"
    
    local response
    response=$(make_request "POST" "/app/agents" "$data")
    
    if command -v jq >/dev/null 2>&1; then
        local agent_id
        agent_id=$(echo "$response" | jq -r '.agent.id // empty')
        if [[ -n "$agent_id" ]]; then
            success "Agent created with ID: $agent_id"
        else
            error "Failed to create agent"
        fi
    else
        echo "$response"
    fi
}

cmd_agents_get() {
    local agent_id="$1"
    
    if [[ -z "$agent_id" ]]; then
        error "Agent ID is required. Usage: agents get <id>"
    fi
    validate_id "$agent_id"
    
    info "Getting agent: $agent_id"
    
    local response
    response=$(make_request "GET" "/my-agents/characters/$agent_id")
    
    if command -v jq >/dev/null 2>&1; then
        echo "$response" | jq '.data.character'
    else
        echo "$response"
    fi
}

cmd_agents_delete() {
    local agent_id="$1"
    
    if [[ -z "$agent_id" ]]; then
        error "Agent ID is required. Usage: agents delete <id>"
    fi
    validate_id "$agent_id"
    
    warn "This will permanently delete the agent. Continue? [y/N]"
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        info "Operation cancelled"
        return 0
    fi
    
    info "Deleting agent: $agent_id"
    
    local response
    response=$(make_request "DELETE" "/my-agents/characters/$agent_id")
    
    if [[ $? -eq 0 ]]; then
        success "Agent deleted"
    else
        error "Failed to delete agent"
    fi
}

cmd_chat() {
    local agent_id="$1"
    local message="$2"
    
    if [[ -z "$agent_id" || -z "$message" ]]; then
        error "Agent ID and message are required. Usage: chat <agent-id> <message>"
    fi
    
    info "Chatting with agent: $agent_id"
    
    validate_id "$agent_id"
    local safe_message
    safe_message=$(json_escape "$message")
    local data="{
        \"model\": \"$agent_id\",
        \"messages\": [{\"role\": \"user\", \"content\": \"$safe_message\"}]
    }"
    
    local response
    response=$(make_request "POST" "/chat/completions" "$data")
    
    if command -v jq >/dev/null 2>&1; then
        echo "$response" | jq -r '.choices[0].message.content // .error.message // "No response"'
    else
        echo "$response"
    fi
}

cmd_images_generate() {
    local prompt="$1"
    
    if [[ -z "$prompt" ]]; then
        error "Prompt is required. Usage: images generate <prompt>"
    fi
    
    info "Generating image: $prompt"
    
    local safe_prompt
    safe_prompt=$(json_escape "$prompt")
    local data="{
        \"prompt\": \"$safe_prompt\",
        \"model\": \"flux-pro\",
        \"width\": 1024,
        \"height\": 1024
    }"
    
    local response
    response=$(make_request "POST" "/images/generate" "$data")
    
    if command -v jq >/dev/null 2>&1; then
        local image_url
        image_url=$(echo "$response" | jq -r '.data[0].url // .error.message // "No image URL"')
        echo "Image URL: $image_url"
    else
        echo "$response"
    fi
}

# Help text
show_help() {
    cat << EOF
elizaOS Cloud CLI Client

Usage: $0 <command> [args...]

Commands:
    status                      Check API connectivity
    agents list                 List your agents
    agents create <name> [bio]  Create a new agent
    agents get <id>             Get agent details
    agents delete <id>          Delete an agent
    chat <agent-id> <message>   Chat with an agent
    images generate <prompt>    Generate an image

Environment Variables:
    ELIZACLOUD_API_KEY         Your elizaOS Cloud API key (required)
    ELIZACLOUD_BASE_URL        API base URL (default: https://elizacloud.ai/api/v1)

Examples:
    $0 status
    $0 agents create "Support Bot" "Customer support specialist"
    $0 chat agent-123 "Hello, how are you?"
    $0 images generate "A futuristic city"

EOF
}

# Main command router
main() {
    if [[ $# -eq 0 ]]; then
        show_help
        exit 1
    fi
    
    case "$1" in
        status)
            check_api_key
            cmd_status
            ;;
        agents)
            check_api_key
            case "$2" in
                list)
                    cmd_agents_list
                    ;;
                create)
                    cmd_agents_create "$3" "$4"
                    ;;
                get)
                    cmd_agents_get "$3"
                    ;;
                delete)
                    cmd_agents_delete "$3"
                    ;;
                *)
                    error "Unknown agents command: $2. Use 'list', 'create', 'get', or 'delete'"
                    ;;
            esac
            ;;
        chat)
            check_api_key
            cmd_chat "$2" "$3"
            ;;
        images)
            check_api_key
            case "$2" in
                generate)
                    cmd_images_generate "$3"
                    ;;
                *)
                    error "Unknown images command: $2. Use 'generate'"
                    ;;
            esac
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1. Use --help for usage information"
            ;;
    esac
}

# Run main function with all arguments
main "$@"