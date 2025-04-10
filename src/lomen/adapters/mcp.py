"""MCP adapter for Lomen tools."""

from typing import Any, Dict, Type

from ..plugins.base import BaseTool


class MCPAdapter:
    """Adapter to convert Lomen tools to MCP tools."""

    @staticmethod
    def convert(
        tool_cls: Type[BaseTool], credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert a Lomen tool to an MCP tool specification."""
        # Get tool properties
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "")
        tool_args_schema = getattr(tool_cls, "Params", None)
        
        # Create wrapper function to handle params correctly
        def _execute_tool(params: Dict[str, Any]):
            if params:
                params_obj = tool_cls.Params(**params)
            else:
                params_obj = tool_cls.Params()
            return tool_cls.execute(params_obj, credentials)
            
        # This is a simple implementation that could be enhanced
        # based on actual MCP requirements
        return {
            "name": tool_name,
            "description": tool_description,
            "parameters": {"type": "object", "properties": {}, "required": []},
            "function": _execute_tool,
        }
