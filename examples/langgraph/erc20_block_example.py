import os
import getpass
from typing import Annotated, AsyncGenerator
from typing_extensions import TypedDict

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from lomen.adapters.langchain import LangChainAdapter
from lomen.plugins.erc20 import ERC20Plugin
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import uvicorn


# Load environment variables from .env file
load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")

# Check if required environment variables are set
required_env_vars = ["OPENAI_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

plugin = ERC20Plugin(
    credentials={
        "RPC_URL": os.environ.get(
            "ETHEREUM_RPC_URL", "https://eth-mainnet.alchemyapi.io/v2/your-api-key"
        )
    }
)

lc_tools = [LangChainAdapter.convert(tool, plugin.credentials) for tool in plugin.tools]


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize LangGraph
graph_builder = StateGraph(State)
tools = lc_tools

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    "tools",
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")

graph = graph_builder.compile()

# Initialize FastAPI
app = FastAPI(title="Chat API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatInput(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {"examples": [{"message": "What is LangGraph?"}]}
    }


async def stream_chat_response(user_input: str) -> AsyncGenerator[str, None]:
    try:
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            for value in event.values():
                message = value["messages"][-1]
                if hasattr(message, "content"):
                    yield f"data: {message.content}\n\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    yield "data: [DONE]\n\n"


@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    return StreamingResponse(
        stream_chat_response(chat_input.message), media_type="text/event-stream"
    )


if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
