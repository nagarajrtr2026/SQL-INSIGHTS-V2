from fastapi import APIRouter, Response
from pydantic import BaseModel
from app.agents.report_agent import create_report

router = APIRouter()


class ReportRequest(BaseModel):
    title: str
    rows: list
    insights: list


@router.post("/generate")
async def generate(req: ReportRequest):
    pdf = create_report(req.title, req.rows, req.insights, [])
    return Response(content=pdf, media_type="application/pdf")
