from pydantic import BaseModel
from typing import Any, Dict


class ChatRequest(BaseModel):
    connection: Dict[str, Any]
    prompt: str


class ChatResponse(BaseModel):
    sql: str
    rows: Any
    insights: Any
