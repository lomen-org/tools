# Lomen Examples

This directory contains examples demonstrating how to use Lomen with different frameworks.

## Setup

1. Create a `.env` file in the root directory based on `.env.example`
2. Add your API keys and endpoints to the `.env` file

## Examples

### LangGraph Examples

The `langgraph` directory contains examples of using Lomen with LangGraph:

- `erc20_block_example.py`: Demonstrates how to use the ERC20 BlockNumberTool with LangGraph
  - Run with: `python examples/langgraph/erc20_block_example.py`

### MCP Examples

The `mcp` directory contains examples of using Lomen with Model Completion Protocol (MCP):

- `erc20_block_example.py`: Demonstrates how to use the ERC20 BlockNumberTool with MCP
  - Run with: `python examples/mcp/erc20_block_example.py`

## Additional Requirements

These examples require additional dependencies:

```bash
uv add langchain_core langgraph python-dotenv
```