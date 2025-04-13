"""Base classes for Lomen plugins."""

from typing import List


class BaseTool:
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

    def get_params(self):
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
        raise NotImplementedError

    @property
    def tools(self) -> List[BaseTool]:
        """List of tools provided by the plugin."""
        raise NotImplementedError
