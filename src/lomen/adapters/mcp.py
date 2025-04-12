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
        for tool_instance in plugin.tools:
            tool_name = getattr(tool_instance, "name", tool_instance.__class__.__name__)

            # All tools should now have 'arun', register it directly
            if hasattr(tool_instance, "arun") and callable(tool_instance.arun):
                exec_func = tool_instance.arun
                description = tool_instance.arun.__doc__ or ""

                # Register the arun method, relying on FastMCP introspection
                server.add_tool(
                    exec_func,
                    name=tool_name,
                    description=description,
                )
            else:
                print(
                    f"Warning: Tool '{tool_name}' from plugin '{plugin.name}' has no callable 'run' or 'arun' method."
                )

    return server
