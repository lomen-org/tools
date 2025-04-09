"""Tests for LangChain adapter."""

from typing import Any, Dict

from pydantic import BaseModel

from lomen.adapters.langchain import LangChainAdapter
from lomen.plugins.base import BaseTool


class TestTool(BaseTool):
    """Test tool for LangChain adapter."""

    name = "test_tool"

    class Params(BaseModel):
        value: str

    @classmethod
    def execute(cls, params: Dict[str, Any], credentials: Dict[str, Any]) -> str:
        return f"Executed with {params['value']} and {credentials['API_KEY']}"


def test_langchain_adapter_conversion():
    """Test LangChain adapter correctly converts Lomen tools."""
    # Convert the tool
    lc_tool = LangChainAdapter.convert(TestTool, {"API_KEY": "test_key"})

    # Verify basic properties
    assert lc_tool.name == "test_tool"
    assert lc_tool.args_schema is not None

    # Test execution
    result = lc_tool.func(value="test_value")
    assert result == "Executed with test_value and test_key"
