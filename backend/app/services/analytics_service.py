from typing import List, Dict


def summarize_rows(rows: List[Dict]) -> List[str]:
    # Lightweight wrapper: future: call analysis agent
    if not rows:
        return ["No data to analyze."]
    return [f"Returned {len(rows)} rows."]
