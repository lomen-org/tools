"""Base classes for Lomen plugins."""

from typing import List


class BaseTool:
    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def get_params(self):
        raise NotImplementedError("Subclasses must implement this method")


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
