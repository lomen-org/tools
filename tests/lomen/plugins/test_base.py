"""Tests for the base plugin module."""

from unittest.mock import MagicMock

import pytest

from lomen.plugins.base import BasePlugin, BaseTool


def test_base_tool():
    """Test BaseTool abstract methods."""
    tool = BaseTool()
    
    # Test that run method raises NotImplementedError
    with pytest.raises(NotImplementedError) as excinfo:
        tool.run("test")
    assert "Subclasses must implement this method" in str(excinfo.value)
    
    # Test that get_params method raises NotImplementedError
    with pytest.raises(NotImplementedError) as excinfo:
        tool.get_params()
    assert "Subclasses must implement this method" in str(excinfo.value)


def test_base_plugin():
    """Test BasePlugin abstract methods."""
    plugin = BasePlugin()
    
    # Test that name property raises NotImplementedError
    with pytest.raises(NotImplementedError) as excinfo:
        _ = plugin.name
    assert "NotImplementedError" in str(excinfo.type)
    
    # Test that tools property raises NotImplementedError
    with pytest.raises(NotImplementedError) as excinfo:
        _ = plugin.tools
    assert "NotImplementedError" in str(excinfo.type)


class ConcretePlugin(BasePlugin):
    """Concrete implementation of BasePlugin for testing."""
    
    @property
    def name(self):
        return "test_plugin"
    
    @property
    def tools(self):
        return [MagicMock(spec=BaseTool)]


def test_concrete_plugin():
    """Test concrete implementation of BasePlugin."""
    plugin = ConcretePlugin()
    
    # Test that name property returns the expected value
    assert plugin.name == "test_plugin"
    
    # Test that tools property returns a list of tools
    tools = plugin.tools
    assert isinstance(tools, list)
    assert len(tools) == 1


def test_blockchain_plugin():
    """Test BlockchainPlugin implementation."""
    from lomen.plugins.blockchain import BlockchainPlugin
    
    plugin = BlockchainPlugin()
    
    # Test that name property returns the expected value
    assert plugin.name == "blockchain"
    
    # Test that tools property returns a list of tools
    tools = plugin.tools
    assert isinstance(tools, list)
    assert len(tools) == 1


def test_evm_rpc_plugin():
    """Test EvmRpcPlugin implementation."""
    from lomen.plugins.evm_rpc import EvmRpcPlugin
    
    plugin = EvmRpcPlugin()
    
    # Test that name property returns the expected value
    assert plugin.name == "evm_rpc"
    
    # Test that tools property returns a list of tools
    tools = plugin.tools
    assert isinstance(tools, list)
    assert len(tools) == 2