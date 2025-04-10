"""Blockchain plugin for Lomen."""

from typing import List, Type

from ..base import BasePlugin, BaseTool
from .tools import BlockchainMetadataTool


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
    def required_credentials(self) -> List[str]:
        """Return the required credentials for the plugin."""
        return []  # No required credentials

    @property
    def tools(self) -> List[Type[BaseTool]]:
        """Return the tools provided by the plugin."""
        return [BlockchainMetadataTool]