import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from .tool import get_current_weather



llm=ChatGroq(model="llama-3.1-8b-instant")

SYSTEM_PROMPT = (
    "You are a weather assistant. Use get_current_weather for any weather "
    "query. If the tool returns an error, say so plainly — never invent "
    "weather data. Report temperature, feels-like, and conditions clearly."
)

class WeatherState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

tools = [get_current_weather]
llm_with_tools = llm.bind_tools(tools)

def call_model(state: WeatherState) -> WeatherState:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

builder = StateGraph(WeatherState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", tools_condition)  # → "tools" or END
builder.add_edge("tools", "agent")

graph = builder.compile()

async def run_weather_agent(query: str) -> str:
    result = await graph.ainvoke({"messages": [("user", query)]})
    return result["messages"][-1].content
