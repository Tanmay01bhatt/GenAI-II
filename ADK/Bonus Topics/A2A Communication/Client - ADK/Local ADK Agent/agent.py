from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)


research_agent = RemoteA2aAgent(
    name="research_agent",
    description="A remote LangGraph agent that answers technical questions.",
    agent_card=(
        "http://localhost:8001/a2a/research_agent"
        f"{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)


root_agent = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="An orchestrator that can delegate questions to a remote research agent.",
    instruction="""
You are an orchestrator.

You have access to a remote research agent.

When the user asks a technical question that should be answered by
the research agent, use the research_agent tool.

After receiving the result, present it clearly to the user.
""",
    tools=[
        AgentTool(agent=research_agent)
    ],
)