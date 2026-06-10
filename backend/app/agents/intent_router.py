from pydantic import BaseModel
from app.services.llm_service import GroqClient


class IntentResult(BaseModel):
    category: str
    original_prompt: str


def route_intent(prompt: str, schema: str = "") -> IntentResult:
    """
    Semantic intent router for Genora AI.
    """

    query = prompt.lower().strip()

    # --------------------------------------------------
    # Fast Rules (No LLM Needed)
    # --------------------------------------------------

    greetings = [
        "hi",
        "hello",
        "hey",
        "yo",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if query in greetings:
        return IntentResult(
            category="chat",
            original_prompt=prompt
        )

    report_keywords = [
        "report",
        "pdf",
        "export",
        "download report",
        "generate report"
    ]

    visualization_keywords = [
        "chart",
        "graph",
        "plot",
        "visualize",
        "visualization",
        "bar chart",
        "line chart",
        "pie chart",
        "scatter",
        "heatmap",
        "histogram"
    ]

    analytics_keywords = [
        "analyze",
        "analytics",
        "analysis",
        "insight",
        "insights",
        "compare",
        "comparison",
        "correlation",
        "trend",
        "distribution",
        "statistics",
        "kpi",
        "dashboard"
    ]

    sql_keywords = [
        "sql",
        "postgresql",
        "query code",
        "select statement",
        "sql query"
    ]

    dataset_query_keywords = [
        "list",
        "show",
        "display",
        "give",
        "find",
        "top",
        "highest",
        "lowest",
        "best",
        "worst",
        "count",
        "average",
        "sum",
        "total"
    ]

    if any(k in query for k in report_keywords):
        return IntentResult(
            category="report",
            original_prompt=prompt
        )

    if any(k in query for k in visualization_keywords):
        return IntentResult(
            category="visualization",
            original_prompt=prompt
        )

    if any(k in query for k in analytics_keywords):
        return IntentResult(
            category="analytics",
            original_prompt=prompt
        )

    if any(k in query for k in sql_keywords):
        return IntentResult(
            category="sql",
            original_prompt=prompt
        )

    if any(k in query for k in dataset_query_keywords):
        return IntentResult(
            category="dataset_query",
            original_prompt=prompt
        )

    # --------------------------------------------------
    # LLM Semantic Classification
    # --------------------------------------------------

    try:

        client = GroqClient()

        llm_prompt = f"""
You are an intent classification engine.

Classify the user query into exactly ONE category.

Available Categories:

chat
dataset_query
dataset_qa
sql
analytics
visualization
report

Definitions:

chat:
General conversation.
Examples:
What is AI?
Who are you?
Explain machine learning.

dataset_query:
User wants actual dataset values.
Examples:
List restaurant names
Show top 5 restaurants
Highest voted restaurant
Display all cities

dataset_qa:
Questions about dataset structure.
Examples:
What columns exist?
What is the datatype of votes?
How many columns are available?

sql:
User explicitly asks for SQL code.

analytics:
User requests analysis, comparison,
statistics, trends, insights or KPIs.

visualization:
User explicitly asks for charts,
graphs or plots.

report:
User explicitly asks for reports,
PDF export or downloadable documents.

User Query:
{prompt}

Return ONLY one word:

chat
dataset_query
dataset_qa
sql
analytics
visualization
report
"""

        response = client.generate_text(
            llm_prompt,
            options={
                "temperature": 0
            }
        )

        category = response.strip().lower()

        allowed = {
            "chat",
            "dataset_query",
            "dataset_qa",
            "sql",
            "analytics",
            "visualization",
            "report"
        }

        if category in allowed:

            print(
                f"[Intent Router] {category}"
            )

            return IntentResult(
                category=category,
                original_prompt=prompt
            )

    except Exception as e:

        print(
            "[Intent Router Error]",
            e
        )

    # --------------------------------------------------
    # Safe Default
    # --------------------------------------------------

    return IntentResult(
        category="chat",
        original_prompt=prompt
    )