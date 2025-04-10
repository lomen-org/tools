"""Main example using Lomen plugins with MCP."""

from mcp.server.fastmcp import FastMCP

# Import the plugins
from lomen.plugins.evm_rpc import EvmRpcPlugin
from lomen.plugins.blockchain import BlockchainPlugin

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Initialize the plugins - no credentials needed
evm_rpc_plugin = EvmRpcPlugin()
blockchain_plugin = BlockchainPlugin()

# Initialize the MCP server
mcp_server = FastMCP("lomen")

# Register all plugin tools with the MCP server
from lomen.adapters.mcp import MCPAdapter
MCPAdapter.get_mcp_tools([evm_rpc_plugin, blockchain_plugin], server=mcp_server)

if __name__ == "__main__":
    # Run the API with uvicorn
    mcp_server.run(transport="stdio")
