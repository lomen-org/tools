"""Plugin registry for discovering and accessing Lomen plugins."""

import importlib
import pkgutil
import inspect
from typing import Dict, List, Type, Any, Optional

from .plugins.base import BasePlugin


class PluginRegistry:
    """Registry for discovering and accessing Lomen plugins."""

    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def discover_plugins(self, package_name: str = "lomen.plugins") -> None:
        """Discover all plugins in the given package.

        Args:
            package_name: The package to search for plugins
        """
        package = importlib.import_module(package_name)

        for _, name, is_pkg in pkgutil.iter_modules(
            package.__path__, package.__name__ + "."
        ):
            if is_pkg:
                try:
                    module = importlib.import_module(name)
                    # Look for plugin classes in the module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, BasePlugin)
                            and attr is not BasePlugin
                        ):
                            # Instantiate the plugin and add it to the registry
                            plugin_instance = attr()
                            self._plugins[plugin_instance.name] = plugin_instance
                except (ImportError, AttributeError) as e:
                    # Skip modules that can't be imported or don't contain plugins
                    continue

    def register_plugin(self, plugin: BasePlugin) -> None:
        """Register a plugin instance.

        Args:
            plugin: The plugin instance to register
        """
        self._plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name.

        Args:
            name: The name of the plugin

        Returns:
            The plugin instance or None if not found
        """
        return self._plugins.get(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all registered plugins with their metadata.

        Returns:
            List of dictionaries containing plugin metadata
        """
        return [
            {
                "name": plugin.name,
                "description": plugin.description,
                "readme": plugin.readme,
                "tools_count": len(plugin.tools),
            }
            for plugin in self._plugins.values()
        ]

    def get_plugin_details(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin.

        Args:
            name: The name of the plugin

        Returns:
            Dictionary containing plugin details or None if not found
        """
        plugin = self.get_plugin(name)
        if not plugin:
            return None

        return {
            "name": plugin.name,
            "description": plugin.description,
            "readme": plugin.readme,
            "tools": plugin.get_tool_details(),
        }

    def _get_serializable_params(self, tool) -> Dict[str, Any]:
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

    def list_all_tools(self) -> List[Dict[str, Any]]:
        """List all tools from all plugins.

        Returns:
            List of dictionaries containing tool metadata
        """
        tools = []
        for plugin_name, plugin in self._plugins.items():
            for tool in plugin.tools:
                tools.append(
                    {
                        "plugin_name": plugin_name,
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": self._get_serializable_params(tool),
                    }
                )
        return tools


# Global registry instance
registry = PluginRegistry()


def initialize_registry():
    """Initialize the global registry by discovering all plugins."""
    registry.discover_plugins()
    return registry
