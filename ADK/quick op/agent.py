from google.adk.agents.llm_agent import Agent

def greeting_tool() -> str:
    """Returns a warm, friendly greeting."""
    return "Hello from your specialized greeting tool! Welcome."

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A friendly agent that provides a special greeting.',
    instruction='You are a friendly agent. When the user greets you, you MUST use the greeting_tool to respond.',
    tools=[greeting_tool],
)