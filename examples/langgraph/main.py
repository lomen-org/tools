"""Main example using Lomen plugins with LangGraph and OpenAI."""

import asyncio
import os
from typing import Annotated, List, Sequence, TypedDict

from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor, tools_condition

# Import the plugins
from lomen.plugins.evm_rpc import EvmRpcPlugin
from lomen.plugins.blockchain import BlockchainPlugin

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Make sure OPENAI_API_KEY is set in your .env file or environment variables

# Define the state for the agent
class AgentState(TypedDict):
    """State for the agent."""
    messages: Annotated[List, "Messages sent so far"]
    tools: Annotated[Sequence[BaseTool], "Tools the agent has access to"]


# Initialize the plugins - no credentials needed
evm_rpc_plugin = EvmRpcPlugin()
blockchain_plugin = BlockchainPlugin()

# Get all tools in LangChain format
from lomen.adapters.langchain import LangChainAdapter
all_tools = LangChainAdapter.get_langchain_tools([evm_rpc_plugin, blockchain_plugin])

# Define a custom system prompt for the chain
PROMPT = """You are an expert blockchain assistant specializing in various blockchain networks. 
You have access to the following tools:

{tools}

To use a tool, use the following format:

```
<tool_name>: <tool_input>
```

Where tool_input is a JSON object with the tool's parameters.

For EVM tools that require chain information, first use the blockchain_metadata tool with the chain ID 
to get the appropriate RPC URL, and then use that information with the EVM tools.

Here are all supported blockchain networks and their chain IDs:

Mainnets:
- 1: Ethereum Mainnet (ETH)
- 10: Optimism (ETH)
- 25: Cronos Mainnet (CRO)
- 56: BNB Smart Chain (BNB)
- 100: Gnosis Chain (xDAI)
- 137: Polygon (MATIC)
- 324: zkSync Era (ETH)
- 5000: Mantle (MNT)
- 8453: Base (ETH)
- 42161: Arbitrum One (ETH)
- 42220: Celo (CELO)
- 43114: Avalanche C-Chain (AVAX)
- 59144: Linea (ETH)
- 534352: Scroll (ETH)

Testnets:
- 5: Goerli Testnet (ETH)
- 97: BNB Smart Chain Testnet (BNB)
- 11155111: Sepolia Testnet (ETH)
- 80001: Polygon Mumbai Testnet (MATIC)
- 421613: Arbitrum Goerli Testnet (ETH)

If you need information about blockchains, always use the tools at your disposal.
Respond in a helpful and concise way.

Begin!

{messages}"""

# Create the prompt template
prompt = ChatPromptTemplate.from_template(PROMPT)


# Function to create a new agent
def create_agent(tools):
    """Create a new agent that can use tools."""
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="gpt-4o")
    
    # Create the agent
    return model.bind_tools(tools)


async def main():
    """Run the main example."""
    print("Initializing agent with blockchain tools...")
    print(f"Available tools: {[tool.name for tool in all_tools]}")
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Create an agent with tools
    agent = create_agent(all_tools)
    
    # Create the tool executor
    tool_executor = ToolExecutor(all_tools)
    
    # Define nodes for the graph
    workflow.add_node("agent", agent)
    workflow.add_node("tools", tool_executor)
    
    # Define edges for the graph
    workflow.add_edge("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    workflow.add_edge(tools_condition, END)
    
    # Compile the graph
    app = workflow.compile()
    
    # Initialize state with tools
    state = {"messages": [], "tools": all_tools}
    
    # Run the app with a query
    result = await app.ainvoke(
        state, 
        {"messages": [{"role": "user", "content": "What is the current block number on Ethereum? First get the metadata for Ethereum Mainnet (chain ID 1), then use that information to get the block number."}]}
    )
    
    # Print the final message
    print("\nFinal response:")
    print(result["messages"][-1]["content"])

    # Ask another question
    follow_up_result = await app.ainvoke(
        result,  # Use the previous state with conversation history
        {"messages": result["messages"] + [{"role": "user", "content": "Get information about Polygon (chain ID 137). What's its RPC URL and current block number?"}]}
    )
    
    # Print the follow-up response
    print("\nFollow-up response:")
    print(follow_up_result["messages"][-1]["content"])


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())