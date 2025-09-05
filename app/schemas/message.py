from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

Role = Literal["system", "user", "assistant", "tool"]

class Message(BaseModel):
    id: Optional[str] = None
    role: Role
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    thread_id: str
    user_id: str
    messages: List[Message]

class ChatChunk(BaseModel):
    type: Literal["text", "metadata"]
    text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
