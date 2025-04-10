"""Main example using Lomen plugins with MCP."""

from mcp.server.fastmcp import FastMCP

# Import the plugins
from lomen.plugins.evm_rpc import EvmRpcPlugin

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Initialize the plugins - no credentials needed for EVM RPC
evm_rpc_plugin = EvmRpcPlugin()

# Initialize the MCP server
mcp_server = FastMCP("lomen")

# Register all plugin tools with the MCP server
evm_rpc_plugin.get_mcp_tools(server=mcp_server)

if __name__ == "__main__":
    # Run the API with uvicorn
    mcp_server.run(transport="stdio")
