import json
from typing import List, Dict, Any

def auto_visualize(rows: List[Dict], user_query: str = "") -> Dict[str, Any]:
    """
    Selects the best visualization format (bar, line, pie, histogram, scatter, heatmap, kpi)
    based on the shape, data types, and query intention, returning a JSON-serialized configuration.
    """
    if not rows:
        return {"type": "empty", "data": {}}

    try:
        import pandas as pd
        import plotly.express as px
        
        df = pd.DataFrame(rows)
        cols = list(df.columns)
        
        if not cols:
            return {"type": "empty", "data": {}}

        # 1. Detect if it fits a KPI Card
        # e.g., a single row and single column (like COUNT, SUM) OR simple aggregate results
        if len(df) == 1 and len(cols) == 1:
            val = df.iloc[0, 0]
            try:
                # Format float cleanly
                if isinstance(val, (int, float)):
                    val = f"{val:,.2f}" if isinstance(val, float) else f"{val:,}"
            except Exception:
                pass
            return {
                "type": "kpi",
                "title": cols[0].replace("_", " ").upper(),
                "value": str(val)
            }

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = [c for c in cols if c not in numeric_cols]
        date_cols = [c for c in cols if any(kw in c.lower() for kw in ("date", "time", "year", "month", "created"))]

        lower_query = user_query.lower()

        # 2. Check if user explicitly asked for a Heatmap OR Correlation chart
        if "heatmap" in lower_query or "correlation" in lower_query:
            if len(numeric_cols) >= 2:
                corr_df = df[numeric_cols].corr()
                fig = px.imshow(
                    corr_df,
                    text_auto=".2f",
                    color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap Matrix"
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "correlation", "figure": fig.to_json()}

        # 2a. Check for Grouped/Comparison Bar Chart
        if "comparison" in lower_query or "grouped" in lower_query or "compare" in lower_query:
            if categorical_cols and numeric_cols:
                x_col = categorical_cols[0]
                y_col = numeric_cols[0]
                color_col = categorical_cols[1] if len(categorical_cols) > 1 else None
                fig = px.bar(
                    df,
                    x=x_col,
                    y=y_col,
                    color=color_col,
                    barmode="group",
                    title=f"Comparison: {y_col} by {x_col}" + (f" and {color_col}" if color_col else "")
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "bar", "figure": fig.to_json()}


        # 2b. Check for Box Plot
        if "box" in lower_query or "boxplot" in lower_query:
            if numeric_cols:
                x_col = categorical_cols[0] if categorical_cols else None
                y_col = numeric_cols[0]
                fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot: {y_col}" + (f" grouped by {x_col}" if x_col else ""))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "boxplot", "figure": fig.to_json()}

        # 3. Check for Scatter Plot
        if "scatter" in lower_query or (len(numeric_cols) >= 2 and not categorical_cols):
            x_col = numeric_cols[0]
            y_col = numeric_cols[1]
            fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Distribution: {y_col} vs {x_col}")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
            )
            return {"type": "scatter", "figure": fig.to_json()}

        # 4. Check for Histogram: User asked for distribution/histogram, or we have 1 numeric column and many rows (>20)
        if "histogram" in lower_query or "distribution" in lower_query:
            if numeric_cols:
                fig = px.histogram(df, x=numeric_cols[0], title=f"Frequency Distribution: {numeric_cols[0]}")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "histogram", "figure": fig.to_json()}

        # 5. Check for Line Chart (Trends)
        if date_cols and numeric_cols:
            x_col = date_cols[0]
            y_col = numeric_cols[0]
            try:
                df_temp = df.copy()
                df_temp[x_col] = pd.to_datetime(df_temp[x_col], errors="coerce")
                df_sorted = df_temp.sort_values(by=x_col)
            except Exception:
                df_sorted = df
            fig = px.line(df_sorted, x=x_col, y=y_col, title=f"Chronological Trend: {y_col} over {x_col}")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
            )
            return {"type": "line", "figure": fig.to_json()}

        # 6. Check for Pie Chart vs Bar Chart (Categorical breakdown)
        if categorical_cols and numeric_cols:
            x_col = categorical_cols[0]
            y_col = numeric_cols[0]
            unique_count = df[x_col].nunique()
            if 2 <= unique_count <= 6 or "pie" in lower_query:
                fig = px.pie(df, names=x_col, values=y_col, title=f"Composition breakdown of {y_col} by {x_col}")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "pie", "figure": fig.to_json()}
            else:
                fig = px.bar(df, x=x_col, y=y_col, title=f"Comparison: {y_col} by {x_col}")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
                )
                return {"type": "bar", "figure": fig.to_json()}

        # 7. Default to standard Table layout if no visualization makes sense
        if numeric_cols:
            fig = px.line(df, y=numeric_cols[0], title=f"Data Trend: {numeric_cols[0]}")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f4f4f5", "family": "Inter, sans-serif"}
            )
            return {"type": "line", "figure": fig.to_json()}
            
        return {"type": "table", "data": rows}

    except Exception as e:
        print("Visualization Agent warning, returning empty:", e)
        return {"type": "table", "data": rows}
