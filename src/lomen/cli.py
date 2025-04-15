#!/usr/bin/env python3
"""Command-line interface for running Lomen MCP server."""

import argparse
import asyncio
import os
import importlib
import sys
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn

from lomen.adapters.mcp import register_mcp_tools
from lomen.plugins.base import BasePlugin


def find_plugins() -> Dict[str, type]:
    """Find and return all available plugin classes."""
    from lomen.plugins import oneinch, blockchain, evm_rpc

    plugin_modules = [oneinch, blockchain, evm_rpc]
    plugins = {}

    for module in plugin_modules:
        for item_name in dir(module):
            item = getattr(module, item_name)
            try:
                if (
                    isinstance(item, type)
                    and issubclass(item, BasePlugin)
                    and item is not BasePlugin
                ):
                    plugins[item.__name__.lower().replace("plugin", "")] = item
            except TypeError:
                # Not a class or other type error
                continue

    return plugins


def instantiate_plugins(
    plugin_names: List[str], all_plugins: bool = False
) -> List[BasePlugin]:
    """Instantiate the requested plugins."""
    available_plugins = find_plugins()
    print(available_plugins)
    if all_plugins:
        plugin_names = list(available_plugins.keys())

    instances = []
    for name in plugin_names:
        if name not in available_plugins:
            print(f"Warning: Plugin '{name}' not found and will be skipped")
            continue

        plugin_class = available_plugins[name]

        try:
            # No API key needed - plugins get them from environment
            instance = plugin_class()
            instances.append(instance)
            print(f"Loaded plugin: {instance.name}")
        except Exception as e:
            print(f"Error initializing plugin '{name}': {e}")
    return instances


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Run Lomen MCP server with specified plugins and tools"
    )

    # Create mutually exclusive group for the plugin/tool selection options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Use all available plugins")
    group.add_argument(
        "--tools", type=str, help="Comma-separated list of tools to include"
    )
    group.add_argument(
        "--plugins", type=str, help="Comma-separated list of plugins to include"
    )

    # Server settings
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to listen on (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )

    args = parser.parse_args()

    # Initialize FastAPI app and MCP server
    server = FastMCP("Lomen MCP Server")

    # Load the appropriate plugins
    if args.all:
        plugins = instantiate_plugins([], all_plugins=True)
    elif args.plugins:
        plugin_names = [name.strip() for name in args.plugins.split(",")]
        plugins = instantiate_plugins(plugin_names)
    elif args.tools:
        # This would need a more complex implementation to find specific tools
        # For now, we'll just print an error and exit
        print("Tool-specific selection not yet implemented.")
        print("Please use --plugins to select specific plugins instead.")
        sys.exit(1)

    if not plugins:
        print(
            "Error: No plugins could be loaded. Please check your environment variables for API keys and try again."
        )
        sys.exit(1)
    print(plugins)
    # Register the plugin tools with the MCP server
    server = register_mcp_tools(server, plugins)

    server.run(transport="stdio")


if __name__ == "__main__":
    main()
