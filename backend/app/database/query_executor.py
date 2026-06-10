from sqlalchemy import text
from app.utils.sql_validator import validate_sql
from concurrent.futures import ThreadPoolExecutor


def execute_query_sync(engine, sql: str):

    validate_sql(sql)

    with engine.connect() as conn:

        result = conn.execute(text(sql))

        try:
            rows = [
                dict(row._mapping)
                for row in result
            ]

        except Exception as e:

            print("QUERY ERROR:", e)

            rows = []

    return rows


def execute_query(engine, sql: str):

    with ThreadPoolExecutor(max_workers=1) as ex:

        future = ex.submit(
            execute_query_sync,
            engine,
            sql
        )

        return future.result()