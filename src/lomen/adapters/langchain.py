"""LangChain adapter for Lomen tools."""

from typing import Any, Dict, Type

from langchain.tools import Tool as LCTool

from ..plugins.base import BaseTool


class LangChainAdapter:
    """Adapter to convert Lomen tools to LangChain tools."""

    @staticmethod
    def convert(tool_cls: Type[BaseTool], credentials: Dict[str, Any]) -> LCTool:
        """Convert a Lomen tool to a LangChain tool."""
        # Define a new LangChain tool class
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "")
        tool_args_schema = getattr(tool_cls, "Params", None)

        # Create simple function for the tool
        def _run_tool(**kwargs):
            return tool_cls.execute(kwargs, credentials)

        # Create and return the LangChain tool
        return LCTool(
            name=tool_name,
            description=tool_description,
            args_schema=tool_args_schema,
            func=_run_tool,
        )
