"""Tests for the GetBlock tool."""

from unittest.mock import MagicMock, patch

import pytest
from web3.middleware import ExtraDataToPOAMiddleware

from lomen.plugins.evm_rpc.tools.get_block import (
    GetBlock,
    GetBlockParams,
)


def test_get_block_params():
    """Test the parameters for the GetBlock tool."""
    params = GetBlockParams(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
        block_number=15000000,
        full_transactions=True,
        is_poa=False,
    )
    assert params.rpc_url == "https://ethereum-rpc.publicnode.com"
    assert params.chain_id == 1
    assert params.block_number == 15000000
    assert params.full_transactions is True
    assert params.is_poa is False


def test_get_block_init():
    """Test initializing the GetBlock tool."""
    tool = GetBlock()
    assert tool.name == "get_block"
    assert tool.get_params() == GetBlockParams


@pytest.fixture
def sample_block_data():
    """Sample block data for testing."""
    return {
        "difficulty": 123456789,
        "extraData": b"example data",
        "gasLimit": 12345678,
        "gasUsed": 1234567,
        "hash": "0x1234567890abcdef",
        "miner": "0xabcdef1234567890",
        "nonce": "0x1234567890abcdef",
        "number": 15000000,
        "parentHash": "0x0987654321fedcba",
        "receiptsRoot": "0xfedcba0987654321",
        "sha3Uncles": "0x1234567890abcdef",
        "size": 1000,
        "stateRoot": "0xabcdef1234567890",
        "timestamp": 1600000000,
        "totalDifficulty": "12345678901234567890",
        "transactions": [],
        "transactionsRoot": "0x1234567890abcdef",
        "uncles": [],
    }


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_ethereum(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool on Ethereum Mainnet."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = sample_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
        block_number=17000000,
        full_transactions=True,
        is_poa=False,
    )

    # Verify the result contains the expected block data
    assert result["number"] == sample_block_data["number"]
    assert result["hash"] == sample_block_data["hash"]
    assert result["extraData"] == sample_block_data["extraData"].hex()

    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with(
        "https://ethereum-rpc.publicnode.com"
    )
    mock_web3.eth.get_block.assert_called_once_with(17000000, full_transactions=True)


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_base(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool on Base."""
    # Modify sample data for Base
    base_block_data = dict(sample_block_data)
    base_block_data["number"] = 5230000

    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = base_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://mainnet.base.org",
        chain_id=8453,
        block_number=5230000,
        full_transactions=False,
        is_poa=False,
    )

    # Verify the result contains the expected block data
    assert result["number"] == 5230000
    assert result["hash"] == "0x1234567890abcdef"
    assert result["parentHash"] == "0x0987654321fedcba"

    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://mainnet.base.org")
    mock_web3.eth.get_block.assert_called_once_with(5230000, full_transactions=False)


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_polygon(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool on Polygon."""
    # Modify sample data for Polygon
    polygon_block_data = dict(sample_block_data)
    polygon_block_data["number"] = 50000000

    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = polygon_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://polygon-rpc.com",
        chain_id=137,
        block_number=50000000,
        full_transactions=False,
        is_poa=True,  # Polygon is a PoA chain
    )

    # Verify the result contains the expected block data
    assert result["number"] == 50000000
    assert result["hash"] == "0x1234567890abcdef"
    assert result["parentHash"] == "0x0987654321fedcba"

    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://polygon-rpc.com")
    mock_web3.eth.get_block.assert_called_once_with(50000000, full_transactions=False)
    # Verify middleware was injected for PoA
    mock_web3.middleware_onion.inject.assert_called_once()


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_celo(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool on Celo."""
    # Modify sample data for Celo
    celo_block_data = dict(sample_block_data)
    celo_block_data["number"] = 20920000

    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = celo_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://forno.celo.org",
        chain_id=42220,
        block_number=20920000,
        full_transactions=False,
        is_poa=True,  # Celo is a PoA chain
    )

    # Verify the result contains the expected block data
    assert result["number"] == 20920000
    assert result["hash"] == "0x1234567890abcdef"
    assert result["parentHash"] == "0x0987654321fedcba"

    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://forno.celo.org")
    mock_web3.eth.get_block.assert_called_once_with(20920000, full_transactions=False)
    # Verify middleware was injected for PoA
    mock_web3.middleware_onion.inject.assert_called_once()


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_optimism(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool on Optimism."""
    # Modify sample data for Optimism
    optimism_block_data = dict(sample_block_data)
    optimism_block_data["number"] = 107000000

    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = optimism_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://mainnet.optimism.io",
        chain_id=10,
        block_number=107000000,
        full_transactions=True,
        is_poa=False,
    )

    # Verify the result contains the expected block data
    assert result["number"] == 107000000
    assert result["hash"] == "0x1234567890abcdef"
    assert result["parentHash"] == "0x0987654321fedcba"

    # Verify the Web3 instance was created correctly
    mock_web3_class.HTTPProvider.assert_called_once_with("https://mainnet.optimism.io")
    mock_web3.eth.get_block.assert_called_once_with(107000000, full_transactions=True)


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_with_poa(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool with POA chain."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = sample_block_data

    # Create the tool
    tool = GetBlock()

    # Run the tool with is_poa=True
    await tool.arun(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
        block_number=15000000,
        full_transactions=False,
        is_poa=True,
    )

    # Verify the middleware was injected
    mock_web3.middleware_onion.inject.assert_called_once_with(
        ExtraDataToPOAMiddleware, layer=0
    )


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_with_byte_array_transactions(mock_web3_class, sample_block_data):
    """Test running the GetBlock tool with byte array transactions."""
    # Create a modified sample data with byte array in the transactions list
    block_data_with_bytes = dict(sample_block_data)
    block_data_with_bytes["transactions"] = [b"\x12\x34", b"\x56\x78", "0x9abc"]

    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.return_value = block_data_with_bytes

    # Create the tool
    tool = GetBlock()

    # Run the tool
    result = await tool.arun(
        rpc_url="https://ethereum-rpc.publicnode.com",
        chain_id=1,
        block_number=15000000,
        full_transactions=True,
        is_poa=False,
    )

    # Verify the transactions were properly converted from bytes to hex strings
    # Note: byte arrays will be converted to their hex representation
    assert "transactions" in result
    assert len(result["transactions"]) == 3
    assert isinstance(result["transactions"][0], str)
    assert isinstance(result["transactions"][1], str)
    assert isinstance(result["transactions"][2], str)
    # The third item was already a string and should remain unchanged
    assert result["transactions"][2] == "0x9abc"


@pytest.mark.asyncio
@patch("lomen.plugins.evm_rpc.tools.get_block.Web3", autospec=True)
async def test_get_block_run_with_exception(mock_web3_class):
    """Test running the GetBlock tool with an exception."""
    # Create mock instances
    mock_web3 = MagicMock()
    mock_provider = MagicMock()

    # Set up the mock hierarchy
    mock_web3_class.HTTPProvider.return_value = mock_provider
    mock_web3_class.return_value = mock_web3
    mock_web3.eth.get_block.side_effect = Exception("Block not found")

    # Create the tool
    tool = GetBlock()

    # Run the tool and check for exception
    with pytest.raises(Exception) as excinfo:
        await tool.arun(
            rpc_url="https://ethereum-rpc.publicnode.com",
            chain_id=1,
            block_number=15000000,
            full_transactions=False,
            is_poa=False,
        )
    assert "Failed to get block" in str(excinfo.value)
    assert "Block not found" in str(excinfo.value)
