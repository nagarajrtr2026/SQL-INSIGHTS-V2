import plotly.io as pio


def chart_from_figure_json(fig_json: str) -> str:
    # returns HTML div string for embedding
    try:
        return pio.to_html(fig_json, full_html=False)
    except Exception:
        return ""
