import json
import re
import os
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from app.database.connection import build_db_url, create_sync_engine
from app.database.query_executor import execute_query
from app.core.config import settings

router = APIRouter()


class DBConnect(BaseModel):
    kind: str
    host: str
    port: int
    username: str
    password: str
    database: str


@router.post("/test")
async def test_connection(payload: DBConnect):
    url = build_db_url(payload.kind, payload.host, payload.port, payload.username, payload.password, payload.database)
    try:
        engine = create_sync_engine(url)
        rows = execute_query(engine, "SELECT 1;")
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute")
async def execute(payload: dict):
    # payload: {connection, sql}
    conn = payload.get("connection")
    sql = payload.get("sql")
    if not conn or not sql:
        raise HTTPException(status_code=400, detail="connection and sql required")
    url = build_db_url(conn.get("kind"), conn.get("host"), conn.get("port"), conn.get("username"), conn.get("password"), conn.get("database"))
    engine = create_sync_engine(url)
    rows = execute_query(engine, sql)
    return {"rows": rows}


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    connection: str = Form("null")
):
    try:
        # 1. Parse connection string safely
        if connection and connection not in ("null", "undefined", '""', "''"):
            try:
                conn = json.loads(connection)
                url = build_db_url(
                    conn.get("kind", "postgresql"),
                    conn.get("host", "localhost"),
                    conn.get("port", 5432),
                    conn.get("username", "postgres"),
                    conn.get("password", "postgres"),
                    conn.get("database", "agentic_ai")
                )
            except Exception:
                url = build_db_url("postgresql", settings.DB_HOST, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME)
        else:
            url = build_db_url("postgresql", settings.DB_HOST, settings.DB_PORT, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME)


        # 2. Sanitize and build table name from filename
        filename, ext = os.path.splitext(file.filename)
        # Keep only alphanumeric and underscores
        safe_name = re.sub(r"[^a-zA-Z0-9_]", "", filename.lower())
        if not safe_name:
            safe_name = "dataset"
        table_name = f"t_{safe_name}"

        # 3. Read spreadsheet data using pandas
        ext = ext.lower()
        if ext == ".csv":
            df = pd.read_csv(file.file)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV or Excel file.")

        # 4. Auto-clean column names to be SQL-compliant
        cleaned_columns = []
        for col in df.columns:
            # Strip, lowercase, replace spaces/special chars with underscores
            clean_col = re.sub(r"[^a-zA-Z0-9_]", "_", str(col).strip().lower())
            # Strip duplicate underscores
            clean_col = re.sub(r"__+", "_", clean_col).strip("_")
            if not clean_col:
                clean_col = f"col_{len(cleaned_columns) + 1}"
            cleaned_columns.append(clean_col)
        df.columns = cleaned_columns

        # 5. Write dataset to SQL database
        engine = create_sync_engine(url)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False, method="multi", chunksize=1000)

        # 6. Infer database schema structures dynamically for the AI agent
        schema_fields = []
        for col, dtype in zip(df.columns, df.dtypes):
            dtype_str = str(dtype).lower()
            if "int" in dtype_str:
                sql_type = "INTEGER"
            elif "float" in dtype_str or "double" in dtype_str or "num" in dtype_str:
                sql_type = "FLOAT"
            elif "date" in dtype_str or "time" in dtype_str:
                sql_type = "DATE"
            else:
                sql_type = "TEXT"
            schema_fields.append(f"    {col} {sql_type}")
        
        schema_str = f"{table_name}(\n" + ",\n".join(schema_fields) + "\n)"
        
        # Run schema analysis agent
        from app.agents import schema_agent
        profile = schema_agent.analyze_schema(df, table_name)
        
        # 7. Store dataset metadata globally
        from app.core.state import active_dataset
        active_dataset.set_dataset(table_name, schema_str, list(df.columns), profile=profile)
        print("GLOBALLY STORED ACTIVE DATASET METADATA:")
        print(f"Table: {table_name}")
        print(f"Schema: {schema_str}")
        print(f"Profile: {profile}")

        return {
            "ok": True,
            "table_name": table_name,
            "rows": len(df),
            "columns": list(df.columns),
            "schema": schema_str,
            "profile": profile
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=400, detail=f"Failed to process and upload dataset: {str(e)}")


