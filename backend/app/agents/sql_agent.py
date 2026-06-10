import re
from app.services.llm_service import GroqClient


def nl_to_sql(
    nl: str,
    schema: str = ""
) -> str:

    if not schema or not schema.strip():
        raise ValueError(
            "No active dataset schema available."
        )

    client = GroqClient()

    prompt = f"""
You are a PostgreSQL SQL generation engine.

ACTIVE DATABASE SCHEMA:

{schema}

USER REQUEST:

{nl}

RULES:

1. Return ONLY SQL.
2. No markdown.
3. No explanations.
4. No comments.
5. Use ONLY tables and columns present in schema.
6. Never invent tables.
7. Never invent columns.
8. Never use SELECT *.
9. Explicitly list columns.
10. Use PostgreSQL syntax.
11. Query must end with semicolon.
12. Generate only SELECT queries.

Examples:

User:
List restaurant names

SQL:
SELECT restaurant_name
FROM t_dataset;

User:
Show top 5 restaurants by votes

SQL:
SELECT restaurant_name, votes
FROM t_dataset
ORDER BY votes DESC
LIMIT 5;

User:
Highest rated restaurant

SQL:
SELECT restaurant_name, aggregate_rating
FROM t_dataset
ORDER BY aggregate_rating DESC
LIMIT 1;

SQL:
"""

    response = client.generate_text(
        prompt,
        options={
            "temperature": 0
        }
    )

    return clean_extracted_sql(response)


def clean_extracted_sql(
    sql_text: str
) -> str:

    if not sql_text:
        raise ValueError(
            "Empty SQL response"
        )

    sql = sql_text.strip()

    sql = re.sub(
        r"```sql|```",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.strip()

    match = re.search(
        r"((SELECT|WITH)[\s\S]*?;)",
        sql,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    sql = sql.strip()

    if (
        sql.upper().startswith("SELECT")
        or
        sql.upper().startswith("WITH")
    ):

        if not sql.endswith(";"):
            sql += ";"

        return sql

    raise ValueError(
        f"Unable to extract SQL: {sql_text}"
    )


def self_heal_sql(
    prompt: str,
    bad_sql: str,
    error_msg: str,
    schema: str
):

    client = GroqClient()

    repair_prompt = f"""
You are a PostgreSQL SQL repair engine.

DATABASE SCHEMA:

{schema}

USER REQUEST:

{prompt}

FAILED SQL:

{bad_sql}

ERROR:

{error_msg}

RULES:

1. Fix SQL.
2. Return ONLY SQL.
3. Use ONLY schema columns.
4. Never invent columns.
5. Never invent tables.
6. PostgreSQL syntax only.
7. End with semicolon.

CORRECTED SQL:
"""

    response = client.generate_text(
        repair_prompt,
        options={
            "temperature": 0
        }
    )

    return clean_extracted_sql(response)