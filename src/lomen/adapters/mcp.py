from mcp.server.fastmcp import FastMCP
from typing import List
from lomen.plugins.base import BasePlugin


def register_mcp_tools(server: FastMCP, plugins: List[BasePlugin]):
    for plugin in plugins:
        for tool in plugin.tools:
            server.add_tool(tool, tool.__name__, tool.__doc__)
    return server
