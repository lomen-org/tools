"""Tests for MCP adapter."""

import asyncio
from typing import Any, Dict

from pydantic import BaseModel
import mcp

from lomen.adapters.mcp import MCPAdapter
from lomen.plugins.base import BaseTool


# This is a test model, not a test case - rename to fix the warning
class ParamsModel(BaseModel):
    """Parameters model for testing."""
    value: str


class TestTool(BaseTool):
    """Test tool for MCP adapter."""

    name = "test_tool"

    class Params(BaseModel):
        value: str

    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]) -> str:
        """Execute the test tool with params and credentials."""
        return f"Executed with {params.value} and {credentials['API_KEY']}"


def test_mcp_adapter_conversion():
    """Test MCP adapter correctly converts Lomen tools."""
    # Convert the tool to dictionary format (backward compatibility)
    tool_dict = MCPAdapter.convert(TestTool, {"API_KEY": "test_key"})

    # Verify the returned dictionary format
    assert isinstance(tool_dict, dict)
    assert tool_dict["name"] == "test_tool"
    assert "description" in tool_dict
    assert "parameters" in tool_dict
    assert "function" in tool_dict
    assert callable(tool_dict["function"])
    
    # Test execution
    result = tool_dict["function"]({"value": "test_value"})
    assert result == "Executed with test_value and test_key"
    
    # Test create_mcp_tool method (returns proper MCP Tool)
    mcp_tool = MCPAdapter.create_mcp_tool(TestTool, {"API_KEY": "test_key"})
    
    # Verify it's an instance of mcp.Tool
    assert isinstance(mcp_tool, mcp.Tool)
    assert mcp_tool.name == "test_tool"
    assert mcp_tool.description is not None
    
    # MCP Tool does not directly have a 'function' attribute
    # It's a proper Pydantic model with 'name', 'description', and 'inputSchema'
    assert mcp_tool.name == "test_tool"
    assert mcp_tool.description == "Test tool for MCP adapter."
    assert "value" in mcp_tool.inputSchema["properties"]
