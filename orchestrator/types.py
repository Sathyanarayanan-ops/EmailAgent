from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage

class OrchestratorState(TypedDict, total=False):
    user_input: str
    active_agent: str
    chat_history: list[BaseMessage]
    agent_outputs: dict
