from sqlalchemy import inspect
from typing import Dict, Any, List
from app.core.state import active_dataset


def get_schema_context(engine=None) -> Dict[str, Any]:

    table_name = active_dataset.table_name
    columns_list: List[Dict[str, str]] = []
    schema_str = ""

    # --------------------------
    # Database Reflection
    # --------------------------

    if engine:

        try:

            inspector = inspect(engine)

            tables = inspector.get_table_names()

            if active_dataset.table_name in tables:

                table_name = active_dataset.table_name

            else:

                valid_tables = [
                    t
                    for t in tables
                    if not t.startswith("pg_")
                    and not t.startswith("sql_")
                ]

                if valid_tables:

                    table_name = valid_tables[0]

            if table_name:

                cols = inspector.get_columns(
                    table_name
                )

                schema_lines = []

                for col in cols:

                    name = col["name"]

                    col_type = str(
                        col["type"]
                    ).upper()

                    columns_list.append(
                        {
                            "name": name,
                            "type": col_type
                        }
                    )

                    schema_lines.append(
                        f"    {name} {col_type}"
                    )

                schema_str = (
                    f"{table_name}(\n"
                    + ",\n".join(schema_lines)
                    + "\n)"
                )

        except Exception as e:

            print(
                "[Schema Reflection Error]",
                e
            )

    # --------------------------
    # Active Dataset Fallback
    # --------------------------

    if (
        not schema_str
        and active_dataset.schema_str
    ):

        table_name = (
            active_dataset.table_name
        )

        schema_str = (
            active_dataset.schema_str
        )

        columns_list = []

        for col in active_dataset.columns:

            columns_list.append(
                {
                    "name": col,
                    "type": "TEXT"
                }
            )

    # --------------------------
    # No Schema Available
    # --------------------------

    if not schema_str:

        raise ValueError(
            "No active dataset schema available."
        )

    return {

        "table": table_name,

        "columns": columns_list,

        "schema_str": schema_str

    }