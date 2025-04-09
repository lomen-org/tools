"""Base classes for Lomen plugins."""

from typing import Any, Dict, List, Type

from pydantic import BaseModel


class BaseTool:
    """Base class for all Lomen tools."""

    @classmethod
    @property
    def name(cls) -> str:
        """Name of the tool."""
        raise NotImplementedError

    @classmethod
    def execute(cls, params: BaseModel, credentials: Dict[str, Any]) -> Any:
        """Execute the tool with the given parameters and credentials."""
        raise NotImplementedError


class BasePlugin:
    """Base class for all Lomen plugins."""

    def __init__(self, credentials: Dict[str, Any]):
        """Initialize the plugin with the given credentials."""
        self.credentials = credentials
        self._validate_credentials()

    @property
    def name(self) -> str:
        """Name of the plugin."""
        raise NotImplementedError

    @property
    def required_credentials(self) -> List[str]:
        """List of required credential keys."""
        return []

    @property
    def tools(self) -> List[Type[BaseTool]]:
        """List of tools provided by the plugin."""
        raise NotImplementedError

    def _validate_credentials(self) -> None:
        """Validate that all required credentials are provided."""
        missing = [
            key for key in self.required_credentials if key not in self.credentials
        ]
        if missing:
            raise ValueError(f"Missing credentials: {missing}")
