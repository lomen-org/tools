"""Blockchain plugin for Lomen."""

from typing import List

from lomen.plugins.base import BasePlugin, BaseTool

from .tools.blockchain_metadata import GetBlockchainMetadata


class BlockchainPlugin(BasePlugin):
    """Plugin for blockchain metadata and utilities.

    This plugin provides tools for working with various blockchain networks,
    including retrieving network metadata like RPC URLs and explorer links.
    """

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "blockchain"

    @property
    def description(self) -> str:
        """Description of what the plugin does."""
        return "Provides tools for blockchain metadata and network information."

    @property
    def readme(self) -> str:
        """Detailed documentation for the plugin."""
        return """
# Blockchain Plugin

This plugin provides utilities and tools for working with various blockchain networks.
It currently includes functionality to retrieve metadata about supported blockchains,
such as RPC URLs, explorer links, and other network-specific information.

## Supported Networks

The plugin supports a wide range of EVM-compatible networks, including:
- Ethereum Mainnet
- Optimism
- BNB Smart Chain
- Polygon
- Arbitrum
- Avalanche
- Base
- Linea
- zkSync Era
- And various testnets

## Tools

- `get_blockchain_metadata`: Retrieves detailed metadata for a specific blockchain network

## Example

```python
from lomen.plugins.blockchain import BlockchainPlugin

plugin = BlockchainPlugin()
metadata_tool = plugin.tools[0]

# Get Ethereum mainnet metadata
result = await metadata_tool.arun(chain_id=1)
print(f"Network name: {result['name']}")
print(f"RPC URL: {result['rpc_url']}")
```
"""

    @property
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin."""
        return [GetBlockchainMetadata()]
