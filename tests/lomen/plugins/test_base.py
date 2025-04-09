"""Tests for base plugin functionality."""

from typing import List, Type

import pytest

from lomen.plugins.base import BasePlugin, BaseTool


class DummyTool(BaseTool):
    name = "dummy_tool"

    @classmethod
    def execute(cls, params, credentials):
        return "dummy_result"


class DummyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "dummy"

    @property
    def required_credentials(self) -> List[str]:
        return ["API_KEY"]

    @property
    def tools(self) -> List[Type[BaseTool]]:
        return [DummyTool]


def test_plugin_initialization():
    """Test that a plugin can be initialized with valid credentials."""
    plugin = DummyPlugin(credentials={"API_KEY": "test_key"})
    assert plugin.name == "dummy"
    assert plugin.required_credentials == ["API_KEY"]
    assert plugin.credentials == {"API_KEY": "test_key"}


def test_plugin_missing_credentials():
    """Test that plugin initialization fails with missing credentials."""
    with pytest.raises(ValueError) as excinfo:
        DummyPlugin(credentials={})
    assert "Missing credentials" in str(excinfo.value)


def test_plugin_tools():
    """Test that plugin tools are accessible."""
    plugin = DummyPlugin(credentials={"API_KEY": "test_key"})
    tools = plugin.tools
    assert len(tools) == 1
    assert tools[0].name == "dummy_tool"
