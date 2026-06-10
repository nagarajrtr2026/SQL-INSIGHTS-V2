import json
from app.services.llm_service import GroqClient
from app.core.state import active_dataset


def handle_chat(
    prompt: str,
    intent: str,
    schema_context: dict
) -> str:

    query = prompt.lower().strip()

    greetings = {
        "hi",
        "hello",
        "hey",
        "yo",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if query in greetings:

        return (
            "Hello 👋 I'm Genora AI. "
            "You can chat with me, explore datasets, generate SQL queries, "
            "create analytics, visualizations and reports."
        )

    table_name = schema_context.get(
        "table",
        "No Active Dataset"
    )

    schema_str = schema_context.get(
        "schema_str",
        ""
    )

    profile_context = (
        json.dumps(
            active_dataset.profile,
            indent=2
        )
        if active_dataset.profile
        else "No dataset profile available."
    )

    client = GroqClient()

    if intent == "dataset_qa":

        llm_prompt = f"""
You are Genora AI.

ACTIVE TABLE:
{table_name}

SCHEMA:
{schema_str}

PROFILE:
{profile_context}

USER QUESTION:
{prompt}

RULES:

1. Answer ONLY using schema/profile.
2. Never invent columns.
3. Never invent tables.
4. Be concise.
5. Use markdown.
6. If information is unavailable, say so.

ANSWER:
"""

    else:

        llm_prompt = f"""
You are Genora AI.

USER QUESTION:
{prompt}

RULES:

1. Answer naturally like ChatGPT.
2. Be concise.
3. Be accurate.
4. Do not mention SQL unless asked.
5. Do not mention datasets unless asked.
6. Do not mention reports unless asked.
7. Use markdown if helpful.

ANSWER:
"""

    try:

        response = client.generate_text(
            llm_prompt,
            options={
                "temperature": 0.3
            }
        )

        if response and response.strip():

            return response.strip()

    except Exception as e:

        print(
            "[Chat Engine Error]",
            e
        )

    return (
        "I'm unable to generate a response right now. "
        "Please try again."
    )