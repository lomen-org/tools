"""MCP adapter for Lomen tools."""

import inspect
from typing import Any, Dict, Type, List, Callable, get_type_hints
import json

import mcp
from pydantic import create_model, BaseModel

from ..plugins.base import BaseTool


class MCPAdapter:
    """Adapter to convert Lomen tools to MCP tools."""

    @staticmethod
    def convert(
        tool_cls: Type[BaseTool], credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert a Lomen tool to an MCP compatible tool dictionary.
        
        This adapter creates a dictionary representing an MCP tool from a Lomen tool class.
        Since we need to keep backward compatibility with tests, we return a dictionary
        with the same structure as before, containing:
        - name: The tool name
        - description: The tool description
        - parameters: JSON schema for the parameters
        - function: A callable function that executes the tool
        
        Args:
            tool_cls: The Lomen tool class to convert
            credentials: The credentials to use with the tool
            
        Returns:
            A dictionary compatible with MCP tool format
        """
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "") or f"Tool for {tool_name}"
        
        # Create a wrapper function that will receive parameters
        def execute_tool(params: Dict[str, Any] = None):
            """Execute the tool with the provided parameters."""
            # Create Params object if the tool expects it
            if hasattr(tool_cls, "Params"):
                params_obj = tool_cls.Params(**params) if params else tool_cls.Params()
                return tool_cls.execute(params_obj, credentials)
            else:
                # Direct execution if no Params class is defined
                return tool_cls.execute(params or {}, credentials)
        
        # Define parameter schema for the tool
        parameters = {"type": "object", "properties": {}, "required": []}
        
        if hasattr(tool_cls, "Params"):
            params_class = tool_cls.Params
            try:
                # Use Pydantic's built-in schema generation
                schema = params_class.model_json_schema()
                
                # Extract properties and required fields
                if "properties" in schema:
                    parameters["properties"] = schema.get("properties", {})
                if "required" in schema:
                    parameters["required"] = schema.get("required", [])
            except AttributeError:
                # Fallback for Pydantic v1
                schema = params_class.schema()
                if "properties" in schema:
                    parameters["properties"] = schema.get("properties", {})
                if "required" in schema:
                    parameters["required"] = schema.get("required", [])
        
        # Return the tool as a dictionary for backward compatibility
        return {
            "name": tool_name,
            "description": tool_description,
            "parameters": parameters,
            "function": execute_tool
        }
        
    @staticmethod
    def register_with_server(
        tool_cls: Type[BaseTool], credentials: Dict[str, Any], server
    ) -> None:
        """
        Register a Lomen tool directly with an MCP server.
        
        This uses the server's decorator pattern to register the tool,
        which is the recommended approach in the MCP documentation.
        
        Args:
            tool_cls: The Lomen tool class to register
            credentials: The credentials to use with the tool
            server: An MCP server instance (FastMCP)
            
        Returns:
            None
        """
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "") or f"Tool for {tool_name}"
        
        # Use the server's tool decorator to register the tool function
        @server.tool(name=tool_name, description=tool_description)
        async def tool_function(**kwargs):
            """Dynamic tool function for the MCP server."""
            # Create Params object if the tool expects it
            if hasattr(tool_cls, "Params"):
                params = tool_cls.Params(**kwargs) if kwargs else tool_cls.Params()
                result = tool_cls.execute(params, credentials)
            else:
                # Direct execution if no Params class is defined
                result = tool_cls.execute(kwargs, credentials)
            return result
        
        # The decorator registers the tool with the server
        # No return value needed
    
    @staticmethod
    def create_mcp_tool(
        tool_cls: Type[BaseTool], credentials: Dict[str, Any]
    ) -> mcp.Tool:
        """
        Create a proper MCP Tool object for use with the MCP server.
        
        This method creates a Tool object that follows the MCP protocol.
        
        Args:
            tool_cls: The Lomen tool class to convert
            credentials: The credentials to use with the tool
            
        Returns:
            An MCP Tool instance
        """
        tool_name = tool_cls.name
        tool_description = getattr(tool_cls, "__doc__", "") or f"Tool for {tool_name}"
        
        # Get parameter schema
        input_schema = {"type": "object", "properties": {}, "required": []}
        
        if hasattr(tool_cls, "Params"):
            params_class = tool_cls.Params
            try:
                # Use Pydantic's schema generation
                schema = params_class.model_json_schema()
                
                if "properties" in schema:
                    input_schema["properties"] = schema.get("properties", {})
                if "required" in schema:
                    input_schema["required"] = schema.get("required", [])
            except AttributeError:
                # Fallback for older Pydantic
                schema = params_class.schema()
                if "properties" in schema:
                    input_schema["properties"] = schema.get("properties", {})
                if "required" in schema:
                    input_schema["required"] = schema.get("required", [])
                    
        # Create async wrapper function
        async def async_tool(**kwargs):
            """Async wrapper for the tool execution."""
            if hasattr(tool_cls, "Params"):
                params = tool_cls.Params(**kwargs) if kwargs else tool_cls.Params()
                return tool_cls.execute(params, credentials)
            else:
                return tool_cls.execute(kwargs, credentials)
        
        # Create the Tool instance
        # The exact way to create a Tool depends on the MCP version, 
        # but inputSchema is required 
        return mcp.Tool(
            name=tool_name,
            description=tool_description,
            inputSchema=input_schema,
            func=async_tool
        )
