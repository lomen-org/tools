"""1inch plugin for Lomen."""

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

    Args:
        api_key: The API key for the 1inch Developer Portal.
    """

    def __init__(self, api_key: str):
        """Initializes the plugin with the necessary API key."""
        if not api_key:
            raise ValueError(
                "1inch API key must be provided during plugin initialization."
            )
        self.api_key = api_key
        super().__init__()  # Call parent initializer if needed, though BasePlugin's is empty

    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "oneinch"

    @property
    def tools(self) -> List[BaseTool]:
        """Return the tools provided by the plugin, initialized with the API key."""
        # Instantiate each tool and pass the stored API key
        return [
            GetAddressFromDomain(api_key=self.api_key),
            GetTokenInfoBySymbol(api_key=self.api_key),
            GetTokenInfoByAddress(api_key=self.api_key),
            GetPortfolio(api_key=self.api_key),
            GetPortfolioAllChains(api_key=self.api_key),
            GetProfitAndLoss(api_key=self.api_key),
            GetProtocolInvestments(api_key=self.api_key),
            GetNFTsForAddress(api_key=self.api_key),
        ]
