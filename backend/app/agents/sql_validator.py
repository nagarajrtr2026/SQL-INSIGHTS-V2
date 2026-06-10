import re
from typing import Dict, Any

SQL_KEYWORDS = {
    "select",
    "from",
    "where",
    "group",
    "by",
    "order",
    "limit",
    "offset",
    "having",
    "and",
    "or",
    "not",
    "in",
    "like",
    "ilike",
    "is",
    "null",
    "as",
    "join",
    "on",
    "left",
    "right",
    "inner",
    "outer",
    "sum",
    "avg",
    "min",
    "max",
    "count",
    "distinct",
    "desc",
    "asc",
    "with",
    "over",
    "partition",
    "rank",
    "dense_rank",
    "row_number",
    "coalesce",
    "cast",
    "case",
    "when",
    "then",
    "else",
    "end",
    "true",
    "false",
    "between",
    "exists",
    "any",
    "all"
}

PROHIBITED_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "grant",
    "revoke"
}


def validate_sql(
    sql: str,
    schema_context: Dict[str, Any]
) -> str:

    if not sql or not sql.strip():
        raise ValueError(
            "Generated SQL is empty."
        )

    sql_clean = sql.strip()

    # Remove quoted strings
    sql_no_strings = re.sub(
        r"'[^']*'",
        "",
        sql_clean
    )

    # -----------------------
    # Read-only validation
    # -----------------------

    first_word = (
        sql_no_strings
        .split()[0]
        .lower()
    )

    if first_word not in (
        "select",
        "with"
    ):
        raise ValueError(
            "Only SELECT/WITH queries are allowed."
        )

    # -----------------------
    # Security validation
    # -----------------------

    lowered = sql_no_strings.lower()

    for keyword in PROHIBITED_KEYWORDS:

        if re.search(
            rf"\b{keyword}\b",
            lowered
        ):
            raise ValueError(
                f"Blocked SQL keyword: {keyword}"
            )

    # -----------------------
    # Schema validation
    # -----------------------

    allowed_columns = {
        c["name"].lower()
        for c in schema_context.get(
            "columns",
            []
        )
    }

    table_name = (
        schema_context.get(
            "table",
            ""
        )
        .lower()
        .strip()
    )

    identifiers = re.findall(
        r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
        sql_no_strings
    )

    for identifier in identifiers:

        token = identifier.lower()

        # SQL keyword
        if token in SQL_KEYWORDS:
            continue

        # Active table
        if token == table_name:
            continue

        # Real column
        if token in allowed_columns:
            continue

        # aliases like t,s,a,b
        if len(token) <= 2:
            continue

        # Ignore unknown identifiers
        print(
            f"[Validator Warning] Unknown identifier ignored: {token}"
        )

    # -----------------------
    # Final cleanup
    # -----------------------

    sql_clean = (
        sql_clean
        .replace("`", "")
        .strip()
    )

    if not sql_clean.endswith(";"):
        sql_clean += ";"

    return sql_clean