import pandas as pd
from typing import List, Dict, Any
from app.agents import visualization_agent, analysis_agent


def process_analytics(
    rows: List[Dict[str, Any]],
    user_query: str
) -> Dict[str, Any]:

    if not rows:

        return {
            "chart": {
                "type": "empty",
                "data": {}
            },
            "insights": [
                "No data available for analysis."
            ],
            "recommendations": []
        }

    df = pd.DataFrame(rows)

    query = user_query.lower()

    analytics_keywords = [
        "analyze",
        "analytics",
        "analysis",
        "compare",
        "comparison",
        "correlation",
        "distribution",
        "trend",
        "insight",
        "insights",
        "statistics",
        "kpi",
        "dashboard"
    ]

    visualization_keywords = [
        "chart",
        "graph",
        "plot",
        "visualize",
        "bar",
        "line",
        "pie",
        "scatter",
        "heatmap",
        "histogram"
    ]

    is_analytics = any(
        k in query
        for k in analytics_keywords
    )

    is_visualization = any(
        k in query
        for k in visualization_keywords
    )

    # Dataset query → no analytics
    if not is_analytics and not is_visualization:

        return {
            "chart": {
                "type": "empty",
                "data": {}
            },
            "insights": [],
            "recommendations": []
        }

    # --------------------------
    # Generate Insights
    # --------------------------

    try:

        insights = (
            analysis_agent.generate_insights(
                rows,
                user_query
            )
        )

    except Exception as e:

        print(
            "[Analytics Engine] Insight Error:",
            e
        )

        insights = [
            "Analytics completed."
        ]

    # --------------------------
    # Generate Visualization
    # --------------------------

    try:

        chart = (
            visualization_agent.auto_visualize(
                rows,
                user_query
            )
        )

    except Exception as e:

        print(
            "[Analytics Engine] Chart Error:",
            e
        )

        chart = {
            "type": "table",
            "data": rows
        }

    # --------------------------
    # Dynamic Recommendations
    # --------------------------

    recommendations = []

    if insights:

        recommendations = [
            "Investigate high-performing categories.",
            "Review outliers for business impact.",
            "Compare results with historical data.",
            "Monitor trends over time."
        ]

    return {
        "chart": chart,
        "insights": insights,
        "recommendations": recommendations
    }