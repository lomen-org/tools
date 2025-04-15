"""Example plugin implementation demonstrating description functions."""

from typing import List, Dict, Any
from .base import BasePlugin, BaseTool


class ExampleTool(BaseTool):
    @property
    def name(self) -> str:
        return "example_tool"

    @property
    def description(self) -> str:
        return "An example tool that demonstrates the metadata implementation."

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input_text": {
                    "type": "string",
                    "description": "Text input to process",
                },
                "option": {
                    "type": "string",
                    "enum": ["option1", "option2"],
                    "description": "Processing option to use",
                },
            },
            "required": ["input_text"],
        }

    async def arun(self, input_text: str, option: str = "option1") -> str:
        """Process the input text based on the selected option.

        Args:
            input_text: The text to process
            option: Processing option to use

        Returns:
            Processed text
        """
        if option == "option1":
            return input_text.upper()
        else:
            return input_text.lower()


class AnotherExampleTool(BaseTool):
    @property
    def name(self) -> str:
        return "another_example_tool"

    @property
    def description(self) -> str:
        return "Another example tool that demonstrates multiple tools in one plugin."

    def get_params(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "number": {"type": "integer", "description": "Number to process"}
            },
            "required": ["number"],
        }

    async def arun(self, number: int) -> int:
        """Double the input number.

        Args:
            number: The number to double

        Returns:
            Doubled number
        """
        return number * 2


class ExamplePlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "example_plugin"

    @property
    def description(self) -> str:
        return "An example plugin demonstrating the metadata implementation."

    @property
    def readme(self) -> str:
        return """
# Example Plugin

This plugin demonstrates how to implement the metadata functions in a Lomen plugin.

## Tools

- `example_tool`: Processes text input based on selected option
- `another_example_tool`: Doubles a number

## Usage

```python
from lomen.plugins.example_plugin import ExamplePlugin

plugin = ExamplePlugin()
result = await plugin.tools[0].arun(input_text="hello", option="option1")
print(result)  # Outputs: HELLO
```
"""

    @property
    def tools(self) -> List[BaseTool]:
        return [ExampleTool(), AnotherExampleTool()]
