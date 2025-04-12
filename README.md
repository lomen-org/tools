# Lomen

Lomen is a plugin-based framework for managing blockchain/web3 tools. It provides a unified interface for different blockchain tools with framework adapters for LangChain and MCP.

## Features

- Plugin-based architecture for blockchain/web3 tools
- Credential management and validation
- Framework adapters (LangChain, MCP)
- Type hints and Pydantic validation

## Installation

```bash
pip install lomen
```

## Requirements

- Python 3.10+
- Pydantic >=2.0
- langchain >=0.1.0
- python-dotenv >=1.0.0
- aiohttp >=3.9.0
- web3 >=6.0.0

## Quick Start

```python
# Initialize a plugin with credentials
from lomen.plugins.evm_rpc import EVMRPCPlugin

plugin = EVMRPCPlugin(credentials={"RPC_URL": "https://your-rpc-url"})

# Get the current block number
from lomen.plugins.evm_rpc.tools import GetBlockNumberTool

block_number = GetBlockNumberTool.execute(
    GetBlockNumberTool.Params(),
    credentials={"RPC_URL": "https://your-rpc-url"}
)
print(f"Current block number: {block_number}")

# Use with LangChain
lc_tools = plugin.get_langchain_tools()

# Use with your LangChain agent or LangGraph
# agent = Agent(tools=lc_tools, ...)

# Use with MCP (Model Context Protocol)
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp_server = FastMCP("my_plugin")

# Register tools with the MCP server
plugin.get_mcp_tools(server=mcp_server)

# Run the MCP server
mcp_server.run(transport="stdio")  # or other transport methods
```

## Creating Custom Plugins

To create a custom plugin:

1. Subclass `BasePlugin` and implement the required methods
2. Create tools by implementing the `BaseTool` interface
3. Register your plugin and tools

Example:

```python
from typing import List, Type, Dict, Any
from pydantic import BaseModel, Field
from lomen.plugins.base import BasePlugin, BaseTool

class MyCustomTool(BaseTool):
    name = "my_custom_tool"
    
    class Params(BaseModel):
        param1: str = Field(..., description="Parameter description")
    
    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]):
        # Tool implementation
        return f"Result: {params.param1}"

class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "my_plugin"
    
    @property
    def required_credentials(self) -> List[str]:
        return ["API_KEY"]
    
    @property
    def tools(self) -> List[Type[BaseTool]]:
        return [MyCustomTool]
```

## Contributing

We welcome contributions to Lomen! Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/username/lomen.git
cd lomen

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT