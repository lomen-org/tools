"""Tests for the GetBlockNumber tool."""

from unittest.mock import MagicMock, patch

import pytest

from lomen.plugins.evm_rpc.tools.get_block_number import (
    GetBlockNumber,
    GetBlockNumberParams,
)


def test_get_block_number_params():
    """Test the parameters for the GetBlockNumber tool."""
    params = GetBlockNumberParams(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
    )
    assert params.rpc_url == "https://ethereum-rpc.publicnode.com"
    assert params.chain_id == 1


def test_get_block_number_init():
    """Test initializing the GetBlockNumber tool."""
    tool = GetBlockNumber()
    assert tool.name == "get_block_number"
    assert tool.get_params() == GetBlockNumberParams


@patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3", autospec=True)
def test_get_block_number_run_ethereum(mock_web3_class):
    """Test running the GetBlockNumber tool on Ethereum Mainnet."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()
    
    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.block_number = 17000000
    
    # Create the tool
    tool = GetBlockNumber()
    
    # Run the tool
    result = tool.run(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
    )
    
    # Verify the result
    assert result["block_number"] == 17000000
    
    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://ethereum-rpc.publicnode.com")
    mock_web3_class.assert_called_once()


@patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3", autospec=True)
def test_get_block_number_run_base(mock_web3_class):
    """Test running the GetBlockNumber tool on Base."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()
    
    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.block_number = 5230000
    
    # Create the tool
    tool = GetBlockNumber()
    
    # Run the tool
    result = tool.run(
        rpc_url="https://mainnet.base.org",
        chain_id=8453,
    )
    
    # Verify the result
    assert result["block_number"] == 5230000
    
    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://mainnet.base.org")
    mock_web3_class.assert_called_once()


@patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3", autospec=True)
def test_get_block_number_run_polygon(mock_web3_class):
    """Test running the GetBlockNumber tool on Polygon."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()
    
    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.block_number = 50000000
    
    # Create the tool
    tool = GetBlockNumber()
    
    # Run the tool
    result = tool.run(
        rpc_url="https://polygon-rpc.com",
        chain_id=137,
    )
    
    # Verify the result
    assert result["block_number"] == 50000000
    
    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://polygon-rpc.com")
    mock_web3_class.assert_called_once()


@patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3", autospec=True)
def test_get_block_number_run_celo(mock_web3_class):
    """Test running the GetBlockNumber tool on Celo."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()
    
    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.block_number = 20920000
    
    # Create the tool
    tool = GetBlockNumber()
    
    # Run the tool
    result = tool.run(
        rpc_url="https://forno.celo.org",
        chain_id=42220,
    )
    
    # Verify the result
    assert result["block_number"] == 20920000
    
    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://forno.celo.org")
    mock_web3_class.assert_called_once()


@patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3", autospec=True)
def test_get_block_number_run_optimism(mock_web3_class):
    """Test running the GetBlockNumber tool on Optimism."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()
    
    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.block_number = 107000000
    
    # Create the tool
    tool = GetBlockNumber()
    
    # Run the tool
    result = tool.run(
        rpc_url="https://mainnet.optimism.io",
        chain_id=10,
    )
    
    # Verify the result
    assert result["block_number"] == 107000000
    
    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://mainnet.optimism.io")
    mock_web3_class.assert_called_once()


def test_get_block_number_run_with_exception():
    """Test running the GetBlockNumber tool with an exception."""
    # Create a patched version of Web3 that will raise an exception
    with patch("lomen.plugins.evm_rpc.tools.get_block_number.Web3") as mock_web3_class:
        # When Web3 is instantiated, it should raise an exception
        mock_web3_class.side_effect = Exception("Connection error")
        
        # Create the tool
        tool = GetBlockNumber()
        
        # Run the tool and verify it handles the exception properly
        with pytest.raises(Exception) as excinfo:
            tool.run(
                rpc_url="https://ethereum-rpc.publicnode.com",
                chain_id=1,
            )
        
        # Check the exception message
        assert "Failed to get block number" in str(excinfo.value)
        assert "Connection error" in str(excinfo.value)