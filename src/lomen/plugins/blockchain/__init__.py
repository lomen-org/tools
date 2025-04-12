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
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin."""
        return [GetBlockchainMetadata()]
