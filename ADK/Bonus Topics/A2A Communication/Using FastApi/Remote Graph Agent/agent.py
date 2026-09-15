from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START, END


model = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google_genai",
)


def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("llm", call_model)

builder.add_edge(START, "llm")
builder.add_edge("llm", END)

graph = builder.compile()