"""ERC20 plugin for Lomen."""

from typing import List, Type

from ..base import BasePlugin, BaseTool
from .tools import BlockNumberTool


class ERC20Plugin(BasePlugin):
    """Plugin for ERC20-related operations."""

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "erc20"

    @property
    def required_credentials(self) -> List[str]:
        """Return the required credentials for the plugin."""
        return ["RPC_URL"]

    @property
    def tools(self) -> List[Type[BaseTool]]:
        """Return the tools provided by the plugin."""
        return [BlockNumberTool]
