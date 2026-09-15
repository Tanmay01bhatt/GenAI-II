import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

from tool import convert_currency

weather_url = os.environ.get("WEATHER_A2A_URL", "http://localhost:8001")

remote_weather_agent = RemoteA2aAgent(
    name="weather_agent",
    description="Remote agent that reports current weather for a city.",
    agent_card=f"{weather_url}{AGENT_CARD_WELL_KNOWN_PATH}",
)

llm  = LiteLlm(model="groq/llama-3.3-70b-versatile")

root_agent = Agent(
    name="finance_agent",
    model=llm,
    description="Converts currencies and can also check weather via a remote agent.",
    instruction=(
        "You are a finance assistant. Use convert_currency for currency conversion "
        "requests. For weather-related questions, delegate to the weather_agent tool. "
        "Never guess a rate or weather condition — if a tool errors, state it plainly."
    ),
    tools=[convert_currency, AgentTool(agent=remote_weather_agent)],
)




