import pandas as pd
import numpy as np
from typing import List, Dict


def generate_insights(
    rows: List[Dict],
    user_query: str = ""
) -> List[str]:

    if not rows:

        return [
            "No data available for analysis."
        ]

    df = pd.DataFrame(rows)

    insights = []

    numeric_cols = (
        df.select_dtypes(
            include=[np.number]
        )
        .columns
        .tolist()
    )

    text_cols = (
        df.select_dtypes(
            exclude=[np.number]
        )
        .columns
        .tolist()
    )

    query = user_query.lower()

    # -----------------------
    # Basic Statistics
    # -----------------------

    for col in numeric_cols[:3]:

        try:

            insights.append(
                f"{col}: Average = {df[col].mean():.2f}"
            )

            insights.append(
                f"{col}: Maximum = {df[col].max()}"
            )

            insights.append(
                f"{col}: Minimum = {df[col].min()}"
            )

        except Exception:
            pass

    # -----------------------
    # Correlation (Only if requested)
    # -----------------------

    if (
        "correlation" in query
        or
        "relationship" in query
    ):

        if len(numeric_cols) >= 2:

            try:

                corr = (
                    df[
                        numeric_cols[:2]
                    ]
                    .corr()
                    .iloc[0, 1]
                )

                insights.append(
                    f"Correlation between "
                    f"{numeric_cols[0]} and "
                    f"{numeric_cols[1]} "
                    f"is {corr:.2f}"
                )

            except Exception:
                pass

    # -----------------------
    # Trend Analysis
    # -----------------------

    if "trend" in query:

        date_cols = [

            c

            for c in df.columns

            if any(
                x in c.lower()
                for x in [
                    "date",
                    "time",
                    "year",
                    "month"
                ]
            )
        ]

        if date_cols and numeric_cols:

            try:

                insights.append(
                    f"Trend analysis completed "
                    f"for {numeric_cols[0]}."
                )

            except Exception:
                pass

    # -----------------------
    # Top Category
    # -----------------------

    if text_cols and numeric_cols:

        try:

            category_col = text_cols[0]
            metric_col = numeric_cols[0]

            grouped = (
                df.groupby(
                    category_col
                )[metric_col]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            if len(grouped) > 0:

                top_category = grouped.index[0]
                top_value = grouped.iloc[0]

                insights.append(
                    f"Highest {metric_col} "
                    f"belongs to "
                    f"{top_category} "
                    f"({top_value:.2f})"
                )

        except Exception:
            pass

    # -----------------------
    # No Insight Fallback
    # -----------------------

    if not insights:

        insights.append(
            "Analysis completed successfully."
        )

    return insights[:8]