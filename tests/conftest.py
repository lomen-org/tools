"""Common test fixtures for Lomen tests."""

from unittest.mock import MagicMock

import pytest
from web3 import Web3

from lomen.plugins.blockchain import BlockchainPlugin
from lomen.plugins.evm_rpc import EvmRpcPlugin


@pytest.fixture
def blockchain_plugin():
    """Return a BlockchainPlugin instance."""
    return BlockchainPlugin()


@pytest.fixture
def evm_rpc_plugin():
    """Return an EvmRpcPlugin instance."""
    return EvmRpcPlugin()


@pytest.fixture
def mock_web3():
    """Create a mock Web3 instance."""
    mock = MagicMock(spec=Web3)
    mock.eth = MagicMock()
    mock.middleware_onion = MagicMock()
    return mock


@pytest.fixture
def sample_block_data():
    """Return sample block data for testing."""
    return {
        "number": 12345,
        "hash": "0x123456789abcdef",
        "parentHash": "0xabcdef123456789",
        "nonce": "0x1234567890abcdef",
        "sha3Uncles": "0x1234567890abcdef",
        "logsBloom": "0x",
        "transactionsRoot": "0x1234567890abcdef",
        "stateRoot": "0x1234567890abcdef",
        "receiptsRoot": "0x1234567890abcdef",
        "miner": "0x1234567890abcdef",
        "difficulty": 123456789,
        "totalDifficulty": 12345678901234567890,
        "extraData": b"example data",
        "size": 12345,
        "gasLimit": 12345678,
        "gasUsed": 1234567,
        "timestamp": 1234567890,
        "transactions": [],
        "uncles": []
    }