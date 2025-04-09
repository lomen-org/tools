"""
Example of using Lomen ERC20 tools with LangGraph.

This example demonstrates how to:
1. Initialize an ERC20 plugin
2. Convert the BlockNumberTool to LangChain format
3. Use it in a simple LangGraph
"""

import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph

from lomen.plugins.erc20 import ERC20Plugin
from lomen.adapters.langchain import LangChainAdapter

# Load environment variables from .env file
load_dotenv()

# Initialize the ERC20 plugin with credentials
plugin = ERC20Plugin(credentials={
    "RPC_URL": os.environ.get("ETHEREUM_RPC_URL", "https://eth-mainnet.alchemyapi.io/v2/your-api-key")
})

# Convert tools to LangChain format
lc_tools = [LangChainAdapter.convert(tool, plugin.credentials) for tool in plugin.tools]

# Simple state type definition for the graph
class GraphState:
    messages: List[Any]
    tools: List[BaseTool]

# Create example functions for the LangGraph

def call_block_number_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    """Call the block number tool and add result to messages."""
    # Find the block number tool
    block_number_tool = next(tool for tool in state["tools"] if tool.name == "erc20_block_number")
    
    # Execute the tool
    result = block_number_tool.func()
    
    # Add result to the messages
    state["messages"].append(
        AIMessage(content=f"The current Ethereum block number is: {result}")
    )
    
    return state

def agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """Simple agent node that just routes to the block_number tool."""
    # This would normally be an LLM that decides what to do next
    return "get_block_number"  # Always route to get_block_number action

# Create a simple LangGraph
builder = StateGraph(GraphState)

# Add nodes
builder.add_node("agent", agent)
builder.add_node("get_block_number", call_block_number_tool)

# Add edges
builder.add_edge("agent", "get_block_number")
builder.add_edge("get_block_number", END)

# Compile the graph
graph = builder.compile()

# Initialize state
initial_state = {
    "messages": [HumanMessage(content="What's the current Ethereum block number?")],
    "tools": lc_tools
}

# Run the graph
result = graph.invoke(initial_state)

# Print final messages
for message in result["messages"]:
    print(f"{message.type}: {message.content}")


if __name__ == "__main__":
    print("\nLomen ERC20 Tool with LangGraph Example")
    print("----------------------------------------")
    print("To run this example, set ETHEREUM_RPC_URL in your .env file.")