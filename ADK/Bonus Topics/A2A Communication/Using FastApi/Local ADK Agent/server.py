import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from google.genai import types
from google.adk.runners import InMemoryRunner

from agent import root_agent


app = FastAPI(
    title="Google ADK API",
    version="1.0.0",
)


# Create Runner once
runner = InMemoryRunner(
    agent=root_agent,
    app_name="adk_a2a_client",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    user_id = "user"
    session_id = str(uuid.uuid4())

    # Create ADK session
    await runner.session_service.create_session(
        app_name="adk_a2a_client",
        user_id=user_id,
        session_id=session_id,
    )

    # Convert incoming HTTP request to ADK Content
    user_message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=request.message
            )
        ],
    )

    final_text = ""

    # Run ADK agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):

        if event.is_final_response():

            if (
                event.content
                and event.content.parts
            ):
                final_text = event.content.parts[0].text or ""

    return ChatResponse(
        response=final_text
    )