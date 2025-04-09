"""
Example of using Lomen ERC20 tools with MCP (Model Completion Protocol).

This example demonstrates how to:
1. Initialize an ERC20 plugin
2. Convert the BlockNumberTool to MCP format
3. Print the MCP specification (which would be used with an MCP-compatible framework)
"""

import os
import json
from dotenv import load_dotenv

from lomen.plugins.erc20 import ERC20Plugin
from lomen.adapters.mcp import MCPAdapter

# Load environment variables from .env file
load_dotenv()

def main():
    """Run the example code."""
    print("\nLomen ERC20 Tool with MCP Example")
    print("----------------------------------")
    print("To run this example, set ETHEREUM_RPC_URL in your .env file.")
    
    # Initialize the ERC20 plugin with credentials
    rpc_url = os.environ.get("ETHEREUM_RPC_URL", "https://eth-mainnet.alchemyapi.io/v2/your-api-key")
    print(f"\nInitializing ERC20Plugin with RPC URL: {rpc_url}")
    
    plugin = ERC20Plugin(credentials={
        "RPC_URL": rpc_url
    })
    
    # Convert tools to MCP format
    mcp_tools = [MCPAdapter.convert(tool, plugin.credentials) for tool in plugin.tools]
    
    # Print MCP tool specifications
    print("\nMCP Tool Specifications:")
    print("------------------------")
    for tool in mcp_tools:
        print(f"\nTool Name: {tool['name']}")
        print(f"Description: {tool['description']}")
        print("Parameters:")
        print(json.dumps(tool['parameters'], indent=2))
    
    # Example of using the tool (this would be handled by the MCP framework)
    print("\nExample Usage:")
    print("-------------")
    # Find the block number tool
    block_number_tool = next(tool for tool in mcp_tools if tool['name'] == "erc20_block_number")
    
    try:
        # Execute the tool
        print("Calling erc20_block_number tool...")
        result = block_number_tool['function']({})
        print(f"Current Ethereum block number: {result}")
    except Exception as e:
        print(f"Error executing tool: {e}")
        print("Note: You need a valid RPC URL to run this example")
    
    print("\nIn a real MCP implementation, these tools would be registered with")
    print("an MCP-compatible framework, allowing the model to call them directly.")

if __name__ == "__main__":
    main()