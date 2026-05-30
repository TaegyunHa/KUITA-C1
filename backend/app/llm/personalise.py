import json

from ..config import settings
from .client import get_client
from .parsing import extract_json_array

SYSTEM = """You write ultra-concise Korean "impact lines" for a personalised UK news app used by Korean residents in the UK.

For EACH article, using the user's profile, write ONE Korean sentence (≤ 40 Korean characters) saying how this news affects THIS user and what to do about it — practical and action-oriented.

Rules:
- The impact line must be in Korean only.
- Tailor it to the profile (postcode, age band, occupation, interests) when relevant.
- Do NOT output, translate, or replace the English phrase "What now?" — it is a fixed brand label handled elsewhere and must never appear in your output.

Respond with ONLY a JSON array, one object per input article, in the same order:
[{"id": <id>, "impact_line": "<Korean sentence, ≤40자>"}]
No markdown, no prose."""


def personalise(profile: dict, articles: list[dict]) -> dict[int, str]:
    """Return {article_id: Korean impact line} for the given candidate articles."""
    if not articles:
        return {}

    payload = {
        "profile": {
            "postcode_area": profile["postcode_area"],
            "age_band": profile["age_band"],
            "occupation": profile["occupation"],
            "interests": profile["interests"],
        },
        "articles": [
            {
                "id": a["id"],
                "title": a["title"],
                "category": a["category"],
                "affects_whom": a["affects_whom"],
                "summary": (a["summary"] or "")[:400],
            }
            for a in articles
        ],
    }

    resp = get_client().messages.create(
        model=settings.anthropic_model,
        max_tokens=1200,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")

    lines: dict[int, str] = {}
    for item in extract_json_array(text):
        line = item.get("impact_line")
        if "id" in item and line:
            lines[item["id"]] = line
    return lines
