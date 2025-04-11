"""EVM RPC plugin for Lomen."""

from typing import List, Callable, Dict, Optional, Any

from ..base import BasePlugin

# Import after defining the class to avoid circular imports
from .tools.get_block_number import get_block_number
from .tools.get_block import get_block


class EvmRpcPlugin(BasePlugin):

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "evm_rpc"

    @property
    def tools(self) -> List[Callable]:
        """Return the tools provided by the plugin."""
        return [get_block_number, get_block]
