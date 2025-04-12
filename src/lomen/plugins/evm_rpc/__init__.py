"""EVM RPC plugin for Lomen."""

from typing import List

from ..base import BasePlugin, BaseTool
from .tools.get_block import GetBlock

# Import after defining the class to avoid circular imports
from .tools.get_block_number import GetBlockNumber


class EvmRpcPlugin(BasePlugin):
    """
    Plugin for interacting with EVM-compatible blockchains using RPC.

    This plugin provides tools for querying blockchain data, such as block numbers
    and details.
    """

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "evm_rpc"

    @property
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin."""
        return [GetBlockNumber(), GetBlock()]
