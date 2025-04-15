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
    def description(self) -> str:
        """Description of what the plugin does."""
        return "Provides access to 1inch Developer Portal API for blockchain data and portfolio tracking."

    @property
    def readme(self) -> str:
        """Detailed documentation for the plugin."""
        return """
# 1inch Plugin

This plugin provides access to the 1inch Developer Portal API, enabling tools for:
- Portfolio tracking across various EVM chains
- Token information retrieval
- NFT data access
- Domain resolution
- Protocol investment analysis
- Profit and loss calculations

## Setup

To use this plugin, you must set the `ONEINCH_API_KEY` environment variable with your 1inch Developer Portal API key.

```bash
export ONEINCH_API_KEY=your_api_key_here
```

## Tools

- `get_address_from_domain`: Resolves blockchain domains to wallet addresses
- `get_token_info_by_symbol`: Gets token information by its symbol
- `get_token_info_by_address`: Gets token information by its contract address
- `get_portfolio`: Gets portfolio data for a wallet on a specific chain
- `get_portfolio_all_chains`: Gets portfolio data for a wallet across all supported chains
- `get_profit_and_loss`: Gets profit/loss information for a wallet
- `get_protocol_investments`: Gets protocol investment data for a wallet
- `get_nfts_for_address`: Gets NFTs owned by a wallet

## Example

```python
from lomen.plugins.oneinch import OneInchPlugin

plugin = OneInchPlugin()
address_tool = plugin.tools[0]

# Resolve a domain
result = await address_tool.arun(domain="vitalik.eth")
print(f"Address: {result}")
```
"""

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
