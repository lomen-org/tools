"""
Example of using Lomen ERC20 tools with MCP (Model Completion Protocol).

This example demonstrates how to:
1. Initialize an ERC20 plugin
2. Convert the BlockNumberTool to MCP format using the official MCP package
3. Create an MCP server with FastAPI
4. Allow models to call the tools via the MCP protocol
"""

import os
import asyncio
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
import mcp
from mcp.fastapi import add_routes

from lomen.plugins.erc20 import ERC20Plugin
from lomen.adapters.mcp import MCPAdapter

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Lomen MCP Server")

# Initialize the ERC20 plugin with credentials
rpc_url = os.environ.get("ETHEREUM_RPC_URL", "https://eth-mainnet.alchemyapi.io/v2/your-api-key")

plugin = ERC20Plugin(credentials={
    "RPC_URL": rpc_url
})

# Convert tools to proper MCP Tool objects
mcp_tools = [MCPAdapter.create_mcp_tool(tool, plugin.credentials) for tool in plugin.tools]

# Create an MCP registry with our tools
registry = mcp.Registry()

# Register the tools with the MCP registry
for tool in mcp_tools:
    registry.register_tool(tool)

# Add MCP routes to the FastAPI app
add_routes(app, registry)

# Direct tool execution example
@app.get("/example/block-number")
async def example_block_number():
    """Example endpoint that directly executes the block number tool."""
    try:
        # Get the block number tool from the registry
        block_number_tool = registry.get_tool("erc20_block_number")
        if not block_number_tool:
            return {"error": "Block number tool not found in registry"}
            
        # Execute the tool
        result = await block_number_tool.function()
        return {"success": True, "block_number": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Information endpoint
@app.get("/info")
async def info():
    """Get information about the registered tools."""
    tools_info = []
    for tool_name in registry.get_tool_names():
        tool = registry.get_tool(tool_name)
        tools_info.append({
            "name": tool.name,
            "description": tool.description,
        })
    return {"tools": tools_info}

def main():
    """Run the example code."""
    print("\nLomen ERC20 Tool with MCP Example")
    print("----------------------------------")
    print("To run this example, set ETHEREUM_RPC_URL in your .env file.")
    print(f"\nInitializing ERC20Plugin with RPC URL: {rpc_url}")
    print("\nStarting MCP server on http://0.0.0.0:8000")
    print("\nMCP endpoints:")
    print("- GET /mcp/tools: Get all available tools")
    print("- GET /mcp/tools/{tool_name}: Get information about a specific tool")
    print("- POST /mcp/tools/{tool_name}: Execute a tool")
    print("\nCustom endpoints:")
    print("- GET /example/block-number: Example endpoint to get the current block number")
    print("- GET /info: Get information about the registered tools")
    print("\nPress Ctrl+C to stop the server")
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()