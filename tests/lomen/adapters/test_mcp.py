"""Tests for MCP adapter."""

from typing import Any, Dict

from pydantic import BaseModel

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
    # Convert the tool
    mcp_tool = MCPAdapter.convert(TestTool, {"API_KEY": "test_key"})

    # Verify basic properties
    assert mcp_tool["name"] == "test_tool"
    assert "description" in mcp_tool
    assert "parameters" in mcp_tool
    assert "function" in mcp_tool

    # Test execution function
    result = mcp_tool["function"]({"value": "test_value"})
    assert result == "Executed with test_value and test_key"
