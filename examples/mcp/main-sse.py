import sys
import os  # Import os to access environment variables
from dotenv import load_dotenv  # Import load_dotenv

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

from lomen.adapters.mcp import register_mcp_tools
from lomen.plugins.blockchain import BlockchainPlugin
from lomen.plugins.evm_rpc import EvmRpcPlugin
from lomen.plugins.oneinch import OneInchPlugin  # Import the new plugin

# Create an MCP server instance with an identifier ("wiki")
mcp = FastMCP("Lomen")

# Set up the SSE transport for MCP communication.
sse = SseServerTransport("/messages/")


# Load environment variables from .env file in the current directory
load_dotenv()

# Get the API key from environment variable (will be populated by load_dotenv if .env exists)
oneinch_api_key = os.getenv("ONEINCH_API_KEY")
if not oneinch_api_key:
    print("Error: ONEINCH_API_KEY environment variable not set. 1inch tools will fail.")
    # Decide if you want to exit or continue without 1inch tools
    # For this example, we'll proceed but the tools will raise errors if called.
    # sys.exit("Exiting due to missing ONEINCH_API_KEY.")

# Instantiate all plugins
blockchain_plugin = BlockchainPlugin()
evm_rpc_plugin = EvmRpcPlugin()
# Pass the API key during instantiation if it exists
oneinch_plugin = OneInchPlugin(api_key=oneinch_api_key) if oneinch_api_key else None

# Register tools from all plugins
# Filter out the oneinch_plugin if the key was missing and it's None
active_plugins = [
    p for p in [blockchain_plugin, evm_rpc_plugin, oneinch_plugin] if p is not None
]
mcp = register_mcp_tools(mcp, active_plugins)


async def handle_sse(request: Request) -> None:
    _server = mcp._mcp_server
    try:
        # Create initialization options before entering SSE connection
        init_options = _server.create_initialization_options()

        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (reader, writer):
            await _server.run(reader, writer, init_options)
    except Exception as e:
        print(f"Error in SSE connection: {str(e)}")
        raise


# Create the Starlette app with two endpoints:
app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)


def start_server():
    """Start the uvicorn server with proper shutdown handling"""
    print("Starting server... Press Ctrl+C to stop")

    # We'll use standard uvicorn run without reload to have better control
    # over the shutdown process
    server = uvicorn.Server(
        uvicorn.Config(
            app="main-sse:app",
            host="localhost",
            port=8000,
            log_level="info",
            workers=1,
        )
    )

    # Use the uvicorn server's own signal handlers
    server.run()


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
