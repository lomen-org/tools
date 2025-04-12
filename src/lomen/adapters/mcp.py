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

            # Determine the execution function and description
            exec_func = None
            description = ""

            # Prefer arun if available (for async tools)
            if hasattr(tool_instance, "arun") and callable(tool_instance.arun):
                exec_func = tool_instance.arun
                description = tool_instance.arun.__doc__ or ""
            # Fallback to run (for sync tools)
            elif hasattr(tool_instance, "run") and callable(tool_instance.run):
                exec_func = tool_instance.run
                description = tool_instance.run.__doc__ or ""

            if exec_func:
                # Get schema if available (used by FastMCP for validation/metadata)
                schema = None
                if hasattr(tool_instance, "get_params") and callable(
                    tool_instance.get_params
                ):
                    # FastMCP expects the Pydantic model class itself
                    schema = tool_instance.get_params()

                # Register the tool with the determined function and schema
                # Pass the function as the first positional argument
                server.add_tool(
                    exec_func,
                    name=tool_name,
                    description=description,
                    # Remove the unexpected args_schema keyword argument
                    # Assume FastMCP infers schema from function type hints
                )
            else:
                print(
                    f"Warning: Tool '{tool_name}' from plugin '{plugin.name}' has no callable 'run' or 'arun' method."
                )

    return server
