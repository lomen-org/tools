"""Main example using Lomen plugins with MCP."""

import os

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# Import the plugins
from lomen.plugins.evm_rpc import EvmRpcPlugin

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Initialize the plugins
evm_rpc_plugin = EvmRpcPlugin(credentials={"RPC_URL": os.getenv("RPC_URL")})

# Initialize the MCP server
mcp_server = FastMCP("lomen")

# Register all plugin tools with the MCP server
evm_rpc_plugin.get_mcp_tools(server=mcp_server)

if __name__ == "__main__":
    # Run the API with uvicorn
    mcp_server.run(transport="stdio")
