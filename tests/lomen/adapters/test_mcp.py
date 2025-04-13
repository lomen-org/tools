"""Tests for the MCP adapter."""

from unittest.mock import MagicMock, AsyncMock

from lomen.adapters.mcp import register_mcp_tools
from lomen.plugins.base import BasePlugin, BaseTool


class MockTool(BaseTool):
    """Mock tool for testing."""

    name = "test_tool"

    async def arun(self, param1: str, param2: int):
        """Test tool that does nothing."""
        return {"result": f"{param1}_{param2}"}

    def get_params(self):
        """Return parameters for the tool."""
        return {
            "param1": {"title": "Param1", "type": "string"},
            "param2": {"title": "Param2", "type": "integer"},
        }


class MockPlugin(BasePlugin):
    """Mock plugin for testing."""

    name = "test_plugin"
    tools = [MockTool()]


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
    # Check that add_tool was called once
    assert mock_server.add_tool.call_count == 1
    # Check arguments passed to add_tool
    call_args = mock_server.add_tool.call_args
    # Check positional arg (the function)
    assert callable(call_args.args[0])
    # Check keyword args
    assert call_args.kwargs.get("name") == "test_tool"
    assert call_args.kwargs.get("description") == "Test tool that does nothing."


def test_register_mcp_tools_multiple_plugins():
    """Test registering tools from multiple plugins."""
    # Create a mock MCP server
    mock_server = MagicMock()
    mock_server.add_tool = MagicMock()

    # Create mock plugins
    plugin1 = MagicMock(spec=BasePlugin)
    tool1 = MagicMock(spec=BaseTool)
    tool1.name = "tool1"
    tool1.arun.__doc__ = "Tool 1 description"
    plugin1.tools = [tool1]

    plugin2 = MagicMock(spec=BasePlugin)
    tool2 = MagicMock(spec=BaseTool)
    tool2.name = "tool2"
    tool2.arun.__doc__ = "Tool 2 description"
    plugin2.tools = [tool2]

    # Register the plugins with MCP
    server = register_mcp_tools(mock_server, [plugin1, plugin2])

    # Verify the tools were registered correctly
    assert server == mock_server
    assert mock_server.add_tool.call_count == 2

    # Check the arguments of the first call
    call1_args = mock_server.add_tool.call_args_list[0]
    assert callable(call1_args.args[0])
    assert call1_args.kwargs.get("name") == "tool1"
    assert call1_args.kwargs.get("description") == "Tool 1 description"

    # Check the arguments of the second call
    call2_args = mock_server.add_tool.call_args_list[1]
    assert callable(call2_args.args[0])
    assert call2_args.kwargs.get("name") == "tool2"
    assert call2_args.kwargs.get("description") == "Tool 2 description"
