# Agentic AI for Automated Insight Generation from SQL Databases

This repository contains a scaffold for a production-ready Agentic AI SaaS that connects to SQL databases, generates SQL from natural language, executes queries read-only, analyzes results, visualizes data, and generates PDF reports.

Quick start (backend):

1. Build and run backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. API endpoints:
- `GET /health` — health check
- `POST /api/database/test` — test DB connection
- `POST /api/database/execute` — execute read-only SQL
- `POST /api/chat/query` — NL -> SQL -> execute -> insights

This scaffold includes:
- FastAPI backend with modular agents and services
- SQL safety validator (read-only enforcement)
- Plotly and ReportLab stubs for visualization and PDF
- Dockerfile and docker-compose for local development

Next steps:
- Implement frontend Next.js app (scaffold exists in `frontend/`)
- Improve LLM prompts and robust error handling
- Add user auth, session management, and secure secrets
- Harden DB connection pooling and async execution
