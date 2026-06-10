from fastapi import APIRouter
from pydantic import BaseModel
from app.agents import orchestrator

router = APIRouter()


class ChatRequest(BaseModel):
    connection: dict
    prompt: str


@router.post("/query")
async def query(req: ChatRequest):
    return orchestrator.run(req.prompt, req.connection)
