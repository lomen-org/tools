from typing import List

from mcp.server.fastmcp import FastMCP

from lomen.plugins.base import BasePlugin


def register_mcp_tools(server: FastMCP, plugins: List[BasePlugin]) -> FastMCP:
    """
    Register tools from plugins to the MCP server.

    Args:
        server: The MCP server instance.
        plugins: A list of BasePlugin instances.

    Returns:
        The MCP server instance with the registered tools.
    """
    for plugin in plugins:
        for tool_interface in plugin.tools:
            description = ""
            if hasattr(tool_interface, "run") and callable(tool_interface.run):
                description = tool_interface.run.__doc__ or ""
            tool_name = getattr(
                tool_interface, "name", tool_interface.__class__.__name__
            )
            server.add_tool(tool_interface.run, tool_name, description)
    return server
