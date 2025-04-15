"""Example of how YMCP would use the Lomen registry to access plugin metadata."""

import asyncio
import json
from lomen.registry import initialize_registry


async def ymcp_get_all_plugins():
    """Example of how YMCP would get a list of all plugins."""
    registry = initialize_registry()
    plugins = registry.list_plugins()

    print("Available Plugins:")
    print(json.dumps(plugins, indent=2))

    return plugins


async def ymcp_get_plugin_details(plugin_name):
    """Example of how YMCP would get details about a specific plugin."""
    registry = initialize_registry()
    details = registry.get_plugin_details(plugin_name)

    if details:
        print(f"Plugin Details for {plugin_name}:")
        print(json.dumps(details, indent=2))
    else:
        print(f"Plugin '{plugin_name}' not found")

    return details


async def ymcp_list_all_tools():
    """Example of how YMCP would get a list of all tools."""
    registry = initialize_registry()
    tools = registry.list_all_tools()

    print("Available Tools:")
    print(json.dumps(tools, indent=2))

    return tools


async def ymcp_execute_tool(plugin_name, tool_name, **params):
    """Example of how YMCP would execute a tool."""
    registry = initialize_registry()
    plugin = registry.get_plugin(plugin_name)

    if not plugin:
        print(f"Plugin '{plugin_name}' not found")
        return None

    # Find the tool
    tool = next((t for t in plugin.tools if t.name == tool_name), None)

    if not tool:
        print(f"Tool '{tool_name}' not found in plugin '{plugin_name}'")
        return None

    # Execute the tool
    try:
        result = await tool.arun(**params)
        print(f"Result from {plugin_name}.{tool_name}:")
        print(result)
        return result
    except Exception as e:
        print(f"Error executing {plugin_name}.{tool_name}: {str(e)}")
        return None


async def main():
    """Run examples of YMCP integration."""
    # Get all plugins
    await ymcp_get_all_plugins()
    print("\n" + "-" * 50 + "\n")

    # List all tools
    await ymcp_list_all_tools()
    print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
