"""1inch plugin for Lomen."""

import os
from typing import List

from lomen.plugins.base import BasePlugin, BaseTool

# Import tools after they are defined to avoid circular imports
# (We will create these files next)
from .tools.get_address_from_domain import GetAddressFromDomain
from .tools.get_token_info import GetTokenInfoBySymbol, GetTokenInfoByAddress
from .tools.get_portfolio import GetPortfolio, GetPortfolioAllChains
from .tools.get_profit_and_loss import GetProfitAndLoss
from .tools.get_protocol_investments import GetProtocolInvestments
from .tools.get_nfts import GetNFTsForAddress


class OneInchPlugin(BasePlugin):
    """
    Plugin for interacting with the 1inch Developer Portal API.

    Provides tools for portfolio tracking, token information, NFT data,
    domain resolution, and more across various EVM chains.
    """

    API_KEY_ENV = "ONEINCH_API_KEY"

    def __init__(self):
        """Initializes the plugin by retrieving the API key from environment."""
        self.api_key = os.environ.get(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(
                f"{self.API_KEY_ENV} environment variable must be set for 1inch plugin."
            )
        super().__init__()  # Call parent initializer if needed, though BasePlugin's is empty

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "oneinch"

    @property
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin."""
        # Each tool will get its own API key from environment
        return [
            GetAddressFromDomain(),
            GetTokenInfoBySymbol(),
            GetTokenInfoByAddress(),
            GetPortfolio(),
            GetPortfolioAllChains(),
            GetProfitAndLoss(),
            GetProtocolInvestments(),
            GetNFTsForAddress(),
        ]
