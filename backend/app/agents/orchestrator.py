import os
import json
from fastapi import HTTPException
from app.agents import (
    intent_router, schema_engine, sql_validator,
    analytics_engine, chat_engine, report_engine,
    sql_agent, response_agent
)
from app.database.connection import build_db_url, create_sync_engine
from app.database.query_executor import execute_query
from app.core.state import active_dataset

def run(prompt: str, connection_dict: dict) -> dict:

    # ------------------------------
    # 1. Intent Detection
    # ------------------------------

    router_res = intent_router.route_intent(prompt)
    intent = router_res.category

    print(f"[Intent] {intent}")

    # ------------------------------
    # 2. Build Database Connection
    # ------------------------------

    url = build_db_url(
        connection_dict.get("kind", "postgresql"),
        connection_dict.get("host", "localhost"),
        connection_dict.get("port", 5432),
        connection_dict.get("username", "postgres"),
        connection_dict.get("password", "postgres"),
        connection_dict.get("database", "agentic_ai")
    )

    engine = create_sync_engine(url)

    # ------------------------------
    # 3. Load Active Schema
    # ------------------------------

    schema_ctx = schema_engine.get_schema_context(engine)
    schema_str = schema_ctx["schema_str"]

    print(
        f"[Schema] Table = {schema_ctx.get('table')}"
    )

    # ------------------------------
    # 4. CHAT
    # ------------------------------

    if intent == "chat":

        response_text = chat_engine.handle_chat(
            prompt,
            intent,
            schema_ctx
        )

        return {
            "sql": "",
            "rows": [],
            "insights": [],
            "chart": {
                "type": "empty",
                "data": {}
            },
            "response": response_text
        }

    # ------------------------------
    # 5. DATASET METADATA QA
    # ------------------------------

    if intent == "dataset_qa":

        response_text = chat_engine.handle_chat(
            prompt,
            intent,
            schema_ctx
        )

        return {
            "sql": "",
            "rows": [],
            "insights": [],
            "chart": {
                "type": "empty",
                "data": {}
            },
            "response": response_text
        }

    # ------------------------------
    # 6. SQL Generation
    # ------------------------------

    sql = ""
    rows = []

    max_retries = 3
    error_log = ""

    for attempt in range(max_retries):

        try:

            if attempt == 0:

                raw_sql = sql_agent.nl_to_sql(
                    prompt,
                    schema=schema_str
                )

            else:

                raw_sql = sql_agent.self_heal_sql(
                    prompt,
                    sql,
                    error_log,
                    schema_str
                )

            print(
                f"[Raw SQL] {raw_sql}"
            )

            sql = sql_validator.validate_sql(
                raw_sql,
                schema_ctx
            )

            print(
                f"[Validated SQL] {sql}"
            )

            rows = execute_query(
                engine,
                sql
            )

            print(
                f"[Rows Returned] {len(rows)}"
            )

            break

        except Exception as e:

            error_log = str(e)

            print(
                f"[Attempt {attempt}] {error_log}"
            )

            if attempt == max_retries - 1:

                raise HTTPException(
                    status_code=400,
                    detail=error_log
                )

    # ------------------------------
    # 7. SQL ONLY REQUEST
    # ------------------------------

    if intent == "sql":

        return {
            "sql": sql,
            "rows": rows,
            "insights": [],
            "chart": {
                "type": "empty",
                "data": {}
            },
            "response": f"```sql\n{sql}\n```"
        }

    # ------------------------------
    # 8. DATASET QUERY
    # ------------------------------

    if intent == "dataset_query":

        response_text = (
            response_agent.generate_dataset_response(
                prompt,
                rows
            )
        )

        return {
            "sql": sql,
            "rows": rows,
            "insights": [],
            "chart": {
                "type": "empty",
                "data": {}
            },
            "response": response_text
        }

    # ------------------------------
    # 9. ANALYTICS
    # ------------------------------

    analytics = analytics_engine.process_analytics(
        rows,
        prompt
    )

    insights = analytics["insights"]
    chart = analytics["chart"]

    # ------------------------------
    # 10. REPORT
    # ------------------------------

    if intent == "report":

        return {
            "sql": sql,
            "rows": rows,
            "insights": insights,
            "chart": chart,
            "response":
            "PDF report generated successfully."
        }

    # ------------------------------
    # 11. ANALYTICS RESPONSE
    # ------------------------------

    response_text = (
        response_agent.generate_response(
            prompt,
            sql,
            rows,
            insights,
            chart.get(
                "type",
                "table"
            )
        )
    )

    return {
        "sql": sql,
        "rows": rows,
        "insights": insights,
        "chart": chart,
        "response": response_text
    }