from typing import Any


def safe_serialize(obj: Any):
    try:
        import json

        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)
