from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"


class AgentChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"
    memory_type: str = "buffer"  # "buffer", "window", "summary"
    verbose: bool = False