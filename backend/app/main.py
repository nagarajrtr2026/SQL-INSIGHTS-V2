from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, database, reports
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Agentic SQL Insights API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://sql-insights-v2.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(database.router, prefix="/api/database", tags=["database"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.post("/api/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    connection: str = Form("null")
):
    return await database.upload(file, connection)


@app.get("/health")
async def health():
    return {"status": "ok"}

