from typing import List

from langchain_core.tools import StructuredTool

from lomen.plugins.base import BasePlugin


def register_langchain_tools(plugins: List[BasePlugin]) -> List[StructuredTool]:
    """
    Register tools from plugins to the LangChain structured tool.

    Args:
        plugins: A list of BasePlugin instances.

    Returns:
        A list of LangChain StructuredTool instances.
    """
    structured_tools: List[StructuredTool] = []

    def create_wrapper(instance):
        def wrapper(**kwargs):
            return instance.run(**kwargs)

        return wrapper

    for plugin in plugins:
        for tool_class in plugin.tools:
            tool_instance = tool_class  # Create an instance of the tool

            # Get schema if available
            schema = None
            if hasattr(tool_instance, "get_params") and callable(
                tool_instance.get_params
            ):
                schema = tool_instance.get_params()

            # Get description from docstring
            description = tool_instance.run.__doc__ or ""

            # Create wrapper for this specific instance's run method
            wrapper_func = create_wrapper(tool_instance)

            # Create the structured tool
            tool_name = getattr(tool_instance, "name", tool_instance.__class__.__name__)
            structured_tools.append(
                StructuredTool.from_function(
                    func=wrapper_func,
                    name=tool_name,
                    description=description,
                    args_schema=schema,
                    return_direct=False,
                    handle_tool_error=True,
                )
            )
    return structured_tools
