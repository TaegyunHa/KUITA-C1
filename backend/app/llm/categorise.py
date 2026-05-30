import json

from .. import repository
from ..config import settings
from ..taxonomy import CATEGORIES
from .client import get_client

BATCH_SIZE = 10

SYSTEM = f"""You categorise UK news articles for a personalised feed serving Korean residents in the UK.

For EACH article:
- Pick exactly ONE category from this fixed list: {", ".join(CATEGORIES)}.
- Add up to 4 short lowercase free-form tags (e.g. student-visa, central-line, council-tax-band).
- Write a one-sentence English "affects_whom" note: who is most affected and how.

Respond with ONLY a JSON array, one object per input article, in the same order:
[{{"id": <id>, "category": "<one of the list>", "tags": ["..."], "affects_whom": "..."}}]
No markdown, no prose."""


def _extract_json_array(text: str) -> list:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return []


def _categorise_batch(articles: list[dict]) -> list[dict]:
    payload = [
        {"id": a["id"], "title": a["title"], "summary": (a.get("summary") or "")[:500]}
        for a in articles
    ]
    resp = get_client().messages.create(
        model=settings.anthropic_model,
        max_tokens=1500,
        # Static system prompt — flagged for prompt caching across batches in a run.
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")

    updates: list[dict] = []
    for item in _extract_json_array(text):
        if item.get("category") not in CATEGORIES:
            continue
        updates.append(
            {
                "id": item["id"],
                "category": item["category"],
                "tags": json.dumps(item.get("tags", []), ensure_ascii=False),
                "affects_whom": item.get("affects_whom", ""),
            }
        )
    return updates


def run(limit: int) -> int:
    """Categorise up to `limit` uncategorised articles. Returns the number updated."""
    pending = repository.get_uncategorised_articles(limit)
    updated = 0
    for i in range(0, len(pending), BATCH_SIZE):
        try:
            updates = _categorise_batch(pending[i : i + BATCH_SIZE])
        except Exception:
            continue
        updated += repository.update_categories(updates)
    return updated
