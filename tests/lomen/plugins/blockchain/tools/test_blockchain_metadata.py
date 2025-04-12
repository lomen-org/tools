"""Tests for the Blockchain Metadata tool."""

import json
from unittest.mock import mock_open, patch

import pytest

from lomen.plugins.blockchain.tools.blockchain_metadata import (
    GetBlockchainMetadata,
    GetBlockchainMetadataParams,
)


def test_get_blockchain_metadata_params():
    """Test the parameters for the GetBlockchainMetadata tool."""
    params = GetBlockchainMetadataParams(chain_id=1)
    assert params.chain_id == 1


def test_get_blockchain_metadata_init():
    """Test initializing the GetBlockchainMetadata tool."""
    tool = GetBlockchainMetadata()
    assert tool.name == "get_blockchain_metadata"
    assert tool.get_params() == GetBlockchainMetadataParams


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_ethereum(mock_file, mock_path, blockchain_plugin):
    """Test running the GetBlockchainMetadata tool with Ethereum Mainnet."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data for Ethereum
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "1": {
            "name": "Ethereum Mainnet",
            "rpc": "https://ethereum-rpc.publicnode.com",
            "explorer": "https://etherscan.io",
            "currency": "ETH",
            "is_testnet": False,
            "is_poa": False
        }
    })
    
    # Get the tool from the plugin
    tool = blockchain_plugin.tools[0]
    
    # Run the tool
    result = tool.run(chain_id=1)
    
    # Verify the result
    assert result["name"] == "Ethereum Mainnet"
    assert result["rpc"] == "https://ethereum-rpc.publicnode.com"
    assert result["explorer"] == "https://etherscan.io"
    assert result["currency"] == "ETH"
    assert result["is_testnet"] is False
    assert result["is_poa"] is False
    assert result["chain_id"] == 1


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_base(mock_file, mock_path, blockchain_plugin):
    """Test running the GetBlockchainMetadata tool with Base."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data for Base
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "8453": {
            "name": "Base",
            "rpc": "https://mainnet.base.org",
            "explorer": "https://basescan.org",
            "currency": "ETH",
            "is_testnet": False,
            "is_poa": False
        }
    })
    
    # Get the tool from the plugin
    tool = blockchain_plugin.tools[0]
    
    # Run the tool
    result = tool.run(chain_id=8453)
    
    # Verify the result
    assert result["name"] == "Base"
    assert result["rpc"] == "https://mainnet.base.org"
    assert result["explorer"] == "https://basescan.org"
    assert result["currency"] == "ETH"
    assert result["is_testnet"] is False
    assert result["is_poa"] is False
    assert result["chain_id"] == 8453


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_polygon(mock_file, mock_path, blockchain_plugin):
    """Test running the GetBlockchainMetadata tool with Polygon."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data for Polygon
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "137": {
            "name": "Polygon",
            "rpc": "https://polygon-rpc.com",
            "explorer": "https://polygonscan.com",
            "currency": "MATIC",
            "is_testnet": False,
            "is_poa": True
        }
    })
    
    # Get the tool from the plugin
    tool = blockchain_plugin.tools[0]
    
    # Run the tool
    result = tool.run(chain_id=137)
    
    # Verify the result
    assert result["name"] == "Polygon"
    assert result["rpc"] == "https://polygon-rpc.com"
    assert result["explorer"] == "https://polygonscan.com"
    assert result["currency"] == "MATIC"
    assert result["is_testnet"] is False
    assert result["is_poa"] is True
    assert result["chain_id"] == 137


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_celo(mock_file, mock_path, blockchain_plugin):
    """Test running the GetBlockchainMetadata tool with Celo."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data for Celo
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "42220": {
            "name": "Celo",
            "rpc": "https://forno.celo.org",
            "explorer": "https://explorer.celo.org",
            "currency": "CELO",
            "is_testnet": False,
            "is_poa": True
        }
    })
    
    # Get the tool from the plugin
    tool = blockchain_plugin.tools[0]
    
    # Run the tool
    result = tool.run(chain_id=42220)
    
    # Verify the result
    assert result["name"] == "Celo"
    assert result["rpc"] == "https://forno.celo.org"
    assert result["explorer"] == "https://explorer.celo.org"
    assert result["currency"] == "CELO"
    assert result["is_testnet"] is False
    assert result["is_poa"] is True
    assert result["chain_id"] == 42220


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_optimism(mock_file, mock_path, blockchain_plugin):
    """Test running the GetBlockchainMetadata tool with Optimism."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data for Optimism
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "10": {
            "name": "Optimism",
            "rpc": "https://mainnet.optimism.io",
            "explorer": "https://optimistic.etherscan.io",
            "currency": "ETH",
            "is_testnet": False,
            "is_poa": False
        }
    })
    
    # Get the tool from the plugin
    tool = blockchain_plugin.tools[0]
    
    # Run the tool
    result = tool.run(chain_id=10)
    
    # Verify the result
    assert result["name"] == "Optimism"
    assert result["rpc"] == "https://mainnet.optimism.io"
    assert result["explorer"] == "https://optimistic.etherscan.io"
    assert result["currency"] == "ETH"
    assert result["is_testnet"] is False
    assert result["is_poa"] is False
    assert result["chain_id"] == 10


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_invalid_chain(mock_file, mock_path):
    """Test running the GetBlockchainMetadata tool with invalid chain ID."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "1": {
            "name": "Ethereum Mainnet",
            "rpc": "https://ethereum-rpc.publicnode.com",
        }
    })
    
    # Create the tool
    tool = GetBlockchainMetadata()
    
    # Run the tool with invalid chain ID and check for exception
    with pytest.raises(Exception) as excinfo:
        tool.run(chain_id=999)
    assert "Chain ID 999 not found or not supported" in str(excinfo.value)


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_string_chain_id(mock_file, mock_path):
    """Test GetBlockchainMetadata with chain ID that can't be converted to int."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with test data that includes a non-integer chain ID
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps({
        "testnet": {
            "name": "Test Network",
            "rpc": "https://test-network.example.org",
            "explorer": "https://explorer.test-network.example.org",
            "currency": "TEST",
            "is_testnet": True,
            "is_poa": True
        }
    })
    
    # Create the tool
    tool = GetBlockchainMetadata()
    
    # Run the tool with the string chain ID
    result = tool.run(chain_id="testnet")
    
    # Verify the result
    assert result["name"] == "Test Network"
    assert result["rpc"] == "https://test-network.example.org"
    assert result["chain_id"] == "testnet"  # Should keep it as a string


@patch("os.path.join")
@patch("builtins.open")
def test_get_blockchain_metadata_run_file_not_found(mock_file, mock_path):
    """Test running the GetBlockchainMetadata tool with missing chains file."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file to raise FileNotFoundError
    mock_file.side_effect = FileNotFoundError
    
    # Create the tool
    tool = GetBlockchainMetadata()
    
    # Run the tool and check for exception
    with pytest.raises(Exception) as excinfo:
        tool.run(chain_id=1)
    assert "Chains data file not found" in str(excinfo.value)


@patch("os.path.join")
@patch("builtins.open", new_callable=mock_open)
def test_get_blockchain_metadata_run_invalid_json(mock_file, mock_path):
    """Test running the GetBlockchainMetadata tool with invalid JSON."""
    # Set up mock path
    mock_path.return_value = "fake/path/chains.json"
    
    # Set up mock file with invalid JSON
    mock_file.return_value.__enter__.return_value.read.return_value = "{"
    
    # Create the tool
    tool = GetBlockchainMetadata()
    
    # Run the tool and check for exception
    with pytest.raises(Exception) as excinfo:
        tool.run(chain_id=1)
    assert "Invalid chains data file format" in str(excinfo.value)