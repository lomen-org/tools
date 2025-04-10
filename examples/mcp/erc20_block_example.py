"""
Example of using Lomen ERC20 tools with MCP (Model Context Protocol).

This example demonstrates how to:
1. Initialize an ERC20 plugin
2. Use the plugin's get_mcp_tools method to register tools with MCP
3. Create an MCP server with the FastMCP package
4. Allow models to call the tools via the MCP protocol
"""

import os
import asyncio
from typing import Any
from dotenv import load_dotenv

import uvicorn
from starlette.applications import Starlette
from mcp.server.fastmcp import FastMCP

from lomen.plugins.erc20 import ERC20Plugin

# Load environment variables from .env file
load_dotenv()

plugin = ERC20Plugin(
    credentials={
        "RPC_URL": os.environ.get("ETHEREUM_RPC_URL", "https://eth.llamarpc.com")
    }
)

# Initialize FastMCP server
mcp_server = FastMCP("lomen")

# Register tools with the MCP server using the plugin's get_mcp_tools method
plugin.get_mcp_tools(server=mcp_server)


def main():
    """Run the example code."""

    print(
        """
            {
                "mcpServers": {
                    "lomen": {
                        "command": "uv",
                        "args": [
                            "--directory",
                            "REPLACE_WITH_ABSOLUTE_PATH_TO_PROJECT",
                            "run",
                            "examples/mcp/erc20_block_example.py"
                        ]
                    }
                }
            }
            """
    )

    # Create and start the server with SSE transport
    # This will start a web server that Claude Code can connect to

    # Get the Starlette application
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
