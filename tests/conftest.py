"""Pytest configuration for Lomen tests."""

from unittest.mock import Mock, patch

import pytest
from web3 import Web3


@pytest.fixture
def mock_web3():
    """Mock Web3 instance for testing."""
    mock = Mock(spec=Web3)
    # Create the eth attribute first
    mock.eth = Mock()
    mock.eth.block_number = 12345678
    mock.is_connected.return_value = True
    return mock


@pytest.fixture
def mock_web3_provider():
    """Patch Web3.HTTPProvider for testing."""
    with patch("web3.Web3.HTTPProvider") as mock_provider:
        mock_provider.return_value = "mock_provider"
        yield mock_provider


@pytest.fixture
def mock_web3_instance(mock_web3):
    """Patch Web3 instance for testing."""
    with patch("web3.Web3", return_value=mock_web3) as mock_web3_cls:
        yield mock_web3_cls
