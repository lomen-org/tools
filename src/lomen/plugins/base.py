"""Base classes for Lomen plugins."""

import inspect
from typing import List, Dict, Any


class BaseTool:
    @property
    def name(self) -> str:
        """Name of the tool."""
        raise NotImplementedError("Subclasses must implement the 'name' property.")

    @property
    def description(self) -> str:
        """Description of what the tool does."""
        raise NotImplementedError(
            "Subclasses must implement the 'description' property."
        )

    def run(self, *args, **kwargs):
        raise NotImplementedError(
            "Use the asynchronous 'arun' method instead of 'run'."
        )

    async def arun(self, *args, **kwargs):
        """Asynchronous execution method (optional)."""
        # Default implementation raises error, subclasses can override.
        # We don't raise NotImplementedError immediately to allow checking hasattr(tool, 'arun')
        # without needing every tool to implement it if only sync is needed.
        raise NotImplementedError(
            "This tool does not support asynchronous execution via 'arun'."
        )

    def get_params(self) -> Dict[str, Any]:
        """Get the parameters schema for this tool.

        Returns:
            Dictionary describing the parameters required by this tool.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'get_params' method to define input schema."
        )


class BasePlugin:
    """Base class for all Lomen plugins."""

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        """Name of the plugin."""
        raise NotImplementedError("Subclasses must implement the 'name' property.")

    @property
    def description(self) -> str:
        """Description of what the plugin does."""
        raise NotImplementedError(
            "Subclasses must implement the 'description' property."
        )

    @property
    def readme(self) -> str:
        """Detailed documentation for the plugin."""
        return ""  # Optional, defaults to empty string

    @property
    def tools(self) -> List[BaseTool]:
        """List of tools provided by the plugin."""
        raise NotImplementedError("Subclasses must implement the 'tools' property.")

    def _get_serializable_params(self, tool: BaseTool) -> Dict[str, Any]:
        """Get serializable parameter schema from a tool.

        Args:
            tool: The BaseTool instance

        Returns:
            A JSON-serializable dictionary of the tool's parameters
        """
        params = tool.get_params()

        # Handle case where get_params returns a class (Pydantic model class)
        if inspect.isclass(params):
            try:
                # Try to get schema from Pydantic (v1 or v2)
                if hasattr(params, "schema"):
                    return params.schema()
                elif hasattr(params, "model_json_schema"):
                    return params.model_json_schema()
                else:
                    # Fallback for non-Pydantic classes
                    return {"type": "object", "properties": {}}
            except Exception:
                # If schema extraction fails, return empty schema
                return {"type": "object", "properties": {}}

        # Handle case where get_params returns a dict already
        return params

    def get_tool_details(self) -> List[Dict[str, Any]]:
        """Get details for all tools in this plugin.

        Returns:
            List of dictionaries containing tool name, description, and parameter schema.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": self._get_serializable_params(tool),
            }
            for tool in self.tools
        ]
