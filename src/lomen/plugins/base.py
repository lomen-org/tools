"""Base classes for Lomen plugins."""

from typing import List, Callable


class BasePlugin:
    """Base class for all Lomen plugins."""

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        """Name of the plugin."""
        raise NotImplementedError

    @property
    def tools(self) -> List[Callable]:
        """List of tools provided by the plugin."""
        raise NotImplementedError
