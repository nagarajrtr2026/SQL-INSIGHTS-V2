import json
import pandas as pd
from typing import Dict, Any

def analyze_schema(df: pd.DataFrame, table_name: str) -> Dict[str, Any]:
    """
    Analyzes DataFrame columns, types, sample data, and generates a semantic schema profile.
    """
    profile = {
        "table_name": table_name,
        "row_count": len(df),
        "columns": {}
    }
    
    # 1. Gather structural metadata and statistical properties
    for col in df.columns:
        col_series = df[col]
        dtype = str(col_series.dtype)
        unique_cnt = col_series.nunique()
        null_cnt = int(col_series.isnull().sum())
        
        # Get sample values (non-null, converted to string representation)
        samples = col_series.dropna().head(3).tolist()
        samples = [str(x) for x in samples]
        
        col_info = {
            "dtype": dtype,
            "unique_count": unique_cnt,
            "null_count": null_cnt,
            "samples": samples,
            "semantic_type": "unknown",
            "description": ""
        }
        
        # Check numerical properties safely
        if pd.api.types.is_numeric_dtype(col_series):
            import math
            
            raw_min = col_series.min()
            raw_max = col_series.max()
            raw_mean = col_series.mean()
            
            col_info["min"] = float(raw_min) if not pd.isna(raw_min) and not math.isinf(float(raw_min)) else None
            col_info["max"] = float(raw_max) if not pd.isna(raw_max) and not math.isinf(float(raw_max)) else None
            col_info["mean"] = float(raw_mean) if not pd.isna(raw_mean) and not math.isinf(float(raw_mean)) else None
            col_info["is_numeric"] = True
        else:
            col_info["is_numeric"] = False

            
        profile["columns"][col] = col_info

    # 2. Use fast heuristics to infer the semantic meanings and description of the columns
    for col, info in profile["columns"].items():
        col_lower = col.lower()
        if "id" in col_lower or col_lower.endswith("_key") or col_lower.startswith("pk_") or col_lower.startswith("fk_"):
            info["semantic_type"] = "id"
            info["description"] = f"Unique identifier for {col.replace('_', ' ')}"
        elif any(x in col_lower for x in ("date", "time", "year", "month", "timestamp", "day", "created", "updated")):
            info["semantic_type"] = "datetime"
            info["description"] = f"Date/Time timestamp representing {col.replace('_', ' ')}"
        elif any(x in col_lower for x in ("amount", "price", "sales", "revenue", "cost", "tax", "fee", "payment", "rate")):
            info["semantic_type"] = "currency"
            info["description"] = f"Monetary value representing {col.replace('_', ' ')}"
        elif any(x in col_lower for x in ("lat", "lon", "city", "country", "region", "state", "address", "zip", "location")):
            info["semantic_type"] = "geographical"
            info["description"] = f"Geographical property representing {col.replace('_', ' ')}"
        elif info["is_numeric"]:
            info["semantic_type"] = "metric"
            info["description"] = f"Numeric metric value for {col.replace('_', ' ')}"
        else:
            info["semantic_type"] = "category"
            info["description"] = f"Categorical category value for {col.replace('_', ' ')}"
            
    return profile

