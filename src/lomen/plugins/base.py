"""Base classes for Lomen plugins."""

from typing import Any, Dict, List, Type, Optional, Union

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

    def __init__(self, credentials: Optional[Dict[str, Any]] = None):
        """Initialize the plugin with the given credentials."""
        self.credentials = credentials or {}
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
    
    def get_langchain_tools(self):
        """
        Get tools in LangChain format.
        
        Returns a list of LangChain tools ready to use with LangChain 
        or LangGraph frameworks.
        
        Returns:
            List of LangChain tools
        """
        from ..adapters.langchain import LangChainAdapter
        return [LangChainAdapter.convert(tool, self.credentials) for tool in self.tools]
    
    def get_mcp_tools(self, server=None):
        """
        Get tools in MCP format.
        
        If a server is provided, registers tools directly with the server.
        Otherwise, returns a list of MCP Tool objects.
        
        Args:
            server: Optional MCP server to register tools with
            
        Returns:
            List of MCP Tool objects if server is None, otherwise None
        """
        from ..adapters.mcp import MCPAdapter
        
        # If server is provided, register tools directly
        if server:
            for tool_cls in self.tools:
                MCPAdapter.register_with_server(tool_cls, self.credentials, server)
            return None
            
        # Otherwise return MCP Tool objects
        return [MCPAdapter.create_mcp_tool(tool, self.credentials) for tool in self.tools]
