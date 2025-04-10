"""LangChain adapter for Lomen tools."""

from typing import Any, Dict, Type, Union

from langchain_core.tools import BaseTool, StructuredTool

from ..plugins.base import BaseTool as LomenBaseTool


class LangChainAdapter:
    """Adapter to convert Lomen tools to LangChain tools."""

    @staticmethod
    def convert(tool_cls: Type[LomenBaseTool], credentials: Dict[str, Any]) -> BaseTool:
        """Convert a Lomen tool to a LangChain tool."""
        # Define tool properties
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "")
        tool_args_schema = getattr(tool_cls, "Params", None)

        # Create function that will properly handle params
        def _execute_tool(**kwargs):
            # When using no args or empty args, create empty Params object
            if not kwargs:
                params = tool_cls.Params()
            else:
                params = tool_cls.Params(**kwargs)
            return tool_cls.execute(params, credentials)

        # Use StructuredTool which handles parameters correctly
        return StructuredTool(
            name=tool_name,
            description=tool_description,
            func=_execute_tool,
            args_schema=tool_args_schema,
        )
