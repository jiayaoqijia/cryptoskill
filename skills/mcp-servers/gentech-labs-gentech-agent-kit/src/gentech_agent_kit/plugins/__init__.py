"""
GenTech Agent Kit Plugin Loader
Auto-discovers and registers tools from installed plugins.

When a new GenTech plugin is installed (e.g. gentech-defi-intel),
it registers itself here and the Agent Kit loads it automatically.
"""

from __future__ import annotations

import importlib
import json
import logging
import os
import pkgutil
from typing import Any

_LOG = logging.getLogger("gentech-kit.plugins")

# Plugin registry — each plugin exposes a `register(mcp)` function
# New plugins just add themselves here or drop a plugin.json in the plugins dir.

_PLUGIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")


def _discover_file_plugins() -> list[dict[str, Any]]:
    """Scan plugins/ directory for plugin.json manifests."""
    plugins = []
    if not os.path.isdir(_PLUGIN_DIR):
        return plugins
    for entry in sorted(os.listdir(_PLUGIN_DIR)):
        manifest_path = os.path.join(_PLUGIN_DIR, entry, "plugin.json")
        if os.path.isfile(manifest_path):
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                manifest["_path"] = os.path.dirname(manifest_path)
                plugins.append(manifest)
                _LOG.info("Discovered plugin: %s v%s", manifest.get("name", entry), manifest.get("version", "?"))
            except (json.JSONDecodeError, OSError) as exc:
                _LOG.warning("Failed to load plugin %s: %s", entry, exc)
    return plugins


def _discover_package_plugins() -> list[dict[str, Any]]:
    """Scan installed packages for gentech-* entry points."""
    plugins = []
    for mod_info in pkgutil.iter_modules():
        name = mod_info.name
        if not name.startswith("gentech_"):
            continue
        try:
            mod = importlib.import_module(name)
            plugin_info = getattr(mod, "__plugin_manifest__", None)
            if plugin_info:
                plugins.append(plugin_info)
                _LOG.info("Discovered package plugin: %s v%s", plugin_info.get("name", name), plugin_info.get("version", "?"))
        except Exception as exc:
            _LOG.debug("Skipped package %s: %s", name, exc)
    return plugins


def get_plugin_list() -> list[dict[str, Any]]:
    """Return all discovered plugins for the kit_info tool."""
    file_plugins = _discover_file_plugins()
    pkg_plugins = _discover_package_plugins()
    return file_plugins + pkg_plugins


def register_plugins(mcp: Any) -> None:
    """Load and register all plugins with the MCP server."""
    # File-based plugins
    for manifest in _discover_file_plugins():
        _try_register_plugin(mcp, manifest)

    # Package-based plugins
    for manifest in _discover_package_plugins():
        _try_register_plugin(mcp, manifest)


def _try_register_plugin(mcp: Any, manifest: dict[str, Any]) -> None:
    """Try to call a plugin's register function."""
    module_path = manifest.get("module")
    if not module_path:
        return
    try:
        mod = importlib.import_module(module_path)
        register_fn = getattr(mod, "register_gentech_plugin", None)
        if register_fn:
            register_fn(mcp)
            _LOG.info("Registered plugin: %s", manifest.get("name", module_path))
    except Exception as exc:
        _LOG.warning("Failed to register plugin %s: %s", manifest.get("name", module_path), exc)