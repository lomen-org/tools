"""EVM RPC plugin for Lomen."""

from typing import List, Type

from ..base import BasePlugin, BaseTool

# Import after defining the class to avoid circular imports
from .tools import GetBlockNumberTool, GetBlockTool


class EvmRpcPlugin(BasePlugin):
    """Plugin for EVM RPC operations with Ethereum and other EVM-compatible blockchains.

    This plugin provides tools for interacting with EVM-based blockchains such as Ethereum,
    Polygon, Arbitrum, and others. It handles the connection to the blockchain via RPC
    and provides various tools for querying blockchain data.
    """

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "evm_rpc"

    @property
    def required_credentials(self) -> List[str]:
        """Return the required credentials for the plugin."""
        return []  # No required credentials, uses default RPC URL

    @property
    def tools(self) -> List[Type[BaseTool]]:
        """Return the tools provided by the plugin."""
        return [GetBlockNumberTool, GetBlockTool]
