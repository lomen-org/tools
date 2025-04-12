"""Tests for the LangChain adapter."""

from unittest.mock import MagicMock

from langchain_core.tools import StructuredTool

from lomen.adapters.langchain import register_langchain_tools
from lomen.plugins.base import BasePlugin, BaseTool


class MockTool(BaseTool):
    """Mock tool implementation for testing."""
    
    name = "test_tool"
    
    def run(self, param1: str, param2: int):
        """Test tool that does nothing."""
        return {"result": f"{param1}_{param2}"}
    
    def get_params(self):
        """Return parameters for the tool."""
        return {
            "param1": {"title": "Param1", "type": "string"},
            "param2": {"title": "Param2", "type": "integer"}
        }


class MockPlugin(BasePlugin):
    """Test plugin implementation."""
    
    # Override __init__ to avoid the warning
    def __init__(self):
        # No need to call super().__init__() since it's a pass in the base class
        pass
    
    @property
    def name(self) -> str:
        """Return the name of the plugin."""
        return "test"
    
    @property
    def tools(self):
        """Return the tools provided by the plugin."""
        return [MockTool()]


def test_register_langchain_tools():
    """Test registering tools with LangChain."""
    # Create a test plugin
    plugin = MockPlugin()
    
    # Register the plugin with LangChain
    tools = register_langchain_tools([plugin])
    
    # Verify the tools were registered correctly
    assert len(tools) == 1
    assert isinstance(tools[0], StructuredTool)
    assert tools[0].name == "test_tool"
    
    # Test calling the tool
    result = tools[0].invoke({"param1": "test", "param2": 123})
    assert result == {"result": "test_123"}


def test_register_langchain_tools_multiple_plugins():
    """Test registering tools from multiple plugins."""
    # Create mock plugins
    plugin1 = MagicMock(spec=BasePlugin)
    tool1 = MagicMock(spec=BaseTool)
    tool1.name = "tool1"
    tool1.run.__doc__ = "Tool 1 description"
    tool1.get_params.return_value = {"param": {"type": "string"}}
    tool1.run.return_value = "tool1_result"
    plugin1.tools = [tool1]
    
    plugin2 = MagicMock(spec=BasePlugin)
    tool2 = MagicMock(spec=BaseTool)
    tool2.name = "tool2"
    tool2.run.__doc__ = "Tool 2 description"
    tool2.get_params.return_value = {"param": {"type": "string"}}
    tool2.run.return_value = "tool2_result"
    plugin2.tools = [tool2]
    
    # Register the plugins with LangChain
    tools = register_langchain_tools([plugin1, plugin2])
    
    # Verify the tools were registered correctly
    assert len(tools) == 2
    assert tools[0].name == "tool1"
    assert tools[1].name == "tool2"