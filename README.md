# Lomen

Lomen is a plugin-based framework designed to simplify the integration and usage of blockchain/web3 tools within larger applications, particularly AI agents and language models. It provides a standardized structure for defining tools and offers adapters for popular frameworks like LangChain/LangGraph and the Model Context Protocol (MCP).

## Core Concepts

### Plugins (`BasePlugin`)

- **Purpose:** Group related tools under a common theme (e.g., EVM interactions, specific protocol tools).
- **Implementation:** Subclass `lomen.plugins.base.BasePlugin` and implement:
  - `name` (property): A unique string identifier for the plugin.
  - `tools` (property): A list of _instances_ of the tools provided by the plugin.

### Tools (`BaseTool`)

- **Purpose:** Represent individual actions or queries related to blockchains (e.g., get block number, fetch transaction).
- **Implementation:** Subclass `lomen.plugins.base.BaseTool` and implement:
  - `run`: The core execution logic of the tool. It takes specific arguments defined by its Pydantic schema.
  - `get_params`: Returns the Pydantic `BaseModel` class that defines the input parameters (`args_schema`) for the tool. This schema is used by adapters like LangChain for validation and function calling.
  - `name` (attribute): A string identifier for the tool (defaults to the class name if not set).
  - The `run` method's docstring is used as the tool's description by the adapters.

## Available Plugins

Lomen comes with the following built-in plugins:

1.  **Blockchain Plugin (`lomen.plugins.blockchain.BlockchainPlugin`)**

    - **Name:** `blockchain`
    - **Tools:**
      - `get_blockchain_metadata`: Retrieves metadata (RPC URL, explorer link, etc.) for various chains using their chain ID. Reads data from `chains.json`.

2.  **EVM RPC Plugin (`lomen.plugins.evm_rpc.EvmRpcPlugin`)**
    - **Name:** `evm_rpc`
    - **Tools:**
      - `get_block_number`: Fetches the latest block number from an EVM chain via its RPC URL.
      - `get_block`: Fetches detailed information about a specific block number from an EVM chain via its RPC URL. Handles POA chains.

## Installation

```bash
# It's recommended to install from source for now
git clone https://github.com/username/lomen.git
cd lomen
pip install .

# Or install specific extras if needed
# pip install .[dev]
```

_(Note: Update installation instructions once published to PyPI)_

## Requirements

Lomen requires Python 3.10+ and the following core dependencies (see `pyproject.toml` for specific versions):

- `pydantic`
- `langchain`
- `langgraph`
- `python-dotenv`
- `aiohttp`
- `web3`
- `mcp` (for the MCP adapter)
- `fastapi`, `uvicorn`, `starlette` (often used with MCP servers)

## Usage Examples

Lomen tools are primarily designed to be used via framework adapters.

### With LangChain / LangGraph

Use the `register_langchain_tools` adapter to convert Lomen plugin tools into LangChain `StructuredTool` objects.

```python
from lomen.plugins.blockchain import BlockchainPlugin
from lomen.plugins.evm_rpc import EvmRpcPlugin
from lomen.adapters.langchain import register_langchain_tools

# 1. Instantiate your desired plugins
blockchain_plugin = BlockchainPlugin()
evm_rpc_plugin = EvmRpcPlugin()

# 2. Register tools from plugins
lomen_plugins = [blockchain_plugin, evm_rpc_plugin]
langchain_tools = register_langchain_tools(lomen_plugins)

# 3. Use the tools with your LangChain agent or LangGraph
# Example (conceptual - requires agent setup):
# from langchain.agents import AgentExecutor, create_openai_tools_agent
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o", temperature=0)
# prompt = ... # Define your agent prompt
# agent = create_openai_tools_agent(llm, langchain_tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=langchain_tools, verbose=True)
# agent_executor.invoke({"input": "What is the block number for Ethereum mainnet?"})

print(f"Registered {len(langchain_tools)} LangChain tools.")
# You can inspect the tools:
# print(langchain_tools[0].name)
# print(langchain_tools[0].description)
# print(langchain_tools[0].args_schema.schema())
```

_(See the `examples/langgraph` directory for a runnable example)_

### With MCP (Model Context Protocol)

Use the `register_mcp_tools` adapter to add Lomen tools to a FastMCP server.

```python
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.transport.stdio import StdioServerTransport

from lomen.plugins.blockchain import BlockchainPlugin
from lomen.plugins.evm_rpc import EvmRpcPlugin
from lomen.adapters.mcp import register_mcp_tools

async def main():
    # 1. Instantiate your desired plugins
    blockchain_plugin = BlockchainPlugin()
    evm_rpc_plugin = EvmRpcPlugin()
    lomen_plugins = [blockchain_plugin, evm_rpc_plugin]

    # 2. Initialize MCP server
    mcp_server = FastMCP(
        server_info={"name": "lomen-mcp-server", "version": "0.1.0"},
        capabilities={"resources": {}, "tools": {}}, # Define capabilities
    )

    # 3. Register tools with the MCP server
    register_mcp_tools(server=mcp_server, plugins=lomen_plugins)

    print(f"Registered {len(mcp_server.tools)} MCP tools.")
    # You can list tools via MCP request or inspect:
    # print(list(mcp_server.tools.keys()))

    # 4. Run the MCP server (e.g., using stdio transport)
    transport = StdioServerTransport()
    print("Starting MCP server on stdio...")
    await mcp_server.connect(transport)
    await mcp_server.serve() # Keep server running

if __name__ == "__main__":
    # Note: Running asyncio like this might differ in production setups
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("MCP Server stopped.")

```

_(See the `examples/mcp` directory for a runnable example)_

## Creating Custom Plugins

Follow the structure defined in [Core Concepts](#core-concepts).

1.  **Create your Tool Class:** Subclass `BaseTool`, implement `run` and `get_params`. Define the `name` attribute.
2.  **Create your Plugin Class:** Subclass `BasePlugin`, implement `name` and `tools` properties. Instantiate your custom tools within the `tools` property list.

Example:

```python
from typing import List, Type
from pydantic import BaseModel, Field
from lomen.plugins.base import BasePlugin, BaseTool

# 1. Define Tool Parameters Schema
class MyToolParams(BaseModel):
    target_address: str = Field(..., description="The target wallet address")
    amount: float = Field(..., description="Amount to process")

# 2. Define the Tool
class MyCustomTool(BaseTool):
    name = "my_custom_tool" # Tool identifier

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return MyToolParams

    def run(self, target_address: str, amount: float):
        """
        This is the description used by adapters.
        It processes a transaction for the given address and amount.
        """
        # --- Tool implementation ---
        print(f"Executing MyCustomTool for {target_address} with amount {amount}")
        # Access credentials if needed (e.g., from environment variables)
        # import os
        # api_key = os.getenv("MY_PLUGIN_API_KEY")
        # if not api_key:
        #     raise ValueError("MY_PLUGIN_API_KEY not set")
        # ... use api_key ...
        result = {"status": "success", "address": target_address, "processed_amount": amount}
        # -------------------------
        return result

# 3. Define the Plugin
class MyPlugin(BasePlugin):
    @property
    def name(self) -> str:
        """Return the unique name of the plugin."""
        return "my_custom_plugin"

    @property
    def tools(self) -> List[BaseTool]:
        """Return a list of tool instances provided by this plugin."""
        # Instantiate the tools here
        return [MyCustomTool()]

# Now you can use MyPlugin with the adapters:
# my_plugin = MyPlugin()
# lc_tools = register_langchain_tools([my_plugin])
# register_mcp_tools(server=mcp_server, plugins=[my_plugin])
```

## Contributing

We welcome contributions to Lomen! Please see the [contributing guidelines](CONTRIBUTING.md) for more information.

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/username/lomen.git
cd lomen

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linters/formatters (configured in pyproject.toml)
ruff check .
black .
```

## License

MIT
