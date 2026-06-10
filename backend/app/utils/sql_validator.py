import re

FORBIDDEN = [r"\bDROP\b", r"\bDELETE\b", r"\bTRUNCATE\b", r"\bALTER\b", r"\bUPDATE\b", r"\bCREATE\b"]


def validate_sql(sql: str):
    s = sql.upper()
    for pat in FORBIDDEN:
        if re.search(pat, s):
            raise ValueError("Destructive or disallowed SQL detected")
    # Basic allowlist: only SELECT and common read-only statements
    if not re.match(r"^\s*(SELECT|WITH)\b", s):
        raise ValueError("Only read-only SELECT queries are allowed")
    return True
