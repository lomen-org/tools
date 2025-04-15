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
    def description(self) -> str:
        """Description of what the plugin does."""
        return "Tools for interacting with EVM-compatible blockchains using JSON-RPC."

    @property
    def readme(self) -> str:
        """Detailed documentation for the plugin."""
        return """
# EVM RPC Plugin

This plugin provides tools for interacting with Ethereum Virtual Machine (EVM) compatible blockchains
using their JSON-RPC interfaces. It allows querying blockchain data such as blocks and transactions.

## Tools

- `get_block_number`: Retrieves the current block number from an EVM blockchain
- `get_block`: Retrieves detailed information about a specific block

## Usage

```python
from lomen.plugins.evm_rpc import EvmRpcPlugin

plugin = EvmRpcPlugin()
block_number_tool = plugin.tools[0]

# Get the current block number
result = await block_number_tool.arun(
    rpc_url="https://mainnet.infura.io/v3/YOUR_API_KEY",
    chain_id=1
)
print(f"Current block number: {result['block_number']}")
```
"""

    @property
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin."""
        return [GetBlockNumber(), GetBlock()]
