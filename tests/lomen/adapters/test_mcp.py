"""Tests for the MCP adapter."""

from unittest.mock import MagicMock

from lomen.adapters.mcp import register_mcp_tools
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


def test_register_mcp_tools():
    """Test registering tools with MCP."""
    # Create a mock MCP server
    mock_server = MagicMock()
    mock_server.add_tool = MagicMock()
    
    # Create a test plugin
    plugin = MockPlugin()
    
    # Register the plugin with MCP
    server = register_mcp_tools(mock_server, [plugin])
    
    # Verify the tools were registered correctly
    assert server == mock_server
    # Check that add_tool was called once with the correct name and description
    assert mock_server.add_tool.call_count == 1
    args, _ = mock_server.add_tool.call_args
    assert args[1] == "test_tool"
    assert args[2] == "Test tool that does nothing."


def test_register_mcp_tools_multiple_plugins():
    """Test registering tools from multiple plugins."""
    # Create a mock MCP server
    mock_server = MagicMock()
    mock_server.add_tool = MagicMock()
    
    # Create mock plugins
    plugin1 = MagicMock(spec=BasePlugin)
    tool1 = MagicMock(spec=BaseTool)
    tool1.name = "tool1"
    tool1.run.__doc__ = "Tool 1 description"
    plugin1.tools = [tool1]
    
    plugin2 = MagicMock(spec=BasePlugin)
    tool2 = MagicMock(spec=BaseTool)
    tool2.name = "tool2"
    tool2.run.__doc__ = "Tool 2 description"
    plugin2.tools = [tool2]
    
    # Register the plugins with MCP
    server = register_mcp_tools(mock_server, [plugin1, plugin2])
    
    # Verify the tools were registered correctly
    assert server == mock_server
    assert mock_server.add_tool.call_count == 2
    
    # Check the arguments of the first call
    args1, _ = mock_server.add_tool.call_args_list[0]
    assert args1[1] == "tool1"
    assert args1[2] == "Tool 1 description"
    
    # Check the arguments of the second call
    args2, _ = mock_server.add_tool.call_args_list[1]
    assert args2[1] == "tool2"
    assert args2[2] == "Tool 2 description"