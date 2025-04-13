import pytest

from lomen.plugins.oneinch import OneInchPlugin
from lomen.plugins.oneinch.tools.get_address_from_domain import GetAddressFromDomain
from lomen.plugins.oneinch.tools.get_token_info import (
    GetTokenInfoBySymbol,
    GetTokenInfoByAddress,
)
from lomen.plugins.oneinch.tools.get_portfolio import (
    GetPortfolio,
    GetPortfolioAllChains,
)
from lomen.plugins.oneinch.tools.get_profit_and_loss import GetProfitAndLoss
from lomen.plugins.oneinch.tools.get_protocol_investments import GetProtocolInvestments
from lomen.plugins.oneinch.tools.get_nfts import GetNFTsForAddress

# Dummy API Key for testing plugin initialization
DUMMY_API_KEY = "test-plugin-api-key"


def test_plugin_initialization_success():
    """Test successful initialization of the OneInchPlugin."""
    plugin = OneInchPlugin(api_key=DUMMY_API_KEY)
    assert plugin.api_key == DUMMY_API_KEY


def test_plugin_initialization_no_api_key():
    """Test that initializing the plugin without an API key raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        OneInchPlugin(api_key="")  # Pass empty string
    assert "1inch API key must be provided" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo_none:
        OneInchPlugin(api_key=None)  # Pass None
    assert "1inch API key must be provided" in str(excinfo_none.value)


def test_plugin_name():
    """Test the plugin's name property."""
    plugin = OneInchPlugin(api_key=DUMMY_API_KEY)
    assert plugin.name == "oneinch"


def test_plugin_tools_property():
    """Test that the tools property returns instances of all expected tools."""
    plugin = OneInchPlugin(api_key=DUMMY_API_KEY)
    tools = plugin.tools

    expected_tool_types = [
        GetAddressFromDomain,
        GetTokenInfoBySymbol,
        GetTokenInfoByAddress,
        GetPortfolio,
        GetPortfolioAllChains,
        GetProfitAndLoss,
        GetProtocolInvestments,
        GetNFTsForAddress,
    ]

    assert len(tools) == len(expected_tool_types)

    # Check that each tool in the list is an instance of the expected type
    # and that the API key was passed correctly
    for tool_instance, expected_type in zip(tools, expected_tool_types):
        assert isinstance(tool_instance, expected_type)
        assert hasattr(tool_instance, "api_key")
        assert tool_instance.api_key == DUMMY_API_KEY
