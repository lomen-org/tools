import sys

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

from lomen.adapters.mcp import register_mcp_tools
from lomen.plugins.blockchain import BlockchainPlugin
from lomen.plugins.evm_rpc import EvmRpcPlugin

# Create an MCP server instance with an identifier ("wiki")
mcp = FastMCP("Lomen")

# Set up the SSE transport for MCP communication.
sse = SseServerTransport("/messages/")


mcp = register_mcp_tools(mcp, [BlockchainPlugin(), EvmRpcPlugin()])


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
