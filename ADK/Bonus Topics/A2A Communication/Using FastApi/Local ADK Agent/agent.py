from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)


# Remote LangGraph agent
research_agent = RemoteA2aAgent(
    name="research_agent",
    description="A remote LangGraph research agent.",
    agent_card=(
        "http://127.0.0.1:8001/a2a/research_agent"
        f"{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)


# Local ADK orchestrator
root_agent = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="An orchestrator that delegates technical research.",
    instruction="""
You are an orchestrator.

You can use the research_agent tool.

When the user asks a technical question,
use research_agent to get the answer.

Return the result clearly to the user.
""",
    tools=[
        AgentTool(agent=research_agent)
    ],
)