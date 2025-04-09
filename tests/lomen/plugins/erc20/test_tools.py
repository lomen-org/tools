"""Tests for ERC20 plugin tools."""

from unittest.mock import MagicMock, patch

import pytest

from lomen.plugins.erc20 import ERC20Plugin
from lomen.plugins.erc20.tools import BlockNumberTool


def test_erc20_plugin_initialization():
    """Test ERC20Plugin initialization with valid credentials."""
    plugin = ERC20Plugin(credentials={"RPC_URL": "https://example.com"})
    assert plugin.name == "erc20"
    assert plugin.required_credentials == ["RPC_URL"]
    assert "BlockNumberTool" in [tool.__name__ for tool in plugin.tools]


def test_erc20_plugin_missing_credentials():
    """Test ERC20Plugin initialization fails with missing credentials."""
    with pytest.raises(ValueError) as excinfo:
        ERC20Plugin(credentials={})
    assert "Missing credentials" in str(excinfo.value)
    assert "RPC_URL" in str(excinfo.value)


@patch("lomen.plugins.erc20.tools.Web3")
def test_block_number_tool(mock_web3_class):
    """Test BlockNumberTool execution with mocked Web3."""
    # Setup mocks
    mock_web3 = MagicMock()
    mock_web3.eth.block_number = 12345678
    mock_web3.is_connected.return_value = True
    mock_web3_class.return_value = mock_web3
    mock_provider = MagicMock()
    mock_web3_class.HTTPProvider.return_value = mock_provider

    # Execute the tool
    result = BlockNumberTool.execute(
        BlockNumberTool.Params(), credentials={"RPC_URL": "https://example.com"}
    )

    # Verify the correct methods were called
    mock_web3_class.HTTPProvider.assert_called_once_with("https://example.com")
    mock_web3_class.assert_called_once_with(mock_provider)
    mock_web3.is_connected.assert_called_once()

    # Verify the result
    assert result == 12345678


@patch("lomen.plugins.erc20.tools.Web3")
def test_block_number_tool_connection_error(mock_web3_class):
    """Test BlockNumberTool handles connection errors."""
    # Setup mocks
    mock_web3 = MagicMock()
    mock_web3.is_connected.return_value = False
    mock_web3_class.return_value = mock_web3
    mock_provider = MagicMock()
    mock_web3_class.HTTPProvider.return_value = mock_provider

    # Try to execute the tool and expect an error
    with pytest.raises(ConnectionError) as excinfo:
        BlockNumberTool.execute(
            BlockNumberTool.Params(), credentials={"RPC_URL": "https://example.com"}
        )

    assert "Could not connect to node" in str(excinfo.value)
