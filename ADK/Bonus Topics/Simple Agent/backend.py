import os
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from dotenv import load_dotenv
load_dotenv()


APP_NAME = "Simple ADK Agent"

app = FastAPI()

def get_weather(city: str) -> dict:
    """Returns the current weather for a given city."""
    fake_data = {"tokyo": "77°F and sunny", "london": "59°F and rainy"}
    return {"status": "success", "city": city, "weather": fake_data.get(city.lower(), "22°C and clear")}

agent = Agent(
    model="gemini-flash-latest",
    name="assistant",
    instruction="You are a helpful assistant. Use 'get_weather' for weather questions.",
    tools=[get_weather],
)

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

# Pydantic Schema
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.post("/session")
async def create_session(user_id: str):
    session = await session_service.create_session(app_name=APP_NAME, user_id=user_id)
    return {"session_id": session.id}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id
    if not session_id:
        session = await session_service.create_session(app_name=APP_NAME, user_id=req.user_id)
        session_id = session.id

    content = types.Content(role="user", parts=[types.Part(text=req.message)])
    reply = "(no response)"
    async for event in runner.run_async(user_id=req.user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            reply = event.content.parts[0].text

    return ChatResponse(reply=reply, session_id=session_id)