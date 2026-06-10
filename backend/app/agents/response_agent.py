from app.services.llm_service import GroqClient


def generate_dataset_response(
    prompt: str,
    rows: list
) -> str:

    if not rows:
        return "No matching records found."

    total = len(rows)

    preview = rows[:10]

    prompt_text = f"""
User Request:
{prompt}

Returned Records:
{preview}

Total Records:
{total}

Rules:
1. Answer directly.
2. Show key results.
3. Be concise.
4. Do not hallucinate.
5. Use only returned rows.

Response:
"""

    try:

        client = GroqClient()

        response = client.generate_text(
            prompt_text,
            options={
                "temperature": 0.1
            }
        )

        if response and response.strip():
            return response.strip()

    except Exception as e:

        print(
            "[Dataset Response Error]",
            e
        )

    return f"Found {total} matching records."


def generate_response(
    prompt: str,
    sql: str,
    rows: list,
    insights: list,
    chart_type: str
) -> str:

    if not rows:

        return (
            "No matching records were found "
            "for your request."
        )

    client = GroqClient()

    preview_rows = rows[:15]

    insights_text = "\n".join(
        [
            f"- {x}"
            for x in insights[:8]
        ]
    )

    llm_prompt = f"""
You are Genora AI.

USER REQUEST:
{prompt}

EXECUTED SQL:
{sql}

ACTUAL DATA:
{preview_rows}

INSIGHTS:
{insights_text}

CHART:
{chart_type}

RULES:

1. Use ONLY actual data.
2. Never invent values.
3. Never invent statistics.
4. Never invent trends.
5. Never invent rankings.
6. Keep answer concise.
7. Markdown output.
8. Explain findings clearly.

Response:
"""

    try:

        response = client.generate_text(
            llm_prompt,
            options={
                "temperature": 0.1
            }
        )

        if response and response.strip():
            return response.strip()

    except Exception as e:

        print(
            "[Analytics Response Error]",
            e
        )

    return (
        "Analytics completed successfully."
    )