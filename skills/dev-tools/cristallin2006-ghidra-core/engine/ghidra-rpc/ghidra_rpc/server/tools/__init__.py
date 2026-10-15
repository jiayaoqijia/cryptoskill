"""Tool handlers for ghidra-rpc.

Each tool module registers its handlers with the server dispatcher.
"""

from ghidra_rpc.server.main import register_handler


def register_all_tools():
    """Register all tool command handlers."""
    from ghidra_rpc.server.tools import analysis
    from ghidra_rpc.server.tools import decompiler
    from ghidra_rpc.server.tools import search
    from ghidra_rpc.server.tools import xrefs
    from ghidra_rpc.server.tools import navigation
    from ghidra_rpc.server.tools import modifications
    from ghidra_rpc.server.tools import memory
    from ghidra_rpc.server.tools import disassembly
    from ghidra_rpc.server.tools import data_types
    from ghidra_rpc.server.tools import bookmarks
    from ghidra_rpc.server.tools import cfg
    from ghidra_rpc.server.tools import tags
    from ghidra_rpc.server.tools import version_tracking
    from ghidra_rpc.server.tools import processor_context
    from ghidra_rpc.server.tools import cpp
    from ghidra_rpc.server.tools import dsh_tools  # dsh-patch: custom tools
