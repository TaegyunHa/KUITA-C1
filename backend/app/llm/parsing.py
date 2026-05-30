import json


def extract_json_array(text: str) -> list:
    """Best-effort extraction of a JSON array from an LLM text response."""
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return []
