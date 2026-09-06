#!/usr/bin/env python3
# SPDX-License-Identifier: LicenseRef-Blockscout
"""Helper script to find integration test files for MCP tools."""

import sys
from pathlib import Path

# Tool category mapping
TOOL_CATEGORIES = {
    # Address tools
    "get_address_info": "address",
    "get_tokens_by_address": "address",
    "nft_tokens_by_address": "address",
    # Block tools
    "get_block_info": "block",
    "get_block_number": "block",
    # Chain tools
    "get_chains_list": "chains",
    # Contract tools
    "get_contract_abi": "contract",
    "inspect_contract_code": "contract",
    "read_contract": "contract",
    # Transaction tools
    "get_transaction_info": "transaction",
    "get_transactions_by_address": "transaction",
    "get_token_transfers_by_address": "transaction",
    "transaction_summary": "transaction",
    # ENS tools
    "get_address_by_ens_name": "ens",
    # Search tools
    "lookup_token_by_symbol": "search",
    # Direct API tools
    "direct_api_call": "direct_api",
}


def find_integration_test(tool_name: str) -> tuple[str | None, str | None]:
    """
    Find the integration test file for a given tool name.

    Returns:
        A tuple of (file_path, error_message). If successful, error_message is None.
    """
    # Get the project root (assumes this script is in .claude/skills/test-guided-tool-run/scripts/)
    script_dir = Path(__file__).parent
    # Go up 4 levels: scripts -> test-guided-tool-run -> skills -> .claude -> project_root
    project_root = script_dir.parent.parent.parent.parent

    # Get the category for this tool
    category = TOOL_CATEGORIES.get(tool_name)
    if not category:
        available_tools = "\n  ".join(sorted(TOOL_CATEGORIES.keys()))
        return None, f"Unknown tool: {tool_name}\n\nAvailable tools:\n  {available_tools}"

    # Construct the expected test file path
    test_file = project_root / "tests" / "integration" / category / f"test_{tool_name}_real.py"

    if not test_file.exists():
        return None, f"Integration test file not found: {test_file}"

    return str(test_file), None


def print_usage():
    """Print usage information."""
    print("Usage: python find_test.py <tool_name>")
    print()
    print("Examples:")
    print("  python find_test.py get_transaction_info")
    print("  python find_test.py get_address_info")
    print("  python find_test.py lookup_token_by_symbol")
    print()
    print("Available tool categories:")
    categories = {}
    for tool, cat in sorted(TOOL_CATEGORIES.items()):
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(tool)

    for cat, tools in sorted(categories.items()):
        print(f"  {cat}:")
        for tool in tools:
            print(f"    - {tool}")


def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    tool_name = sys.argv[1]

    test_file, error = find_integration_test(tool_name)

    if error:
        print(f"Error: {error}", file=sys.stderr)
        print()
        print_usage()
        sys.exit(1)

    # Success - print the file path and helpful information
    print("Integration test file found:")
    print(f"  {test_file}")
    print()
    print("Next steps:")
    print(f"  1. Read the test file: cat {test_file}")
    print("  2. Or use the Read tool in Claude Code to examine it")
    print()
    print("Key things to look for in the test:")
    print("  - Import statements at the top")
    print("  - How mock_ctx is used (defined in tests/conftest.py)")
    print("  - Real test data (addresses, transaction hashes, etc.)")
    print("  - Expected response structure and assertions")
    print("  - Error handling patterns")
    print()
    print("Then create your test script in the scratchpad directory:")
    print("  /tmp/claude/.../scratchpad/test_your_tool.py")


if __name__ == "__main__":
    main()
