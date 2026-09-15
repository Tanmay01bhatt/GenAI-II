import os
from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import uvicorn
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.genai import types

from agent import run_weather_agent  # your compiled LangGraph StateGraph wrapper


class LangGraphWeatherAgent(BaseAgent):
    """Thin ADK wrapper around the LangGraph weather agent, so it can be
    served with ADK's own A2A utilities instead of raw a2a-sdk classes."""

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        user_text = ctx.user_content.parts[0].text if ctx.user_content else ""
        result_text = await run_weather_agent(user_text)
        yield Event(
            author=self.name,
            content=types.Content(role="model", parts=[types.Part(text=result_text)]),
        )


weather_agent = LangGraphWeatherAgent(
    name="weather_agent",
    description="Reports current weather conditions for a given city.",
)

PORT = int(os.environ.get("WEATHER_A2A_PORT", 8001))
a2a_app = to_a2a(weather_agent, port=PORT)

if __name__ == "__main__":
    uvicorn.run(a2a_app, host="0.0.0.0", port=PORT)